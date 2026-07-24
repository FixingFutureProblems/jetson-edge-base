from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from web.app.plugins.registry import get_plugin


router = APIRouter(
    prefix="/applications/lpr",
    tags=["lpr"],
)


def create_router(
    templates: Jinja2Templates,
    status_builder,
) -> APIRouter:
    @router.get("/")
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

    return router
