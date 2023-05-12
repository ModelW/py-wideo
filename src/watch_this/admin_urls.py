from django.urls import path

import watch_this.views

app_name = "watch_this"
urlpatterns = [
    path("add/", watch_this.views.add, name="add"),
    path("upload/", watch_this.views.upload_file, name="upload"),
]
