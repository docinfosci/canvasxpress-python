import logging
import warnings

from shiny import ui

from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.context import LIBRARY_NONE, CXHtmlDocument, CXLibraryAssets


def _as_fill_item(tag: ui.Tag) -> ui.Tag:
    """
    Marks a tag as one that fills a fillable Shiny container, such as a card.
    Releases of Shiny without fill support give it the full height instead.
    """
    fill = getattr(ui, "fill", None)
    if fill is not None:
        return fill.as_fill_item(tag)

    tag.attrs["style"] = "height: 100%;"
    return tag


def output_canvasxpress(id: str, fill: bool = False) -> ui.TagList:
    """
    Establishes an output reactive placeholder into which a CanvasXpress chart can be rendered.

    Args:
        id: The identifier for the output placeholder.
        fill: True to have the placeholder fill a fillable container, such as a
            card or a fillable page, and pass that height on to its chart. This
            is needed for a chart rendered with `fill_to_height` to take the
            container's height. Default is False.

    Returns:
        A ui.TagList containing the CSS/JS headers and the output UI element.

    Raises:
        ValueError: If id is None.
        TypeError: If id is not a string.
    """
    if id is None:
        raise ValueError(
            "output_canvasxpress requires that id be of type str and not None."
        )

    elif not isinstance(id, str):
        raise TypeError("output_canvasxpress requires that id be of type str.")

    else:
        library = CXLibraryAssets.current()

        return ui.TagList(
            ui.head_content(
                ui.tags.link(href=library.css_url, rel="stylesheet"),
                ui.tags.script(src=library.js_url),
            ),
            ui.output_ui(id, fill=bool(fill), fillable=bool(fill)),
        )


class CXShinyWidget:
    """
    A Shiny for Python compatible class that can be used with Shiny syntax to establish CanvasXpress charts in the
    shiny UI.
    """

    def __init__(
        self,
        canvas: CanvasXpress,
        fill_to_width: bool = False,
        fill_to_height: bool = False,
    ):
        """
        Initializes this object with a valid reference to a CanvasXpress object.

        Args:
            canvas: A valid CanvasXpress object to be rendered in the shiny UI.
            fill_to_width: True to have the chart take the width of the element
                that holds it, such as a Shiny card or column, or the RStudio
                viewer pane, and follow it as it changes, rather than keeping
                its configured width. Default is False.
            fill_to_height: True to have the chart take the height of the
                element that holds it and follow it as it changes, rather than
                keeping its configured height. In a Shiny app this needs a
                container with a height, such as a card with a set height or a
                fillable page, and an `output_canvasxpress(id, fill=True)`
                placeholder; the RStudio viewer fills the pane. Default is
                False.

        Raises:
            ValueError: If canvas is None.
            TypeError: If canvas is not an instance of CanvasXpress.
        """
        if canvas is None:
            raise ValueError("canvas must be an instance of CanvasXpress")

        elif not isinstance(canvas, CanvasXpress):
            raise TypeError("canvas must be an instance of CanvasXpress")

        else:
            self._canvas = canvas
            self._fill_to_width = bool(fill_to_width)
            self._fill_to_height = bool(fill_to_height)

    def _document(self) -> CXHtmlDocument:
        return CXHtmlDocument(
            self._canvas,
            fill_to_width=self._fill_to_width,
            fill_to_height=self._fill_to_height,
        )

    def _repr_html_(self):
        """
        Renders the object as Shiny compliant HTML. The CanvasXpress library is
        provided by the page head, see `output_canvasxpress()`.

        Returns:
            An HTML string representation of the CanvasXpress chart.
        """
        document = self._document()
        wrapper = ui.div(ui.HTML(document.fragment(LIBRARY_NONE)))
        if self._fill_to_height:
            # The wrapper passes the height of a fillable container to the chart.
            wrapper = _as_fill_item(wrapper)

        components = ui.TagList([wrapper])

        return components.get_html_string()

    def _repr_rstudio_viewer_(self):
        """
        Renders the object for display in the RStudio viewer.

        This method writes the chart to a temporary HTML page and opens it
        in the RStudio viewer pane using rpy2.

        Raises:
            RuntimeError: If rpy2 is not available.
        """
        try:
            warnings.filterwarnings("ignore")
            logging.getLogger("rpy2.rinterface_lib.embedded").setLevel(logging.ERROR)

            from rpy2 import robjects

        except Exception as e:
            raise RuntimeError(
                "The RStudio viewer requires rpy2: pip install canvasxpress[rstudio]"
            ) from e

        robjects.globalenv["html"] = self._document().page()
        robjects.r(
            """
            tf <- tempfile(fileext = ".html")
            writeLines(html, tf)
            rstudioapi::viewer(tf)
            """
        )
