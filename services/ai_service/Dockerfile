FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Start both FastAPI and Celery Worker (Simplified for demo, in production use separate containers)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8007 & celery -A tasks worker --loglevel=info"]
