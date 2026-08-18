import asyncio
import os
from mavsdk import System

from adapters import redis

async def print_position(drone):
    # Subscribe to position stream
    async for position in drone.telemetry.position():
        print(f"Latitude: {position.latitude_deg}")
        print(f"Longitude: {position.longitude_deg}")
        print(f"Absolute Altitude: {position.absolute_altitude_m} m")
        print(f"Relative Altitude: {position.relative_altitude_m} m")
        print("-" * 30)

async def publish_telemetry(drone, client):
    json
    client.set(TELEMETRY_KEY, json)
    
def _frame_to_json(frame: position) -> str:
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


async def main():
    host = os.getenv("COTS_HOST", "localhost")
    port = int(os.getenv("COTS_PORT", "6379"))
    client = redis.Redis(host=host, port=port, decode_responses=True)

    try:
        client.ping()
    except redis.RedisError as exc:
        raise SystemExit(f"Could not connect to Redis at {host}:{port}") from exc
    
    print(f"Connected to Redis at {host}:{port}")
    
    drone = System()
    # Connect to a local simulation or device (change connection URL if needed)
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Connected to drone!")
            break

    # Start the telemetry task
    #await print_position(drone)


if __name__ == "__main__":
    asyncio.run(main())
