from rest_framework import serializers

from .models import VideoFile


class VideoFileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoFile
        fields = ["owner", "file", "file_name", "file_size"]
