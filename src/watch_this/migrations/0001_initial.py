# Generated by Django 4.1.9 on 2023-06-19 12:13

import django.db.models.deletion
import taggit.managers
import wagtail.models.collections
import wagtail.search.index
from django.conf import settings
from django.db import migrations, models

import watch_this.storage


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("taggit", "0005_auto_20220424_2025"),
        ("wagtailcore", "0078_referenceindex"),
    ]

    operations = [
        migrations.CreateModel(
            name="UploadedVideo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="created at"
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        help_text="The uploaded video file",
                        upload_to=watch_this.storage.upload_to,
                        verbose_name="file",
                    ),
                ),
                (
                    "uploaded_by_user",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="uploaded by user",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Video",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="created at"
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="title")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("processing", "Processing"),
                            ("success", "Success"),
                            ("failed", "Failed"),
                        ],
                        default="pending",
                        help_text="The status of the video processing (pending means nothing happens on this video yet, processing means the task is running, success means a render is available and failed means the task failed)",
                        max_length=10,
                        verbose_name="status",
                    ),
                ),
                (
                    "collection",
                    models.ForeignKey(
                        default=wagtail.models.collections.get_root_collection_id,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="wagtailcore.collection",
                        verbose_name="collection",
                    ),
                ),
                (
                    "upload",
                    models.ForeignKey(
                        help_text="The uploaded video file",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="watch_this.uploadedvideo",
                        verbose_name="file",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        blank=True,
                        help_text=None,
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                        verbose_name="tags",
                    ),
                ),
                (
                    "uploaded_by_user",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="uploaded by user",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
        migrations.CreateModel(
            name="Render",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="created at"
                    ),
                ),
                (
                    "thumbnails",
                    models.JSONField(
                        default=dict,
                        help_text="Thumbnails of the video",
                        verbose_name="Thumbnails",
                    ),
                ),
                (
                    "videos",
                    models.JSONField(
                        default=dict,
                        help_text="Web-rendered videos",
                        verbose_name="videos",
                    ),
                ),
                (
                    "duration_seconds",
                    models.FloatField(
                        help_text="Duration of the video in seconds",
                        verbose_name="duration in seconds",
                    ),
                ),
                (
                    "original_width",
                    models.IntegerField(
                        help_text="Width of the original video in pixels",
                        verbose_name="original width",
                    ),
                ),
                (
                    "original_height",
                    models.IntegerField(
                        help_text="Height of the original video in pixels",
                        verbose_name="original height",
                    ),
                ),
                (
                    "original_fps",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="FPS of the original video",
                        max_digits=5,
                        verbose_name="original FPS",
                    ),
                ),
                (
                    "original_frame_count",
                    models.IntegerField(
                        help_text="Number of frames in the original video",
                        verbose_name="original frame count",
                    ),
                ),
                (
                    "video",
                    models.OneToOneField(
                        help_text="The video that was rendered",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="watch_this.video",
                        verbose_name="video",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]