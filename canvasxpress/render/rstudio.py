import uuid
from pathlib import Path
from typing import Any, Union, List

import htmlmin
from IPython.display import HTML
from bs4 import BeautifulSoup

from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.base import CXRenderable

_cx_default_css_url = "https://www.canvasxpress.org/dist/canvasXpress.css"

_cx_versioned_css_url = (
    "https://cdnjs.cloudflare.com/ajax/libs/canvasXpress/@cx_version@/canvasXpress.css"
)

_cx_default_js_url = "https://www.canvasxpress.org/dist/canvasXpress.min.js"

_cx_versioned_js_url = "https://cdnjs.cloudflare.com/ajax/libs/canvasXpress/@cx_version@/canvasXpress.min.js"

_cx_intermixed_header = """
<html>
    <meta charset="UTF-8">
    <link 
        href='@css_url@' 
        rel='stylesheet' 
        type='text/css'
    />
    <script 
        src='@js_url@' 
        type='text/javascript'>
    </script>
</html>
"""

_cx_js_intermixed_template = """
<script type="text/javascript">
    @code@
</script>
"""

_cx_html_intermixed_template = """
<html>
    @canvasxpress_license@
    @canvases@
    @js_functions@
</html>
"""


class CXHtml(CXRenderable):
    """
    CXHtml is a `CXRenderable` that renders `CanvasXpress` objects into
    HTML Snippets suitable for use in RStudio
    """

    def __init__(self, *cx: Union[List[CanvasXpress], CanvasXpress, None]):
        """
        Initializes a new `CXHtml` object.
        :praram cx: `Union[List[CanvasXpress], CanvasXpress, None], ...`
            The `CanvasXpress` object(s) to be tracked.  See the `canvas`
            property, except that on initialization cx can be `None`.
            Multiple CanvasXpress objects are supported provided that
            they have distinct `render_to` targets.
        """
        super().__init__(*cx)

    def display_canvasxpress_header(self):
        css_url = _cx_default_css_url
        js_url = _cx_default_js_url
        if CanvasXpress.cdn_edition() is not None:
            css_url = _cx_versioned_css_url.replace(
                "@cx_version@", CanvasXpress.cdn_edition()
            )
            js_url = _cx_versioned_js_url.replace(
                "@cx_version@", CanvasXpress.cdn_edition()
            )

        header_html_text = _cx_intermixed_header.replace("@css_url@", css_url).replace(
            "@js_url@", js_url
        )

        return header_html_text

    def display_debug_code(self, code: str):
        minified_code = htmlmin.Minifier().minify(code)
        pretty_code = BeautifulSoup(minified_code, "html.parser").prettify()
        return pretty_code

    def get_chart_display_code(self, columns: int) -> str:
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
        if len(canvases) < columns:
            columns = len(canvases)

        functions = [part["cx_js"] for part in html_parts]

        cx_license = ""
        for part in html_parts:
            if part.get("cx_license"):
                cx_license = part["cx_license"]
                break

        canvas_table = "<table>"
        column_index = 0
        for chart_index in range(len(canvases)):
            if column_index == 0:
                canvas_table += "<tr>"

            canvas_table += '<td style="padding: 5px"><div>'
            canvas_table += canvases[chart_index]
            canvas_table += "</div></td>"

            column_index += 1
            if column_index == columns:
                column_index = 0
                canvas_table += "</tr>"

        canvas_table += "</table>"

        js_functions = "\n".join(
            [_cx_js_intermixed_template.replace("@code@", fx) for fx in functions]
        )
        html_text = (
            _cx_html_intermixed_template.replace("@canvases@", canvas_table)
            .replace("@canvasxpress_license@", cx_license)
            .replace("@js_functions@", js_functions)
        )

        return html_text

    def display_charts(self, code: str, output_file: str):
        try:
            if output_file is not None:
                file_path_candidate = str(output_file)
                file_path = Path(file_path_candidate)
                if file_path.is_dir():
                    file_path = file_path.joinpath(f"cx_{str(uuid.uuid4())}.html")

                with open(str(file_path), "w") as render_file:
                    render_file.write(code)

        except Exception as e:
            raise RuntimeError(f"Cannot create output file: {e}")

        return code

    def render(self, **kwargs: Any):
        """
        Renders the associated CanvasXpress object appropriate for display in
        a RStudio environment.  Charts cannot have the same name, so render_to
        will be updated with a uuid for each conflicting chart.
        :param kwargs: `Any`
            * Supports `columns` for any positive `int` of `1` or greater, with a
              default value of `1`.  Values less that `1` are ignored.  `columns`
              indicates how many charts should be rendered horizontally if more
              than one chart is being tracked.
            * Supports `output_file` as a string for a path at which the output
              should be saved.  If a file exists at the specified path then
              it will be overwritten.
            * Supports `debug` for displaying the output source.  True indicates
              that the HTML code shall be displayed prior to the parsed output.
              Default is False.
        """
        debug_output_arg = kwargs.get("debug")
        debug_output = bool(debug_output_arg) if debug_output_arg is not None else False

        columns_arg = int(kwargs.get("columns", 1))
        columns = columns_arg if columns_arg > 0 else 1

        output_file_arg = kwargs.get("output_file")
        output_file = (
            output_file_arg
            if output_file_arg is not None and isinstance(output_file_arg, str)
            else None
        )

        code = self.get_chart_display_code(columns)

        try:
            header = self.display_canvasxpress_header()
            body = self.display_charts(code, output_file)
            if debug_output:
                self.display_debug_code(code)

            return HTML(header + body)

        except Exception as e:
            raise RuntimeError(f"Cannot create output cell: {e}")
