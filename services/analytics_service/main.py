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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8008)
