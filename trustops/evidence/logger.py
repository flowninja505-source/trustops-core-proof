from datetime import datetime
from trustops.evidence.hash import generate_sha256_hash
from trustops.security.signing import generate_signature


def create_evidence_record(payload: dict) -> dict:
    """
    Generate evidence record including:
    - Canonical payload hash
    - Cryptographic signature
    - Timestamp
    """

    payload_hash = generate_sha256_hash(payload)
    signature = generate_signature(payload_hash)

    record = {
        "timestamp_utc": datetime.utcnow().isoformat(),
        "payload": payload,
        "payload_hash": payload_hash,
        "signature": signature,
    }

    return record
