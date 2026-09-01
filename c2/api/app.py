import json
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import nats
from fastapi import FastAPI
from fastapi.responses import FileResponse
from nats.aio.client import Client
from nats.aio.msg import Msg

WEB_DIR = Path(__file__).resolve().parents[1] / "web"

nats_url = os.getenv("NATS_SERVER_URL", "nats://127.0.0.1:4222")
nc: Client | None = None
last_payload: dict[str, Any] | None = None


async def on_telemetry(msg: Msg) -> None:
    """Store NATS telemetry frames so the API can serve the latest state."""
    global last_payload
    last_payload = json.loads(msg.data.decode())


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Initialize dependencies on startup and release them on shutdown."""
    global nc
    nc = await nats.connect(nats_url)
    await nc.subscribe("telemetry", cb=on_telemetry)
    yield
    if nc is not None:
        await nc.close()
        nc = None


app = FastAPI(title="C2 API", lifespan=lifespan)



@app.get("/api/hello")
def hello() -> dict[str, str]:
    string: str = json.dumps(last_payload)
    return {"message": string}


@app.get("/")
def index() -> FileResponse:
    return FileResponse(WEB_DIR / "index.html")
