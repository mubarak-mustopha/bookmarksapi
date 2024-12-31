from django.db import models
from django.conf import settings
from django.urls import reverse

from tag.models import Tag


# Create your models here.
class Collection(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="collections",
    )
    parent = models.ForeignKey(
        to="self",
        on_delete=models.SET_NULL,
        related_name="children",
        null=True,
        blank=True,
    )
    description = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("name", "owner"), name="unique-owner-collection"
            )
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):

        return reverse("collection-detail", kwargs={"pk": self.pk})


class Bookmark(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=125)

    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookmarks",
    )
    collection = models.ForeignKey(
        to=Collection, on_delete=models.CASCADE, null=True, blank=True
    )
    tags = models.ManyToManyField(to=Tag, related_name="bookmarks")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    expiry_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("title", "owner"), name="unique-owner-bookmark"
            )
        ]

    def __str__(self):
        return self.title
