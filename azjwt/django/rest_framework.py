from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class BearerAuthentication(TokenAuthentication):
    keyword = "Bearer"

    def authenticate(self, request):
        return super().authenticate(request)
        
    def authenticate_credentials(self, key):
        user = authenticate(bearer_token=key)
        if user is None:
            msg = _("Failed to authenticate with provided credentials.")
            raise AuthenticationFailed(msg)
        return user
