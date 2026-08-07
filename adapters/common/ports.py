from typing import Protocol

from adapters.common.models import Command, Result, TelemetryFrame


class HealthCheck(Protocol):
    def ping(self) -> bool: ...


class TelemetrySource(Protocol):
    def get_latest(self) -> TelemetryFrame: ...


class CommandSink(Protocol):
    def send_command(self, cmd: Command) -> Result: ...


class Adapter(HealthCheck, TelemetrySource, CommandSink, Protocol):
    @property
    def name(self) -> str: ...
