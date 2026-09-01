# IntegrationsMono

This project connects **PX4 SITL** to a **C2 API** through a MAVLink bridge and NATS.

```
PX4 SITL  --MAVLink-->  mavlink-bridge  --NATS telemetry-->  c2-api  --HTTP-->  browser
```

## Project layout

- `adapters/` — shared models (`TelemetryFrame`) used by the MAVLink bridge
- `c2/` — FastAPI command-and-control service and web UI
- `mavlinkBridge/` — reads vehicle position over MAVLink and publishes JSON to NATS
- `environments/dev/` — Docker Compose stack for local development
- `ingestion/px4/` — helper to pull/push the PX4 SITL image

## Prerequisites

- Docker and Docker Compose
- Python 3.12 (for local run/debug)
- Optional: a Python virtual environment for local app execution

From the repo root, install deps once:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Quick start

From the repository root:

```bash
docker compose -f environments/dev/docker-compose.yml up --build
```

This starts NATS, PX4 SITL, the MAVLink bridge, and the C2 API.

Open the app in your browser:

```text
http://127.0.0.1:8000
```

Stop everything:

```bash
docker compose -f environments/dev/docker-compose.yml down
```

Rebuild a single service (example: the bridge):

```bash
docker compose -f environments/dev/docker-compose.yml up -d --build --no-deps mavlink-bridge
```

---

## Build the individual Docker images

### MAVLink bridge

```bash
docker build -f mavlinkBridge/Dockerfile -t mavlink-bridge:local .
```

### C2 API

```bash
docker build -f c2/Dockerfile -t c2-api:local .
```

### Run the MAVLink bridge manually

NATS and a MAVLink source must already be running on the host:

```bash
docker run --rm -it --network host mavlink-bridge:local
```

---

## Local development without Docker Compose

### Run the C2 API locally while NATS stays in Docker

```bash
docker compose -f environments/dev/docker-compose.yml up nats
source .venv/bin/activate
NATS_SERVER_URL=nats://localhost:4222 uvicorn c2.api.app:app --reload --app-dir .
```

### Run the MAVLink bridge locally

```bash
source .venv/bin/activate
python -m mavlinkBridge.reader
```

The bridge expects NATS at `nats://localhost:4222` and MAVLink at `udpin://0.0.0.0:14550` unless you override `NATS_SERVER_URL` and `MAVSDK_SYSTEM_ADDRESS`.

---

## PX4 SITL image helper

```bash
GITHUB_ORG=acme PX4_VERSION=latest bash ingestion/px4/ingest.sh
```

This pulls the upstream PX4 SITL image and pushes it to your GHCR third-party registry.

---

## Troubleshooting notes

- If a service fails with an `exec format error`, verify the image architecture matches your host machine.
- If you are debugging a local Python app, use the repo root as the working directory.
- If Docker build caching causes confusion, rebuild with `--no-cache` or recreate the container with `docker compose up --force-recreate --build`.
