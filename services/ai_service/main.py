from fastapi import FastAPI
from tasks import process_study
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Radiology AI Service")

class AIRequest(BaseModel):
    study_instance_uid: str
    instance_uids: List[str]

@app.post("/process")
async def start_processing(request: AIRequest):
    task = process_study.delay(request.study_instance_uid, request.instance_uids)
    return {"task_id": task.id, "status": "Processing started"}

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    from tasks import celery_app
    task_result = celery_app.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8007)
