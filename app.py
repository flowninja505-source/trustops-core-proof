import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from trustops.evidence.logger import create_evidence_record
from supabase import create_client

# Load environment variables
load_dotenv(dotenv_path=".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")  # use service key

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase credentials not set.")

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# FastAPI app
app = FastAPI(title="TrustOps Core Proof API")

# Root endpoint
@app.get("/")
def root():
    return {"status": "ok", "message": "TrustOps Core Proof API running"}

# Pydantic model for request payload
class EvidencePayload(BaseModel):
    decision_id: str
    actor: str
    action: str
    context: dict

# POST /evidence endpoint
@app.post("/evidence")
def generate_evidence(payload: EvidencePayload):
    record = create_evidence_record(payload.dict())
    return record
