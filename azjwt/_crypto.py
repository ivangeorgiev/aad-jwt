import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers

def jwk_to_rsa_pem(jwk):
    def decode_value(val):
        decoded = base64.urlsafe_b64decode(ensure_bytes(val) + b"==")
        return int.from_bytes(decoded, "big")

    def ensure_bytes(key):
        if isinstance(key, str):
            key = key.encode("utf-8")
        return key

    return (
        RSAPublicNumbers(n=decode_value(jwk["n"]), e=decode_value(jwk["e"]))
        .public_key(default_backend())
        .public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    )
