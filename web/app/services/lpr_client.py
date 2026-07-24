from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, AsyncIterator

import httpx


DEFAULT_LPR_BASE_URL = "http://127.0.0.1:8000"


class LprServiceError(RuntimeError):
    """Fehler bei der Kommunikation mit dem LPR-Dienst."""


@dataclass(frozen=True)
class LprStream:
    body: AsyncIterator[bytes]
    media_type: str


class LprClient:
    """
    Client für den eigenständigen Jetson-LPR-Dienst.

    Die Basis-URL kann bei Bedarf über die Umgebungsvariable
    JETSON_LPR_BASE_URL geändert werden.
    """

    def __init__(self, base_url: str | None = None) -> None:
        configured_url = (
            base_url
            or os.getenv("JETSON_LPR_BASE_URL")
            or DEFAULT_LPR_BASE_URL
        )

        self.base_url = configured_url.rstrip("/")

    def build_url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    async def get_health(self) -> dict[str, Any]:
        return await self._get_json("/health")

    async def get_status(self) -> dict[str, Any]:
        return await self._get_json("/api/status")

    async def _get_json(self, path: str) -> dict[str, Any]:
        timeout = httpx.Timeout(
            connect=2.0,
            read=3.0,
            write=3.0,
            pool=2.0,
        )

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(self.build_url(path))
                response.raise_for_status()
                payload = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise LprServiceError(
                f"LPR-Dienst nicht erreichbar: {exc}"
            ) from exc

        if not isinstance(payload, dict):
            raise LprServiceError(
                "LPR-Dienst lieferte keine gültige JSON-Antwort"
            )

        return payload

    async def open_stream(self, path: str) -> LprStream:
        """
        Öffnet einen LPR-MJPEG-Stream.

        Client und Upstream-Antwort werden automatisch geschlossen,
        sobald der Browser die Verbindung beendet.
        """

        timeout = httpx.Timeout(
            connect=3.0,
            read=None,
            write=3.0,
            pool=3.0,
        )

        client = httpx.AsyncClient(timeout=timeout)

        try:
            request = client.build_request(
                "GET",
                self.build_url(path),
            )
            response = await client.send(
                request,
                stream=True,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            await client.aclose()

            raise LprServiceError(
                f"LPR-Stream nicht erreichbar: {exc}"
            ) from exc

        async def stream_body() -> AsyncIterator[bytes]:
            try:
                async for chunk in response.aiter_raw():
                    yield chunk
            finally:
                await response.aclose()
                await client.aclose()

        media_type = response.headers.get(
            "content-type",
            "multipart/x-mixed-replace; boundary=frame",
        )

        return LprStream(
            body=stream_body(),
            media_type=media_type,
        )
