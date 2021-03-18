import uuid
from os import unlink
from time import sleep

from IPython.display import display, IFrame

from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.base import CXRenderable


class CXNoteBook(CXRenderable):

    def __init__(
            self,
            cx: CanvasXpress
    ):
        super().__init__(cx)

    def render(self):
        """
        Renders the provided CanvasXpress object appropriate for display in
        an IPython (e.g., Jupyter NoteBook/Lab) environment.
        :param cx: A valid CanvasXpress object.
        """
        html_parts: dict = self.canvas.render_to_html_parts()

        html_template = \
            """
            @canvas@                  
            <link href='https://www.canvasxpress.org/dist/canvasXpress.css' rel='stylesheet' type='text/css'/>
            <script src='https://www.canvasxpress.org/dist/canvasXpress.min.js' type='text/javascript'></script>
            <script type="text/javascript">
                onReady(function () {
                    @code@
                })
            </script>
            """

        html = html_template \
            .replace("@canvas@", html_parts["cx_canvas"]) \
            .replace("@code@", html_parts["cx_js"])

        temp_filename = f"temp_{str(uuid.uuid4())}.html"
        with open(temp_filename, "w") as temp_file:
            temp_file.write(html)

        display(
            IFrame(
                temp_filename,
                self.canvas.width + 10,
                self.canvas.height + 10
            ),
            metadata=dict(isolated=True)
        )

        sleep(1)
        unlink(temp_filename)
