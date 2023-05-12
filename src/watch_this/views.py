from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _
from rest_framework import status
from wagtail.admin import messages

from . import get_video_model
from .forms import UploadedVideoForm, get_video_form


def add(request: HttpRequest) -> HttpResponse:
    VideoModel = get_video_model()
    VideoForm = get_video_form()

    if request.method == "POST":
        video = VideoModel(uploaded_by_user=request.user)
        form = VideoForm(request.POST, request.FILES, instance=video)

        if form.is_valid():
            # form.save()
            obj = form.save(commit=False)
            obj.save()
            form.save_m2m()

            messages.success(
                request,
                _("Video '%(video_title)s' added.") % {"video_title": video.title},
                # buttons=[
                #     messages.button(
                #         reverse("watch_this:edit", args=(video.id,)), _("Edit")
                #     )
                # ],
            )

            # return redirect("watch_this:index")
            return redirect("watch_this:add")
        else:
            messages.error(request, _("The video could not be created due to errors."))
    else:
        form = VideoForm()

    return TemplateResponse(
        request,
        "watch_this/videos/add.html",
        {
            "form": form,
        },
    )


def upload_file(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    form = UploadedVideoForm(request.POST, request.FILES)

    if not form.is_valid():
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST, content=form.errors)

    form.save()
    return HttpResponse(status=status.HTTP_201_CREATED, content=form.data)
