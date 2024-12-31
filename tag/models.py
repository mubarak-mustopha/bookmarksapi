from django.db import models
from django.conf import settings


# Create your models here.
class Tag(models.Model):
    name = models.SlugField()
    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_tags",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("name", "owner"), name="unique-owner-tag")
        ]

    def __str__(self):
        return self.name
