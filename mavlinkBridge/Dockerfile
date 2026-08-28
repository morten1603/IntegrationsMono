FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml ./
COPY adapters ./adapters
COPY mavlinkBridge ./mavlinkBridge

RUN pip install --no-cache-dir -e .

ENV PYTHONPATH=/app

ENV PYTHONUNBUFFERED=1
CMD ["python", "-u", "-m", "mavlinkBridge.reader"]
