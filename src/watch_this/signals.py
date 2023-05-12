from django.db.models.signals import pre_delete
from django.dispatch import receiver

from . import get_video_model
from .models import AbstractVideo, UploadedVideo


@receiver(pre_delete, sender=UploadedVideo)
def on_video_file_pre_delete(instance: UploadedVideo, *args, **kwargs):
    instance.file.delete(save=False)


@receiver(pre_delete, sender=get_video_model())
def on_video_file_pre_delete(instance: AbstractVideo, *args, **kwargs):
    instance.file.delete(save=False)
