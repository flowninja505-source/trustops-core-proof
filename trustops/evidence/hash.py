import json
import hashlib


def canonicalize_payload(payload: dict) -> str:
    """
    Convert payload to deterministic JSON string.
    Ensures stable hashing regardless of key order.
    """
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def generate_sha256_hash(payload: dict) -> str:
    """
    Generate SHA256 hash from canonicalized payload.
    """
    canonical = canonicalize_payload(payload)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
