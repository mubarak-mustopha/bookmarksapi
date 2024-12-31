from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.

from .validators import validate_username


class User(AbstractUser):
    first_name = None
    last_name = None

    username = models.CharField(
        ("username"),
        max_length=150,
        unique=True,
        help_text=("Required. 150 characters or fewer. Letters, digits and _ only."),
        validators=[validate_username],
        error_messages={
            "unique": ("A user with that username already exists."),
        },
    )
    email = models.EmailField("Email address", blank=True, default="", unique=True)

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
