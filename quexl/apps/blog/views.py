from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from quexl.apps.blog.models import Blog
from quexl.apps.blog.models import Comment
from quexl.apps.blog.models import Dislike
from quexl.apps.blog.models import Like
from quexl.apps.blog.serializers import BlogSerializer
from quexl.apps.blog.serializers import CommentSerializer
from quexl.apps.blog.serializers import DislikeSerializer
from quexl.apps.blog.serializers import LikeSerializer
from quexl.helpers.model_wrapper import RetrieveUpdateDestroyAPIViewWrapper
from quexl.utils.renderers import DefaultRenderer


class BlogList(ListCreateAPIView):
    """
    blog view for listing and creating blogs
    """

    name = "blog"
    pluralized_name = "blogs"
    permission_classes = (IsAuthenticated,)
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    renderer_classes = (DefaultRenderer,)

    def create(self, request, **kwargs):
        """overide creating of blog """
        self.operation = "Create blog "
        return super(ListCreateAPIView, self).create(request, **kwargs)


class BlogDetail(RetrieveUpdateDestroyAPIViewWrapper):
    """
    blog view for updating and deleting a blog instance
    """

    permission_classes = (IsAuthenticated,)
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    renderer_classes = (DefaultRenderer,)
    name = "blog"
    pluralized_name = "blogs"

    def update(self, request, *args, **kwargs):
        self.operation = "Update blog"
        return super(RetrieveUpdateDestroyAPIViewWrapper, self).update(
            request, *args, **kwargs
        )


class CommentList(ListCreateAPIView):
    """
    comments view for listing and creating comments
    """

    name = "comment"
    pluralized_name = "comments"
    permission_classes = (IsAuthenticated,)
    queryset = Comment.objects.filter(level=0)
    serializer_class = CommentSerializer
    renderer_classes = (DefaultRenderer,)

    def create(self, request, **kwargs):
        """overide creating of comment """
        self.operation = "Create comment "
        return super(ListCreateAPIView, self).create(request, **kwargs)


class CommentDetail(RetrieveUpdateDestroyAPIViewWrapper):
    """
    comment view for updating and deleting a comment instance
    """

    permission_classes = (IsAuthenticated,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    renderer_classes = (DefaultRenderer,)
    name = "comment"
    pluralized_name = "comments"

    def update(self, request, *args, **kwargs):
        self.operation = "Update comment"
        return super(RetrieveUpdateDestroyAPIViewWrapper, self).update(
            request, *args, **kwargs
        )


class LikeList(ListCreateAPIView):
    """
    services view for listing and creating parameter s
    """

    name = "blog like"
    pluralized_name = "blog likes"
    permission_classes = (IsAuthenticated,)
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    renderer_classes = (DefaultRenderer,)

    def create(self, request, **kwargs):
        """overide creating of like """
        self.operation = "Like blog "
        return super(ListCreateAPIView, self).create(request, **kwargs)


class DislikeList(ListCreateAPIView):
    """
    services view for listing and creating parameter s
    """

    name = "blog dislike"
    pluralized_name = "blog dislikes"
    permission_classes = (IsAuthenticated,)
    queryset = Dislike.objects.all()
    serializer_class = DislikeSerializer
    renderer_classes = (DefaultRenderer,)

    def create(self, request, **kwargs):
        """overide creating of dislike """
        self.operation = "Dislike blog "
        return super(ListCreateAPIView, self).create(request, **kwargs)
