from django.contrib.auth.backends import ModelBackend
from .models import CustomUser
from django.utils import timezone


class CustomUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=username)
        except CustomUser.DoesNotExist:
            return None

        if user.check_password(password) and not user.is_blocked:
            user.last_login = timezone.now()
            user.save()
            return user

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
