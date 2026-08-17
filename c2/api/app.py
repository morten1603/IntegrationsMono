from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from adapters.redis.adapter import RedisAdapter

redis_adapter = RedisAdapter(name="redis")

app = FastAPI(title="C2 API")
WEB_DIR = Path(__file__).resolve().parents[1] / "web"


def get_flight_state() -> str:
    frame = redis_adapter.get_latest()
    return (
        f"lat={frame.latitude:.5f} lon={frame.longitude:.5f} "
        f"alt={frame.altitude_m:.1f}m bat={frame.battery_pct}% "
        f"mode={frame.mode} armed={frame.armed}"
    )


@app.get("/api/hello")
def hello() -> dict[str, str]:
    return {"message": get_flight_state()}


@app.get("/")
def index() -> FileResponse:
    return FileResponse(WEB_DIR / "index.html")
