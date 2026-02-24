import hashlib
import hmac
import json
from datetime import datetime, timezone
from trustops.db.client import supabase


def generate_payload_hash(payload: dict) -> str:
    payload_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(payload_bytes).hexdigest()


def sign_payload(payload_hash: str, signing_secret: str) -> str:
    return hmac.new(
        signing_secret.encode(),
        payload_hash.encode(),
        hashlib.sha256
    ).hexdigest()


def create_evidence_record(payload: dict, signing_secret: str) -> dict:
    if not signing_secret:
        raise ValueError("Signing secret not provided")

    payload_hash = generate_payload_hash(payload)
    signature = sign_payload(payload_hash, signing_secret)

    record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "payload": payload,
        "payload_hash": payload_hash,
        "signature": signature,
    }

    # Insert into Supabase
    response = supabase.table("evidence_records").insert(record).execute()

    if hasattr(response, "error") and response.error:
        raise Exception(response.error)

    return record
