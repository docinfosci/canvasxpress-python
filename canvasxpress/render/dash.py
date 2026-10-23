"""
This module provides an integration solution for the CanvasXpress class and the base dash component for a feature-
rich integration with Plotly's Dash framework.

`CXDashElement` is a Dash component backed by the CanvasXpress React wrapper shipped in
`canvasxpress/render/resources`, so no separate JavaScript build or package is required.
"""

import json
import sys
from typing import Any, List, Optional, Union

from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.base import CXRenderFactory

_DASH_NAMESPACE: str = "canvasxpress"
"""The Dash namespace: the package that serves the component's JavaScript, and the
`window` object under which the component is registered in the browser."""

_DASH_JS_DIST: List[dict] = [
    # The React wrapper must load before the Dash component that uses it.
    {
        "relative_package_path": "render/resources/canvasxpress-react.js",
        "namespace": _DASH_NAMESPACE,
    },
    {
        "relative_package_path": "render/resources/canvasxpress-dash.js",
        "namespace": _DASH_NAMESPACE,
    },
]
"""The JavaScript Dash serves for `CXDashElement`, relative to the canvasxpress package."""

try:
    from dash.development.base_component import Component, _explicitize_args

except ImportError:
    Component = None


if Component is not None:
    # Dash collects component JavaScript from the top-level package module of
    # each registered component, which for CXDashElement is canvasxpress.
    setattr(sys.modules[_DASH_NAMESPACE], "_js_dist", _DASH_JS_DIST)
    setattr(sys.modules[_DASH_NAMESPACE], "_css_dist", [])

    class CXDashElement(Component):
        """A CXDashElement component.
        CXDashElement implements a Plotly Dash integration of CanvasXpress React.
        Properties are defined for use by the CanvasXpress class to update
        CanvasXpress aspects such as data, config, and sizing.

        Keyword arguments:

        - id (string; required):
            The ID of the element for use in function calls and element
            identification.

        - after_render (string; optional):
            JSON list of [function name, [arguments]] calls applied after
            the chart is created.

        - config (string; optional):
            The configuration JSON dictating formatting and content
            management.

        - css_url (string; optional):
            The CSS CDN URL that should be used for CanvasXpress
            functionality.

        - data (string; optional):
            The data JSON, generally in the XYZ format.

        - events (string; optional):
            The events functions for increased reactivity.

        - height (string; optional):
            The element height.

        - js_url (string; optional):
            The Javascript URL that should be used for CanvasXpress
            functionality.

        - license_url (string; optional):
            The URL of a CanvasXpress license script.

        - width (string; optional):
            The element width."""

        _children_props: List[str] = []
        _base_nodes = ["children"]
        _namespace = _DASH_NAMESPACE
        _type = "CXDashElement"

        def __init__(
            self,
            id: Optional[Union[str, dict]] = None,
            data: Optional[str] = None,
            config: Optional[str] = None,
            events: Optional[str] = None,
            after_render: Optional[str] = None,
            js_url: Optional[str] = None,
            css_url: Optional[str] = None,
            width: Optional[str] = None,
            height: Optional[str] = None,
            license_url: Optional[str] = None,
            **kwargs,
        ):
            self._prop_names = [
                "id",
                "after_render",
                "config",
                "css_url",
                "data",
                "events",
                "height",
                "js_url",
                "license_url",
                "width",
            ]
            self._valid_wildcard_attributes = []
            self.available_properties = list(self._prop_names)
            self.available_wildcard_properties = []
            _explicit_args = kwargs.pop("_explicit_args")
            _locals = locals()
            _locals.update(kwargs)  # For wildcard attrs and excess named props
            args = {k: _locals[k] for k in _explicit_args}

            for k in ["id"]:
                if k not in args:
                    raise TypeError("Required argument `" + k + "` was not specified.")

            super().__init__(**args)

    setattr(CXDashElement, "__init__", _explicitize_args(CXDashElement.__init__))

else:

    class CXDashElement:
        """Placeholder used when Dash is not installed."""

        def __init__(self, *args: Any, **kwargs: Any):
            raise ImportError(
                "Dash is required for CXDashElement: pip install canvasxpress[dash]"
            )


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
            license_url=cx.license_url if cx.license_available else None,
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
