import uuid
import os
from copy import deepcopy
import tempfile
from time import sleep
from typing import Any, Union, List
import webbrowser

from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.base import CXRenderable

_cx_fx_template = """
<script type="text/javascript">
    onReady(function () {
        @code@
    })
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
        />
        <script 
                src='@js_url@' 
                type='text/javascript'>
        </script>

        <!-- 2. Include script to initialize object -->
        @js_functions@

    </head>
    <body>
        <!-- 3. DOM element where the visualization will be displayed -->
        @canvases@
     </body>
</html>
"""


class CXBrowserPopup(CXRenderable):
    """
    CXBrowserPopup is a `CXRenderable` that renders `CanvasXpress` objects into
    a Web page that is displayed in a pop-up browser window.
    """

    def __init__(self, *cx: Union[List[CanvasXpress], CanvasXpress, None]):
        """
        Initializes a new `CXBrowserPopup` object.
        :praram cx: `Union[List[CanvasXpress], CanvasXpress, None], ...`
            The `CanvasXpress` object(s) to be tracked.  See the `canvas`
            property, except that on initialization cx can be `None`.
            Multiple CanvasXpress objects are supported provided that
            they have distinct `render_to` targets.
        """
        super().__init__(*cx)

    def render(self, **kwargs: Any):
        """
        Renders the associated CanvasXpress object appropriate for display in
        a pop-up browser window.  Charts cannot have the same name,
        so render_to will be updated with a uuid for each conflicting chart.
        :param kwargs: `Any`
            Supports `columns` for any positive `int` of `1` or greater, with a
            default value of `1`.  Values less that `1` are ignored.  `columns`
            indicates how many charts should be rendered horizontally in the
            browser if more than one chart is being tracked.
        """
        render_targets = list()

        if self.canvas is None:
            pass

        elif isinstance(self.canvas, CanvasXpress):
            render_targets.append(deepcopy(self.canvas))

        else:
            for chart in self.canvas:
                render_targets.append(deepcopy(chart))

        used_render_targets = list()
        for target in render_targets:
            original_render_target = target.render_to
            if original_render_target in used_render_targets:
                target.render_to = (
                    original_render_target + "_" + str(uuid.uuid4()).replace("-", "_")
                )

            used_render_targets.append(target.render_to)

        render_targets.reverse()

        html_parts = [target.render_to_html_parts() for target in render_targets]

        canvases = [part["cx_canvas"] for part in html_parts]

        functions = [part["cx_js"] for part in html_parts]

        cx_license = ""
        for part in html_parts:
            if part.get("cx_license"):
                cx_license = part["cx_license"]
                break

        columns_arg = int(kwargs.get("columns", 1))
        columns = columns_arg if columns_arg > 0 else 1
        if len(canvases) < columns:
            columns = len(canvases)

        page_width = 0
        page_height = 0
        chart_count = len(canvases)
        canvas_table = '<table style="width:100%">'

        while chart_count > 0:
            candidate_width = 0
            candidate_height = 0

            canvas_table += "<tr>"
            for c in range(columns):
                canvas_table += "<td>"
                if chart_count > 0:
                    canvas_table += canvases[chart_count - 1]

                    candidate_width += render_targets[chart_count - 1].width
                    if render_targets[chart_count - 1].height > candidate_height:
                        candidate_height = render_targets[chart_count - 1].height

                canvas_table += "</td>"
                chart_count = chart_count - 1

            canvas_table += "</tr>"

            if candidate_width > page_width:
                page_width = candidate_width
            page_height += candidate_height

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

        tempdir = tempfile.TemporaryDirectory()

        temp_filename = os.path.join(tempdir.name, f"{str(uuid.uuid4())}.html")
        with open(temp_filename, "w") as temp_file:
            temp_file.write(html)

        webbrowser.open("file://" + temp_filename, new=1)

        sleep(2)
        tempdir.cleanup()
