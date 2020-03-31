"""serializers for blog models"""

from mptt.exceptions import InvalidMove
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError

from quexl.apps.blog.models import Blog
from quexl.apps.blog.models import Comment
from quexl.apps.blog.models import Dislike
from quexl.apps.blog.models import Like


class BlogSerializer(serializers.ModelSerializer):
    """
    serializer for the blog model
    """

    class Meta:
        model = Blog
        fields = "__all__"
        read_only_fields = ("author", "slug", "created_at", "updated_at")

    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()

    def get_likes(self, blog):
        likes = Like.objects.filter(blog=blog.pk).count()
        return likes

    def get_dislikes(self, blog):
        dislikes = Dislike.objects.filter(blog=blog.pk).count()
        return dislikes

    def create(self, validated_data):
        """
        create a blog with author as the current user
        """
        validated_data.update({"author": self.context["request"].user})
        blog = Blog.objects.create(**validated_data)
        return blog


class CommentSerializer(serializers.ModelSerializer):
    """
    serializer for comment model
    """

    class Meta:
        model = Comment
        exclude = ("lft", "rght", "tree_id", "level")
        read_only_fields = ("parent", "user")

    parent_id = serializers.CharField(required=False, write_only=True)
    replies = serializers.SerializerMethodField()

    def get_replies(self, parent):
        queryset = parent.get_children()
        serializer = CommentSerializer(
            queryset, many=True, context=self.context
        )
        return serializer.data

    def create(self, validated_data):
        """
        create new category instance
        """
        validated_data.update({"user": self.context["request"].user})
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        update Comment details
        """
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        try:
            instance.save()
        except InvalidMove:
            raise ValidationError(
                {
                    "name": "A Comment cannot be a \
                        sub-comment of one of its sub-subcomments"
                }
            )
        return instance


class LikeSerializer(serializers.ModelSerializer):
    """
    serializer for the like model
    """

    class Meta:
        model = Like
        fields = "__all__"
        read_only_fields = ("user", "created_at", "updated_at")

    def create(self, validated_data):
        """
        create a like with user as the current user
        """
        try:
            validated_data.update({"user": self.context["request"].user})
            like = Like.objects.create(**validated_data)
            return like
        except BaseException:
            like = Like.objects.filter(blog=validated_data["blog"].id)
            like = like.filter(user=self.context["request"].user)
            like.delete()
            raise NotFound("Like not found")


class DislikeSerializer(serializers.ModelSerializer):
    """
    serializer for the dislike model
    """

    class Meta:
        model = Dislike
        fields = "__all__"
        read_only_fields = ("user", "created_at", "updated_at")

    def create(self, validated_data):
        """
        create a dislike with user as the current user
        """
        try:
            validated_data.update({"user": self.context["request"].user})
            dislike = Dislike.objects.create(**validated_data)
            return dislike
        except BaseException:
            dislike = Dislike.objects.filter(blog=validated_data["blog"].id)
            dislike = dislike.filter(user=self.context["request"].user)
            dislike.delete()
            raise NotFound("Dislike not found")
