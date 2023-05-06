from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from . import _conf as conf

class MyAuthentication(BaseAuthentication):
    scheme = "bearer"
    
    @property
    def realm(self):
        return conf.REST_FRAMEWORK['REALM']

    def authenticate(self, request) -> tuple:
        raise AuthenticationFailed("Yes")

    def authenticate_header(self, request):
        header = self.scheme.capitalize()
        if self.realm:
            header += f' realm="{self.realm}"'
        return header
