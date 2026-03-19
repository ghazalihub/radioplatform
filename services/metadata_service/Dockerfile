FROM python:3.9-slim
WORKDIR /app
COPY ./services/metadata_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./services/metadata_service /app/services/metadata_service
COPY ./shared /app/shared
WORKDIR /app/services/metadata_service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
