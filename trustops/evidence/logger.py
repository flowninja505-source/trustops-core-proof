import hashlib
import hmac
import json
from datetime import datetime
from trustops.db.client import supabase, SUPABASE_SERVICE_ROLE_KEY

SIGNING_SECRET = "dev_secret_key_123"  # or from env

def create_evidence_record(payload: dict) -> dict:
    try:
        timestamp = datetime.utcnow().isoformat()
        payload_str = json.dumps(payload, sort_keys=True)
        payload_hash = hashlib.sha256(payload_str.encode()).hexdigest()
        signature = hmac.new(SIGNING_SECRET.encode(), payload_hash.encode(), "sha256").hexdigest()
        
        record = {
            "timestamp_utc": timestamp,
            "payload": payload,
            "payload_hash": payload_hash,
            "signature": signature
        }

        # Insert into Supabase
        response = supabase.table("evidence_records").insert(record).execute()
        if response.get("error"):
            return {"error": response["error"]}
        return record
    except Exception as e:
        return {"error": str(e)}
