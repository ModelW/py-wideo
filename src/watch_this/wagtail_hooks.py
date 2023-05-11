from django.urls import path, reverse
from wagtail import hooks
from wagtail.admin.menu import MenuItem

from .views import index


@hooks.register("register_icons")
def register_icons(icons: list[str]):
    return icons + [f"{__package__}/icons/video.svg"]


@hooks.register("register_admin_urls")
def register_videos_url() -> list:
    return [path("videos/", index, name="videos")]


@hooks.register("register_admin_menu_item")
def register_videos_menu_item() -> MenuItem:
    return MenuItem("Videos", reverse("videos"), icon_name="video")
