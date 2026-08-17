"""Publish simulated telemetry into Redis (COTS stand-in)."""

import json
import os
import time

import redis

from adapters.common.models import TelemetryFrame, utc_now
from simulation.vehicle import SimulatedVehicle

# Must stay in sync with RedisAdapter.TELEMETRY_KEY
TELEMETRY_KEY = "cots:telemetry"


def _frame_to_json(frame: TelemetryFrame) -> str:
    return json.dumps(
        {
            "timestamp": frame.timestamp.isoformat(),
            "latitude": frame.latitude,
            "longitude": frame.longitude,
            "altitude_m": frame.altitude_m,
            "battery_pct": frame.battery_pct,
            "mode": frame.mode,
            "armed": frame.armed,
            "source": frame.source,
            "extra": frame.extra,
        }
    )


def main() -> None:
    host = os.getenv("COTS_HOST", "localhost")
    port = int(os.getenv("COTS_PORT", "6379"))
    client = redis.Redis(host=host, port=port, decode_responses=True)

    try:
        client.ping()
    except redis.RedisError as exc:
        raise SystemExit(f"Could not connect to Redis at {host}:{port}") from exc

    print(f"Connected to Redis at {host}:{port}")
    vehicle = SimulatedVehicle(name="simulator")

    publish_interval = float(os.getenv("TELEMETRY_INTERVAL_S", "1.0"))
    while True:
        frame = vehicle.next_telemetry()
        client.set(TELEMETRY_KEY, _frame_to_json(frame))
        print(
            json.dumps(
                {
                    "published": True,
                    "source": frame.source,
                    "timestamp": utc_now().isoformat(),
                }
            )
        )
        time.sleep(publish_interval)


if __name__ == "__main__":
    main()
