import os
import pydicom
from pynetdicom import AE, evt, StoragePresentationContexts, QueryRetrievePresentationContexts
from pynetdicom.sop_class import (
    CTImageStorage, MRImageStorage, PositronEmissionTomographyImageStorage,
    PatientRootQueryRetrieveInformationModelFind,
    PatientRootQueryRetrieveInformationModelMove,
    PatientRootQueryRetrieveInformationModelGet
)
import requests
import io
from utils import extract_metadata, validate_dicom

# Configuration
STORAGE_SERVICE_URL = os.getenv("STORAGE_SERVICE_URL", "http://storage-service:8003/upload")
METADATA_SERVICE_URL = os.getenv("METADATA_SERVICE_URL", "http://metadata-service:8002/instances")

def handle_find(event):
    """Handle a C-FIND request event."""
    ds = event.dataset
    print(f"Received C-FIND request: {ds}")

    # In a real system, query the metadata service here
    # For now, return a placeholder success
    yield 0xFF00, None # Pending

def handle_move(event):
    """Handle a C-MOVE request event."""
    ds = event.dataset
    print(f"Received C-MOVE request: {ds}")
    return "DEST_AE", 0x0000

def handle_get(event):
    """Handle a C-GET request event."""
    ds = event.dataset
    print(f"Received C-GET request: {ds}")
    return 0x0000

def handle_store(event):
    """Handle a C-STORE request event."""
    ds = event.dataset
    ds.file_meta = event.file_meta

    # 0. Validate DICOM
    is_valid, error_msg = validate_dicom(ds)
    if not is_valid:
        print(f"Validation failed: {error_msg}")
        return 0xC000 # Processing Failure

    # 1. Save to Storage Service
    buffer = io.BytesIO()
    ds.save_as(buffer)
    buffer.seek(0)

    files = {'file': ('dicom_file.dcm', buffer)}
    try:
        storage_resp = requests.post(STORAGE_SERVICE_URL, files=files)
        storage_resp.raise_for_status()
        file_info = storage_resp.json()
        file_path = file_info['file_path']
    except Exception as e:
        print(f"Error saving to storage service: {e}")
        return 0xC001 # Error: Out of Resources

    # 2. Extract and Save Metadata
    metadata = extract_metadata(ds)
    metadata["instance"]["file_path"] = file_path

    try:
        base_url = METADATA_SERVICE_URL.rsplit('/', 1)[0]
        # Create Patient
        resp = requests.post(f"{base_url}/patients", json=metadata["patient"])
        resp.raise_for_status()

        # Create Study
        study_data = metadata["study"]
        study_data["patient_id"] = metadata["patient"]["patient_id"]
        resp = requests.post(f"{base_url}/studies", json=study_data)
        resp.raise_for_status()

        # Create Series
        series_data = metadata["series"]
        series_data["study_instance_uid"] = metadata["study"]["study_instance_uid"]
        resp = requests.post(f"{base_url}/series", json=series_data)
        resp.raise_for_status()

        # Create Instance
        instance_data = metadata["instance"]
        instance_data["series_instance_uid"] = metadata["series"]["series_instance_uid"]
        resp = requests.post(f"{base_url}/instances", json=instance_data)
        resp.raise_for_status()
    except Exception as e:
        print(f"Error saving to metadata service: {e}")
        return 0xC000 # Processing Failure (0xC000 is a generic failure in DICOM)

    print(f"Successfully processed DICOM: {metadata['instance']['sop_instance_uid']}")
    return 0x0000 # Success

handlers = [
    (evt.EVT_C_STORE, handle_store),
    (evt.EVT_C_FIND, handle_find),
    (evt.EVT_C_MOVE, handle_move),
    (evt.EVT_C_GET, handle_get),
]

ae = AE(ae_title=b'RADIOLOGY_PACS')
ae.supported_contexts = StoragePresentationContexts + QueryRetrievePresentationContexts

def start_dicom_server():
    print("Starting DICOM C-STORE SCP on port 11112...")
    ae.start_server(('', 11112), block=True, evt_handlers=handlers)

if __name__ == "__main__":
    start_dicom_server()
