import uuid
from pathlib import Path
from typing import Any, Union, List
from urllib.parse import quote

from IPython.display import display, HTML, IFrame

from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.base import CXRenderable

_cx_iframe_padding = 50

_cx_default_css_url = "https://www.canvasxpress.org/dist/canvasXpress.css"

_cx_versioned_css_url = (
    "https://cdnjs.cloudflare.com/ajax/libs/canvasXpress/@cx_version@/canvasXpress.css"
)

_cx_default_js_url = "https://www.canvasxpress.org/dist/canvasXpress.min.js"

_cx_versioned_js_url = "https://cdnjs.cloudflare.com/ajax/libs/canvasXpress/@cx_version@/canvasXpress.min.js"

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

_nb_iframe_template = "data:text/html,@html@"


class CXNoteBook(CXRenderable):
    """
    CXNoteBook is a `CXRenderable` that renders `CanvasXpress` objects into
    `IPython` containers (Jupyter Notebooks).
    """

    def __init__(self, *cx: Union[List[CanvasXpress], CanvasXpress, None]):
        """
        Initializes a new `CXNoteBook` object.
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
        an IPython (e.g., Jupyter NoteBook/Lab) environment.  Charts cannot
        have the same name, so render_to will be updated with a uuid for each
        conflicting chart.
        :param kwargs: `Any`
            * Supports `columns` for any positive `int` of `1` or greater, with a
              default value of `1`.  Values less that `1` are ignored.  `columns`
              indicates how many charts should be rendered horizontally in the
              Jupyter Notebook if more than one chart is being tracked.
            * Supports `output_file` as a string for a path at which the output
              should be saved.  If a file exists at the specified path then
              it will be overwritten.  This permits Jupyter sessions to render
              output that is saved and accessible in later sessions.
        """
        render_targets = list()

        if self.canvas is None:
            pass

        elif isinstance(self.canvas, CanvasXpress):
            render_targets.append(self.canvas)

        else:
            render_targets.extend(self.canvas)

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

        iframe_width = 0
        iframe_height = 0
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

            if candidate_width > iframe_width:
                iframe_width = candidate_width
            iframe_height += candidate_height

        iframe_width += _cx_iframe_padding
        iframe_height += _cx_iframe_padding

        css_url = _cx_default_css_url
        js_url = _cx_default_js_url
        if CanvasXpress.cdn_edition() is not None:
            css_url = _cx_versioned_css_url.replace(
                "@cx_version@", CanvasXpress.cdn_edition()
            )
            js_url = _cx_versioned_js_url.replace(
                "@cx_version@", CanvasXpress.cdn_edition()
            )

        js_functions = "\n".join(
            [_cx_fx_template.replace("@code@", fx) for fx in functions]
        )

        html_text = (
            _cx_html_template.replace("@canvases@", canvas_table)
            .replace("@canvasxpress_license@", cx_license)
            .replace("@js_functions@", js_functions)
            .replace("@css_url@", css_url)
            .replace("@js_url@", js_url)
        )

        iframe_html = _nb_iframe_template.replace("@html@", quote(html_text))

        try:
            if kwargs.get("output_file") is not None:
                file_path_candidate = str(kwargs.get("output_file"))
                file_path = Path(file_path_candidate)
                if file_path.is_dir():
                    file_path = file_path.joinpath(f"cx_{str(uuid.uuid4())}.html")

                with open(str(file_path), "w") as render_file:
                    render_file.write(html_text)

        except Exception as e:
            raise RuntimeError(f"Cannot create output file: {e}")

        try:
            display(
                IFrame(
                    src=iframe_html,
                    width=iframe_width,
                    height=iframe_height,
                ),
            )

        except Exception as e:
            raise RuntimeError(f"Cannot create output cell: {e}")
