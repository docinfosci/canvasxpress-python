"""
This module provides an integration solution for the CanvasXpress class and the base dash component for a feature-
rich integration with Plotly's Dash framework.
"""

import json
from typing import List, Union, Any

from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.base import CXRenderFactory
from cxdash import CXDashElement


class CXElementFactory(CXRenderFactory):
    """
    CXDashElementFactory converts CanvasXpress objects into PlotlyDash elements that will
    render CanvasXpress charts into the Dash UI.
    """

    def __init__(self, *cx: Union[List[CanvasXpress], CanvasXpress, None]):
        """
        Initializes a new CXElementFactory object.

        Args:
            cx: The CanvasXpress object(s) to be tracked. See the `canvas`
                property, except that on initialization cx can be None.
                Multiple CanvasXpress objects are supported provided that
                they have distinct `render_to` targets.

        Raises:
            TypeError: If any cx member is not a CanvasXpress instance.
        """
        super().__init__(*cx)

    @classmethod
    def render(cls, cx: CanvasXpress) -> CXDashElement:
        """
        Converts the provided CanvasXpress object into a CXDashElement object that is
        primed by the configuration represented by the CanvasXpress object.

        Args:
            cx: The CanvasXpress object to render.

        Returns:
            A CXDashElement with the configuration as represented by cx.

        Raises:
            ValueError: If cx is None.
        """
        element_parts = cx.prepare_html_element_parts()
        dash_element = CXDashElement(
            id=element_parts["renderTo"],
            data=(
                element_parts["data"]
                if isinstance(element_parts["data"], str)
                else json.dumps(element_parts["data"])
            ),
            config=json.dumps(
                {**element_parts["config"], **element_parts["otherParams"]}
            ),
            events=element_parts["events"],
            after_render=json.dumps(element_parts["afterRender"]),
            js_url=cx.js_library_url(),
            css_url=cx.css_library_url(),
            width=str(element_parts["width"]),
            height=str(element_parts["height"]),
        )

        return dash_element

    def render_all(self, **kwargs: Any) -> List[CXDashElement]:
        """
        Provides a list of objects that can be used by the target domain or container
        to create CanvasXpress illustrations or instantiations.

        Args:
            kwargs: Parameters specific to implementations are supported.
                The essential create_element call should work with no extra parameters,
                and with parameters that do not apply to the implementation.

        Returns:
            A list of CXDashElement objects, one for each tracked CanvasXpress object.
        """
        if isinstance(self.canvas, CanvasXpress):
            return [CXElementFactory.render(self.canvas)]

        else:
            return [CXElementFactory.render(cx) for cx in self.canvas]
