import json
import hashlib


def hash_payload(payload: dict) -> str:
    # Ensure deterministic ordering
    payload_string = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(payload_string.encode()).hexdigest()
