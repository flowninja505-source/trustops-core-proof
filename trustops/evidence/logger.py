from datetime import datetime
import hashlib
import hmac
import json
from trustops.db.client import supabase

SIGNING_SECRET = "dev_secret_key_123"  # or load from .env if you want dynamic

def generate_payload_hash(payload: dict) -> str:
    """Generate SHA256 hash of the payload JSON string."""
    payload_str = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(payload_str.encode("utf-8")).hexdigest()

def sign_payload(payload_hash: str) -> str:
    """HMAC-SHA256 signature of the payload hash using the signing secret."""
    return hmac.new(
        SIGNING_SECRET.encode("utf-8"),
        payload_hash.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

def create_evidence_record(payload: dict) -> dict:
    """Insert an evidence record into Supabase and return the signed result."""
    timestamp = datetime.utcnow().isoformat()
    payload_hash = generate_payload_hash(payload)
    signature = sign_payload(payload_hash)

    record = {
        "timestamp_utc": timestamp,
        "payload": payload,
        "payload_hash": payload_hash,
        "signature": signature
    }

    try:
        response = supabase.table("evidence_records").insert(record).execute()
        # Log result for dev
        print("✅ Insert success:", json.dumps(record, indent=2))
        return record
    except Exception as e:
        print("❌ Insert failed:", e)
        return {
            "timestamp_utc": timestamp,
            "payload": payload,
            "error": str(e)
        }
