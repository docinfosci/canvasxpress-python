"""
This module provides the web assets that put CanvasXpress charts into a page: the
CanvasXpress library, stylesheet and license (`CXLibraryAssets`), and the canvas
element and initialization JavaScript of each chart (`CXChartAssets`).
"""

import copy
import json
import re
import uuid
from html import escape
from pathlib import Path
from typing import List, Optional, Sequence, Union

from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.context.files import ANONYMOUS_NAME

LOADER_JS: str = (
    Path(__file__).parent.parent / "resources" / "canvasxpress-loader.js"
).read_text(encoding="utf-8")
"""The JavaScript that defines `window.canvasxpress.loadLibrary()`, which loads the
CanvasXpress library, stylesheet and license on demand, once per page."""

FILL_JS: str = (
    Path(__file__).parent.parent / "resources" / "canvasxpress-fill.js"
).read_text(encoding="utf-8")
"""The JavaScript that defines `window.canvasxpress.fillContainer()`, which keeps a
chart sized to its container for the `fill_to_width` and `fill_to_height` options."""

_SCRIPT_END = re.compile(r"</(script)", re.IGNORECASE)

_REFERRER_POLICY: str = "origin-when-cross-origin"


def escape_script(code: str) -> str:
    """
    Escapes JavaScript for use inside a `<script>` element.

    A `</script` sequence, such as in chart data, would otherwise end the element
    early. It is written as `<\\/script`, which JavaScript reads the same way.

    Args:
        code: The JavaScript code.

    Returns:
        The code, safe for use inside a `<script>` element.
    """
    return _SCRIPT_END.sub(r"<\\/\1", code)


def fill_options(
    width: int, height: int, fill_to_width: bool, fill_to_height: bool
) -> dict:
    """
    Provides the options argument of `window.canvasxpress.fillContainer()`.

    Args:
        width: The chart's configured width in pixels.
        height: The chart's configured height in pixels.
        fill_to_width: Whether the chart follows its container's width.
        fill_to_height: Whether the chart follows its container's height.

    Returns:
        The options, as a dict for JSON.
    """
    return {
        "fillToWidth": bool(fill_to_width),
        "fillToHeight": bool(fill_to_height),
        "width": int(width),
        "height": int(height),
    }


def fill_container_js(
    target_id: str,
    width: int,
    height: int,
    fill_to_width: bool,
    fill_to_height: bool,
) -> str:
    """
    Provides JavaScript that keeps a chart sized to its layout cell, as rendered
    by `CXHtmlDocument` with `fill_to_width` or `fill_to_height`. `FILL_JS` must
    run first.

    Args:
        target_id: The chart's element ID.
        width: The chart's configured width in pixels, kept unless filled.
        height: The chart's configured height in pixels, kept unless filled.
        fill_to_width: Whether the chart follows its cell's width.
        fill_to_height: Whether the chart follows its cell's height.

    Returns:
        The JavaScript.
    """
    selector = json.dumps(f'[data-canvasxpress-cell="{target_id}"]')
    options = json.dumps(fill_options(width, height, fill_to_width, fill_to_height))
    return (
        f"window.canvasxpress.fillContainer("
        f"document.querySelector({selector}), {json.dumps(target_id)}, {options});"
    )


def script_element(code: str) -> str:
    """
    Wraps JavaScript in a `<script>` element.

    Args:
        code: The JavaScript code.

    Returns:
        The HTML `<script>` element.
    """
    return f'<script type="text/javascript">\n{escape_script(code)}\n</script>'


class CXLibraryAssets:
    """
    The CanvasXpress library, stylesheet and license that a page needs before it
    can draw charts.
    """

    def __init__(
        self,
        js_url: str,
        css_url: str,
        license_url: Optional[str] = None,
    ):
        """
        Initializes a new CXLibraryAssets object.

        Args:
            js_url: The URL of the CanvasXpress JavaScript library.
            css_url: The URL of the CanvasXpress stylesheet.
            license_url: The URL of a CanvasXpress license script, if any.
        """
        self.js_url: str = js_url
        self.css_url: str = css_url
        self.license_url: Optional[str] = license_url

    @classmethod
    def current(cls, license_url: Optional[str] = None) -> "CXLibraryAssets":
        """
        Provides the library assets configured for the CanvasXpress class, such as
        via `CanvasXpress.set_cdn_edition()`.

        Args:
            license_url: The URL of a CanvasXpress license script, if any.

        Returns:
            The library assets for the active CanvasXpress configuration.
        """
        return cls(
            js_url=CanvasXpress.js_library_url(),
            css_url=CanvasXpress.css_library_url(),
            license_url=license_url,
        )

    def stylesheet_tag(self) -> str:
        """
        Returns:
            The `<link>` element that loads the stylesheet.
        """
        return (
            f'<link href="{escape(self.css_url)}" rel="stylesheet" type="text/css"'
            f' referrerpolicy="{_REFERRER_POLICY}">'
        )

    def license_tag(self) -> str:
        """
        Returns:
            The `<script>` element that loads the license, or "" without a license.
        """
        if not self.license_url:
            return ""

        return (
            f'<script src="{escape(self.license_url)}" type="text/javascript"'
            f' referrerpolicy="{_REFERRER_POLICY}"></script>'
        )

    def library_tag(self) -> str:
        """
        Returns:
            The `<script>` element that loads the CanvasXpress library.
        """
        return (
            f'<script src="{escape(self.js_url)}" type="text/javascript"'
            f' referrerpolicy="{_REFERRER_POLICY}"></script>'
        )

    def tags(self) -> str:
        """
        Provides the elements that load the stylesheet, the license and then the
        library, in that order, for pages that are parsed as a whole.

        Returns:
            The HTML elements, one per line.
        """
        return "\n".join(
            tag
            for tag in [self.stylesheet_tag(), self.license_tag(), self.library_tag()]
            if tag
        )

    def to_loader_dict(self) -> dict:
        """
        Returns:
            The argument for `window.canvasxpress.loadLibrary()`.
        """
        return {
            "jsUrl": self.js_url,
            "cssUrl": self.css_url,
            "licenseUrl": self.license_url,
        }

    def loader_js(self, code: str) -> str:
        """
        Provides JavaScript that loads the library on demand and then runs code.

        Use it where the page may not provide CanvasXpress and the code cannot be
        placed after `<script>` elements that load it, such as in Jupyter outputs.

        Args:
            code: The JavaScript to run once CanvasXpress is available.

        Returns:
            The JavaScript, including the loader.
        """
        return (
            f"{LOADER_JS}\n"
            f"window.canvasxpress.loadLibrary({json.dumps(self.to_loader_dict())})\n"
            f"  .then(function () {{\n{code}\n  }})\n"
            f"  .catch(function (error) {{\n"
            f'    console.error("CanvasXpress could not be loaded:", error);\n'
            f"  }});"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CXLibraryAssets):
            return NotImplemented

        return (self.js_url, self.css_url, self.license_url) == (
            other.js_url,
            other.css_url,
            other.license_url,
        )

    def __repr__(self) -> str:
        return (
            f"CXLibraryAssets(js_url={self.js_url!r}, css_url={self.css_url!r}, "
            f"license_url={self.license_url!r})"
        )


class CXChartAssets:
    """
    The canvas element and initialization JavaScript that draw one chart.
    """

    def __init__(
        self,
        target_id: str,
        canvas: str,
        js: str,
        width: int,
        height: int,
        license_url: Optional[str] = None,
        name: Optional[str] = None,
    ):
        """
        Initializes a new CXChartAssets object. See `from_canvas()`.

        Args:
            target_id: The chart's element ID, used as its CanvasXpress renderTo.
            canvas: The chart's `<canvas>` element.
            js: The JavaScript that creates the chart.
            width: The chart width in pixels.
            height: The chart height in pixels.
            license_url: The URL of the chart's license script, if any.
            name: The name of the chart for file names. Defaults to target_id.
        """
        self.target_id: str = target_id
        self.name: str = name or target_id
        self.canvas: str = canvas
        self.js: str = js
        self.width: int = width
        self.height: int = height
        self.license_url: Optional[str] = license_url

    @classmethod
    def from_canvas(
        cls, cx: CanvasXpress, target_id: Optional[str] = None
    ) -> "CXChartAssets":
        """
        Renders a CanvasXpress object into chart assets without changing it.

        Args:
            cx: The CanvasXpress object to render.
            target_id: The element ID to render the chart under. Defaults to the
                chart's `render_to`, which for an anonymous chart is a new ID.

        Returns:
            The chart's assets.

        Raises:
            TypeError: If cx is not a CanvasXpress object.
        """
        if not isinstance(cx, CanvasXpress):
            raise TypeError("cx must be of type CanvasXpress")

        # Fix the ID on a copy: an anonymous chart provides a new ID on each access,
        # and the caller's chart keeps its own ID.
        rendered = copy.copy(cx)
        rendered.render_to = cx.render_to if target_id is None else target_id
        html_parts = rendered.render_to_html_parts()

        return cls(
            target_id=rendered.render_to,
            canvas=html_parts["cx_canvas"],
            js=html_parts["cx_js"],
            width=rendered.width,
            height=rendered.height,
            license_url=cx.license_url if cx.license_available else None,
            name=ANONYMOUS_NAME if cx.anonymous else cx.render_to,
        )

    @classmethod
    def from_canvases(
        cls, charts: Union[CanvasXpress, Sequence[CanvasXpress], None]
    ) -> List["CXChartAssets"]:
        """
        Renders CanvasXpress objects for use on the same page. Charts that share a
        `render_to` ID are given unique IDs so that each one displays; the caller's
        charts are not changed.

        Args:
            charts: A CanvasXpress object, a sequence of them, or None.

        Returns:
            The chart assets, in the order of charts.

        Raises:
            TypeError: If any chart is not a CanvasXpress object.
        """
        if charts is None:
            return []

        if isinstance(charts, CanvasXpress):
            charts = [charts]

        assets: List[CXChartAssets] = []
        used_ids = set()
        for cx in charts:
            if not isinstance(cx, CanvasXpress):
                raise TypeError("All charts must be of type CanvasXpress")

            # IDs are compared as rendered, since render_to removes some characters.
            chart = cls.from_canvas(cx)
            if chart.target_id in used_ids:
                chart = cls.from_canvas(cx, f"{chart.target_id}_{uuid.uuid4().hex}")
            used_ids.add(chart.target_id)

            assets.append(chart)

        return assets

    def __repr__(self) -> str:
        return (
            f"CXChartAssets(target_id={self.target_id!r}, name={self.name!r}, "
            f"width={self.width!r}, "
            f"height={self.height!r}, license_url={self.license_url!r})"
        )
