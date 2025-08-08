# Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
ENV OPENAI_API_KEY=""
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
