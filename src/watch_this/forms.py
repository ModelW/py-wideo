from django.forms import ModelForm

from .models import UploadedVideo, Video
from .widgets import VideoUploadWidget


class UploadedVideoForm(ModelForm):
    class Meta:
        model = UploadedVideo
        fields = ["file"]


class BaseVideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ["title", "upload", "tags"]


class VideoForm(BaseVideoForm):
    class Meta(BaseVideoForm.Meta):
        widgets = {"upload": VideoUploadWidget()}
