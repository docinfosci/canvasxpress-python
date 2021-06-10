import uuid
from os import unlink
from time import sleep
from typing import Any, Union, List

from IPython.display import display, IFrame

from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.base import CXRenderable

_cx_iframe_padding = 20

_cx_fx_template = """
<script type="text/javascript">
    onReady(function () {
        @code@
    })
</script>
"""

_cx_html_template = """
<html>
    <head>
        <meta charset="UTF-8">
        <title>Flask CanvasXpress Example</title>
    </head>
    <body>
        <!-- 1. DOM element where the visualization will be displayed -->
        @canvases@

        <!-- 2. Include the CanvasXpress library -->
        @canvasxpress_license@
        <link 
                href='https://www.canvasxpress.org/dist/canvasXpress.css' 
                rel='stylesheet' 
                type='text/css'
        />
        <script 
                src='https://www.canvasxpress.org/dist/canvasXpress.min.js' 
                type='text/javascript'>
        </script>

        <!-- 3. Include script to initialize object -->
        @js_functions@
     </body>
</html>
"""


class CXNoteBook(CXRenderable):
    """
    CXNoteBook is a `CXRenderable` that renders `CanvasXpress` objects into
    `IPython` containers (Jupyter Notebooks).
    """

    def __init__(
            self,
            cx: Union[List[CanvasXpress], CanvasXpress, None]
    ):
        """
        Initializes a new `CXNoteBook` object.
        :praram cx: `value: Union[List[CanvasXpress], CanvasXpress, None]`
            The `CanvasXpress` object(s) to be tracked.  See the `canvas`
            property, except that on initialization cx can be `None`.
            Multiple CanvasXpress objects are supported provided that
            they have distinct `render_to` targets.
        """
        super().__init__(cx)

    def render(
            self,
            **kwargs: Any
    ):
        """
        Renders the associated CanvasXpress object appropriate for display in
        an IPython (e.g., Jupyter NoteBook/Lab) environment.
        :param kwargs: `Any`
            Supports `columns` for any positive `int` of `1` or greater, with a
            default value of `1`.  Values less that `1` are ignored.  `columns`
            indicates how many charts should be rendered horizontally in the
            Jupyter Notebook if more than one chart is being tracked.
        """
        render_targets = list()

        if self.canvas is None:
            pass

        elif isinstance(self.canvas, CanvasXpress):
            render_targets.append(self.canvas)

        else:
            render_targets.extend(self.canvas)

        html_parts = [
            target.render_to_html_parts()
            for target in render_targets
        ]

        canvases = [
            part["cx_canvas"]
            for part in html_parts
        ]

        functions = [
            part["cx_js"]
            for part in html_parts
        ]

        license = ""
        for part in html_parts:
            if part.get("cx_license"):
                license = part["cx_license"]
                break

        columns_arg = int(kwargs.get("columns", 1))
        columns = columns_arg if columns_arg > 0 else 1
        if len(canvases) < columns:
            columns = len(canvases)

        chart_count = len(canvases)
        canvas_table = '<table style="width:100%">'
        while chart_count > 0:
            canvas_table += "<tr>"
            for c in range(columns):
                canvas_table += "<td>"
                if chart_count > 0:
                    canvas_table += canvases[chart_count - 1]
                canvas_table += "</td>"
                chart_count = chart_count - 1
            canvas_table += "</tr>"


        html = _cx_html_template \
            .replace("@canvases@", canvas_table) \
            .replace("@canvasxpress_license@", license) \
            .replace("@code@", "\n".join(functions))

        temp_filename = f"temp_{str(uuid.uuid4())}.html"
        with open(temp_filename, "w") as temp_file:
            temp_file.write(html)

        display(
            IFrame(
                temp_filename,
                f"{self.canvas.element_width + _cx_iframe_padding}px",
                f"{self.canvas.element_height + _cx_iframe_padding}px"
            )
        )

        sleep(2)
        unlink(temp_filename)
