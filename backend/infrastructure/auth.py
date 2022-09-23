import jwt

from django.utils.translation import ugettext_lazy as _
from authentication.models import User
from rest_framework import authentication, exceptions
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings


jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class JWTAuthentication(BaseJSONWebTokenAuthentication):
    """
    Simple JWT based authentication.

    Clients should authenticate by passing the API Key in the "Authorization"
    HTTP header, prepended with the string "Bearer ".  For example:

        Authorization: Bearer <jwt_token>
    """

    www_authenticate_realm = 'api-open'

    def get_jwt_value(self, request):
        auth = authentication.get_authorization_header(request).split()
        if not auth or auth[0].lower().decode() != api_settings.JWT_AUTH_HEADER_PREFIX.lower():
            return None

        if len(auth) == 1:
            msg = _('Invalid Authorization header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)

        elif len(auth) > 2:
            msg = _('Invalid Authorization header. Credentials string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1]

        except UnicodeError:
            msg = _('Invalid Authorization header. Credentials string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return token

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        return '{0} realm="{1}"'.format(api_settings.JWT_AUTH_HEADER_PREFIX, self.www_authenticate_realm)

    def authenticate(self, request):
        """
        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication.  Otherwise returns `None`.
        """
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return None

        try:
            payload = jwt_decode_handler(jwt_value)

        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise exceptions.AuthenticationFailed(msg)

        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise exceptions.AuthenticationFailed(msg)

        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()
        user = self.authenticate_credentials(payload)

        return (user, jwt_value)

    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id and email.
        """
        username = jwt_get_username_from_payload(payload)

        if not username:
            msg = _('Invalid payload.')
            raise exceptions.AuthenticationFailed(msg)
        try:
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            msg = _('Invalid signature.')
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = _('User account is disabled.')
            raise exceptions.AuthenticationFailed(msg)

        return user
