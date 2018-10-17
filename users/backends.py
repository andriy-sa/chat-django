import jwt
from django.conf import settings
from jwt.exceptions import DecodeError
from rest_framework import authentication, exceptions

from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Bearer'
    user = None
    token = None

    def authenticate(self, request):
        request.user = None

        auth_header_prefix = self.authentication_header_prefix.lower()
        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header or len(auth_header) != 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        self.token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            raise exceptions.AuthenticationFailed('Incorrect auth header prefix.')

        self.__authenticate_credentials()
        return self.user, self.token

    def __authenticate_credentials(self):
        try:
            payload = jwt.decode(self.token, settings.SECRET_KEY)
        except DecodeError:
            raise exceptions.AuthenticationFailed('Invalid authentication. Could not decode token.')

        try:
            self.user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No user matching this token was found.')

        if not self.user.is_active:
            raise exceptions.AuthenticationFailed('This user has been deactivated.')
