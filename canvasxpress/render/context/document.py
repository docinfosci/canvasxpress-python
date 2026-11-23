"""
This module assembles CanvasXpress charts into HTML for the renderers in
`canvasxpress.render`: a full page, a fragment for a page that is already
displayed, or the parts of a page for frameworks that place them separately.
"""

from html import escape
from typing import List, Optional, Sequence, Tuple, Union

from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.context.assets import (
    FILL_JS,
    CXChartAssets,
    CXLibraryAssets,
    fill_container_js,
    script_element,
)
from canvasxpress.render.context.files import page_file_name

LIBRARY_NONE: str = "none"
"""The page already provides the CanvasXpress library and stylesheet, such as
through the head of a Shiny app. A chart license is still loaded."""

LIBRARY_TAGS: str = "tags"
"""The library is loaded by `<link>` and `<script>` elements that precede the
charts, for HTML that the browser parses as a whole, such as a saved page or a
Quarto document."""

LIBRARY_LOADER: str = "loader"
"""The library is loaded on demand by JavaScript that then creates the charts,
for HTML that is inserted into a page that is already displayed."""

LIBRARY_MODES: List[str] = [LIBRARY_NONE, LIBRARY_TAGS, LIBRARY_LOADER]

DEFAULT_GAP: int = 10
"""The default space between charts, in pixels."""


class CXHtmlDocument:
    """
    CXHtmlDocument arranges one or more CanvasXpress charts into HTML, and provides
    that HTML in the forms needed by each rendering context.

    Charts are placed in a grid, in the order given, with `columns` charts per row.
    Charts that share a `render_to` ID are given unique IDs; the caller's charts
    are not changed.

    With `fill_to_width`, the grid takes the full width of the element that holds
    it, divided equally between the columns, and each chart is redrawn at the
    width of its column whenever that changes. With `fill_to_height`, the grid
    takes the full height of the element that holds it, divided equally between
    the rows, and each chart is redrawn at the height of its row. A dimension that
    is not filled keeps its configured size. Height can only be filled where the
    holding element's height is given to it, such as by a fixed height or a
    fillable layout; where that height comes from the charts themselves, they
    keep their configured heights.

    This is provided by the canvasxpress package for live Python framework
    contexts, and is separate from CanvasXpress's own `resizable` option; see
    `FILL_JS`.
    """

    def __init__(
        self,
        charts: Union[CanvasXpress, Sequence[CanvasXpress], None] = None,
        columns: int = 1,
        gap: int = DEFAULT_GAP,
        title: str = "CanvasXpress",
        library: Optional[CXLibraryAssets] = None,
        fill_to_width: bool = False,
        fill_to_height: bool = False,
    ):
        """
        Initializes a new CXHtmlDocument object.

        Args:
            charts: A CanvasXpress object, a sequence of them, or None.
            columns: The number of charts per row. Values less than 1 are
                treated as 1, and values greater than the number of charts as
                the number of charts.
            gap: The space between charts in pixels.
            title: The title of a full page.
            library: The library assets to load. Defaults to those configured for
                the CanvasXpress class, with the first chart license found.
            fill_to_width: Whether the charts follow the width of the element
                that holds them, rather than keeping their configured widths.
            fill_to_height: Whether the charts follow the height of the element
                that holds them, rather than keeping their configured heights.

        Raises:
            TypeError: If any chart is not a CanvasXpress object.
            ValueError: If columns or gap is not an int.
        """
        self.charts: List[CXChartAssets] = CXChartAssets.from_canvases(charts)

        self.columns: int = min(max(int(columns), 1), max(len(self.charts), 1))
        self.gap: int = max(int(gap), 0)
        self.title: str = str(title)
        self.fill_to_width: bool = bool(fill_to_width)
        self.fill_to_height: bool = bool(fill_to_height)

        if library is None:
            license_url = next(
                (chart.license_url for chart in self.charts if chart.license_url),
                None,
            )
            library = CXLibraryAssets.current(license_url=license_url)

        self.library: CXLibraryAssets = library

    def rows(self) -> List[List[CXChartAssets]]:
        """
        Returns:
            The charts, grouped into rows of `columns` charts.
        """
        return [
            self.charts[index : index + self.columns]
            for index in range(0, len(self.charts), self.columns)
        ]

    @property
    def size(self) -> Tuple[int, int]:
        """
        The space needed to display the arranged charts, in pixels, for contexts
        that must reserve it, such as an iframe. With `fill_to_width` or
        `fill_to_height` it is the size of the charts as configured, before they
        follow their container.

        Returns:
            A tuple of (width, height).
        """
        rows = self.rows()
        width = max(
            (
                sum(chart.width for chart in row) + self.gap * (len(row) - 1)
                for row in rows
            ),
            default=0,
        )
        height = sum(max(chart.height for chart in row) for row in rows)
        height += self.gap * max(len(rows) - 1, 0)

        return width, height

    @property
    def file_name(self) -> str:
        """
        The file name for the page, from the chart names in order, such as
        `scatter_heatmap.html`, or `anonymous` for a chart without a `render_to`
        ID. See `page_file_name()`.

        Returns:
            The file name, including the `.html` extension.
        """
        return page_file_name([chart.name for chart in self.charts])

    @property
    def fills(self) -> bool:
        """
        Whether the charts follow their container in either dimension.
        """
        return self.fill_to_width or self.fill_to_height

    def layout_html(self) -> str:
        """
        Provides the chart canvases arranged in a grid. Each cell is identified by
        a `data-canvasxpress-cell` attribute holding its chart's ID.

        Returns:
            The HTML grid, or "" if there are no charts.
        """
        if not self.charts:
            return ""

        # A filled dimension is shared equally, whatever the content: a column or
        # row sized by its canvas would follow the chart rather than lead it.
        styles = ["display: grid", "box-sizing: border-box", f"gap: {self.gap}px"]
        if self.fill_to_width:
            styles += [
                f"grid-template-columns: repeat({self.columns}, minmax(0, 1fr))",
                "width: 100%",
            ]
        else:
            styles.append(f"grid-template-columns: repeat({self.columns}, max-content)")
        if self.fill_to_height:
            styles += [
                f"grid-template-rows: repeat({len(self.rows())}, minmax(0, 1fr))",
                "height: 100%",
            ]
        style = "; ".join(styles) + ";"

        cells = "\n".join(
            f'  <div class="canvasxpress-chart"'
            f' data-canvasxpress-cell="{chart.target_id}">{chart.canvas}</div>'
            for chart in self.charts
        )

        return f'<div class="canvasxpress-layout" style="{style}">\n{cells}\n</div>'

    def scripts_html(self) -> str:
        """
        Provides a `<script>` element per chart that creates the chart, preceded
        with `fill_to_width` or `fill_to_height` by one that defines
        `fillContainer()`. These require the CanvasXpress library to be loaded
        first.

        Returns:
            The HTML `<script>` elements, or "" if there are no charts.
        """
        if not self.charts:
            return ""

        scripts = [script_element(FILL_JS)] if self.fills else []
        scripts += [script_element(self._chart_code(chart)) for chart in self.charts]

        return "\n".join(scripts)

    def chart_js(self) -> str:
        """
        Provides JavaScript that creates every chart. An error in one chart is
        logged and does not prevent the others from being created. With
        `fill_to_width` or `fill_to_height` it also defines `fillContainer()` and
        applies it to each chart.

        Returns:
            The JavaScript, or "" if there are no charts.
        """
        if not self.charts:
            return ""

        parts = [FILL_JS] if self.fills else []
        parts += [
            "try {\n"
            f"{self._chart_code(chart)}\n"
            "} catch (error) {\n"
            f'  console.error("CanvasXpress chart {chart.target_id} failed:", error);\n'
            "}"
            for chart in self.charts
        ]

        return "\n".join(parts)

    def _chart_code(self, chart: CXChartAssets) -> str:
        """
        Provides the JavaScript that creates a chart and, with `fill_to_width` or
        `fill_to_height`, then has it follow the size of its layout cell.
        """
        if not self.fills:
            return chart.js

        fill = fill_container_js(
            chart.target_id,
            chart.width,
            chart.height,
            self.fill_to_width,
            self.fill_to_height,
        )
        return f"{chart.js}\n{fill}"

    def loader_js(self) -> str:
        """
        Provides JavaScript that loads the CanvasXpress library on demand and then
        creates every chart. The canvases must be in the page first; see
        `layout_html()`.

        Returns:
            The JavaScript, or "" if there are no charts.
        """
        if not self.charts:
            return ""

        return self.library.loader_js(self.chart_js())

    def fragment(self, library: str = LIBRARY_NONE) -> str:
        """
        Provides the arranged charts as HTML for use within a page.

        Args:
            library: How the CanvasXpress library is provided: `LIBRARY_NONE`,
                `LIBRARY_TAGS` or `LIBRARY_LOADER`.

        Returns:
            The HTML, or "" if there are no charts.

        Raises:
            ValueError: If library is not a valid mode.
        """
        if library not in LIBRARY_MODES:
            raise ValueError(f"library must be one of {', '.join(LIBRARY_MODES)}")

        if not self.charts:
            return ""

        if library == LIBRARY_LOADER:
            parts = [self.layout_html(), script_element(self.loader_js())]

        elif library == LIBRARY_TAGS:
            parts = [self.library.tags(), self.layout_html(), self.scripts_html()]

        else:
            parts = [
                self.library.license_tag(),
                self.layout_html(),
                self.scripts_html(),
            ]

        return "\n".join(part for part in parts if part)

    def page(self) -> str:
        """
        Provides the arranged charts as a complete HTML page. With
        `fill_to_height` the page body takes the full height of the window, which
        the charts then fill.

        Returns:
            The HTML page.
        """
        body = "\n".join(
            part for part in [self.layout_html(), self.scripts_html()] if part
        )

        # A page's height otherwise comes from its content, which leaves nothing
        # to fill. The padding stands in for the body margin it replaces.
        style = (
            "<style>\n"
            "html, body { height: 100%; margin: 0; }\n"
            "body { padding: 8px; box-sizing: border-box; }\n"
            "</style>\n"
            if self.fill_to_height
            else ""
        )

        return (
            "<!DOCTYPE html>\n"
            "<html>\n"
            "<head>\n"
            '<meta charset="UTF-8">\n'
            f"<title>{escape(self.title)}</title>\n"
            f"{style}"
            f"{self.library.tags()}\n"
            "</head>\n"
            "<body>\n"
            f"{body}\n"
            "</body>\n"
            "</html>\n"
        )
