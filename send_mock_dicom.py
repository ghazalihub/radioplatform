from pynetdicom import AE
from pydicom import dcmread

def send_dicom(filename="mock.dcm"):
    ae = AE()
    ae.add_requested_context('1.2.840.10008.5.1.4.1.1.2') # CT Image Storage

    ds = dcmread(filename)

    assoc = ae.associate('127.0.0.1', 11112)
    if assoc.is_established:
        print("Association established")
        status = assoc.send_c_store(ds)
        if status:
            print(f"C-STORE status: {status}")
        else:
            print("C-STORE failed")
        assoc.release()
    else:
        print("Association failed")

if __name__ == "__main__":
    send_dicom()
