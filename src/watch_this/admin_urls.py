from django.urls import path

import watch_this.views

app_name = "watch_this"
urlpatterns = [
    path("", watch_this.views.IndexView.as_view(), name="index"),
    path(
        "results/",
        watch_this.views.ListingResultsView.as_view(),
        name="listing_results",
    ),
    path("add/", watch_this.views.add, name="add"),
    path("<int:video_id>/", watch_this.views.edit, name="edit"),
    path("<int:video_id>/delete/", watch_this.views.delete, name="delete"),
    path("upload/", watch_this.views.upload_file, name="upload"),
]
