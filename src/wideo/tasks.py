import subprocess
from os.path import join
from tempfile import mkdtemp

from celery import shared_task
from django.core.files.base import ContentFile
from django.db.transaction import atomic

from . import get_render_model, get_video_model
from .codecs import get_presets
from .ffmpeg import get_video_info
from .models import RemoteVideoFile, UploadedVideo


@shared_task
def delete_orphan_uploaded_videos():
    """
    Delete all the instances of UploadedVideo that are not related to any Video
    anymore (result of changing the video file while editing a Video).
    """
    used_ids = get_video_model().objects.values("upload_id")
    UploadedVideo.objects.exclude(id__in=used_ids).delete()


@shared_task
@atomic
def encode_video(video_id: int):
    """
    Encodes a specific video with whichever presets have been specified in the settings.
    """
    video = get_video_model().objects.filter(id=video_id).first()

    if not video:
        return

    working_dir = mkdtemp()
    presets_map = get_presets()
    renders = {}
    ffmpegs = []

    def get_render_temp_file(r: get_render_model()) -> str:
        """
        Creates a simple unique path to a temporary file, used for storing outputs of
        ffmpeg.
        """
        return join(working_dir, str(r.id))

    # The input file must be written to the disk so that ffmpeg can access it randomly.
    # Streaming the file directly to ffmpeg's stdin would be simpler, but ffmpeg would
    # then not always be able to determine what type of file is its input.
    with video.upload.file.open("rb") as uploaded_file:
        input_file_path = join(working_dir, "input")

        with open(input_file_path, "wb") as input_file:
            while buf := uploaded_file.read(1024**2):
                input_file.write(buf)

    for preset_label, preset in presets_map.items():
        # Fill the render with bogus data until we can get info from the encoded videos
        render = get_render_model().objects.create(
            video=video,
            mime="",
            duration=0,
            width=0,
            height=0,
            frames_per_second=0,
            frame_count=0,
        )
        renders[preset_label] = render
        flags = preset["ffmpeg_flags"]
        command = f"ffmpeg -y -i {input_file_path} -f {preset['extension']} {' '.join(flags)} {get_render_temp_file(render)}"
        ffmpegs.append(subprocess.Popen(command, shell=True))

    def cleanup():
        """
        If something goes wrong during processing (invalid file...), stop everything and
        ensure we don't keep any unused Render objects.
        """
        for f in ffmpegs:
            f.kill()

        for r in renders.values():
            r.delete()

    # Wait for all ffmpeg processes to successfully finish their job (otherwise, panic
    # and abort everything immediately)
    for ffmpeg in ffmpegs:
        if ffmpeg.wait():
            cleanup()
            return

    # After all videos have been correctly generated, we just need to write them into
    # their respective Render objects
    for preset_label, preset in presets_map.items():
        render = renders[preset_label]

        with open(get_render_temp_file(render), "rb") as file:
            name = f"{render.video.title}_{preset_label}.{preset['extension']}"
            render.file = ContentFile(b"", name=name)

            with render.file.open("wb") as target:
                while buf := file.read(1024**2):
                    target.write(buf)

            # Don't forget to get info from the generated videos, and to store it in the
            # previously created Render objects
            video_info = get_video_info(file)

            for field in RemoteVideoFile.INFORMATION_FIELDS:
                setattr(render, field, video_info[field])

            render.save()
