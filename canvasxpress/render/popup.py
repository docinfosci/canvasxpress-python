import webbrowser
from pathlib import Path
from typing import Any, List, Union

from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.base import CXRenderable
from canvasxpress.render.context import (
    CXHtmlDocument,
    temp_directory,
    write_html_file,
)


class CXBrowserPopup(CXRenderable):
    """
    CXBrowserPopup is a CXRenderable that renders CanvasXpress objects into
    a Web page that is displayed in a pop-up browser window.
    """

    def __init__(self, *cx: Union[List[CanvasXpress], CanvasXpress, None]):
        """
        Initializes a new CXBrowserPopup object.

        Args:
            cx: The CanvasXpress object(s) to be tracked. See the `canvas`
                property, except that on initialization cx can be None.
                Multiple CanvasXpress objects are supported provided that
                they have distinct `render_to` targets.

        Raises:
            TypeError: If any cx member is not a CanvasXpress instance.
        """
        super().__init__(*cx)

    def render(self, **kwargs: Any) -> Path:
        """
        Renders the associated CanvasXpress objects for display in
        a pop-up browser window. Charts cannot have the same name,
        so conflicting charts are displayed under unique IDs.

        The page is written to the user's `canvasxpress-python-<user>` folder in
        the system temporary directory, where it remains so that the browser can
        load it. It is named after the charts, such as `scatter_heatmap.html`, or
        `anonymous.html` for a chart without a `render_to` ID, so rendering the
        same charts again replaces the page rather than adding a file.

        Args:
            kwargs: Supports the following parameters:
                columns: Any positive int of 1 or greater, with a default
                    value of 1. Values less than 1 are ignored. Indicates
                    how many charts should be rendered horizontally in the
                    browser if more than one chart is being tracked.
                fill_to_width: True to have the charts share the width of the
                    browser window and follow it as it is resized, rather than
                    keeping their configured widths. Default is False.
                fill_to_height: True to have the charts share the height of the
                    browser window and follow it as it is resized, rather than
                    keeping their configured heights. Default is False.

        Returns:
            The path of the page displayed.
        """
        document = CXHtmlDocument(
            self.canvas,
            columns=kwargs.get("columns", 1),
            fill_to_width=bool(kwargs.get("fill_to_width", False)),
            fill_to_height=bool(kwargs.get("fill_to_height", False)),
        )

        page_path = write_html_file(
            document.page(), temp_directory() / document.file_name
        )

        webbrowser.open(page_path.resolve().as_uri(), new=1)

        return page_path
