from fastapi import FastAPI, Request, HTTPException, UploadFile, File
from fastapi.responses import Response, StreamingResponse
import requests
import os

app = FastAPI(title="DICOMweb Service")

METADATA_SERVICE_URL = os.getenv("METADATA_SERVICE_URL", "http://metadata-service:8002")
STORAGE_SERVICE_URL = os.getenv("STORAGE_SERVICE_URL", "http://storage-service:8003")

@app.get("/rs/studies")
async def qido_studies(request: Request):
    """QIDO-RS Search for Studies."""
    # Map DICOM tags to metadata service query parameters
    dicom_params = dict(request.query_params)
    params = {}
    if '00100020' in dicom_params: # PatientID
        params['patient_id'] = dicom_params['00100020']
    if '0020000D' in dicom_params: # StudyInstanceUID
        params['study_instance_uid'] = dicom_params['0020000D']

    try:
        resp = requests.get(f"{METADATA_SERVICE_URL}/studies", params=params)
        resp.raise_for_status()
        studies = resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # In a real system, convert the relational data to DICOM JSON format
    return studies

@app.get("/rs/studies/{study_uid}/series")
async def qido_series(study_uid: str, request: Request):
    """QIDO-RS Search for Series within a Study."""
    params = dict(request.query_params)
    # Placeholder implementation
    return [{"series_instance_uid": "1.2.3.4.5.6"}]

@app.get("/rs/studies/{study_uid}/series/{series_uid}/instances")
async def qido_instances(study_uid: str, series_uid: str, request: Request):
    """QIDO-RS Search for Instances within a Series."""
    # Placeholder implementation
    return [{"sop_instance_uid": "1.2.3.4.5.6.7"}]

@app.get("/rs/studies/{study_uid}/series/{series_uid}/instances/{sop_uid}")
async def wado_instance(study_uid: str, series_uid: str, sop_uid: str):
    """WADO-RS Retrieve Instance."""
    # 1. Get file_path from metadata service
    try:
        resp = requests.get(f"{METADATA_SERVICE_URL}/instances/{sop_uid}")
        resp.raise_for_status()
        instance = resp.json()
        file_path = instance['file_path']
        file_id = os.path.basename(file_path)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Instance not found")

    # 2. Proxy request to storage service
    try:
        storage_resp = requests.get(f"{STORAGE_SERVICE_URL}/download/{file_id}", stream=True)
        storage_resp.raise_for_status()
        return StreamingResponse(storage_resp.iter_content(chunk_size=8192), media_type="application/dicom")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving from storage: {e}")

@app.post("/rs/studies")
async def stow_studies(file: UploadFile = File(...)):
    """STOW-RS Store Instance."""
    # In a real system, this would:
    # 1. Store the file in Storage Service
    # 2. Extract metadata and save to Metadata Service

    # Proxy to storage service for now
    try:
        files = {'file': (file.filename, file.file, file.content_type)}
        storage_resp = requests.post(f"{STORAGE_SERVICE_URL}/upload", files=files)
        storage_resp.raise_for_status()
        return storage_resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error storing DICOM: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
