from __future__ import annotations

import os
import socket
import subprocess
import threading
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from web.app.plugins.registry import get_enabled_plugins
from web.app.routes.lpr import create_router as create_lpr_router


APP_VERSION = "0.1.0-dev"

APP_DIRECTORY = Path(__file__).resolve().parent
BOOT_ID_PATH = Path("/proc/sys/kernel/random/boot_id")
UPTIME_PATH = Path("/proc/uptime")

app = FastAPI(
    title="Jetson Edge Base",
    version=APP_VERSION,
)

app.mount(
    "/static",
    StaticFiles(directory=APP_DIRECTORY / "static"),
    name="static",
)

templates = Jinja2Templates(
    directory=APP_DIRECTORY / "templates",
)

_request_counter = 0
_request_counter_lock = threading.Lock()


def next_request_number() -> int:
    global _request_counter

    with _request_counter_lock:
        _request_counter += 1
        return _request_counter


def read_text(path: Path, fallback: str = "unbekannt") -> str:
    try:
        return path.read_text(encoding="utf-8").strip()
    except OSError:
        return fallback


def get_uptime_seconds() -> int:
    try:
        raw_value = UPTIME_PATH.read_text(encoding="utf-8").split()[0]
        return int(float(raw_value))
    except (OSError, ValueError, IndexError):
        return 0


def format_duration(total_seconds: int) -> str:
    days, remainder = divmod(total_seconds, 86_400)
    hours, remainder = divmod(remainder, 3_600)
    minutes, seconds = divmod(remainder, 60)

    if days:
        return f"{days} Tage, {hours:02d}:{minutes:02d}:{seconds:02d}"

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def run_command(command: list[str]) -> str:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=3,
            check=False,
        )
        return result.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        return ""


def get_active_connections() -> list[dict[str, str]]:
    output = run_command(
        [
            "nmcli",
            "-t",
            "-f",
            "NAME,TYPE,DEVICE",
            "connection",
            "show",
            "--active",
        ]
    )

    connections: list[dict[str, str]] = []

    for line in output.splitlines():
        if not line:
            continue

        parts = line.split(":", 2)

        if len(parts) != 3:
            continue

        name, connection_type, device = parts

        connections.append(
            {
                "name": name,
                "type": connection_type,
                "device": device,
            }
        )

    return connections


def determine_network_mode(
    connections: list[dict[str, str]],
) -> str:
    for connection in connections:
        if connection["type"] in {"802-3-ethernet", "ethernet"}:
            return "LAN"

    for connection in connections:
        if connection["type"] in {"802-11-wireless", "wifi"}:
            if connection["name"].endswith("-wlan"):
                return "Access Point"

            return "WLAN-Client"

    return "Offline oder unbekannt"


def get_ip_addresses() -> list[str]:
    output = run_command(["hostname", "-I"])

    return [
        address
        for address in output.split()
        if address
    ]


def build_status() -> dict[str, Any]:
    now = datetime.now().astimezone()
    uptime_seconds = get_uptime_seconds()
    active_connections = get_active_connections()

    return {
        "status": "ok",
        "service": "jetson-edge-web",
        "version": APP_VERSION,
        "hostname": socket.gethostname(),
        "generated_at": now.isoformat(timespec="seconds"),
        "boot_id": read_text(BOOT_ID_PATH),
        "uptime_seconds": uptime_seconds,
        "uptime": format_duration(uptime_seconds),
        "network_mode": determine_network_mode(active_connections),
        "ip_addresses": get_ip_addresses(),
        "active_connections": active_connections,
        "process_id": os.getpid(),
    }


@app.middleware("http")
async def disable_browser_cache(request: Request, call_next):
    response = await call_next(request)

    response.headers["Cache-Control"] = (
        "no-store, no-cache, must-revalidate, max-age=0"
    )
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response


app.include_router(
    create_lpr_router(
        templates=templates,
        status_builder=build_status,
    )
)


@app.get("/")
def index(request: Request):
    status = build_status()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "active_page": "dashboard",
            "page_eyebrow": "Systemübersicht",
            "page_title": "Dashboard",
            "status": status,
            "request_id": uuid.uuid4().hex[:12],
            "request_number": next_request_number(),
            "plugins": get_enabled_plugins(),
        },
    )


@app.get("/api/status", response_class=JSONResponse)
def api_status() -> JSONResponse:
    return JSONResponse(build_status())


@app.get("/health", response_class=JSONResponse)
def health() -> JSONResponse:
    return JSONResponse(
        {
            "status": "ok",
            "service": "jetson-edge-web",
            "version": APP_VERSION,
        }
    )
