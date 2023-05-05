import requests


def tenant_metadata_endpoint(tenant_id) -> str:
    template = (
        "https://login.microsoftonline.com"
        "/{TENANT_ID}/v2.0/.well-known/openid-configuration"
    )
    format_args = {
        "TENANT_ID": tenant_id,
    }
    return template.format(**format_args)


class OpenIdDiscovery:
    verify: bool = True
    metadata_endpoint_template = (
        "https://login.microsoftonline.com"
        "/{TENANT_ID}/v2.0/.well-known/openid-configuration"
    )

    def __init__(self, metadata_endpoint: str):
        self.metadata_endpoint = metadata_endpoint

    def get_configuration(self) -> dict:
        response = requests.get(self.metadata_endpoint, verify=self.verify)
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

    def get_key(self, key_id: str) -> str:
        for key in self.get_keys()["keys"]:
            if key.get("kid") == key_id:
                return key
        raise self.UnknownKeyError(key_id)

    class RetrieveError(Exception):
        pass

    class UnknownKeyError(Exception):
        pass
