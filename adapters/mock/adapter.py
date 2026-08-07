import json
import math
import time

from adapters.common.models import Command, CommandType, Result, TelemetryFrame, utc_now


class MockAdapter:
    """In-memory adapter that simulates a UAV sending telemetry."""

    def __init__(self, name: str = "mock") -> None:
        self._name = name
        self._start = time.monotonic()
        self._armed = False
        self._mode = "STABILIZE"

    @property
    def name(self) -> str:
        return self._name

    def ping(self) -> bool:
        return True

    def get_latest(self) -> TelemetryFrame:
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

    def send_command(self, cmd: Command) -> Result:
        if cmd.type == CommandType.ARM:
            self._armed = True
            return Result(success=True, message="Mock vehicle armed")
        if cmd.type == CommandType.DISARM:
            self._armed = False
            return Result(success=True, message="Mock vehicle disarmed")
        if cmd.type == CommandType.SET_MODE:
            mode = str(cmd.params.get("mode", "GUIDED"))
            self._mode = mode
            return Result(success=True, message=f"Mock mode set to {mode}")
        return Result(success=False, message=f"Unsupported command: {cmd.type}")

    def to_json(self) -> str:
        frame = self.get_latest()
        payload = {
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
        return json.dumps(payload)
