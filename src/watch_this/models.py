import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from wagtail.models import CollectionMember
from wagtail.search import index

from .storage import upload_to


class TimestampedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        verbose_name=_("created at"), auto_now_add=True, db_index=True
    )


class UserUpload(models.Model):
    class Meta:
        abstract = True

    uploaded_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("uploaded by user"),
        null=True,
        blank=True,
        editable=False,
        on_delete=models.SET_NULL,
    )
    uploaded_by_user.wagtail_reference_index_ignore = True


class UploadedVideo(TimestampedModel, UserUpload):
    file = models.FileField(
        upload_to=upload_to,
        verbose_name=_("file"),
        help_text=_("The uploaded video file"),
    )

    def __str__(self) -> str:
        return str(self.file)


class AbstractVideo(index.Indexed, CollectionMember, TimestampedModel, UserUpload):
    class Meta:
        abstract = True

    class ProcessStatus(models.TextChoices):
        pending = "pending"
        processing = "processing"
        success = "success"
        failed = "failed"

    title = models.CharField(max_length=255, verbose_name=_("title"))
    file = models.FileField(
        upload_to=upload_to,
        verbose_name=_("file"),
        help_text=_("The rendered video file"),
    )
    status = models.CharField(
        max_length=max(len(x) for x, _ in ProcessStatus.choices),
        choices=ProcessStatus.choices,
        default=ProcessStatus.pending,
        verbose_name=_("status"),
        help_text=_(
            "The status of the video processing (pending means nothing "
            "happens on this video yet, processing means the task is running, "
            "success means a render is available and failed means the task "
            "failed)"
        ),
    )
    tags = TaggableManager(help_text=None, blank=True, verbose_name=_("tags"))
    search_fields = CollectionMember.search_fields + [
        index.SearchField("title", boost=10),
        index.AutocompleteField("title"),
        index.FilterField("title"),
        index.RelatedFields(
            "tags",
            [
                index.SearchField("name", boost=10),
                index.AutocompleteField("name"),
            ],
        ),
        index.FilterField("uploaded_by_user"),
    ]


class Video(AbstractVideo):
    admin_form_fields = (
        "title",
        "file",
        "tags",
    )


class AbstractRender(TimestampedModel):
    """
    If a video as processed correctly, a render is created with pointers to
    all the outputs of the rendering process.
    """

    class Meta:
        abstract = True

    thumbnails = models.JSONField(
        default=dict,
        verbose_name=_("Thumbnails"),
        help_text=_("Thumbnails of the video"),
    )
    videos = models.JSONField(
        default=dict,
        verbose_name=_("videos"),
        help_text=_("Web-rendered videos"),
    )
    duration_seconds = models.FloatField(
        verbose_name=_("duration in seconds"),
        help_text=_("Duration of the video in seconds"),
    )
    original_width = models.IntegerField(
        verbose_name=_("original width"),
        help_text=_("Width of the original video in pixels"),
    )
    original_height = models.IntegerField(
        verbose_name=_("original height"),
        help_text=_("Height of the original video in pixels"),
    )
    original_fps = models.DecimalField(
        verbose_name=_("original FPS"),
        help_text=_("FPS of the original video"),
        max_digits=5,
        decimal_places=2,
    )
    original_frame_count = models.IntegerField(
        verbose_name=_("original frame count"),
        help_text=_("Number of frames in the original video"),
    )


class Render(AbstractRender):
    video = models.OneToOneField(
        to=Video,
        on_delete=models.CASCADE,
        verbose_name=_("video"),
        help_text=_("The video that was rendered"),
    )
