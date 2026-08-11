FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml ./
COPY adapters ./adapters
COPY simulation ./simulation

RUN pip install --no-cache-dir redis

ENV PYTHONPATH=/app

CMD ["python", "-m", "simulation.publisher"]
