from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import shutil
import uuid
from cryptography.fernet import Fernet
from io import BytesIO

app = FastAPI(title="Radiology Storage Service")

ENCRYPTION_KEY = os.getenv("STORAGE_ENCRYPTION_KEY", Fernet.generate_key().decode())
fernet = Fernet(ENCRYPTION_KEY.encode())

HOT_STORAGE_DIR = os.getenv("HOT_STORAGE_DIR", "/tmp/radiology_hot")
COLD_STORAGE_DIR = os.getenv("COLD_STORAGE_DIR", "/tmp/radiology_cold")

for d in [HOT_STORAGE_DIR, COLD_STORAGE_DIR]:
    if not os.path.exists(d):
        os.makedirs(d)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    # All new uploads go to hot storage
    file_path = os.path.join(HOT_STORAGE_DIR, file_id)

    content = await file.read()
    encrypted_content = fernet.encrypt(content)

    with open(file_path, "wb") as buffer:
        buffer.write(encrypted_content)

    return {"file_id": file_id, "file_path": file_path}

@app.get("/download/{file_id}")
async def download_file(file_id: str):
    file_path = os.path.join(HOT_STORAGE_DIR, file_id)
    if not os.path.exists(file_path):
        file_path = os.path.join(COLD_STORAGE_DIR, file_id)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    with open(file_path, "rb") as buffer:
        encrypted_content = buffer.read()
        decrypted_content = fernet.decrypt(encrypted_content)

    # Write decrypted to temporary buffer for response
    # In a real system, use streaming with on-the-fly decryption
    temp_path = f"{file_path}_tmp"
    with open(temp_path, "wb") as f:
        f.write(decrypted_content)

    return FileResponse(temp_path, filename=f"{file_id}.dcm")

@app.post("/archive/{file_id}")
async def archive_file(file_id: str):
    """Move file from hot to cold storage."""
    hot_path = os.path.join(HOT_STORAGE_DIR, file_id)
    cold_path = os.path.join(COLD_STORAGE_DIR, file_id)

    if not os.path.exists(hot_path):
        raise HTTPException(status_code=404, detail="File not found in hot storage")

    shutil.move(hot_path, cold_path)
    return {"message": "File archived to cold storage"}

@app.delete("/delete/{file_id}")
async def delete_file(file_id: str):
    file_path = os.path.join(HOT_STORAGE_DIR, file_id)
    if not os.path.exists(file_path):
        file_path = os.path.join(COLD_STORAGE_DIR, file_id)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    os.remove(file_path)
    return {"message": "File deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
