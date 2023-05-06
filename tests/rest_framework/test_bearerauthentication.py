from types import SimpleNamespace
from unittest.mock import patch

import pytest
from rest_framework.exceptions import AuthenticationFailed

from azjwt.django import _rest_framework
from azjwt.django._rest_framework import BearerAuthentication


class TestBearerAuthentication:
    def test_should_authenticate_with_valid_credentials(
        self,
        # Given
        django_authenticate_patch,
        django_request,
        valid_token_in_request,
    ):
        auth = BearerAuthentication()
        # When
        response = auth.authenticate(django_request)
        # Then
        django_authenticate_patch.assert_called_once_with(
            bearer_token=valid_token_in_request
        )
        assert response == django_authenticate_patch.return_value

    def test_should_raise_authenticationfailure_token_doesnt_authenticate(
        self,
        # Given
        django_request,
        valid_token_in_request,
        authenticate_returns_none,
    ):
        auth = BearerAuthentication()
        # When / Then
        with pytest.raises(
            AuthenticationFailed,
            match="Failed to authenticate with provided credentials.",
        ):
            auth.authenticate(django_request)


@pytest.fixture(name="django_authenticate_patch")
def given_authenticate_patch():
    with patch.object(_rest_framework, "authenticate") as func_patch:
        yield func_patch


@pytest.fixture(name="authenticate_returns_none")
def given_authenticate_returns_none(django_authenticate_patch):
    django_authenticate_patch.return_value = None
    return django_authenticate_patch


@pytest.fixture(name="django_request")
def given_django_request():
    return SimpleNamespace(META={})


@pytest.fixture(name="valid_token_in_request")
def given_valid_credentials(django_request):
    django_request.META["HTTP_AUTHORIZATION"] = "Bearer 1234"
    return "1234"
