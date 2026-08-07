from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any


class CommandType(str, Enum):
    ARM = "arm"
    DISARM = "disarm"
    SET_MODE = "set_mode"


@dataclass
class TelemetryFrame:
    timestamp: datetime
    latitude: float
    longitude: float
    altitude_m: float
    battery_pct: float
    mode: str
    armed: bool
    source: str
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class Command:
    type: CommandType
    params: dict[str, Any] = field(default_factory=dict)


@dataclass
class Result:
    success: bool
    message: str


def utc_now() -> datetime:
    return datetime.now(UTC)
