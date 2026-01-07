# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from django.shortcuts import get_object_or_404
# from rest_framework.decorators import permission_classes
# from rest_framework.views import APIView
# from rest_framework.generics import (
#     ListCreateAPIView,
#     GenericAPIView,
#     RetrieveUpdateDestroyAPIView,
# )
# from rest_framework import mixins
# import rest_framework.status as HTTP_STATUS
from blog.api.v1.permissions import IsOwnerOrReadonlyPermission
from blog.api.v1.pagination import GlobalPagination
from .serializer import PostSerializer, CategorySerializer
from ...models import Post, Category
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

"""
@api_view(http_method_names=["get", "post"])
@permission_classes([IsAuthenticatedOrReadOnly])
def postList(request):
    if request.method == "GET":
        posts = Post.objects.filter(status=True)
        serialized_data = PostSerializer(posts, many=True)
        return Response(serialized_data.data)
    elif request.method == "POST":
        serialized_data = PostSerializer(data=request.data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        return Response(serialized_data.data)
"""


"""
class PostList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer

    def get(self, request):
        posts = Post.objects.filter(status=True)
        serialized_data = PostSerializer(posts, many=True)
        return Response(serialized_data.data)

    def post(self, request):
        serialized_data = PostSerializer(data=request.data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        return Response(serialized_data.data)
"""


"""
@api_view(http_method_names=["get", "put", "delete"])
@permission_classes([IsAuthenticatedOrReadOnly])
def postDetail(request, id: int):
    post = get_object_or_404(Post, pk=id, status=True)

    if request.method == "GET":
        serialized_data = PostSerializer(post)
        return Response(serialized_data.data)
    elif request.method == "PUT":
        serialized_data = PostSerializer(post, data=request.data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        return Response(serialized_data.data)
    elif request.method == "DELETE":
        post.delete()
        return Response({"detail": "Post deleted successfully"}, status=204)
"""


"""
class PostDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer

    def get(self, request, id):
        post = get_object_or_404(Post, pk=id)
        serialized_data = self.serializer_class(post)
        return Response(serialized_data.data)

    def put(self, request, id):
        post = get_object_or_404(Post, pk=id)
        serialized_data = self.serializer_class(post, data=request.data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        return Response(serialized_data.data)

    def delete(self, request, id):
        post = get_object_or_404(Post, pk=id)
        post.delete()
        return Response(
            {"detail": "post removed successfully"},
            status=HTTP_STATUS.HTTP_204_NO_CONTENT,
        )
"""


"""
class PostDetail(
    GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
"""


"""
class PostList(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)

class PostDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
"""


class PostModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadonlyPermission]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "author", "status"]
    search_fields = ["title", "content"]
    ordering_fields = ["created_date", "published_date", "title"]
    pagination_class = GlobalPagination  # Disable pagination for simplicity


class CategoryModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
