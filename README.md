# Tools for Azure Active Directory JWT Tokens

## Example: OpenIdDiscovery to get a signature key

In this example we use the openid discovery metadata to find a signing public key for a tenant. Common scenario is a JWT signature validation.

```python
from azjwt import *
url = tenant_metadata_endpoint("3a15932d-3fd9-4278-a753-beb05cdf0c6d")
discovery = OpenIdDiscovery(url)
key = discovery.get_key("nOo3ZDrODABD1jKWhXslMN_KXEg")
rsa = jwk_to_rsa_pem(key)
print(rsa.decode())
```

The result of the execution of this code is a RSA key:

```
-----BEGIN PUBLIC KEY-----
MAABIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoaLLT9hkcSj2tGfZsjbu
7Xz1Krs0qEicXPmEsJKOBQHauZ/kRM1HdEkgOJbUznUspE6xOuOSXjlzErqBxXAu
4SCvcvVOCYG2v9G3+uIrLF5dstD0sYHBo1VomtKxzF90Vslrkn6rNQgUGIWgvuQT
xm1uRklYFPEcTMRw0LnYknzJ06GC9ljKR617wABVrZNkBuDgQKj37qcyxoaxIGdx
EcmVFZXJyrxDgdXh9owRmZn6LIJlGjZ9m59emfuwnBnsIQG7DirJwe9SXrLXnexR
QWqyzCdkYaOqkpKrsjuxUj2+MHX31FqsdpJJsOAvYXGOYBKJRjhGrGdONVrZdUdT
BQIDAQAB
-----END PUBLIC KEY-----
```

The key id (`kid`) could be obtained from the JWT token, using PyJWT package. Here is an example:

```python
import jwt

headers = jwt.get_unverified_headers(token)
key_id = headers["kid"]
```

