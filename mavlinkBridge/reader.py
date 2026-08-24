import asyncio
import os
import nats

from nats.aio.client import Client
from mavsdk import System

from adapters.common.models import TelemetryFrame, utc_now
from adapters.redis.adapter import RedisAdapter


async def print_position(drone: System):
    async for position in drone.telemetry.position():
        print(f"Latitude: {position.latitude_deg}")
        print(f"Longitude: {position.longitude_deg}")
        print(f"Absolute Altitude: {position.absolute_altitude_m} m")
        print(f"Relative Altitude: {position.relative_altitude_m} m")
        print("-" * 30)


# async def publish_telemetry(drone: System, adapter: RedisAdapter):
#     position = await drone.telemetry.position()
#     frame = TelemetryFrame(
#         timestamp=utc_now(),
#         latitude=float(position.latitude_deg),
#         longitude=float(position.longitude_deg),
#         altitude_m=float(position.absolute_altitude_m),
#         battery_pct=0.0,
#         mode="UNKNOWN",
#         armed=False,
#         source="mavlink",
#         extra={"relative_altitude_m": getattr(position, "relative_altitude_m", 0.0)},
#     )
#     return adapter.publish_telemetry(frame)

async def publish_telemetry(drone: System, nc: Client):
    position = await drone.telemetry.position()
    frame = TelemetryFrame(
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
    return nc.publish("telemetry", frame.json().encode())


async def main():
    host = os.getenv("COTS_HOST", "localhost")
    port = int(os.getenv("COTS_PORT", "6379"))
    adapter = RedisAdapter(host=host, port=port, name="mavlink")

    if not adapter.ping():
        raise SystemExit(f"Could not connect to Redis at {host}:{port}")

    print(f"Connected to Redis at {host}:{port}")

    nc = await nats.connect("nats://localhost:4222")
    print("Connected to NATS at nats://localhost:4222")

    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Connected to drone!")
            break

    while True:
        #result = await publish_telemetry(drone, adapter)
        result = await publish_telemetry(drone, nc)
        if not result.success:
            print(result.message)
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
