"""
This module provides an integration solution for the CanvasXpress class and the base streamlit component for a feature-
rich integration with Streamlit's framework.
"""
import json
from typing import Union

from canvasxpress.canvas import CanvasXpress
from cxstreamlit import CXStreamlit


def plot(cx: CanvasXpress) -> Union[object, None]:
    """
    Converts the provided CanvasXpress object into a CXStreamlit object that is
    primed by the configuration represented by the CanvasXpress object.
    :param cx: `CanvasXpress` The CanvasXpress object to render.  An exception is
        raised if cx is `None`.
    :returns: `CXStreamlit` A CXStreamlit with the configuration as represented
        by cx.  'None' if cx is invalid.
    """

    if cx is None:
        return None

    if not isinstance(cx, CanvasXpress):
        return None

    else:
        element_parts = cx.prepare_html_element_parts()
        streamlit_element: object = CXStreamlit(
            id=element_parts["renderTo"],
            data=element_parts["data"]
            if isinstance(element_parts["data"], str)
            else json.dumps(element_parts["data"]),
            config=json.dumps(
                {**element_parts["config"], **element_parts["otherParams"]}
            ),
            events=element_parts["events"],
            after_render=json.dumps(element_parts["afterRender"]),
            cdn_edition=cx.cdn_edition(),
            width=str(element_parts["width"]),
            height=str(element_parts["height"]),
        )

        return streamlit_element
