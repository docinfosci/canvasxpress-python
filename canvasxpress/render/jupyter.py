import uuid
from pathlib import Path
from typing import Any, Union, List

import minify_html
from IPython.display import display, HTML, Javascript, Code
from bs4 import BeautifulSoup

from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.base import CXRenderable

_cx_iframe_padding = 50

_cx_js_intermixed_template = """
// 1. First, handle CSS Insertion and wait for it to be completely ready
new Promise((cssResolve, cssReject) => {
    const cssUrl = "{{css_url}}";
    let existingLink = document.querySelector(`head link[href="${cssUrl}"]`);

    if (!existingLink) {
        const link = document.createElement("link");
        link.rel = "stylesheet";
        link.type = "text/css";
        link.href = cssUrl;
        link.onload = () => {
            link.dataset.state = "loaded";
            link.dispatchEvent(new Event("assetLoaded"));
            cssResolve();
        };
        link.onerror = () => {
            link.dataset.state = "failed";
            link.dispatchEvent(new Event("assetFailed"));
            cssReject(new Error(`Failed to load CSS: ${cssUrl}`));
        };
        document.head.appendChild(link);
    } else if (existingLink.dataset.state === "loaded") {
        cssResolve();
    } else if (existingLink.dataset.state === "failed") {
        cssReject(new Error(`Failed to load CSS: ${cssUrl}`));
    } else {
        // Safe queueing for subsequent runs initiated while CSS is downloading
        existingLink.addEventListener('assetLoaded', () => cssResolve(), { once: true });
        existingLink.addEventListener('assetFailed', () => cssReject(new Error(`Failed to load CSS: ${cssUrl}`)), { once: true });
    }
})
.then(() => {
    // 2. CSS is guaranteed ready. Now handle JS Insertion
    return new Promise((jsResolve, jsReject) => {
        const scriptUrl = '{{js_url}}';
        let existingScript = document.querySelector(`script[src="${scriptUrl}"]`);

        if (existingScript) {
            if (existingScript.dataset.state === "loaded") {
                jsResolve();
            } else if (existingScript.dataset.state === "failed") {
                jsReject(new Error(`Failed to load script: ${scriptUrl}`));
            } else {
                // Safe queueing for subsequent runs initiated while JS is downloading
                existingScript.addEventListener('assetLoaded', () => jsResolve(), { once: true });
                existingScript.addEventListener('assetFailed', () => jsReject(new Error(`Failed to load script: ${scriptUrl}`)), { once: true });
            }
        } else {
            const script = document.createElement("script");
            script.type = "text/javascript";
            script.src = scriptUrl;
            script.dataset.state = "loading";

            script.onload = () => {
                script.dataset.state = "loaded";
                script.dispatchEvent(new Event("assetLoaded"));
                jsResolve();
            };
            script.onerror = () => {
                script.dataset.state = "failed";
                script.dispatchEvent(new Event("assetFailed"));
                jsReject(new Error(`Failed to load script: ${scriptUrl}`));
            };
            document.head.appendChild(script);
        }
    });
})
.then(() => { 
    // 3. Both CSS and JS are ready in order. Run user payload.
    {{code}} 
})
.catch((error) => {
    console.error("CanvasXpress injection failed:", error);
});

"""


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

    def display_debug_code(self, code: str):
        minified_code = minify_html.minify(
            code,
            minify_js=True,
            minify_css=True,
            remove_processing_instructions=True,
        )

        pretty_code = BeautifulSoup(minified_code, "html.parser").prettify()
        return Code(
            data=pretty_code,
            language="javascript",
        )

    def get_chart_display_code(self, columns: int) -> list:
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

        canvas_table = f'\n<div style="display: grid; grid-template-columns: repeat({columns}, 1fr); gap: 10px; width: 100%;">'

        for canvas in reversed(canvases):
            canvas_table += f"\n  <div>{canvas}</div>"

        canvas_table += "\n</div>"

        content: list = [
            HTML(data=cx_license),
            HTML(data=canvas_table),
        ]

        for fx in functions:
            content.append(
                Javascript(
                    data=(
                        _cx_js_intermixed_template.replace("{{code}}", fx)
                        .replace("{{css_url}}", CanvasXpress.css_library_url())
                        .replace("{{js_url}}", CanvasXpress.js_library_url())
                        .replace("@id@", str(uuid.uuid4()))
                        .replace("-", "")
                    ),
                ),
            )

        return content

    def display_charts(self, code: str, output_file: str):
        try:
            if output_file is not None:
                file_path_candidate = str(output_file)
                file_path = Path(file_path_candidate)
                if file_path.is_dir():
                    file_path = file_path.joinpath(f"cx_{str(uuid.uuid4())}.html")

                with open(str(file_path), "w") as render_file:
                    render_file.write(
                        """
                        <html>
                        <body>
                        """
                    )
                    for element in code:
                        render_file.write(str(element))
                    render_file.write(
                        """
                        </body>
                        </html>
                        """
                    )

        except Exception as e:
            return HTML("<div>Cannot create output file: {e}</div>")

        return code

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
            * Supports `debug` for displaying the output source.  True indicates
              that the HTML code shall be displayed prior to the parsed output.
              Default is False.
        """
        try:
            debug_output_arg = kwargs.get("debug")
            debug_output = (
                bool(debug_output_arg) if debug_output_arg is not None else False
            )

            columns_arg = int(kwargs.get("columns", 1))
            columns = columns_arg if columns_arg > 0 else 1

            output_file_arg = kwargs.get("output_file")
            output_file = (
                output_file_arg
                if output_file_arg is not None and isinstance(output_file_arg, str)
                else None
            )

            code = self.get_chart_display_code(columns)

            if debug_output:
                return self.display_debug_code(code)
            else:
                return self.display_charts(code, output_file)

        except Exception as e:
            return HTML(f"<div>Cannot create output cell: {e}</div>")
