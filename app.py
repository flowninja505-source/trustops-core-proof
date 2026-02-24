import os
from fastapi import FastAPI
from trustops.evidence.logger import create_evidence_record
from trustops.db.client import supabase

# Determine current environment
ENV = os.getenv("ENV", "dev").lower()
SIGNING_SECRET = os.getenv(f"SIGNING_SECRET_{ENV.upper()}")

app = FastAPI(title="TrustOps Core Proof")

# Health endpoint
@app.get("/health")
def health_check():
    return {"status": "ok", "env": ENV}

# Evidence endpoint
@app.post("/evidence")
def evidence(payload: dict):
    record = create_evidence_record(payload, signing_secret=SIGNING_SECRET)
    return {
        "timestamp_utc": record["timestamp_utc"],
        "payload": payload,
        "payload_hash": record["payload_hash"],
        "signature": record["signature"],
    }
