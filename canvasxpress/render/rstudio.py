from pathlib import Path
from typing import Any, List, Optional, Union

from bs4 import BeautifulSoup
from IPython.display import HTML

from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.base import CXRenderable
from canvasxpress.render.context import (
    LIBRARY_NONE,
    LIBRARY_TAGS,
    CXHtmlDocument,
    CXLibraryAssets,
    write_html_file,
)


class CXHtml(CXRenderable):
    """
    CXHtml is a CXRenderable that renders CanvasXpress objects into
    HTML Snippets suitable for use in RStudio.
    """

    def __init__(self, *cx: Union[List[CanvasXpress], CanvasXpress, None]):
        """
        Initializes a new CXHtml object.

        Args:
            cx: The CanvasXpress object(s) to be tracked. See the `canvas`
                property, except that on initialization cx can be None.
                Multiple CanvasXpress objects are supported provided that
                they have distinct `render_to` targets.

        Raises:
            TypeError: If any cx member is not a CanvasXpress instance.
        """
        super().__init__(*cx)

    def display_canvasxpress_header(self) -> str:
        """
        Provides the HTML elements that load the CanvasXpress stylesheet and
        library.

        Returns:
            The HTML elements.
        """
        library = CXLibraryAssets.current()
        return "\n".join([library.stylesheet_tag(), library.library_tag()])

    def display_debug_code(self, code: str) -> str:
        """
        Formats HTML code for reading.

        Args:
            code: The HTML code.

        Returns:
            The formatted HTML code.
        """
        pretty_code = BeautifulSoup(code, "html.parser").prettify()
        return pretty_code

    def get_chart_display_code(
        self,
        columns: int,
        fill_to_width: bool = False,
        fill_to_height: bool = False,
    ) -> str:
        """
        Provides the arranged charts as HTML for a page that already loads the
        CanvasXpress library, such as after `display_canvasxpress_header()`.

        Args:
            columns: The number of charts per row.
            fill_to_width: Whether the charts follow the width of the element
                that holds them.
            fill_to_height: Whether the charts follow the height of the element
                that holds them, where the layout gives it one.

        Returns:
            The HTML, or "" if there are no charts.
        """
        return CXHtmlDocument(
            self.canvas,
            columns=columns,
            fill_to_width=fill_to_width,
            fill_to_height=fill_to_height,
        ).fragment(LIBRARY_NONE)

    def display_charts(
        self, code: str, output_file: Optional[str], file_name: Optional[str] = None
    ) -> str:
        """
        Writes code to output_file, if provided, and returns it.

        Args:
            code: The HTML code.
            output_file: The file path, or a directory in which to write
                file_name, or None.
            file_name: The file name to use when output_file is a directory.
                Defaults to `anonymous.html`.

        Returns:
            The code.

        Raises:
            RuntimeError: If the file cannot be written.
        """
        try:
            if output_file is not None:
                write_html_file(code, Path(str(output_file)), file_name)

        except Exception as e:
            raise RuntimeError(f"Cannot create output file: {e}")

        return code

    def render(self, **kwargs: Any):
        """
        Renders the associated CanvasXpress objects for display in
        a RStudio environment. Charts cannot have the same name, so
        conflicting charts are displayed under unique IDs.

        Args:
            kwargs: Supports the following parameters:
                columns: Any positive int of 1 or greater, with a default
                    value of 1. Values less than 1 are ignored. Indicates
                    how many charts should be rendered horizontally if more
                    than one chart is being tracked.
                output_file: A string for a path at which the charts should
                    also be saved as a standalone HTML page. If a file exists
                    at the specified path then it will be overwritten, and if
                    the path is a directory the page is saved in it under the
                    chart names, such as `scatter_heatmap.html`.
                debug: True indicates that the formatted HTML code shall be
                    printed. Default is False.
                fill_to_width: True to have the charts share the width of the
                    element that holds them, such as the viewer pane or a Quarto
                    column, and follow it as it changes, rather than keeping
                    their configured widths. Default is False.
                fill_to_height: True to have the charts follow the height of
                    the element that holds them, rather than keeping their
                    configured heights. This only has an effect where the
                    layout sets that height, as it does for the page saved with
                    output_file, which fills the browser window. Default is
                    False.

        Returns:
            An IPython HTML object containing the rendered chart(s).

        Raises:
            RuntimeError: If there is an error creating the output cell.
        """
        debug_output = bool(kwargs.get("debug") or False)
        fill_to_width = bool(kwargs.get("fill_to_width") or False)
        fill_to_height = bool(kwargs.get("fill_to_height") or False)

        columns_arg = int(kwargs.get("columns", 1))
        columns = columns_arg if columns_arg > 0 else 1

        output_file = kwargs.get("output_file")
        if not isinstance(output_file, str):
            output_file = None

        document = CXHtmlDocument(
            self.canvas,
            columns=columns,
            fill_to_width=fill_to_width,
            fill_to_height=fill_to_height,
        )

        try:
            # Elements that load the library precede the charts, as the HTML is
            # parsed as a whole, such as in a Quarto document.
            code = document.fragment(LIBRARY_TAGS)
            if output_file is not None:
                self.display_charts(document.page(), output_file, document.file_name)

            if debug_output:
                print(self.display_debug_code(code))

            return HTML(code)

        except Exception as e:
            raise RuntimeError(f"Cannot create output cell: {e}")
