from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import PostSerializer
from ...models import Post
from django.shortcuts import get_object_or_404


@api_view(http_method_names=["get", "post"])
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


@api_view(http_method_names=["get"])
def postDetail(request, id: int):
    post = get_object_or_404(Post, pk=id, status=True)

    serialized_data = PostSerializer(post)

    return Response(serialized_data.data)
