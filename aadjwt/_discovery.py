import requests


class OpenIdDiscovery:
    verify: bool = True
    metadata_endpoint_template = (
        "https://login.microsoftonline.com"
        "/{TENANT_ID}/v2.0/.well-known/openid-configuration"
    )
    tenant_id: str

    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id

    def get_configuration(self) -> dict:
        url = self.make_metadata_endpoint()
        response = requests.get(url, verify=self.verify)
        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            raise self.RetrieveError() from error
        return response.json()
    
    def get_keys(self) -> dict:
        url = self.get_configuration()["jwks_uri"]
        response = requests.get(url, verify=self.verify)
        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            raise self.RetrieveError() from error
        return response.json()


    def make_metadata_endpoint(self):
        format_args = {
            "TENANT_ID": self.tenant_id,
        }
        self.metadata_endpoint = self.metadata_endpoint_template.format(**format_args)

    class RetrieveError(Exception):
        pass
