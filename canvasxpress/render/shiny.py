import warnings
import logging

from shiny import ui

from canvasxpress.canvas import CanvasXpress

_cx_default_css_url = "https://www.canvasxpress.org/dist/canvasXpress.css"
_cx_versioned_css_url = "https://cdnjs.cloudflare.com/ajax/libs/canvasXpress/@cx_version@/canvasXpress.css"

_cx_default_js_url = "https://www.canvasxpress.org/dist/canvasXpress.min.js"
_cx_versioned_js_url = "https://cdnjs.cloudflare.com/ajax/libs/canvasXpress/@cx_version@/canvasXpress.min.js"

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
    """
    if id is None:
        raise ValueError("output_canvasxpress requires that id be of type str and not None.")

    elif not isinstance(id, str):
        raise TypeError("output_canvasxpress requires that id be of type str.")

    else:
        css_url = _cx_default_css_url
        js_url = _cx_default_js_url
        if CanvasXpress.cdn_edition() is not None:
            css_url = _cx_versioned_css_url.replace(
                "@cx_version@", CanvasXpress.cdn_edition()
            )
            js_url = _cx_versioned_js_url.replace(
                "@cx_version@", CanvasXpress.cdn_edition()
            )

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
        Initializes this object with a valid reference to a CanvasXpress object.  An invalid reference will result in
        a ValueError (`None`) or TypeError (an object not of the type `CanvasXpress`) exception.
        :param canvas: `CanvasXpress` - A valid CanvasXpress object to be rendered in the shiny UI.
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
        Renders the object as Shiny compliant HTML.
        """
        try:
            warnings.filterwarnings("ignore")
            logging.getLogger("rpy2.rinterface_lib.embedded").setLevel(logging.ERROR)

            from rpy2 import robjects
        except:
            robjects = None

        # Get the header assets.
        css_url = _cx_default_css_url
        js_url = _cx_default_js_url
        if CanvasXpress.cdn_edition() is not None:
            css_url = _cx_versioned_css_url.replace(
                "@cx_version@", CanvasXpress.cdn_edition()
            )
            js_url = _cx_versioned_js_url.replace(
                "@cx_version@", CanvasXpress.cdn_edition()
            )

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
