"""
This module provides an integration solution for the CanvasXpress class and the base dash component for a feature-
rich integration with Plotly's Dash framework.
"""
from typing import List, Union, Any

from canvasxpress.canvas import CanvasXpress
from cxdash import CXDashElement
from canvasxpress.render.base import CXRenderFactory


class CXDashElementFactory(CXRenderFactory):
    """
    CXDashElementFactory converts CanvasXpress objects into PlotlyDash elements that will
    render CanvasXpress charts into the Dash UI.
    """

    def __init__(self, *cx: Union[List[CanvasXpress], CanvasXpress, None]):
        """
        Initializes a new `CXDashRenderFactory` object.
        :param cx: `Union[List[CanvasXpress], CanvasXpress, None], ...`
            The `CanvasXpress` object(s) to be tracked.  See the `canvas`
            property, except that on initialization cx can be `None`.
            Multiple CanvasXpress objects are supported provided that
            they have distinct `render_to` targets.
        """
        super().__init__(*cx)

    @classmethod
    def convert(cls, cx: CanvasXpress) -> CXDashElement:
        """
        Converts the provided CanvasXpress object into a CXDashElement object that is
        primed by the configuration represented by the CanvasXpress object.
        :param cx: `CanvasXpress` The CanvasXpress object to convert.  An exception is
            raised if cx is `None`.
        :returns: `CXDashElement` A CXDashElement with the configuration as represented
            by cx.
        """
        element_parts = cx.prepare_html_element_parts()
        dash_element = CXDashElement(
            id=element_parts["renderTo"],
            data=element_parts["data"],
            config=element_parts["config"],
            events=element_parts["events"],
            width=element_parts["width"],
            height=element_parts["height"],
        )

        return dash_element

    def renderables(self, **kwargs: Any) -> List[CXDashElement]:
        """
        Provides a list of objects that can be used by the target domain or container
        to create CanvasXpress illustrations or instantiations.
        Not implemented.
        :param kwargs: `Any`
            Parameters specific to implementations are supported.  The essential
            render call should work with no extra parameters, and with
            parameters that do not apply to the implementation.
        """
        return [CXDashElementFactory.convert(cx) for cx in self.canvas]
