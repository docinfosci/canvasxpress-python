import base64
import json
import os
from datetime import datetime
from typing import Any

from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.base import CXRenderable
from canvasxpress.render.environment import (
    is_ipython_available,
    is_shiny_available,
)
from canvasxpress.context.platform import (
    DEFAULT_KEY_SYMBOLS,
    MACOS_KEY_SYMBOLS,
    detect_browser,
    detect_os,
)
from canvasxpress.util.template import render_from_template

with open(
    os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "util", "json_template.json"
    )
) as template_file:
    JSON_TEMPLATE = template_file.read()


class CXJSON(CXRenderable):
    """
    CXJSON is a `CXRenderable` that renders `CanvasXpress` objects into reproducible JSON descriptions.
    """

    @staticmethod
    def render_to_json(cx: CanvasXpress) -> str:
        """
        Renders the given CanvasXpress object into a reproducible JSON form.
        :param cx: `CanvasXpress`
            The `CanvasXpress` object to be converted.
        :returns: `str`
            A `str` bearing the reproducible JSON.
        """

        if cx is None:
            raise ValueError("cx cannot be None.")

        current_version = CanvasXpress.cdn_edition()
        os_name = detect_os()
        browser_name, browser_version = detect_browser()
        is_jupyter = is_ipython_available()
        is_shiny = is_shiny_available()
        key_symbols = MACOS_KEY_SYMBOLS if os_name == "Mac OS" else DEFAULT_KEY_SYMBOLS

        data = cx.data.render_to_dict(config=cx.config)
        if "raw" in data:
            data = data["raw"]

        values = {
            "version": current_version,
            "renderTo": cx.render_to,
            "data": data,
            "config": cx.config.render_to_dict(),
            "events": {event.id: {} for event in cx.events.events},
            "afterRender": [
                [config.label, config.value, *config.extra]
                for config in cx.after_render.configs
            ],
            "buildDate": datetime.now().strftime("%m-%d-%Y"),
            "client": base64.b64encode(f"0::1::{current_version}::".encode()).decode(),
            "href": f"file://{os.path.abspath('.')}",
            "services": "https://www.canvasxpress.org/cgi-bin/services.py",
            "browser": browser_name,
            "browserVersion": browser_version,
            "os": os_name,
            "alt": key_symbols["alt"],
            "command": key_symbols["command"],
            "control": key_symbols["control"],
            "shift": key_symbols["shift"],
            "isShiny": is_shiny,
            "isJupyter": is_jupyter,
        }

        reproducible_json = render_from_template(
            JSON_TEMPLATE,
            {key: json.dumps(value) for key, value in values.items()},
        )

        return reproducible_json

    def render(self, **kwargs: Any) -> list:
        """
        Renders the associated CanvasXpress object appropriate to create reproducible JSON.
        :param kwargs: `Any`
            * Unused.
        :returns: `list[str]`
            A list of `str`, one each of a reproducible JSON representation per tracked CanvasXpress object.
        """
        if self.canvas is None:
            return []
        elif isinstance(self.canvas, list):
            return [CXJSON.render_to_json(cx) for cx in self.canvas if cx is not None]
        else:
            return [CXJSON.render_to_json(self.canvas)]
