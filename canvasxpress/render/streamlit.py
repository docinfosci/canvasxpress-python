import uuid
from typing import Union, List

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


def plot(
    cx: Union[CanvasXpress, List[CanvasXpress]],
    columns: int = 1,
) -> Union[object, None]:
    """
    Renders the provided CanvasXpress object(s) for display in a Streamlit application.
    :param cx: `Union[CanvasXpress, List[CanvasXpress]]`
        The `CanvasXpress` object(s) to be tracked. Charts cannot have the same name,
        so render_to will be updated with a uuid for each conflicting chart.
    :param columns: `int`
        Indicates how many charts should be rendered horizontally in the Streamlit
        application if more than one chart is being tracked. Any positive `int` of `1`
        or greater is accepted, with a default value of `1`. Values less than `1`
        are ignored.
    :returns: `None` or raises a `TypeError` exception if `cx` is not a CanvasXpress
        object or list of CanvasXpress objects.
    """

    columns = int(columns)
    columns = columns if columns > 0 else 1

    render_targets = list()

    if cx is None:
        return None

    elif isinstance(cx, CanvasXpress):
        render_targets.append(cx)

    else:
        render_targets.extend(cx)

    used_render_targets = list()
    for i, target in enumerate(render_targets):
        if not isinstance(target, CanvasXpress):
            raise TypeError(f"Item {i} in argument 'cx' is not a CanvasXpress object")

        original_render_target = target.render_to
        if original_render_target in used_render_targets:
            target.render_to = (
                original_render_target + "_" + str(uuid.uuid4()).replace("-", "_")
            )

        used_render_targets.append(target.render_to)

    render_targets.reverse()

    html_parts = [target.render_to_html_parts() for target in render_targets]

    canvases = [part["cx_canvas"] for part in html_parts]
    if len(canvases) < columns:
        columns = len(canvases)

    functions = [part["cx_js"] for part in html_parts]

    cx_license = ""
    for part in html_parts:
        if part.get("cx_license"):
            cx_license = part["cx_license"]
            break

    iframe_width = 0
    iframe_height = 0
    chart_count = len(canvases)

    canvas_table = '<div class="d-flex flex-column">'

    while chart_count > 0:
        candidate_width = 0
        candidate_height = 0

        canvas_table += '<div class="d-flex flex-row">'
        for c in range(columns):
            canvas_table += '<div class="p-2">'
            if chart_count > 0:
                canvas_table += canvases[chart_count - 1]

                candidate_width += render_targets[chart_count - 1].width
                if render_targets[chart_count - 1].height > candidate_height:
                    candidate_height = render_targets[chart_count - 1].height

            canvas_table += "</div>"
            chart_count = chart_count - 1

        canvas_table += "</div>"

        if candidate_width > iframe_width:
            iframe_width = candidate_width
        iframe_height += candidate_height

    canvas_table += "</div>"

    iframe_width += _cx_iframe_padding
    iframe_height += _cx_iframe_padding

    js_functions = "\n".join(
        [_cx_fx_template.replace("@code@", fx) for fx in functions]
    )

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
        _cx_html_template.replace("@canvases@", canvas_table)
        .replace("@canvasxpress_license@", cx_license)
        .replace("@js_functions@", js_functions)
        .replace("@css_url@", css_url)
        .replace("@js_url@", js_url)
    )

    components.html(html, width=iframe_width, height=iframe_height)
