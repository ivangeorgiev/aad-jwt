import requests


class OpenIdDiscovery:
    verify: bool = True
    metadata_endpoint_template = (
        "https://login.microsoftonline.com"
        "/{TENANT_ID}/v2.0/.well-known/openid-configuration"
    )

    def discover(self, tenant_id: str):
        url = self.make_metadata_endpoint(tenant_id)
        response = requests.get(url, verify=self.verify)
        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            raise self.ConfigurationFetchError() from error
        return response.json()

    def make_metadata_endpoint(self, tenant_id: str):
        format_args = {
            "TENANT_ID": tenant_id,
        }
        self.metadata_endpoint = self.metadata_endpoint_template.format(**format_args)

    class ConfigurationFetchError(Exception):
        pass
