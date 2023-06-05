from django.dispatch import receiver
from django.test.signals import setting_changed
from wagtail.permission_policies.collections import CollectionOwnershipPermissionPolicy

from watch_this import get_video_model
from watch_this.models import Video

permission_policy = None


class VideosPermissionPolicyGetter:
    def __get__(self, obj, objtype=None):
        return permission_policy


def set_permission_policy():
    global permission_policy
    permission_policy = CollectionOwnershipPermissionPolicy(
        get_video_model(), auth_model=Video, owner_field_name="uploaded_by_user"
    )


@receiver(setting_changed)
def update_permission_policy(signal, sender, setting, **kwargs):
    if setting == "WATCH_THIS_VIDEO_MODEL":
        set_permission_policy()


set_permission_policy()
