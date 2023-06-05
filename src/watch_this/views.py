from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import TemplateView
from rest_framework import status
from wagtail.admin import messages
from wagtail.admin.auth import PermissionPolicyChecker
from wagtail.admin.forms.search import SearchForm
from wagtail.admin.models import popular_tags_for_model
from wagtail.models import Collection
from wagtail.search.backends import get_search_backend

from . import get_video_model
from .forms import UploadedVideoForm, get_video_form
from .permissions import permission_policy

permission_checker = PermissionPolicyChecker(permission_policy)

INDEX_PAGE_SIZE = getattr(settings, "WATCH_THIS_INDEX_PAGE_SIZE", 30)
USAGE_PAGE_SIZE = getattr(settings, "WATCH_THIS_USAGE_PAGE_SIZE", 20)


class BaseListingView(TemplateView):
    ENTRIES_PER_PAGE_CHOICES = sorted({10, 30, 60, 100, 250, INDEX_PAGE_SIZE})
    ORDERING_OPTIONS = {
        "-created_at": _("Newest"),
        "created_at": _("Oldest"),
        "title": _("Title: (A -> Z)"),
        "-title": _("Title: (Z -> A)"),
        "file_size": _("File size: (low to high)"),
        "-file_size": _("File size: (high to low)"),
    }
    default_ordering = "-created_at"

    @method_decorator(permission_checker.require_any("add", "change", "delete"))
    def get(self, request):
        return super().get(request)

    def get_num_entries_per_page(self):
        entries_per_page = self.request.GET.get("entries_per_page", INDEX_PAGE_SIZE)
        try:
            entries_per_page = int(entries_per_page)
        except ValueError:
            entries_per_page = INDEX_PAGE_SIZE
        if entries_per_page not in self.ENTRIES_PER_PAGE_CHOICES:
            entries_per_page = INDEX_PAGE_SIZE

        return entries_per_page

    def get_valid_orderings(self):
        return self.ORDERING_OPTIONS

    def get_ordering(self):
        # TODO: remove this method when this view will be based on the
        # generic model index view from wagtail.admin.views.generic.models.IndexView
        ordering = self.request.GET.get("ordering")
        if ordering is None or ordering not in self.get_valid_orderings():
            ordering = self.default_ordering
        return ordering

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get ordering
        ordering = self.get_ordering()

        # Get videos (filtered by user permission and ordered by `ordering`)
        videos = (
            permission_policy.instances_user_has_any_permission_for(
                self.request.user, ["change", "delete"]
            )
            .order_by(ordering)
            .select_related("collection")
            # .prefetch_renditions("max-165x165")
        )

        # Filter by collection
        self.current_collection = None
        collection_id = self.request.GET.get("collection_id")
        if collection_id:
            try:
                self.current_collection = Collection.objects.get(id=collection_id)
                videos = videos.filter(collection=self.current_collection)
            except (ValueError, Collection.DoesNotExist):
                pass

        # Search
        query_string = None
        if "q" in self.request.GET:
            self.form = SearchForm(self.request.GET, placeholder=_("Search videos"))
            if self.form.is_valid():
                query_string = self.form.cleaned_data["q"]
                if query_string:
                    search_backend = get_search_backend()
                    videos = search_backend.autocomplete(query_string, videos)
        else:
            self.form = SearchForm(placeholder=_("Search videos"))

        # Filter by tag
        self.current_tag = self.request.GET.get("tag")
        if self.current_tag:
            try:
                videos = videos.filter(tags__name=self.current_tag)
            except AttributeError:
                self.current_tag = None

        entries_per_page = self.get_num_entries_per_page()
        paginator = Paginator(videos, per_page=entries_per_page)
        videos = paginator.get_page(self.request.GET.get("p"))

        next_url = reverse("watch_this:index")
        request_query_string = self.request.META.get("QUERY_STRING")
        if request_query_string:
            next_url += "?" + request_query_string

        context.update(
            {
                "videos": videos,
                "query_string": query_string,
                "is_searching": bool(query_string),
                "next": next_url,
                "entries_per_page": entries_per_page,
                "ENTRIES_PER_PAGE_CHOICES": self.ENTRIES_PER_PAGE_CHOICES,
                "current_ordering": ordering,
                "ORDERING_OPTIONS": self.ORDERING_OPTIONS,
            }
        )

        return context


class IndexView(BaseListingView):
    template_name = "watch_this/videos/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        collections = permission_policy.collections_user_has_any_permission_for(
            self.request.user, ["add", "change"]
        )
        if len(collections) < 2:
            collections = None

        Video = get_video_model()

        context.update(
            {
                "search_form": self.form,
                "popular_tags": popular_tags_for_model(Video),
                "current_tag": self.current_tag,
                "collections": collections,
                "current_collection": self.current_collection,
                "user_can_add": permission_policy.user_has_permission(
                    self.request.user, "add"
                ),
                "app_label": Video._meta.app_label,
                "model_name": Video._meta.model_name,
            }
        )
        return context


class ListingResultsView(BaseListingView):
    template_name = "watch_this/videos/results.html"


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

            return redirect("watch_this:index")
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
