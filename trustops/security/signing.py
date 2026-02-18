import hmac
import hashlib
import os


def generate_signature(message: str) -> str:
    """
    Generate HMAC-SHA256 signature for a message using SIGNING_SECRET.
    """
    secret = os.getenv("SIGNING_SECRET")

    if not secret:
        raise ValueError("SIGNING_SECRET not set in environment.")

    signature = hmac.new(
        secret.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    return signature


def verify_signature(message: str, signature: str) -> bool:
    """
    Verify HMAC-SHA256 signature.
    """
    expected = generate_signature(message)
    return hmac.compare_digest(expected, signature)
