from unittest.mock import patch
import pytest
from azjwt import OpenIdDiscovery, tenant_metadata_endpoint

class TestTenantMetadataEndpointFunction:
    def test_should_return_metadata_endpoint_for_teannt(self):
        expected = "https://login.microsoftonline.com/<tenant-id>/v2.0/.well-known/openid-configuration"
        assert tenant_metadata_endpoint("<tenant-id>") == expected


class TestOpenIdDiscovery:
    def test_should_set_metadata_endpoint_when_created(
        self,
        openid_discovery: OpenIdDiscovery,
        metadata_endpoint: str,
    ):
        assert openid_discovery.metadata_endpoint == metadata_endpoint

    def test_should_discover_configuration(
        self,
        # Given
        openid_discovery: OpenIdDiscovery,
        openid_configuration: dict,
    ):
        # When
        config = openid_discovery.get_configuration()
        # Then
        assert config == openid_configuration

    def test_should_raise_RetrieveError_when_fetch_fails(
        self,
        # Given
        openid_discovery: OpenIdDiscovery,
        fetch_openid_configuration_returns_400,
    ):
        # When / Then
        with pytest.raises(OpenIdDiscovery.RetrieveError, match=""):
            openid_discovery.get_configuration()

    def test_should_discover_keys(
        self,
        # Given
        openid_discovery: OpenIdDiscovery,
        get_configuration_mock: str,
        keys: str,
    ):
        # When
        actual_keys = openid_discovery.get_keys()
        # Then
        get_configuration_mock.assert_called_once_with()
        assert actual_keys == keys

    def test_should_raise_RetrieveError_when_failed_to_fetch_keys(
        self,
        # Given
        openid_discovery: OpenIdDiscovery,
        get_configuration_mock: str,
        fetch_keys_returns_400,
    ):
        # When / Then
        with pytest.raises(OpenIdDiscovery.RetrieveError, match=""):
            openid_discovery.get_keys()

    def test_should_get_a_key(
        self,
        # Given
        openid_discovery: OpenIdDiscovery,
        get_keys_mock: str,
        known_key: dict,
    ):
        # When
        actual_key = openid_discovery.get_key(known_key["kid"])
        # Then
        get_keys_mock.assert_called_once_with()
        assert actual_key == known_key

    def test_should_raise_UnknownKeyError_trying_to_get_unknown_key(
        self,
        # Given
        openid_discovery: OpenIdDiscovery,
        get_keys_mock: str,
        unknown_key: dict,
    ):
        # When / Then
        with pytest.raises(OpenIdDiscovery.UnknownKeyError, match=unknown_key["kid"]):
            openid_discovery.get_key(unknown_key["kid"])


@pytest.fixture(name="openid_discovery")
def given_openid_discovery(metadata_endpoint) -> OpenIdDiscovery:
    return OpenIdDiscovery(metadata_endpoint)



@pytest.fixture(name="openid_configuration")
def mock_openid_configuration(
    requests_mocker: str, metadata_endpoint: str
):
    config = {
        "jwks_uri": "actual-jwks-url",
        "issuer": "actual-issuer",
    }
    requests_mocker.get(metadata_endpoint, json=config)
    yield config


@pytest.fixture(name="fetch_openid_configuration_returns_400")
def given_fetch_openid_configuration_returns_400(requests_mocker, metadata_endpoint):
    requests_mocker.get(metadata_endpoint, status_code=400)


@pytest.fixture(name="metadata_endpoint")
def given_metadata_endpoint() -> str:
    url = "https://endpoint-url"
    return url


@pytest.fixture(name="get_configuration_mock")
def mock_get_configuration(openid_discovery):
    with patch.object(openid_discovery, "get_configuration") as func_mock:
        func_mock.return_value = {
            "jwks_uri": "https://jwks_uri",
            "issuer": "https://issuer",
        }
        yield func_mock


@pytest.fixture(name="keys")
def mock_keys(requests_mocker):
    keys = {
        "key": "value",
    }
    requests_mocker.get("https://jwks_uri", json=keys)
    return keys


@pytest.fixture(name="fetch_keys_returns_400")
def given_fetch_keys_returns_400(requests_mocker):
    requests_mocker.get("https://jwks_uri", status_code=400)


@pytest.fixture(name="known_key")
def given_known_key():
    return {"kid": "known-key-id"}


@pytest.fixture(name="unknown_key")
def given_unknown_key():
    return {"kid": "unknown-key-id"}


@pytest.fixture(name="get_keys_mock")
def given_get_keys_mock(openid_discovery, known_key):
    with patch.object(openid_discovery, "get_keys") as func_mock:
        func_mock.return_value = {"keys": [known_key]}
        yield func_mock
