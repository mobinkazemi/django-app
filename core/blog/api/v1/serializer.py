from rest_framework import serializers
from blog.models import Post, Category
from accounts.models import Profile


# class PostSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
        ]


class PostSerializer(serializers.ModelSerializer):
    content_snippet = serializers.CharField(
        source="get_content_snippet", read_only=True
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "image",
            "author",
            "title",
            "content",
            "category",
            "content_snippet",
            "status",
            "created_date",
            "published_date",
        ]

        read_only_fields = [
            "author",
        ]

    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)

        #
        #
        #
        # 1. Handle Category field
        rep["category"] = (
            CategorySerializer(instance.category, context={"request": request}).data
            if instance.category
            else None
        )

        #
        #
        #
        # 2. Handle snippet field (remove in object detail - exists in objects list)

        if request.__dict__.get("parser_context", {}).get("kwargs", {}).get("pk"):
            #  Detail api requested
            rep.pop("content_snippet")
        else:
            # List api requested
            rep.pop("content")

        return rep

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request and request.user else None
        if user:
            validated_data["author"] = Profile.objects.get(user__id=user.id)

        return super().create(validated_data)
