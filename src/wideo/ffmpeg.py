from subprocess import run
from typing import BinaryIO, Optional

import magic
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile

from wideo.exceptions import InvalidVideoFile


def compute_division(division: str) -> Optional[float]:
    if division == "N/A":
        return None

    a, b = division.split("/")
    return float(a) / float(b)


def try_round(n: Optional[float]) -> Optional[float]:
    return round(n, 2) if n is not None else n


def get_video_info(file: BinaryIO) -> dict:
    """
    Uses ffprobe to retrieve some basic information about a video file (size,
    duration...)
    """
    data = None

    if isinstance(file, InMemoryUploadedFile):
        filename = "-"
        position = file.tell()
        file.seek(0)
        data = file.read()
        file.seek(position)
        mime = magic.from_buffer(data, mime=True)
    else:
        filename = (
            file.temporary_file_path()
            if isinstance(file, TemporaryUploadedFile)
            else file.name
        )
        mime = magic.from_file(filename, mime=True)

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
        key: try_round(compute_division(value) if "/" in value else float(value))
        for key, value in (line.split("=") for line in ffprobe.stdout.decode().split())
    }

    if ffprobe.returncode:
        raise InvalidVideoFile

    if not info["nb_frames"]:
        info["nb_frames"] = round(info["avg_frame_rate"] * info["duration"])

    info["mime"] = mime
    # Rename some keys to fit the models used in wideo
    info["frame_count"] = info["nb_frames"]
    info["frames_per_second"] = info["avg_frame_rate"]
    del info["nb_frames"]
    del info["avg_frame_rate"]
    return info
