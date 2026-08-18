# IntegrationsMono

This project brings together a Redis-backed integration layer, a small simulation publisher, a C2 API, and a MAVLink bridge. The repository is organized around adapters, runtime services, and local development environments.

## Project layout

- `adapters/` — adapters for shared integration logic and model/port abstractions
- `c2/` — FastAPI command-and-control service
- `simulation/` — simulation data publisher
- `mavlinkBridge/` — MAVLink reader/bridge entrypoint
- `environments/dev/` — Docker Compose files for local development
- `ingestion/redis/` — Redis ingestion helper script

## Prerequisites

- Docker and Docker Compose
- Python 3.12 (for local run/debug)
- Optional: a Python virtual environment for local app execution

## Quick start

### 1) Start the development stack

From the repository root:

```bash
docker compose -f environments/dev/docker-compose.yml up --build
```

This starts the Redis-backed services and the C2 API.

Open the app in your browser:

```text
http://127.0.0.1:8000
```

Stop everything:

```bash
docker compose -f environments/dev/docker-compose.yml down
```

### 2) Start the simulation stack

```bash
docker compose -f environments/dev/docker-compose-sim.yml up --build
```

This stack includes the Redis service, the simulation publisher, and the C2 API.

---

## Build the individual Docker images

### MAVLink bridge

```bash
docker build -f mavlinkBridge/Dockerfile -t mavlink-bridge:local .
```

### Simulation publisher

```bash
docker build -f simulation/Dockerfile -t simulation-publisher:local .
```

### C2 API

```bash
docker build -f c2/Dockerfile -t c2-api:local .
```

### Run the MAVLink bridge manually

```bash
docker run --rm -it mavlink-bridge:local
```

---

## Local development without Docker Compose

### Run the C2 API locally while Redis and the simulator stay in Docker

```bash
docker compose -f environments/dev/docker-compose.yml up --build cots-hardware simulation-publisher
source .venv/bin/activate
COTS_HOST=localhost COTS_PORT=6379 uvicorn c2.api.app:app --reload --app-dir .
```

### Run the MAVLink bridge locally

```bash
source .venv/bin/activate
PYTHONPATH=/app python -m mavlinkBridge.reader
```

---

## Redis ingestion helper

```bash
GITHUB_ORG=acme REDIS_VERSION=7.2.4 bash -lc 'source ingestion/redis/ingest.sh'
```

This is useful when you want to load or refresh Redis-backed data from a source image or repository.

---

## Troubleshooting notes

- If a service fails with an `exec format error`, verify the image architecture matches your host machine.
- If you are debugging a local Python app, use the repo root as the working directory and make sure `PYTHONPATH` includes `/app`.
- If Docker build caching causes confusion, rebuild with `--no-cache` or recreate the container with `docker compose up --force-recreate --build`.
