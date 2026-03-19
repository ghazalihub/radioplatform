import pydicom
from pydicom.dataset import Dataset, FileDataset
import datetime

def create_mock_dicom(filename="mock.dcm"):
    file_meta = Dataset()
    file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2' # CT Image Storage
    file_meta.MediaStorageSOPInstanceUID = "1.2.3"
    file_meta.ImplementationClassUID = "1.2.3.4"
    file_meta.TransferSyntaxUID = '1.2.840.10008.1.2.1' # Explicit VR Little Endian

    ds = FileDataset(filename, {}, file_meta=file_meta, preamble=b"\0" * 128)
    ds.PatientID = "PAT001"
    ds.PatientName = "DOE^JOHN"
    ds.PatientBirthDate = "19800101"
    ds.PatientSex = "M"
    ds.StudyInstanceUID = "1.2.840.113619.2.55.3.42710123.847.1062380242.1"
    ds.StudyDate = "20230101"
    ds.StudyDescription = "CHEST CT"
    ds.AccessionNumber = "ACC001"
    ds.SeriesInstanceUID = "1.2.840.113619.2.55.3.42710123.847.1062380242.2"
    ds.Modality = "CT"
    ds.SeriesDescription = "AXIAL"
    ds.SeriesNumber = 1
    ds.SOPInstanceUID = "1.2.840.113619.2.55.3.42710123.847.1062380242.3"
    ds.SOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
    ds.InstanceNumber = 1

    # Minimal image data
    ds.Rows = 512
    ds.Columns = 512
    ds.BitsAllocated = 16
    ds.BitsStored = 12
    ds.HighBit = 11
    ds.PixelRepresentation = 0 # unsigned
    ds.SamplesPerPixel = 1
    ds.PixelData = b'\x00' * (512 * 512 * 2)

    ds.save_as(filename)
    print(f"Created {filename}")

if __name__ == "__main__":
    create_mock_dicom()
