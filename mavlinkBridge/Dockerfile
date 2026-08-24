FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml ./
COPY adapters ./adapters
COPY mavlinkBridge ./mavlinkBridge

RUN pip install --no-cache-dir -e .

ENV PYTHONPATH=/app

CMD ["python", "-m", "mavlinkBridge.reader"]
