from celery import Celery
import os
import time
import requests

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

celery_app = Celery("tasks", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

STORAGE_SERVICE_URL = os.getenv("STORAGE_SERVICE_URL", "http://storage-service:8003")
METADATA_SERVICE_URL = os.getenv("METADATA_SERVICE_URL", "http://metadata-service:8002")

@celery_app.task(name="process_study")
def process_study(study_instance_uid: str, instance_uids: list):
    """Asynchronous task to process a study with AI."""
    print(f"Starting AI processing for study {study_instance_uid}")

    results = []
    for sop_uid in instance_uids:
        # 1. Simulate downloading from storage
        # 2. Simulate AI inference (e.g. fracture detection)
        time.sleep(1) # Simulate work
        finding = {"sop_instance_uid": sop_uid, "fracture_detected": False, "confidence": 0.95}
        results.append(finding)

        # Save finding back to metadata service as an annotation
        try:
            requests.post(f"{METADATA_SERVICE_URL}/annotations", json={
                "sop_instance_uid": sop_uid,
                "label": "fracture_detection",
                "data": finding
            })
        except Exception as e:
            print(f"Error saving AI result to metadata service: {e}")

    print(f"Finished AI processing for study {study_instance_uid}")
    return {"study_instance_uid": study_instance_uid, "results": results}

if __name__ == "__main__":
    celery_app.start()
