from django.urls import path, include
from .views import postList, postDetail

app_name = "api-v1"

urlpatterns = [
    path("post/", postList, name="post-list"),
    path("post/<int:id>/", postDetail, name="post-detail"),
]
