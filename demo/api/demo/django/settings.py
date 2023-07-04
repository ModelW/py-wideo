from importlib import metadata
from os.path import join
from pathlib import Path

from celery.schedules import crontab
from model_w.env_manager import EnvManager
from model_w.preset.django import ModelWDjango

REST_FRAMEWORK = {}


def get_package_version() -> str:
    """
    Trying to get the current package version using the metadata module. This
    assumes that the version is indeed set in pyproject.toml and that the
    package was cleanly installed.
    """

    try:
        return metadata.version("demo")
    except metadata.PackageNotFoundError:
        return "0.0.0"


with EnvManager(ModelWDjango()) as env:
    # ---
    # Apps
    # ---

    INSTALLED_APPS = [
        "drf_spectacular",
        "drf_spectacular_sidecar",
        "django_extensions",
        "django.forms",
        "wagtail.contrib.modeladmin",
        "wideo",
        "demo.apps.realtime",
        "demo.apps.cms",
        "demo.apps.people",
    ]

    # ---
    # Plumbing
    # ---

    ROOT_URLCONF = "demo.django.urls"

    WSGI_APPLICATION = "demo.django.wsgi.application"
    ASGI_APPLICATION = "demo.django.asgi.application"

    # ---
    # Auth
    # ---

    AUTH_USER_MODEL = "people.User"

    # ---
    # i18n
    # ---

    LANGUAGES = [
        ("en", "English"),
    ]

    # ---
    # OpenAPI Schema
    # ---

    REST_FRAMEWORK["DEFAULT_SCHEMA_CLASS"] = "drf_spectacular.openapi.AutoSchema"

    SPECTACULAR_SETTINGS = {
        "TITLE": "Demo",
        "VERSION": get_package_version(),
        "SERVE_INCLUDE_SCHEMA": False,
        "SWAGGER_UI_DIST": "SIDECAR",  # shorthand to use the sidecar instead
        "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
        "REDOC_DIST": "SIDECAR",
    }

    # ---
    # Wagtail
    # ---

    WAGTAIL_SITE_NAME = "Demo"
    WAGTAILIMAGES_IMAGE_MODEL = "cms.CustomImage"
    WAGTAILDOCS_DOCUMENT_MODEL = "cms.CustomDocument"

    # ---
    # Celery
    # ---

    CELERY_BEAT_SCHEDULE = {
        "wideo.tasks.delete_orphan_uploaded_videos": {
            "task": "wideo.tasks.delete_orphan_uploaded_videos",
            "schedule": crontab(minute="*/5", hour="*"),
        },
    }

    # ---
    # Wideo
    # ---

    WIDEO_WORKING_DIR = Path(__file__).parent.parent.parent / "wideo_work"
