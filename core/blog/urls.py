from django.urls import path
from .views import indexView, IndexView,RedirectToMaktabkhoonehView, PostListView
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

app_name = "blog"

urlpatterns = [
    path("fbv", indexView, name="fbv-test"),
    path("cbv", IndexView.as_view(), name="cbv-test"),
    path('post/', PostListView.as_view(), name='post-list'),
    path('go-to-maktab/<int:pk>/', RedirectToMaktabkhoonehView.as_view(), name='go-to-maktab'),
]
