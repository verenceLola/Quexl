"""urls for the orders app"""
from django.urls import path

# local imports
from quexl.apps.blog.views import BlogDetail
from quexl.apps.blog.views import BlogList
from quexl.apps.blog.views import CommentDetail
from quexl.apps.blog.views import CommentList
from quexl.apps.blog.views import DislikeList
from quexl.apps.blog.views import LikeList

app_name = "blog"

urlpatterns = [
    path("blog/", BlogList.as_view(), name="blogs"),
    path("blog/<str:pk>", BlogDetail.as_view(), name="blog"),
    path("blog/like/", LikeList.as_view(), name="likes"),
    path("blog/dislike/", DislikeList.as_view(), name="dislikes"),
    path("blog/comment/", CommentList.as_view(), name="comments"),
    path("blog/comment/<str:pk>", CommentDetail.as_view(), name="comment"),
]
