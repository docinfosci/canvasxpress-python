from typing import Any, Union, List

from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.base import CXRenderable
import streamlit.components.v1 as components

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

def plot(cx: Union[CanvasXpress, List[CanvasXpress]], columns: int = 1,) -> Union[object, None]:
    """
    Converts the provided CanvasXpress object into a CXStreamlit object that is
    primed by the configuration represented by the CanvasXpress object.
    :param cx: `CanvasXpress` The CanvasXpress object to render.  An exception is
        raised if cx is `None`.
    :returns: `CXStreamlit` A CXStreamlit with the configuration as represented
        by cx.  'None' if cx is invalid.
    """
    render_targets = list()

    if cx is None:
        return None

    elif isinstance(cx, CanvasXpress):
        render_targets.append(cx)

    else:
        render_targets.extend(cx)

    # TODO: update logic to handle list of CX objects

    element_parts = render_targets[0].render_to_html_parts()
    canvas = element_parts["cx_canvas"]
    function = element_parts["cx_js"]

    cx_license = ""
    if element_parts.get("cx_license"):
        cx_license = part["cx_license"]

    js_function = _cx_fx_template.replace("@code@", function)

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
        _cx_html_template.replace("@canvases@", canvas)
        .replace("@canvasxpress_license@", cx_license)
        .replace("@js_functions@", js_function)
        .replace("@css_url@", css_url)
        .replace("@js_url@", js_url)
    )

    print(html)

    return components.html(html, height=render_targets[0].height)