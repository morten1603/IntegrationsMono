import json
import os
from datetime import datetime
from typing import Any

import redis
from adapters.common.models import Command, Result, TelemetryFrame, utc_now


class RedisAdapter:
    """Adapter that shields the C2 app from a Redis-backed COTS interface."""

    TELEMETRY_KEY = "cots:telemetry"
    COMMAND_KEY = "cots:commands"

    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        name: str = "redis",
    ) -> None:
        self._name = name
        self._host = host or os.getenv("COTS_HOST", "localhost")
        self._port = port or int(os.getenv("COTS_PORT", "6379"))
        self._client = redis.Redis(host=self._host, port=self._port, decode_responses=True)

    @property
    def name(self) -> str:
        return self._name

    def ping(self) -> bool:
        try:
            return bool(self._client.ping())
        except redis.RedisError:
            return False

    def get_latest(self) -> TelemetryFrame:
        raw = self._client.get(self.TELEMETRY_KEY)
        if raw:
            return self._frame_from_dict(json.loads(raw))
        return self._default_frame()

    def publish_telemetry(self, frame: TelemetryFrame) -> Result:
        if not self.ping():
            return Result(success=False, message="Redis COTS unavailable")

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
        self._client.set(self.TELEMETRY_KEY, json.dumps(payload))
        return Result(success=True, message=f"Telemetry published to Redis COTS: {frame.source}")

    def send_command(self, cmd: Command) -> Result:
        if not self.ping():
            return Result(success=False, message="Redis COTS unavailable")

        payload = {"type": cmd.type.value, "params": cmd.params}
        self._client.rpush(self.COMMAND_KEY, json.dumps(payload))
        return Result(success=True, message=f"Command queued in Redis COTS: {cmd.type.value}")

    def _default_frame(self) -> TelemetryFrame:
        return TelemetryFrame(
            timestamp=utc_now(),
            latitude=0.0,
            longitude=0.0,
            altitude_m=0.0,
            battery_pct=0.0,
            mode="UNKNOWN",
            armed=False,
            source=self._name,
            extra={"note": "No telemetry published by COTS yet"},
        )

    @staticmethod
    def _frame_from_dict(data: dict[str, Any]) -> TelemetryFrame:
        timestamp_raw = data.get("timestamp")
        if isinstance(timestamp_raw, str):
            timestamp = datetime.fromisoformat(timestamp_raw.replace("Z", "+00:00"))
        else:
            timestamp = utc_now()

        return TelemetryFrame(
            timestamp=timestamp,
            latitude=float(data.get("latitude", 0.0)),
            longitude=float(data.get("longitude", 0.0)),
            altitude_m=float(data.get("altitude_m", 0.0)),
            battery_pct=float(data.get("battery_pct", 0.0)),
            mode=str(data.get("mode", "UNKNOWN")),
            armed=bool(data.get("armed", False)),
            source=str(data.get("source", "redis")),
            extra=dict(data.get("extra", {})),
        )
