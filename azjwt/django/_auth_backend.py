from typing import Any

import jwt
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http.request import HttpRequest


class UserClaims:
    @classmethod
    def from_dict(cls, claims: dict):
        pass


class JwtUsers:
    @classmethod
    def get_instance(cls) -> "JwtUsers":
        pass

    def get_for_claims(self, claims: UserClaims) -> AbstractBaseUser:
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
