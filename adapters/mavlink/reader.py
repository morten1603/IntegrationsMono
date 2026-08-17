import asyncio
from mavsdk import System

async def print_position(drone):
    # Subscribe to position stream
    async for position in drone.telemetry.position():
        print(f"Latitude: {position.latitude_deg}")
        print(f"Longitude: {position.longitude_deg}")
        print(f"Absolute Altitude: {position.absolute_altitude_m} m")
        print(f"Relative Altitude: {position.relative_altitude_m} m")
        print("-" * 30)

async def main():
    drone = System()
    # Connect to a local simulation or device (change connection URL if needed)
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Connected to drone!")
            break

    # Start the telemetry task
    await print_position(drone)

if __name__ == "__main__":
    asyncio.run(main())
