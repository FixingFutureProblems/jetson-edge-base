from __future__ import annotations

from collections.abc import Callable
from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from web.app.plugins.registry import get_plugin
from web.app.services.lpr_client import (
    LprClient,
    LprServiceError,
)


lpr_client = LprClient()


def create_router(
    templates: Jinja2Templates,
    status_builder: Callable[[], dict[str, Any]],
) -> APIRouter:
    router = APIRouter(
        prefix="/applications/lpr",
        tags=["lpr"],
    )

    @router.get("/", name="lpr_overview")
    def lpr_overview(request: Request):
        plugin = get_plugin("lpr")

        return templates.TemplateResponse(
            request=request,
            name="lpr/index.html",
            context={
                "active_page": "lpr",
                "page_eyebrow": "Anwendung",
                "page_title": "License Plate Recognition",
                "status": status_builder(),
                "plugin": plugin,
            },
        )

    @router.get(
        "/api/status",
        response_class=JSONResponse,
        name="lpr_status",
    )
    async def lpr_status() -> JSONResponse:
        try:
            status = await lpr_client.get_status()

            return JSONResponse(
                {
                    "service_available": True,
                    **status,
                }
            )
        except LprServiceError as exc:
            return JSONResponse(
                status_code=503,
                content={
                    "service_available": False,
                    "running": False,
                    "camera_connected": False,
                    "raw_frame_id": 0,
                    "yolo_frame_id": 0,
                    "camera_fps": 0.0,
                    "yolo_fps": 0.0,
                    "detections": 0,
                    "last_error": str(exc),
                },
            )

    @router.get(
        "/health",
        response_class=JSONResponse,
        name="lpr_health",
    )
    async def lpr_health() -> JSONResponse:
        try:
            health = await lpr_client.get_health()

            return JSONResponse(
                {
                    "service_available": True,
                    **health,
                }
            )
        except LprServiceError as exc:
            return JSONResponse(
                status_code=503,
                content={
                    "service_available": False,
                    "status": "unavailable",
                    "camera": False,
                    "pipeline": False,
                    "error": str(exc),
                },
            )

    @router.get(
        "/stream/raw",
        name="lpr_raw_stream",
    )
    async def lpr_raw_stream():
        return await _create_stream_response("/stream/raw")

    @router.get(
        "/stream/yolo",
        name="lpr_yolo_stream",
    )
    async def lpr_yolo_stream():
        return await _create_stream_response("/stream/yolo")

    return router


async def _create_stream_response(
    upstream_path: str,
) -> StreamingResponse | JSONResponse:
    try:
        stream = await lpr_client.open_stream(upstream_path)
    except LprServiceError as exc:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unavailable",
                "error": str(exc),
            },
        )

    return StreamingResponse(
        stream.body,
        media_type=stream.media_type,
        headers={
            "Cache-Control": "no-store, no-cache, must-revalidate",
            "Pragma": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
