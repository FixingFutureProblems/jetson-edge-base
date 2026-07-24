from __future__ import annotations

import html
import os
import socket
import subprocess
import threading
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse


APP_VERSION = "0.0.1-dev"
BOOT_ID_PATH = Path("/proc/sys/kernel/random/boot_id")
UPTIME_PATH = Path("/proc/uptime")

app = FastAPI(
    title="Jetson Edge Base",
    version=APP_VERSION,
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
        "generated_at": now.isoformat(timespec="milliseconds"),
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


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    status = build_status()
    request_number = next_request_number()
    request_id = uuid.uuid4().hex[:12]

    connection_rows = "".join(
        (
            "<tr>"
            f"<td>{html.escape(connection['name'])}</td>"
            f"<td>{html.escape(connection['type'])}</td>"
            f"<td>{html.escape(connection['device'])}</td>"
            "</tr>"
        )
        for connection in status["active_connections"]
    )

    if not connection_rows:
        connection_rows = (
            '<tr><td colspan="3">Keine aktive Verbindung erkannt</td></tr>'
        )

    ip_addresses = ", ".join(status["ip_addresses"]) or "Keine IP-Adresse erkannt"

    document = f"""<!doctype html>
<html lang="de">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="refresh" content="5">
    <title>Jetson Edge Base</title>
    <style>
        :root {{
            color-scheme: light dark;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
        }}

        body {{
            max-width: 900px;
            margin: 0 auto;
            padding: 24px;
            line-height: 1.5;
        }}

        h1 {{
            margin-bottom: 4px;
        }}

        .status {{
            font-size: 1.15rem;
            font-weight: 700;
        }}

        .ok {{
            color: #21a366;
        }}

        .card {{
            border: 1px solid #7777;
            border-radius: 12px;
            padding: 18px;
            margin-top: 18px;
        }}

        dl {{
            display: grid;
            grid-template-columns: minmax(160px, 220px) 1fr;
            gap: 8px 16px;
        }}

        dt {{
            font-weight: 700;
        }}

        dd {{
            margin: 0;
            overflow-wrap: anywhere;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
        }}

        th, td {{
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #7775;
        }}

        code {{
            overflow-wrap: anywhere;
        }}

        .live {{
            font-weight: 700;
        }}
    </style>
</head>
<body>
    <h1>Jetson Edge Base</h1>
    <div class="status ok">● Webserver läuft</div>

    <section class="card">
        <h2>Live-Diagnose</h2>
        <dl>
            <dt>Seite erzeugt</dt>
            <dd class="live">{html.escape(status["generated_at"])}</dd>

            <dt>Request-ID</dt>
            <dd><code>{request_id}</code></dd>

            <dt>Request-Zähler</dt>
            <dd>{request_number}</dd>

            <dt>Prozess-ID</dt>
            <dd>{status["process_id"]}</dd>
        </dl>
        <p>Diese Seite wird alle fünf Sekunden neu vom Jetson geladen.</p>
    </section>

    <section class="card">
        <h2>System</h2>
        <dl>
            <dt>Hostname</dt>
            <dd>{html.escape(status["hostname"])}</dd>

            <dt>Version</dt>
            <dd>{html.escape(status["version"])}</dd>

            <dt>Boot-ID</dt>
            <dd><code>{html.escape(status["boot_id"])}</code></dd>

            <dt>Laufzeit</dt>
            <dd>{html.escape(status["uptime"])}</dd>
        </dl>
    </section>

    <section class="card">
        <h2>Netzwerk</h2>
        <dl>
            <dt>Netzwerkmodus</dt>
            <dd>{html.escape(status["network_mode"])}</dd>

            <dt>IP-Adressen</dt>
            <dd>{html.escape(ip_addresses)}</dd>
        </dl>

        <table>
            <thead>
                <tr>
                    <th>Verbindung</th>
                    <th>Typ</th>
                    <th>Gerät</th>
                </tr>
            </thead>
            <tbody>
                {connection_rows}
            </tbody>
        </table>
    </section>

    <section class="card">
        <h2>API</h2>
        <p>
            Maschinenlesbarer Status:
            <a href="/api/status"><code>/api/status</code></a>
        </p>
    </section>
</body>
</html>
"""

    return HTMLResponse(document)


@app.get("/api/status")
def api_status() -> JSONResponse:
    status = build_status()
    status["request_id"] = uuid.uuid4().hex
    status["request_number"] = next_request_number()

    return JSONResponse(status)
