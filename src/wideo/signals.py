from django.db.models.signals import post_delete, post_save, pre_delete, pre_save
from django.dispatch import receiver

from . import get_video_model
from .models import AbstractVideo, UploadedVideo
from .tasks import encode_video


@receiver(pre_delete, sender=UploadedVideo)
def on_uploaded_video_pre_delete(instance: UploadedVideo, *args, **kwargs):
    instance.file.delete(save=False)


@receiver(post_delete, sender=get_video_model())
def on_video_post_delete(instance: AbstractVideo, *args, **kwargs):
    instance.upload.delete()


@receiver(pre_save, sender=get_video_model())
def on_video_pre_save(instance: AbstractVideo, *args, **kwargs):
    """
    Whenever a new uploaded video is assigned to a video, encode that video file
    and generate the new renders.
    """
    if old_instance := get_video_model().objects.filter(id=instance.id).first():
        if old_instance.upload_id != instance.upload_id:
            encode_video.delay(video_id=instance.id)


@receiver(post_save, sender=get_video_model())
def on_video_post_save(instance: AbstractVideo, created: bool, *args, **kwargs):
    """
    Whenever a video is created, encode the video file and generate the renders.
    """
    if created:
        encode_video.delay(video_id=instance.id)
