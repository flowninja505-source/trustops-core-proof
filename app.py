import os
from fastapi import FastAPI
from trustops.evidence.logger import create_evidence_record

# Determine environment (default = dev)
ENV = os.getenv("ENV", "dev").lower()

# Load environment-specific signing secret
SIGNING_SECRET = os.getenv(f"SIGNING_SECRET_{ENV.upper()}")

# Fail fast if secret missing
if not SIGNING_SECRET:
    raise ValueError(f"Missing signing secret for environment: {ENV}")

app = FastAPI(title=f"TrustOps Core ({ENV})")


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "environment": ENV,
        "signature_version": "v1"
    }


@app.post("/evidence")
def evidence(payload: dict):
    record = create_evidence_record(
        payload=payload,
        signing_secret=SIGNING_SECRET
    )
    return record
