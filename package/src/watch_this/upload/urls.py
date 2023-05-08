from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import SimpleUploadViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


router.register("simple", SimpleUploadViewSet, basename="simple-upload")


urlpatterns = router.urls
