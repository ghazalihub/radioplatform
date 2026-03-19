from fastapi import FastAPI
from tasks import process_study
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Radiology AI Service")

class AIRequest(BaseModel):
    study_instance_uid: str
    instance_uids: List[str]
    model_name: str = "fracture_detection"

class AIModel(BaseModel):
    name: str
    version: str
    description: str

model_registry = {
    "fracture_detection": AIModel(name="fracture_detection", version="1.0.0", description="Detects bone fractures in X-ray and CT."),
    "lung_nodule": AIModel(name="lung_nodule", version="2.1.0", description="Detects lung nodules in Chest CT.")
}

@app.get("/models")
async def get_models():
    return list(model_registry.values())

@app.post("/process")
async def start_processing(request: AIRequest):
    if request.model_name not in model_registry:
        raise HTTPException(status_code=400, detail="Model not found in registry")
    task = process_study.delay(request.study_instance_uid, request.instance_uids, request.model_name)
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
