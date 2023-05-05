from unittest.mock import patch
import pytest
from aadjwt._discovery import OpenIdDiscovery


class TestOpenIdDiscovery:

    def test_should_make_metadata_endpoint(
        self,
        # Given
        openid_discovery: OpenIdDiscovery,
        tenant_id: str,
        metadata_endpoint_template: str,
        metadata_endpoint: str,
    ):
        # When
        openid_discovery.make_metadata_endpoint(tenant_id)
        # Then
        metadata_endpoint_template.format.assert_called_once_with(TENANT_ID=tenant_id)
        assert openid_discovery.metadata_endpoint == metadata_endpoint

    def test_should_discover_configuration(
        self,
        # Given
        openid_discovery: OpenIdDiscovery,
        tenant_id: str,
        make_metadata_endpoint_mock: str,
        openid_configuration: dict,
    ):
        # When
        config = openid_discovery.discover(tenant_id)
        # Then
        make_metadata_endpoint_mock.assert_called_once_with(tenant_id)
        assert config == openid_configuration

    def test_should_raise_ConfigurationFetchError_when_fetch_fails(
        self,
        # Given
        openid_discovery: OpenIdDiscovery,
        tenant_id: str,
        make_metadata_endpoint_mock: str,
        fetch_openid_configuration_returns_400,
    ):
        # When / Then
        with pytest.raises(OpenIdDiscovery.ConfigurationFetchError, match=""):
            openid_discovery.discover(tenant_id)


@pytest.fixture(name="openid_discovery")
def given_openid_discovery() -> OpenIdDiscovery:
    return OpenIdDiscovery()


@pytest.fixture(name="tenant_id")
def given_tenant_id():
    return "some-tenant-id"


@pytest.fixture(name="openid_configuration")
def mock_openid_configuration(requests_mocker, metadata_endpoint):
    config = {
        "jwks_uri": "actual-jwks-url",
        "issuer": "actual-issuer",
    }
    requests_mocker.get(metadata_endpoint, json=config)
    yield config

@pytest.fixture(name="fetch_openid_configuration_returns_400")
def given_fetch_openid_configuration_returns_400(requests_mocker, metadata_endpoint):
    requests_mocker.get(metadata_endpoint, status_code=400)



@pytest.fixture(name="metadata_endpoint_template")
def mock_metadata_endpoint_template(openid_discovery, metadata_endpoint):
    with patch.object(openid_discovery, "metadata_endpoint_template") as template:
        template.format.return_value = metadata_endpoint
        yield template


@pytest.fixture(name="metadata_endpoint")
def mock_metadata_endpoint() -> str:
    return "https://endpoint-url"


@pytest.fixture(name="make_metadata_endpoint_mock")
def mock_make_metadata_endpoint(
    openid_discovery,
    metadata_endpoint,
):
    with patch.object(openid_discovery, "make_metadata_endpoint") as func_mock:
        func_mock.return_value = metadata_endpoint
        yield func_mock
