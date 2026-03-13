from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from fpdf import FPDF
import io
from fastapi.responses import Response

app = FastAPI(title="Radiology Reporting Service")

class Finding(BaseModel):
    label: str
    description: str
    location: Optional[str] = None

class ReportCreate(BaseModel):
    study_instance_uid: str
    patient_id: str
    findings: List[Finding]
    impression: str
    radiologist_id: str

class Report(ReportCreate):
    id: str
    created_at: datetime
    status: str = "final"

# Mock database
reports_db = {}
templates_db = {
    "CHEST_XR": {
        "name": "Chest X-Ray",
        "findings": ["Lungs are clear", "Heart size is normal", "No pleural effusion"],
        "impression": "Normal Chest X-Ray"
    },
    "BRAIN_MRI": {
        "name": "Brain MRI",
        "findings": ["No acute intracranial hemorrhage", "Ventricular system is midline", "Normal flow voids"],
        "impression": "Normal Brain MRI"
    }
}

@app.get("/templates")
async def get_templates():
    return templates_db

@app.post("/reports", response_model=Report)
async def create_report(report_in: ReportCreate):
    report_id = f"REP-{len(reports_db) + 1}"
    report = Report(
        id=report_id,
        created_at=datetime.utcnow(),
        **report_in.dict()
    )
    reports_db[report_id] = report
    return report

@app.get("/reports/{report_id}", response_model=Report)
async def get_report(report_id: str):
    if report_id not in reports_db:
        raise HTTPException(status_code=404, detail="Report not found")
    return reports_db[report_id]

@app.get("/reports/{report_id}/pdf")
async def get_report_pdf(report_id: str):
    if report_id not in reports_db:
        raise HTTPException(status_code=404, detail="Report not found")

    report = reports_db[report_id]

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(40, 10, f"Radiology Report: {report.id}")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(40, 10, f"Patient ID: {report.patient_id}")
    pdf.ln(10)
    pdf.cell(40, 10, f"Study UID: {report.study_instance_uid}")
    pdf.ln(20)

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(40, 10, "Findings:")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    for finding in report.findings:
        pdf.multi_cell(0, 10, f"- {finding.label}: {finding.description}")

    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(40, 10, "Impression:")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, report.impression)

    pdf_output = pdf.output(dest='S').encode('latin-1')
    return Response(content=pdf_output, media_type="application/pdf")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8006)
