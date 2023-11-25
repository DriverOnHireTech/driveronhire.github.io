from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


def get_userby_email_or_username(username):
    """ get user by email or username

    Args:
        username (str): user email or username
    """
    return User.objects.filter(
        Q(username=username) | Q(email=username) | Q(phone=username)
    ).first()


def authenticate(request, username=None, password=None):
    """ Authenticate a user based on email address as the user name.

    Args:
        request (HTTPRequest): The request object.
        username (str, optional): username or email address. Defaults to None.
        password (str, optional): password. Defaults to None.

    Returns:
        Model: User object if authentication is successful, else None.
    """
    user = get_userby_email_or_username(username)

    if user and user.check_password(password):
        return user
    else:
        return None


class AuthBackend:
    """ Custom authentication backend.
        Allows users to log in using their email address & username.
    """

    def authenticate(self, request, username=None, password=None):
        """ Overrides the authenticate method to allow users to log in using
            email address & username.
        """
        return authenticate(request, username=username, password=password)

    def get_user(self, user_id):
        """ Get a user object from the user_id """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None