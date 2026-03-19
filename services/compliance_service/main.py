from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Radiology Compliance Service")

class Consent(BaseModel):
    patient_id: str
    consent_type: str # e.g. "RESEARCH", "TREATMENT"
    status: str # "GRANTED", "REVOKED"
    timestamp: datetime = datetime.utcnow()

# Mock Database
consent_db = {}

@app.post("/consent")
async def register_consent(consent: Consent):
    consent_db[consent.patient_id] = consent
    return {"status": "Consent recorded"}

@app.get("/consent/{patient_id}")
async def check_consent(patient_id: str):
    if patient_id not in consent_db:
        return {"patient_id": patient_id, "status": "NOT_FOUND"}
    return consent_db[patient_id]

@app.get("/hipaa/audit-trail")
async def get_hipaa_audit():
    """Placeholder for HIPAA compliance reporting."""
    return {"compliance_status": "OK", "last_audit": datetime.utcnow()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8013)
