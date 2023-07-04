from celery import shared_task
from django.db.transaction import atomic


@shared_task
def delete_orphan_uploaded_videos():
    from .models import delete_orphan_uploaded_videos

    delete_orphan_uploaded_videos()


@shared_task
@atomic
def encode_video(video_id: int):
    from .ffmpeg import encode_video

    encode_video(video_id)
