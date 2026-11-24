from typing import Any, List, Union

from bs4 import BeautifulSoup
from IPython.display import HTML, Code, Javascript

from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.base import CXRenderable
from canvasxpress.render.context import (
    CXHtmlDocument,
    CXLibraryAssets,
    write_html_file,
)


def inject_cx_assets() -> Javascript:
    """
    Provides JavaScript that loads the CanvasXpress library and stylesheet into
    the notebook page, if they are not loaded already. Charts rendered by
    `CXNoteBook` load them on their own, so this is only needed for other
    CanvasXpress JavaScript.

    Returns:
        An IPython Javascript display object.
    """
    return Javascript(data=CXLibraryAssets.current().loader_js(""))


class CXNoteBook(CXRenderable):
    """
    CXNoteBook is a CXRenderable that renders CanvasXpress objects into
    IPython containers (Jupyter Notebooks). A `CanvasXpress` object that is
    the result of a cell also renders on its own, via its IPython display
    hook, which emits the same HTML and JavaScript built by the shared
    `CXHtmlDocument`; `CXNoteBook` adds multi-chart `columns`,
    `fill_to_width` and `fill_to_height`, `output_file`, and `debug`.
    """

    def __init__(self, *cx: Union[List[CanvasXpress], CanvasXpress, None]):
        """
        Initializes a new CXNoteBook object.

        Args:
            cx: The CanvasXpress object(s) to be tracked. See the `canvas`
                property, except that on initialization cx can be None.
                Multiple CanvasXpress objects are supported provided that
                they have distinct `render_to` targets.

        Raises:
            TypeError: If any cx member is not a CanvasXpress instance.
        """
        super().__init__(*cx)

    def display_debug_code(self, code: str) -> Code:
        """
        Provides HTML code for display, formatted for reading.

        Args:
            code: The HTML code.

        Returns:
            An IPython Code display object.
        """
        pretty_code = BeautifulSoup(code, "html.parser").prettify()
        return Code(
            data=pretty_code,
            language="html",
        )

    def get_chart_display_code(
        self,
        columns: int,
        fill_to_width: bool = False,
        fill_to_height: bool = False,
    ) -> list:
        """
        Provides the display objects that render the charts in a notebook: the
        arranged canvases, then JavaScript that loads CanvasXpress, if needed,
        and creates the charts.

        Args:
            columns: The number of charts per row.
            fill_to_width: Whether the charts follow the width of the output
                area.
            fill_to_height: Whether the charts follow the height of the output
                area, where the notebook gives it one.

        Returns:
            A list of IPython display objects, empty if there are no charts.
        """
        document = CXHtmlDocument(
            self.canvas,
            columns=columns,
            fill_to_width=fill_to_width,
            fill_to_height=fill_to_height,
        )
        if not document.charts:
            return []

        return [
            HTML(data=document.layout_html()),
            Javascript(data=document.loader_js()),
        ]

    def render(self, **kwargs: Any):
        """
        Renders the associated CanvasXpress objects for display in
        an IPython (e.g., Jupyter NoteBook/Lab) environment. Charts cannot
        have the same name, so conflicting charts are displayed under unique
        IDs.

        Args:
            kwargs: Supports the following parameters:
                columns: Any positive int of 1 or greater, with a default
                    value of 1. Values less than 1 are ignored. Indicates
                    how many charts should be rendered horizontally in the
                    Jupyter Notebook if more than one chart is being tracked.
                output_file: A string for a path at which the charts should
                    also be saved as a standalone HTML page. If a file exists
                    at the specified path then it will be overwritten, and if
                    the path is a directory the page is saved in it under the
                    chart names, such as `scatter_heatmap.html`, or
                    `anonymous.html` for a chart without a `render_to` ID.
                    This permits Jupyter sessions to render output that
                    is saved and accessible in later sessions.
                debug: True indicates that the HTML page for the charts shall
                    be displayed as code instead of the charts. Default is
                    False.
                fill_to_width: True to have the charts share the width of the
                    notebook output area and follow it as it changes, rather
                    than keeping their configured widths. Default is False.
                fill_to_height: True to have the charts follow the height of
                    the output area. A notebook output takes its height from
                    its content, so charts there keep their configured heights;
                    it applies to the page saved with output_file, which fills
                    the browser window. Default is False.

        Returns:
            A list of IPython display objects containing the rendered charts, or
            a Code display object if debug is True.
        """
        try:
            debug_output = bool(kwargs.get("debug") or False)
            fill_to_width = bool(kwargs.get("fill_to_width") or False)
            fill_to_height = bool(kwargs.get("fill_to_height") or False)

            columns_arg = int(kwargs.get("columns", 1))
            columns = columns_arg if columns_arg > 0 else 1

            output_file = kwargs.get("output_file")
            if not isinstance(output_file, str):
                output_file = None

            if debug_output or output_file is not None:
                document = CXHtmlDocument(
                    self.canvas,
                    columns=columns,
                    fill_to_width=fill_to_width,
                    fill_to_height=fill_to_height,
                )
                page = document.page()

                if output_file is not None:
                    try:
                        write_html_file(page, output_file, document.file_name)

                    except Exception as e:
                        return HTML(f"<div>Cannot create output file: {e}</div>")

                if debug_output:
                    return self.display_debug_code(page)

            return self.get_chart_display_code(columns, fill_to_width, fill_to_height)

        except Exception as e:
            return HTML(f"<div>Cannot create output cell: {e}</div>")
