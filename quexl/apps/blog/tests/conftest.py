# config tests file
import pytest

# models imports
from quexl.apps.blog.models import Blog
from quexl.apps.blog.models import Comment
from quexl.apps.blog.models import Dislike
from quexl.apps.blog.models import Like


@pytest.fixture
def create_blog(create_db_user):
    """create a blog instance"""
    blog = Blog()
    blog.author = create_db_user
    blog.title = "This is a title"
    blog.short_description = "This is a short description"
    blog.description = "This is a longer description"
    blog.body = "This is the blog body"
    blog.save()
    return blog


@pytest.fixture
def create_like(create_db_user, create_blog):
    """Creates a like instance"""
    like = Like()
    like.user = create_db_user
    like.blog = create_blog
    like.save()
    return like


@pytest.fixture
def create_dislike(create_db_user, create_blog):
    """Creates a dislike instance"""
    dislike = Dislike()
    dislike.user = create_db_user
    dislike.blog = create_blog
    dislike.save()
    return dislike


@pytest.fixture
def create_comment(create_db_user, create_blog):
    """create a comment instance"""
    comment = Comment()
    comment.user = create_db_user
    comment.blog = create_blog
    comment.body = "This is the comment body"
    comment.save()
    return comment


@pytest.fixture
def create_subcomment(create_db_user, create_blog, create_comment):
    """create a comment instance"""
    comment = Comment()
    comment.user = create_db_user
    comment.blog = create_blog
    comment.parent_id = create_comment.id
    comment.body = "This is the subcomment body"
    comment.save()
    return comment
