import pydicom
from datetime import datetime

def extract_metadata(ds: pydicom.Dataset):
    """Extracts relevant metadata from a pydicom Dataset."""
    metadata = {
        "patient": {
            "patient_id": ds.get("PatientID", "UNKNOWN"),
            "name": str(ds.get("PatientName", "UNKNOWN")),
            "birth_date": parse_dicom_date(ds.get("PatientBirthDate")),
            "sex": ds.get("PatientSex", "O")
        },
        "study": {
            "study_instance_uid": ds.get("StudyInstanceUID"),
            "study_date": parse_dicom_date(ds.get("StudyDate")),
            "study_description": ds.get("StudyDescription", ""),
            "accession_number": ds.get("AccessionNumber", "")
        },
        "series": {
            "series_instance_uid": ds.get("SeriesInstanceUID"),
            "modality": ds.get("Modality"),
            "series_description": ds.get("SeriesDescription", ""),
            "series_number": ds.get("SeriesNumber", 0)
        },
        "instance": {
            "sop_instance_uid": ds.get("SOPInstanceUID"),
            "sop_class_uid": ds.get("SOPClassUID"),
            "instance_number": ds.get("InstanceNumber", 0),
            "metadata_json": {
                "WindowCenter": ds.get("WindowCenter"),
                "WindowWidth": ds.get("WindowWidth"),
                "Rows": ds.get("Rows"),
                "Columns": ds.get("Columns"),
                "PixelSpacing": list(ds.get("PixelSpacing", [])) if ds.get("PixelSpacing") else None
            }
        }
    }
    return metadata

def parse_dicom_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y%m%d")
    except ValueError:
        return None

def validate_dicom(ds: pydicom.Dataset):
    """Validates that mandatory DICOM tags are present."""
    required_tags = ["PatientID", "StudyInstanceUID", "SeriesInstanceUID", "SOPInstanceUID", "Modality"]
    for tag in required_tags:
        if tag not in ds:
            return False, f"Missing required tag: {tag}"
    return True, None
