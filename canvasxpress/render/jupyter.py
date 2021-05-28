import uuid
from os import unlink
from time import sleep

from IPython.display import display, IFrame

from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.base import CXRenderable

_cx_html_template = """
<html>
    <head>
        <meta charset="UTF-8">
        <title>Flask CanvasXpress Example</title>
    </head>
    <body>
        <!-- 1. DOM element where the visualization will be displayed -->
        @canvas@

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
        <script type="text/javascript">
            onReady(function () {
                @code@
            })
        </script>
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
            cx: CanvasXpress
    ):
        """
        Initializes a new CXNoteBook object.
        :praram cx:
            The `CanvasXpress` object to be tracked.  See the `canvas`
            property, except that on initialization cx can be `None`.
        """
        super().__init__(cx)

    def render(self):
        """
        Renders the associated CanvasXpress object appropriate for display in
        an IPython (e.g., Jupyter NoteBook/Lab) environment.
        """
        html_parts: dict = self.canvas.render_to_html_parts()

        html = _cx_html_template \
            .replace("@canvas@", html_parts["cx_canvas"]) \
            .replace("@canvasxpress_license@", html_parts.get("cx_license", "")) \
            .replace("@code@", html_parts["cx_js"])

        temp_filename = f"temp_{str(uuid.uuid4())}.html"
        with open(temp_filename, "w") as temp_file:
            temp_file.write(html)

        display(
            IFrame(
                temp_filename,
                f"{self.canvas.element_width + 20}px",
                f"{self.canvas.element_height + 20}px"
            )
        )

        sleep(2)
        unlink(temp_filename)
