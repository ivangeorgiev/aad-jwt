import pytest

from azjwt import jwk_to_rsa_pem


class TestJwkToRsaPemFunction:
    def test_should_return_rsa_pem(self, jwk, rsa_pem):
        result = jwk_to_rsa_pem(jwk)
        assert result == rsa_pem


@pytest.fixture(name="jwk")
def given_jwk() -> dict:
    return {
        "n": (
            "oaLLT9hkcSj2tGfZsjbu7Xz1Krs0qEicXPmEsJKOBQHauZ_kRM1HdEkgOJ"
            "bUznUspE6xOuOSXjlzErqBxXAu4SCvcvVOCYG2v9G3-uIrLF5dstD0sYHB"
            "o1VomtKxzF90Vslrkn6rNQgUGIWgvuQTxm1uRklYFPEcTIRw0LnYknzJ06G"
            "C9ljKR617wABVrZNkBuDgQKj37qcyxoaxIGdxEcmVFZXJyrxDgdXh9owRmZ"
            "n6LIJlGjZ9m59emfuwnBnsIQG7DirJwe9SXrLXnexRQWqyzCdkYaOqkpKrs"
            "juxUj2-MHX31FqsdpJJsOAvYXGOYBKJRjhGrGdONVrZdUdTBQ"
        ),
        "e": "AQAB",
    }


@pytest.fixture(name="rsa_pem")
def given_rsa_pem() -> bytes:
    return (
        b"-----BEGIN PUBLIC KEY-----\n"
        b"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoaLLT9hkcSj2tGfZsjbu\n"
        b"7Xz1Krs0qEicXPmEsJKOBQHauZ/kRM1HdEkgOJbUznUspE6xOuOSXjlzErqBxXAu\n"
        b"4SCvcvVOCYG2v9G3+uIrLF5dstD0sYHBo1VomtKxzF90Vslrkn6rNQgUGIWgvuQT\n"
        b"xm1uRklYFPEcTIRw0LnYknzJ06GC9ljKR617wABVrZNkBuDgQKj37qcyxoaxIGdx\n"
        b"EcmVFZXJyrxDgdXh9owRmZn6LIJlGjZ9m59emfuwnBnsIQG7DirJwe9SXrLXnexR\n"
        b"QWqyzCdkYaOqkpKrsjuxUj2+MHX31FqsdpJJsOAvYXGOYBKJRjhGrGdONVrZdUdT\n"
        b"BQIDAQAB\n"
        b"-----END PUBLIC KEY-----\n"
    )
