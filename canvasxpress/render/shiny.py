from shiny import ui

from canvasxpress.canvas import CanvasXpress

_cx_default_css_url = "https://www.canvasxpress.org/dist/canvasXpress.css"

_cx_versioned_css_url = (
    "https://cdnjs.cloudflare.com/ajax/libs/canvasXpress/@cx_version@/canvasXpress.css"
)

_cx_default_js_url = "https://www.canvasxpress.org/dist/canvasXpress.min.js"

_cx_versioned_js_url = "https://cdnjs.cloudflare.com/ajax/libs/canvasXpress/@cx_version@/canvasXpress.min.js"

_cx_js_intermixed_template = """
<script type="text/javascript">
    @code@
</script>
"""

_cx_html_intermixed_template = """
<html>
    @canvasxpress_license@
    @canvase@
    @js_functions@
</html>
"""


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
        try:
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
            return ui.TagList(
                ui.div(
                    ui.HTMLDependency(
                        stylesheet=[{"href": css_url}],
                        script=[{"src": js_url}],
                    ),
                    ui.HTML(
                        _cx_html_intermixed_template.replace(
                            "@canvasxpress_license@",
                            "",
                        ).replace(
                            "@canvase@",
                            html_parts["canvas"],
                        ).replace(
                            "@js_functions@",
                            html_parts["cx_js"],
                        )
                    ),
                )
            )

        except Exception as e:
            return None
