from django.urls import include, path
from wagtail import hooks

from . import admin_urls


@hooks.register("register_icons")
def register_icons(icons: list[str]) -> list[str]:
    return icons + [f"{__package__}/icons/video.svg"]


@hooks.register("register_admin_urls")
def register_admin_urls():
    return [
        path(f"{__package__}/", include(admin_urls, namespace="watch_this")),
    ]
