import json
from typing import Any, Union, List

from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.base import CXRenderable

JSON_TEMPLATE: str = """
{
    "renderTo": "@renderTo@",
    "data": @data@,
    "config": @config@,
    "afterRender": @afterRender@,
    "otherParams": @otherParams@,
    "events": @events@,
    "width": @width@,
    "height": @height@
}
""".strip()


class CXJSON(CXRenderable):
    """
    CXJSON is a `CXRenderable` that renders `CanvasXpress` objects into reproducible JSON descriptions.
    """

    def __init__(self, *cx: Union[List[CanvasXpress], CanvasXpress, None]):
        """
        Initializes a new `CXJSON` object.
        :praram cx: `Union[List[CanvasXpress], CanvasXpress, None], ...`
            The `CanvasXpress` object(s) to be tracked.  See the `canvas`
            property, except that on initialization cx can be `None`.
            Multiple CanvasXpress objects are supported provided that
            they have distinct `render_to` targets.
        """
        super().__init__(*cx)

    @classmethod
    def render_to_json(cls, cx: CanvasXpress):
        """
        Renders the given CanvasXpress object into a reproducible JSON form.
        :params cx: `CanasXpress`
            The `CanvasXpress` object to be converted.
        :returns: `str`
            A `str` bearing the reproducible JSON.
        """

        if cx is None:
            raise ValueError("cx cannot be None.")

        cx.update_data_profile(
            cx.data,
            True,
            True,
        )

        cx_element_params = {
            "renderTo": cx.render_to,
            "data": cx.data.render_to_dict(config=cx.config),
            "config": cx.config.render_to_dict(),
            "afterRender": cx.after_render.render_to_list(),
            "otherParams": cx.other_init_params.render_to_dict(),
            "events": "js_events",
            "width": cx.width,
            "height": cx.height,
        }

        # Support unique data without JSON data structure
        if cx_element_params["data"].get("raw"):
            cx_element_params["data"] = cx_element_params["data"]["raw"]

        cx_element_params["events"] = cx.events.render_to_js()

        reproducible_json = JSON_TEMPLATE
        for key in cx_element_params.keys():
            if isinstance(cx_element_params[key], str):
                value = cx_element_params[key]
            else:
                value = json.dumps(cx_element_params[key])
            reproducible_json = reproducible_json.replace(f"@{key}@", value)

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
            reproducible_jsons: list = []
            for cx in self.canvas:
                reproducible_jsons.append(CXJSON.render_to_json(cx))
            return reproducible_jsons
        else:
            return [CXJSON.render_to_json(self.canvas)]
