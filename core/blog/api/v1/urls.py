from django.urls import path, include
from .views import CategoryModelViewSet, PostModelViewSet
from rest_framework.routers import DefaultRouter

app_name = "api-v1"

routes = DefaultRouter()
routes.register("post", PostModelViewSet, basename="post")
routes.register("category", CategoryModelViewSet, basename="category")

urlpatterns = routes.urls
# urlpatterns = [
#     path(
#         "post/",
#         PostViewSet.as_view({"get": "list", "create": "create"}),
#         name="post-list",
#     ),
#     path(
#         "post/<int:pk>/", PostViewSet.as_view({"get": "retrieve"}), name="post-detail"
#     ),
# ]
