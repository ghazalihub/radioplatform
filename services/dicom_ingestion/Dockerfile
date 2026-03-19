FROM python:3.9-slim
WORKDIR /app
COPY ./services/dicom_ingestion/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./services/dicom_ingestion /app/services/dicom_ingestion
COPY ./shared /app/shared
WORKDIR /app/services/dicom_ingestion
CMD ["python", "main.py"]
