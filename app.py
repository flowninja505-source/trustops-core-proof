import os
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from supabase import create_client
from trustops.evidence.logger import create_evidence_record

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("trustops-dev")

# Function to load Supabase client dynamically
def get_supabase_client():
    load_dotenv(dotenv_path=".env")  # reload env each call in dev
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        raise ValueError("Supabase credentials not set.")
    return create_client(url, key)

# FastAPI app
app = FastAPI(title="TrustOps Core Proof API - Dev")

# Root endpoint
@app.get("/")
def root():
    return {"status": "ok", "message": "TrustOps Core Proof API running (dev)"}

# Pydantic model for request payload
class EvidencePayload(BaseModel):
    decision_id: str
    actor: str
    action: str
    context: dict

# POST /evidence endpoint
@app.post("/evidence")
def generate_evidence(payload: EvidencePayload):
    supabase = get_supabase_client()  # get fresh client each request
    try:
        record = create_evidence_record(payload.dict())
        logger.info(f"Inserted record: {record}")
        return record
    except Exception as e:
        logger.error(f"Failed to insert record: {e}")
        return {"error": str(e)}
