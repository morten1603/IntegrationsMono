import asyncio
import json
import os
from dataclasses import asdict

import nats
from mavsdk import System
from mavsdk.telemetry import Position
from nats.aio.client import Client

from adapters.common.models import TelemetryFrame, utc_now


def position_to_frame(position: Position) -> TelemetryFrame:
    return TelemetryFrame(
        timestamp=utc_now(),
        latitude=float(position.latitude_deg),
        longitude=float(position.longitude_deg),
        altitude_m=float(position.absolute_altitude_m),
        battery_pct=0.0,
        mode="UNKNOWN",
        armed=False,
        source="mavlink",
        extra={"relative_altitude_m": getattr(position, "relative_altitude_m", 0.0)},
    )


def frame_to_payload(frame: TelemetryFrame) -> bytes:
    payload = asdict(frame)
    payload["timestamp"] = frame.timestamp.isoformat()
    return json.dumps(payload).encode()


async def publish_position(position: Position, nc: Client) -> None:
    frame = position_to_frame(position)
    await nc.publish("telemetry", frame_to_payload(frame))


async def main() -> None:
    nats_url = os.getenv("NATS_SERVER_URL", "nats://127.0.0.1:4222")
    system_address = os.getenv("MAVSDK_SYSTEM_ADDRESS", "udpin://0.0.0.0:14550")

    nc = await nats.connect(nats_url)
    print(f"Connected to NATS at {nats_url}")

    drone = System()
    print(f"Connecting to drone (MAVSDK) at {system_address}...")
    await drone.connect(system_address=system_address)
    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Connected to drone!")
            break

    try:
        async for position in drone.telemetry.position():
            # print(
            #     f"lat={position.latitude_deg} lon={position.longitude_deg} "
            #     f"alt={position.absolute_altitude_m}m"
            # )
            await publish_position(position, nc)
    finally:
        print("Disconnecting from drone...")
        drone._stop_mavsdk_server()
        print("Disconnecting from NATS...")
        await nc.close()


if __name__ == "__main__":
    asyncio.run(main())
