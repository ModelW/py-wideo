import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Video(models.Model):
    """
    Raw, potentially invalid video file that was uploaded by the user.
    """

    class ProcessStatus(models.TextChoices):
        pending = "pending"
        processing = "processing"
        success = "success"
        failed = "failed"

    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name=_("ID"),
    )
    status = models.CharField(
        max_length=max(len(x) for x, _ in ProcessStatus.choices),
        choices=ProcessStatus.choices,
        default=ProcessStatus.pending,
        verbose_name=_("Status"),
        help_text=_(
            "The status of the video processing (pending means nothing "
            "happens on this video yet, processing means the task is running, "
            "success means a render is available and failed means the task "
            "failed)"
        ),
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Owner"),
        help_text=_("The owner of the video (if any)"),
    )
    file = models.ForeignKey(
        "watch_this_upload.VideoFile",
        on_delete=models.CASCADE,
        verbose_name=_("File"),
        help_text=_("Reference to the video file"),
    )
    date_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date of creation"),
        help_text=_("Date of creation of the video"),
    )


class Render(models.Model):
    """
    If a video as processed correctly, a render is created with pointers to
    all the outputs of the rendering process.
    """

    video = models.OneToOneField(
        Video,
        on_delete=models.CASCADE,
        verbose_name=_("Video"),
        help_text=_("The video that was rendered"),
    )
    date_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date of creation"),
        help_text=_("Date of creation of the render"),
    )
    thumbnails = models.JSONField(
        default=dict,
        verbose_name=_("Thumbnails"),
        help_text=_("Thumbnails of the video"),
    )
    videos = models.JSONField(
        default=dict,
        verbose_name=_("Videos"),
        help_text=_("Web-rendered videos"),
    )
    duration_seconds = models.FloatField(
        verbose_name=_("Duration in seconds"),
        help_text=_("Duration of the video in seconds"),
    )
    original_width = models.IntegerField(
        verbose_name=_("Original width"),
        help_text=_("Width of the original video in pixels"),
    )
    original_height = models.IntegerField(
        verbose_name=_("Original height"),
        help_text=_("Height of the original video in pixels"),
    )
    original_fps = models.DecimalField(
        verbose_name=_("Original FPS"),
        help_text=_("FPS of the original video"),
        max_digits=5,
        decimal_places=2,
    )
    original_frame_count = models.IntegerField(
        verbose_name=_("Original frame count"),
        help_text=_("Number of frames in the original video"),
    )
