from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

app = FastAPI(title="Radiology Audit Service")

class AuditEntry(BaseModel):
    timestamp: datetime = datetime.utcnow()
    user_id: str
    action: str
    resource: str
    details: str

# Mock Database (In production, use Elasticsearch or a high-volume DB)
audit_log_db = []

@app.post("/logs")
async def create_log(entry: AuditEntry):
    audit_log_db.append(entry)
    return {"status": "Logged"}

@app.get("/logs", response_model=List[AuditEntry])
async def get_logs(user_id: Optional[str] = None):
    if user_id:
        return [log for log in audit_log_db if log.user_id == user_id]
    return audit_log_db

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8011)
