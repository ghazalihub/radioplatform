import pytest
from fastapi.testclient import TestClient
from services.reporting_service.main import app

client = TestClient(app)

def test_create_report():
    report_data = {
        "study_instance_uid": "1.2.3",
        "patient_id": "P123",
        "findings": [{"label": "Lungs", "description": "Clear"}],
        "impression": "Normal study",
        "radiologist_id": "RAD1"
    }
    response = client.post("/reports", json=report_data)
    assert response.status_code == 200
    assert response.json()["id"].startswith("REP-")

def test_get_report_pdf():
    # First create a report
    report_data = {
        "study_instance_uid": "1.2.3",
        "patient_id": "P123",
        "findings": [],
        "impression": "Normal",
        "radiologist_id": "RAD1"
    }
    create_resp = client.post("/reports", json=report_data)
    report_id = create_resp.json()["id"]

    response = client.get(f"/reports/{report_id}/pdf")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
