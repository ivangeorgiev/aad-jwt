from unittest.mock import MagicMock, patch
import pytest
from django.http.request import HttpRequest
from azjwt.django import _auth_backend
from azjwt.django._auth_backend import AzureJwtBackend


class TestAzureJwtBackend:
    def test_should_not_authenticate_if_bearer_token_is_not_provided(
        self,
        backend: AzureJwtBackend,
        django_request: HttpRequest,
    ):
        assert backend.authenticate(django_request) is None

    def test_should_not_authenticate_if_bearer_token_is_empty(
        self,
        backend: AzureJwtBackend,
        django_request: HttpRequest,
    ):
        assert backend.authenticate(django_request, bearer_token="") is None

    def test_should_attempt_authenticate_with_token_if_bearer_token_is_provided(
        self,
        backend: AzureJwtBackend,
        django_request: HttpRequest,
        authenticate_with_token_patch: MagicMock,
    ):
        backend.authenticate(django_request, bearer_token="token")
        authenticate_with_token_patch.assert_called_once_with("token")

    def test_should_decode_token(
        self,
        backend: AzureJwtBackend,
        decode_token_patch: MagicMock,
        get_user_for_claims_patch: MagicMock,
        can_authenticate_patch: MagicMock,
    ):
        backend._authenticate_with_token("token")
        decode_token_patch.assert_called_once_with("token")

    def test_should_get_user_from_claims(
        self,
        backend: AzureJwtBackend,
        decode_token_patch: MagicMock,
        get_user_for_claims_patch: MagicMock,
        can_authenticate_patch: MagicMock,
    ):
        backend._authenticate_with_token("token")
        get_user_for_claims_patch.assert_called_once_with(
            decode_token_patch.return_value
        )

    def test_should_authenticate_user_if_allowed_to(
        self,
        backend: AzureJwtBackend,
        decode_token_patch: MagicMock,
        get_user_for_claims_patch: MagicMock,
        user_is_allowed_to_authenticate,
    ):
        user = backend._authenticate_with_token("token")
        assert user is get_user_for_claims_patch.return_value

    def test_should_not_authenticate_user_if_not_allowed_to(
        self,
        backend: AzureJwtBackend,
        decode_token_patch: MagicMock,
        get_user_for_claims_patch: MagicMock,
        user_is_not_allowed_to_authenticate,
    ):
        user = backend._authenticate_with_token("token")
        assert user is None

    def test_should_use_jwtdecoder_to_decode_token(
        self,
        backend: AzureJwtBackend,
        jwtdecoder_patch: MagicMock,
        jwtdecoder_mock: MagicMock,
        userclaims_patch: MagicMock,
    ):
        backend._decode_token("token")
        jwtdecoder_patch.get_instance.assert_called_once_with()
        jwtdecoder_mock.decode.assert_called_once_with("token")

    def test_should_decode_token_into_userclaims(
        self,
        backend: AzureJwtBackend,
        jwtdecoder_mock,
        userclaims_patch,
    ):
        result = backend._decode_token("token")
        claims_dict = jwtdecoder_mock.decode.return_value
        userclaims_patch.from_dict.assert_called_once_with(claims_dict)
        assert result == userclaims_patch.from_dict.return_value

    def test_should_get_user_using_jwtusers_instance(
        self,
        backend: AzureJwtBackend,
        jwtusers_patch: MagicMock,
        jwtusers_mock: MagicMock,
    ):
        result = backend._get_user_for_claims("claims")
        jwtusers_patch.get_instance.assert_called_once_with()
        jwtusers_mock.get_for_claims.assert_called_once_with("claims")
        assert result is jwtusers_mock.get_for_claims.return_value

    def test_should_not_allow_authentication_for_inactive_user(
        self,
        backend: AzureJwtBackend,
    ):
        user = MagicMock()
        user.is_active = False
        assert not backend._can_authenticate(user)


    def test_should_allow_authentication_if_user_has_no_is_active_property(
        self,
        backend: AzureJwtBackend,
    ):
        user = MagicMock()
        assert backend._can_authenticate(user)

@pytest.fixture(name="backend")
def given_backend() -> AzureJwtBackend:
    return AzureJwtBackend()


@pytest.fixture(name="django_request")
def given_django_request() -> HttpRequest:
    return HttpRequest()


@pytest.fixture(name="authenticate_with_token_patch")
def given_authenticatee_with_token_patch(backend) -> MagicMock:
    with patch.object(backend, "_authenticate_with_token") as func_mock:
        yield func_mock


@pytest.fixture(name="decode_token_patch")
def given_decode_token_token_patch(backend) -> MagicMock:
    with patch.object(backend, "_decode_token") as func_mock:
        yield func_mock


@pytest.fixture(name="get_user_for_claims_patch")
def given_get_user_for_claims_patch(backend) -> MagicMock:
    with patch.object(backend, "_get_user_for_claims") as func_mock:
        yield func_mock


@pytest.fixture(name="can_authenticate_patch")
def given_can_authenticate_patch(backend) -> MagicMock:
    with patch.object(backend, "_can_authenticate") as func_mock:
        yield func_mock


@pytest.fixture(name="user_is_allowed_to_authenticate")
def given_user_is_allowed_to_authenticate(can_authenticate_patch) -> MagicMock:
    can_authenticate_patch.return_value = True


@pytest.fixture(name="user_is_not_allowed_to_authenticate")
def given_user_is_not_allowed_to_authenticate(can_authenticate_patch) -> MagicMock:
    can_authenticate_patch.return_value = False


@pytest.fixture(name="jwtdecoder_patch")
def given_jwtdecoder_patch() -> MagicMock:
    with patch.object(_auth_backend, "JwtDecoder") as mock:
        yield mock

@pytest.fixture(name="jwtdecoder_mock")
def given_jwtdecoder_instance(jwtdecoder_patch) -> MagicMock:
    return jwtdecoder_patch.get_instance.return_value


@pytest.fixture(name="userclaims_patch")
def given_userclaims_patch() -> MagicMock:
    with patch.object(_auth_backend, "UserClaims") as mock:
        yield mock


@pytest.fixture(name="jwtusers_patch")
def given_jwtusers_patch() -> MagicMock:
    with patch.object(_auth_backend, "JwtUsers") as mock:
        yield mock


@pytest.fixture(name="jwtusers_mock")
def given_jwtusers_mock(jwtusers_patch) -> MagicMock:
    return jwtusers_patch.get_instance.return_value
