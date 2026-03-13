from fastapi import FastAPI, Request
import hl7
from fhir.resources.patient import Patient as FHIRPatient
import requests
import os

app = FastAPI(title="Radiology Integration Service")

METADATA_SERVICE_URL = os.getenv("METADATA_SERVICE_URL", "http://metadata-service:8002")

@app.post("/hl7/ingest")
async def ingest_hl7(request: Request):
    """Ingest HL7 messages (e.g., ADT - Patient Registration)."""
    raw_message = await request.body()
    # Simplified HL7 parsing
    # h = hl7.parse(raw_message.decode())
    # patient_id = h['PID'][0][3]

    return {"status": "HL7 message received", "message_type": "ADT"}

@app.post("/fhir/Patient")
async def ingest_fhir_patient(patient: dict):
    """Ingest FHIR Patient resources."""
    fhir_patient = FHIRPatient.parse_obj(patient)

    # Sync with Metadata Service
    try:
        requests.post(f"{METADATA_SERVICE_URL}/patients", json={
            "patient_id": fhir_patient.id,
            "name": f"{fhir_patient.name[0].given[0]} {fhir_patient.name[0].family}",
            "sex": fhir_patient.gender[0].upper() if fhir_patient.gender else "O"
        })
    except Exception as e:
        print(f"Error syncing FHIR patient: {e}")

    return {"status": "FHIR Patient synced", "id": fhir_patient.id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8010)
