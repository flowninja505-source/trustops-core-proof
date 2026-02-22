import hmac
import hashlib
import os


def sign_hash(payload_hash: str) -> str:
    """
    Generate HMAC-SHA256 signature for a hash string
    using SIGNING_SECRET from environment.
    """
    secret = os.getenv("SIGNING_SECRET")

    if not secret:
        raise ValueError("SIGNING_SECRET not set in environment.")

    signature = hmac.new(
        secret.encode("utf-8"),
        payload_hash.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    return signature


def verify_hash(payload_hash: str, signature: str) -> bool:
    """
    Verify HMAC-SHA256 signature against provided hash.
    """
    expected = sign_hash(payload_hash)
    return hmac.compare_digest(expected, signature)
