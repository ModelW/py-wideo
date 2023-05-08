from rest_framework import permissions, viewsets

from .models import VideoFile


class SimpleUploadViewSet(viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin):
    permission_classes = [permissions.DjangoModelPermissions]
    queryset = VideoFile.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)
