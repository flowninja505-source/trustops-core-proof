import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from trustops.evidence.logger import create_evidence_record

# Load environment variables
load_dotenv(dotenv_path=".env")

app = FastAPI(title="TrustOps Dev API")

class EvidencePayload(BaseModel):
    decision_id: str
    actor: str
    action: str
    context: dict

@app.get("/")
def root():
    return {"status": "TrustOps Dev API running"}

@app.post("/evidence")
def generate_evidence(payload: EvidencePayload):
    try:
        record = create_evidence_record(payload.dict())
        if "error" in record:
            raise HTTPException(status_code=500, detail=record["error"])
        print("✅ Insert success:", record)
        return record
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
