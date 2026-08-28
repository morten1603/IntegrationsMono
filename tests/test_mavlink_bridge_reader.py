import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from mavlinkBridge.reader import frame_to_payload, position_to_frame, publish_position


def _fake_position(
    *,
    latitude_deg: float = 59.9,
    longitude_deg: float = 10.7,
    absolute_altitude_m: float = 120.0,
    relative_altitude_m: float = 10.0,
) -> MagicMock:
    return MagicMock(
        latitude_deg=latitude_deg,
        longitude_deg=longitude_deg,
        absolute_altitude_m=absolute_altitude_m,
        relative_altitude_m=relative_altitude_m,
    )


def test_position_to_frame_maps_fields() -> None:
    position = _fake_position()

    frame = position_to_frame(position)

    assert frame.latitude == 59.9
    assert frame.longitude == 10.7
    assert frame.altitude_m == 120.0
    assert frame.battery_pct == 0.0
    assert frame.mode == "UNKNOWN"
    assert frame.armed is False
    assert frame.source == "mavlink"
    assert frame.extra["relative_altitude_m"] == 10.0


def test_frame_to_payload_is_json_bytes() -> None:
    frame = position_to_frame(_fake_position())

    raw = frame_to_payload(frame)
    payload = json.loads(raw.decode())

    assert payload["latitude"] == 59.9
    assert payload["longitude"] == 10.7
    assert payload["source"] == "mavlink"
    assert "timestamp" in payload


@pytest.mark.asyncio
async def test_publish_position_publishes_on_telemetry_subject() -> None:
    position = _fake_position(latitude_deg=1.0, longitude_deg=2.0, absolute_altitude_m=3.0)
    nc = AsyncMock()

    await publish_position(position, nc)

    nc.publish.assert_awaited_once()
    subject, data = nc.publish.await_args.args
    assert subject == "telemetry"
    payload = json.loads(data.decode())
    assert payload["latitude"] == 1.0
    assert payload["longitude"] == 2.0
    assert payload["altitude_m"] == 3.0
