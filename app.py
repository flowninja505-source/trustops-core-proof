import os
from fastapi import FastAPI
from trustops.evidence.logger import create_evidence_record
from trustops.db.client import supabase

ENV = os.getenv("ENV", "dev")  # default to dev
SIGNING_SECRET = os.getenv(f"SIGNING_SECRET_{ENV.upper()}")

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok", "env": ENV}

@app.post("/evidence")
def evidence(payload: dict):
    record = create_evidence_record(payload)
    return {
        "timestamp_utc": record["timestamp_utc"],
        "payload": payload,
        "payload_hash": record["payload_hash"],
        "signature": record["signature"],
    }
