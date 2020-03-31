from django.db import models
from django.utils.text import slugify
from mptt.models import MPTTModel
from mptt.models import TreeForeignKey

from quexl.apps.account.models import User
from quexl.apps.services.models import Gallery
from quexl.helpers.fancy_generator import fancy_id_generator


class Blog(models.Model):
    """
    blog model
    """

    id = models.CharField(
        db_index=True,
        max_length=256,
        default=fancy_id_generator,
        primary_key=True,
        editable=False,
    )
    title = models.CharField(unique=True, max_length=100)
    slug = models.SlugField()
    short_description = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    images = models.ForeignKey(
        Gallery, on_delete=models.CASCADE, blank=True, null=True
    )
    description = models.CharField(max_length=300, blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """
        generate  slug from title
        """
        self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)


class Like(models.Model):
    """Like model"""

    id = models.CharField(
        db_index=True,
        max_length=256,
        default=fancy_id_generator,
        primary_key=True,
        editable=False,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "blog")
        verbose_name_plural = "likes"


class Dislike(models.Model):
    """Dislike model"""

    id = models.CharField(
        db_index=True,
        max_length=256,
        default=fancy_id_generator,
        primary_key=True,
        editable=False,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "blog")
        verbose_name_plural = "dislikes"


class Comment(MPTTModel):
    """
    comment model
    """

    id = models.CharField(
        db_index=True,
        max_length=256,
        default=fancy_id_generator,
        primary_key=True,
        editable=False,
    )
    body = models.TextField()
    parent = TreeForeignKey(
        "self",
        db_constraint=True,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ("created_at",)

    class Meta:
        unique_together = ("parent", "body")
        verbose_name_plural = "comments"
