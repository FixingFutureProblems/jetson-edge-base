from __future__ import annotations

from web.app.plugins.lpr.plugin import plugin as lpr_plugin
from web.app.plugins.models import Plugin


PLUGINS: tuple[Plugin, ...] = (
    lpr_plugin,
)


def get_plugins() -> tuple[Plugin, ...]:
    return PLUGINS


def get_enabled_plugins() -> tuple[Plugin, ...]:
    return tuple(
        plugin
        for plugin in PLUGINS
        if plugin.enabled
    )


def get_plugin(plugin_id: str) -> Plugin | None:
    return next(
        (
            plugin
            for plugin in PLUGINS
            if plugin.plugin_id == plugin_id
        ),
        None,
    )
