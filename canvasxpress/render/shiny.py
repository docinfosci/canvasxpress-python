import logging
import warnings

from shiny import ui

from canvasxpress.canvas import CanvasXpress

_cx_js_intermixed_template = """
<script type="text/javascript">
    @code@
</script>
"""

_cx_html_intermixed_template = """
<div>
    @canvasxpress_license@
    @canvase@
    @js_functions@
</div>
"""


def output_canvasxpress(id: str) -> ui.TagList:
    """
    Establishes an output reactive placeholder into which a CanvasXpress chart can be rendered.

    Args:
        id: The identifier for the output placeholder.

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
        css_url = CanvasXpress.css_library_url()
        js_url = CanvasXpress.js_library_url()

        return ui.TagList(
            ui.head_content(
                ui.tags.link(href=css_url, rel="stylesheet"),
                ui.tags.script(src=js_url),
            ),
            ui.output_ui(id),
        )


class CXShinyWidget(object):
    """
    A Shiny for Python compatible class that can be used with Shiny syntax to establish CanvasXpress charts in the
    shiny UI.
    """

    def __init__(self, canvas: CanvasXpress):
        """
        Initializes this object with a valid reference to a CanvasXpress object.

        Args:
            canvas: A valid CanvasXpress object to be rendered in the shiny UI.

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

    def _repr_html_(self):
        """
        Renders the object as Shiny compliant HTML.

        Returns:
            An HTML string representation of the CanvasXpress chart.
        """
        # Get the HTML and JS assets.
        html_parts: dict = self._canvas.render_to_html_parts()

        # Provide the taglist.
        components = ui.TagList(
            [
                ui.div(
                    ui.HTML(
                        _cx_html_intermixed_template.replace(
                            "@canvasxpress_license@",
                            html_parts.get("cx_license", ""),
                        )
                        .replace(
                            "@canvase@",
                            html_parts["cx_canvas"],
                        )
                        .replace(
                            "@js_functions@",
                            _cx_js_intermixed_template.replace(
                                "@code@",
                                html_parts["cx_js"],
                            ),
                        )
                    ),
                ),
            ]
        )

        # Generate the chart DIV and provide it for rendering.
        return components.get_html_string()

    def _repr_rstudio_viewer_(self):
        """
        Renders the object for display in the RStudio viewer.

        This method writes the chart HTML to a temporary file and opens it
        in the RStudio viewer pane using rpy2.
        """
        try:
            warnings.filterwarnings("ignore")
            logging.getLogger("rpy2.rinterface_lib.embedded").setLevel(logging.ERROR)

            from rpy2 import robjects
        except:
            robjects = None

        # Get the header assets.
        css_url = CanvasXpress.css_library_url()
        js_url = CanvasXpress.js_library_url()

        # Get the HTML and JS assets.
        html_parts: dict = self._canvas.render_to_html_parts()

        # Provide the taglist.
        components = [
            ui.div(
                ui.head_content(
                    ui.tags.link(href=css_url, rel="stylesheet"),
                    ui.tags.script(src=js_url),
                ),
                ui.HTML(
                    _cx_html_intermixed_template.replace(
                        "@canvasxpress_license@",
                        html_parts.get("cx_license", ""),
                    )
                    .replace(
                        "@canvase@",
                        html_parts["cx_canvas"],
                    )
                    .replace(
                        "@js_functions@",
                        _cx_js_intermixed_template.replace(
                            "@code@",
                            html_parts["cx_js"],
                        ),
                    )
                ),
            ),
        ]

        # Generate the chart DIV and provide it for rendering.
        ui_components = ui.TagList(components)
        html = ui_components.get_html_string().replace("\n", "")

        robjects.globalenv["html"] = html
        robjects.r(
            """
            tf <- tempfile(fileext = ".html")
            writeLines(html, tf)
            rstudioapi::viewer(tf)
            """
        )
