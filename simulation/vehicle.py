"""In-memory fake UAV used by the simulation harness."""

import math
import time

from adapters.common.models import Command, CommandType, Result, TelemetryFrame, utc_now


class SimulatedVehicle:
    def __init__(self, name: str = "simulator") -> None:
        self._name = name
        self._start = time.monotonic()
        self._armed = False
        self._mode = "STABILIZE"

    @property
    def name(self) -> str:
        return self._name

    def next_telemetry(self) -> TelemetryFrame:
        elapsed = time.monotonic() - self._start
        latitude = 59.9139 + 0.0001 * math.sin(elapsed / 10)
        longitude = 10.7522 + 0.0001 * math.cos(elapsed / 10)
        altitude = 120.0 + 5.0 * math.sin(elapsed / 5)
        battery = max(0.0, 100.0 - elapsed * 0.05)

        return TelemetryFrame(
            timestamp=utc_now(),
            latitude=latitude,
            longitude=longitude,
            altitude_m=altitude,
            battery_pct=round(battery, 1),
            mode=self._mode,
            armed=self._armed,
            source=self._name,
            extra={"simulated": True, "elapsed_s": round(elapsed, 1)},
        )

    def apply_command(self, cmd: Command) -> Result:
        if cmd.type == CommandType.ARM:
            self._armed = True
            return Result(success=True, message="Simulated vehicle armed")
        if cmd.type == CommandType.DISARM:
            self._armed = False
            return Result(success=True, message="Simulated vehicle disarmed")
        if cmd.type == CommandType.SET_MODE:
            mode = str(cmd.params.get("mode", "GUIDED"))
            self._mode = mode
            return Result(success=True, message=f"Simulated mode set to {mode}")
        return Result(success=False, message=f"Unsupported command: {cmd.type}")
