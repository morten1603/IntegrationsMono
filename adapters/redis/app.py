"""Standalone entry point for the Redis adapter container."""

import json
import os
import time

from adapters.common.models import utc_now
from adapters.mock.adapter import MockAdapter
from adapters.redis.adapter import RedisAdapter


def main() -> None:
    adapter = RedisAdapter()
    if not adapter.ping():
        raise SystemExit(f"Could not connect to Redis at {adapter._host}:{adapter._port}")

    print(f"Connected to Redis COTS at {adapter._host}:{adapter._port}")
    simulator = MockAdapter(name="redis-cots-simulator")

    publish_interval = float(os.getenv("TELEMETRY_INTERVAL_S", "1.0"))
    while True:
        frame = simulator.get_latest()
        frame.source = adapter.name
        adapter.publish_telemetry(frame)
        print(json.dumps({"published": True, "timestamp": utc_now().isoformat()}))
        time.sleep(publish_interval)


if __name__ == "__main__":
    main()
