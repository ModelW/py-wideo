from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..utils.storage import upload_to


class VideoFile(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Owner"),
        help_text=_("The owner of the video (if any)"),
    )
    file = models.FileField(
        upload_to=upload_to,
        verbose_name=_("File"),
        help_text=_("The video file"),
    )
    file_name = models.CharField(
        max_length=1000,
        verbose_name=_("File name"),
        help_text=_("Original name of the file"),
    )
    file_size = models.IntegerField(
        verbose_name=_("File size"),
        help_text=_("Size of the file in bytes"),
    )
    date_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date create"),
        help_text=_("Date of creation"),
    )
