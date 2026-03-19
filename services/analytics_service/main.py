from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(title="Radiology Analytics Service")

@app.get("/metrics/modality-usage")
async def get_modality_usage():
    """Returns usage statistics by modality."""
    return {
        "CT": 150,
        "MRI": 80,
        "XR": 300,
        "US": 45
    }

@app.get("/metrics/turnaround-time")
async def get_turnaround_time():
    """Returns average report turnaround time."""
    return {
        "average_hours": 4.5,
        "target_hours": 4.0
    }

@app.get("/metrics/radiologist-productivity")
async def get_radiologist_productivity():
    """Returns productivity metrics per radiologist."""
    return [
        {"radiologist_id": "RAD1", "reports_today": 25, "average_time_per_report": "12m"},
        {"radiologist_id": "RAD2", "reports_today": 18, "average_time_per_report": "15m"}
    ]

@app.get("/metrics/modality-throughput")
async def get_modality_throughput():
    """Returns studies processed per hour per modality."""
    return {
        "CT": [10, 12, 15, 8, 14, 11], # Last 6 hours
        "MRI": [2, 3, 2, 4, 3, 2]
    }

@app.get("/metrics/predictive-workload")
async def get_predictive_workload():
    """Predicts workload for the next 24 hours."""
    return {
        "predicted_studies": 450,
        "confidence_interval": [400, 500],
        "peak_hour": "10:00 AM"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8008)
