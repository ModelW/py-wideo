from django.forms import ModelForm

from .models import UploadedVideo, Video
from .widgets import VideoUploadWidget


def get_video_form():
    return VideoForm


class UploadedVideoForm(ModelForm):
    class Meta:
        model = UploadedVideo
        fields = ["file"]


class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ["title", "file", "tags"]
        widgets = {"file": VideoUploadWidget()}
