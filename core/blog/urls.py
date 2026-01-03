from django.urls import path, include
from .views import (
    indexView,
    IndexView,
    RedirectToMaktabkhoonehView,
    PostListView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

app_name = "blog"

urlpatterns = [
    # path("fbv", indexView, name="fbv-test"),
    # path("cbv", IndexView.as_view(), name="cbv-test"),
    # path(
    #     "go-to-maktab/<int:pk>/",
    #     RedirectToMaktabkhoonehView.as_view(),
    #     name="go-to-maktab",
    # ),
    path("post/", PostListView.as_view(), name="post-list"),
    path("post/create/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/edit/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("api/v1/", include("blog.api.v1.urls")),
]
