# Stage 1: build dependencies
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: final image
FROM python:3.11-slim
WORKDIR /app

# Create non-root user
RUN useradd -m appuser
COPY --from=builder /root/.local /home/appuser/.local
COPY api.py .

ENV PATH=/home/appuser/.local/bin:$PATH
USER appuser

EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]