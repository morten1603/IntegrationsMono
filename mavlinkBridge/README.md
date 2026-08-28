# mavlinkBridge

Reads vehicle position over **MAVLink** (via MAVSDK), maps it to the canonical `TelemetryFrame`, and publishes JSON to **NATS** on the `telemetry` subject.

```
PX4 / SITL  --MAVLink udp://:14540-->  reader  --NATS-->  telemetry
```

## Prerequisites

- Docker (for image build / compose)
- Python 3.11+ with project venv (for local run and unit tests)
- A MAVLink source on `udp://:14540` (e.g. PX4 SITL)
- NATS listening on `nats://localhost:4222`

From the repo root, install deps once:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Build

From the **repository root**:

```bash
docker build -f mavlinkBridge/Dockerfile -t mavlink-bridge:local .
```

Or via compose:

```bash
docker compose -f environments/dev/docker-compose.yml build mavlink-bridge
```

## Run

### With Docker Compose (full stack)

From the repository root:

```bash
docker compose -f environments/dev/docker-compose.yml up --build
```

The `mavlink-bridge` service builds this package and uses host networking so it can reach PX4 SITL on UDP `14540` and NATS on `4222`.

### Docker image only

NATS and a MAVLink source must already be running on the host:

```bash
docker run --rm -it --network host mavlink-bridge:local
```

### Locally (venv)

```bash
source .venv/bin/activate
python -m mavlinkBridge.reader
```

Expected flow:

1. Connect to NATS at `nats://localhost:4222`
2. Connect to the vehicle at `udp://:14540`
3. Print one position update and publish it to NATS subject `telemetry`

## Test

Unit tests cover mapping and publish logic with mocks (no PX4, no NATS server):

```bash
source .venv/bin/activate
pytest tests/test_mavlink_bridge_reader.py -q
```

What is tested:

- `position_to_frame` — MAVSDK position → `TelemetryFrame`
- `frame_to_payload` — frame → JSON bytes
- `publish_position` — publishes on subject `telemetry` (mocked NATS client)

## Layout

| Path | Role |
|---|---|
| `reader.py` | Bridge entrypoint and publish helpers |
| `Dockerfile` | Container image for the bridge |
| `../tests/test_mavlink_bridge_reader.py` | Unit tests |
