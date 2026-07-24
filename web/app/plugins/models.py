from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Plugin:
    plugin_id: str
    name: str
    short_name: str
    description: str
    route: str
    status: str = "available"
    enabled: bool = True
