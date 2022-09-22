from django.contrib.auth.backends import ModelBackend
from authentication.models import User
from django.contrib.auth.hashers import check_password


class UserBackend(ModelBackend):
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)

        except User.DoesNotExist:
            return None


class EmployerBackend(UserBackend):
    """
    Authenticates against the xrefcore.models.users.Employer model.

    This implementation allows for authentication with or without
    a password. Authentication without password was a requirement
    of how users would hit the /auth endpoint in the Open API.
    See https://xrefdev.atlassian.net/browse/XD-2600.

    It also matches the user against a company if it is passed as
    a kwarg.
    """

    def authenticate(self, request, email=None, password=None, username=None, **kwargs):
        # IMPORTANT: assumption here is that the username here will be same as the regular email for a user at this
        # point, and it will get converted to the specific format with company ID (like user+company_id@domain.com)
        # later on to verify existence of such user
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        if not check_password(password, user.password):
            return None

        return user
