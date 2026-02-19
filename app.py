from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from pydantic import BaseModel
from trustops.evidence.logger import create_evidence_record


app = FastAPI(title="TrustOps Core Proof API")


class DecisionPayload(BaseModel):
    decision_id: str
    actor: str
    action: str
    context: dict


@app.get("/")
def root():
    return {"status": "TrustOps API running"}


@app.post("/evidence")
def generate_evidence(payload: DecisionPayload):
    record = create_evidence_record(payload.dict())
    return record
