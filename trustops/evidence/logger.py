from datetime import datetime
from trustops.evidence.hash import hash_payload
from trustops.security.signing import sign_hash
from trustops.db.client import supabase



def create_evidence_record(payload: dict) -> dict:
    timestamp = datetime.utcnow().isoformat()

    payload_hash = hash_payload(payload)
    signature = sign_hash(payload_hash)

    record = {
        "timestamp_utc": timestamp,
        "payload": payload,
        "payload_hash": payload_hash,
        "signature": signature,
    }

    # Insert into Supabase
    response = supabase.table("evidence_records").insert(record).execute()

    if response.data is None:
        raise Exception("Failed to insert evidence record.")

    return record
