from typing import Protocol

from adapters.common.models import Command, Result, TelemetryFrame


class HealthCheck(Protocol):
    def ping(self) -> bool: ...


class TelemetrySource(Protocol):
    def get_latest(self) -> TelemetryFrame: ...


class TelemetryPublisher(Protocol):
    def publish_telemetry(self, frame: TelemetryFrame) -> Result: ...


class CommandSink(Protocol):
    def send_command(self, cmd: Command) -> Result: ...


class Adapter(HealthCheck, TelemetrySource, TelemetryPublisher, CommandSink, Protocol):
    @property
    def name(self) -> str: ...
