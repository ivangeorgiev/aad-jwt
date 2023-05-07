from typing import Any

import jwt
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http.request import HttpRequest

from . import _conf as conf

class UserClaims:
    username: str

    @classmethod
    def from_dict(cls, claims: dict):
        pass


class JwtUsers:

    @property
    def create_missing(self) -> bool:
        return conf.MISSING_USER_ACTION == conf.MissingUserAction.CREATE

    @classmethod
    def get_instance(cls) -> "JwtUsers":
        return JwtUsers()

    def get_for_claims(self, claims: UserClaims) -> AbstractBaseUser | None:
        model = get_user_model()
        try:
            user = model.objects.get(username=claims.username)
        except model.DoesNotExist:
            user = self.create_for_claims(claims) if self.create_missing else None
        return user

    def create_for_claims(self, claims) -> AbstractBaseUser:
        pass

class JwtDecoder:
    @classmethod
    def get_instance(cls) -> "JwtDecoder":
        pass

    def decode(self, token: bytes) -> dict:
        return


class AzureJwtBackend(ModelBackend):
    def authenticate(
        self, request: HttpRequest, bearer_token: str | None = None, **kwargs: Any
    ) -> AbstractBaseUser | None:
        if bearer_token is None or len(bearer_token) == 0:
            return None
        return self._authenticate_with_token(bearer_token)

    def _authenticate_with_token(self, token: str) -> AbstractBaseUser | None:
        claims = self._decode_token(token)
        user = self._get_user_for_claims(claims)
        return user if self._can_authenticate(user) else None

    def _decode_token(self, token: str):
        decoder = JwtDecoder.get_instance()
        claims = decoder.decode(token)
        return UserClaims.from_dict(claims)

    def _get_user_for_claims(self, claims: UserClaims):
        users = JwtUsers.get_instance()
        return users.get_for_claims(claims)

    def _can_authenticate(self, user: AbstractBaseUser):
        return getattr(user, "is_active", True)
