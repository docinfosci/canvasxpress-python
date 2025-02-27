from canvasxpress.canvas import CanvasXpress
import streamlit.components.v1 as components

_cx_iframe_padding = 50

_cx_fx_template = """
<script type="text/javascript">
    @code@
</script>
"""

_cx_default_css_url = "https://www.canvasxpress.org/dist/canvasXpress.css"

_cx_versioned_css_url = (
    "https://cdnjs.cloudflare.com/ajax/libs/canvasXpress/@cx_version@/canvasXpress.css"
)

_cx_default_js_url = "https://www.canvasxpress.org/dist/canvasXpress.min.js"

_cx_versioned_js_url = "https://cdnjs.cloudflare.com/ajax/libs/canvasXpress/@cx_version@/canvasXpress.min.js"

_cx_html_template = """
<html>
    <head>
        <meta charset="UTF-8">
        <title>CanvasXpress</title>

        <!-- 1. Include the CanvasXpress library -->
        @canvasxpress_license@
        <link 
                href='@css_url@' 
                rel='stylesheet' 
                type='text/css'
                referrerpolicy='origin-when-cross-origin'
        />
        <script 
                src='@js_url@' 
                type='text/javascript'>
                referrerpolicy='origin-when-cross-origin'
        </script>
    </head>
    <body>
        <!-- 3. DOM element where the visualization will be displayed -->
        @canvases@
        <!-- 2. Include script to initialize object -->
        @js_functions@
     </body>
</html>
"""


def _get_chart_display_code(cx: CanvasXpress) -> tuple:
    """
    Get the html display code and iframe dimensions for rendering a CanvasXpress
    object in a Streamlit application.
    :param cx: `CanvasXpress`
        The `CanvasXpress` object to be rendered.
    :returns: `tuple` of html, iframe_width, iframe_height
    """
    html_parts = cx.render_to_html_parts()
    canvases = html_parts["cx_canvas"]
    js_functions = _cx_fx_template.replace("@code@", html_parts["cx_js"])

    cx_license = ""
    if html_parts.get("cx_license"):
        cx_license = html_parts["cx_license"]

    css_url = _cx_default_css_url
    js_url = _cx_default_js_url
    if CanvasXpress.cdn_edition() is not None:
        css_url = _cx_versioned_css_url.replace(
            "@cx_version@", CanvasXpress.cdn_edition()
        )
        js_url = _cx_versioned_js_url.replace(
            "@cx_version@", CanvasXpress.cdn_edition()
        )

    html = (
        _cx_html_template.replace("@canvases@", canvases)
        .replace("@canvasxpress_license@", cx_license)
        .replace("@js_functions@", js_functions)
        .replace("@css_url@", css_url)
        .replace("@js_url@", js_url)
    )

    iframe_width = cx.width + _cx_iframe_padding
    iframe_height = cx.height + _cx_iframe_padding

    return html, iframe_width, iframe_height


def plot(cx: CanvasXpress) -> None:
    """
    Renders the provided CanvasXpress object for display in a Streamlit application.
    :param cx: `CanvasXpress`
        The `CanvasXpress` object to be rendered.
    :returns: `None` or raises a `TypeError` exception if `cx` is not a CanvasXpress
        object.
    """
    if cx is None:
        return None

    elif not isinstance(cx, CanvasXpress):
        raise TypeError(f"Argument 'cx' is not a CanvasXpress object")

    html, iframe_width, iframe_height = _get_chart_display_code(cx)

    components.html(html, width=iframe_width, height=iframe_height)
