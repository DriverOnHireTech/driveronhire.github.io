# YourCustomBackend

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CustomAuth(ModelBackend):
    def authenticate(self, request, phone=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return None

        return user
