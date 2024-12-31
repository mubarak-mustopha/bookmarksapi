from django.contrib.auth.backends import BaseBackend

from .models import User


class EmailBackend(BaseBackend):

    def authenticate(self, request=None, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        if user.check_password(password) and user.is_active:
            return user

    def get(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        return user if user.is_active else None
