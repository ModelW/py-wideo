from subprocess import run

import magic
from django.core.files.uploadedfile import (
    InMemoryUploadedFile,
    TemporaryUploadedFile,
    UploadedFile,
)

from watch_this.exceptions import UnsupportedUploadedFileType


def compute_division(division: str) -> float:
    a, b = division.split("/")
    return float(a) / float(b)


def get_video_info(file: UploadedFile) -> dict:
    if isinstance(file, InMemoryUploadedFile):
        filename = "-"
        file.seek(0)
        data = file.read()
        file.seek(0)
        mime = magic.from_buffer(data, mime=True)
    elif isinstance(file, TemporaryUploadedFile):
        filename = file.temporary_file_path()
        data = None
        mime = magic.from_file(filename, mime=True)
    else:
        raise UnsupportedUploadedFileType

    ffprobe = run(
        [
            "ffprobe",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height,nb_frames,avg_frame_rate:format=duration",
            "-of",
            "default=noprint_wrappers=1",
            filename,
        ],
        input=data,
        capture_output=True,
    )

    info = {
        key: round(compute_division(value) if "/" in value else float(value), 2)
        for key, value in (line.split("=") for line in ffprobe.stdout.decode().split())
    }

    info["mime"] = mime
    return info