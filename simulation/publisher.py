"""Publish simulated telemetry into Redis COTS.

This is the simulation harness entrypoint, not part of the Redis adapter.
The Redis adapter only translates Redis <-> the canonical model; this process
invents world state and writes it through the adapter.
"""

import json
import os
import time

from adapters.common.models import utc_now
from adapters.redis.adapter import RedisAdapter
from adapters.simulator.adapter import SimulatorAdapter


def main() -> None:
    redis_adapter = RedisAdapter()
    if not redis_adapter.ping():
        raise SystemExit(
            f"Could not connect to Redis at {redis_adapter._host}:{redis_adapter._port}"
        )

    print(f"Connected to Redis COTS at {redis_adapter._host}:{redis_adapter._port}")
    simulator = SimulatorAdapter(name="redis-cots-simulator")

    publish_interval = float(os.getenv("TELEMETRY_INTERVAL_S", "1.0"))
    while True:
        frame = simulator.get_latest()
        frame.source = redis_adapter.name
        redis_adapter.publish_telemetry(frame)
        print(json.dumps({"published": True, "timestamp": utc_now().isoformat()}))
        time.sleep(publish_interval)


if __name__ == "__main__":
    main()
