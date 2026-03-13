from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import shutil
import uuid

app = FastAPI(title="Radiology Storage Service")

STORAGE_DIR = os.getenv("STORAGE_DIR", "/tmp/radiology_storage")

if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    file_path = os.path.join(STORAGE_DIR, file_id)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"file_id": file_id, "file_path": file_path}

@app.get("/download/{file_id}")
async def download_file(file_id: str):
    file_path = os.path.join(STORAGE_DIR, file_id)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)

@app.delete("/delete/{file_id}")
async def delete_file(file_id: str):
    file_path = os.path.join(STORAGE_DIR, file_id)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    os.remove(file_path)
    return {"message": "File deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
