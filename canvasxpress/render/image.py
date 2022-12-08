import os
import base64
import subprocess
from typing import Any, Union, List
from tempfile import gettempdir, NamedTemporaryFile

from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.base import CXRenderable
from canvasxpress.render.json import CXJSON

PNG_IMAGE: str = "png"
SVG_IMAGE: str = "svg"


class CXImage(CXRenderable):
    """
    CXPng is a `CXRenderable` that renders `CanvasXpress` objects into PNG images without the need for a Web session
    at the client code level.  NodeJS must be installed in the system, and the Python process must have permission
    to interact with NodeJS.
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
        CXImage.install_cx_in_nodejs()

    @classmethod
    def install_cx_in_nodejs(cls):
        availability_status = subprocess.run(
            ["npm", "ls", "canvasxpress-cli"], capture_output=True
        )
        if availability_status.returncode != 0:
            installation_status = subprocess.run(
                ["npm", "install", "canvasxpress-cli", "--save"], capture_output=True
            )
            if installation_status.returncode != 0:
                raise RuntimeError(
                    f"Image rendering is unavailable. "
                    f"Cannot install canvasxpress NodeJS package: {installation_status.stderr.decode('utf-8')}"
                )

    def render(self, **kwargs: Any) -> list:
        """
        Renders the associated CanvasXpress object appropriate to create PNGs.
        :param kwargs: `Any`
            * `format`: Accepts a `str` or `list[str]` with the values `png`, or `svg`.  Each tracked CanvasXpress
              object will be rendered into the specified image formats.  If not provided, then `png` is assumed.
        :returns: `list{dict}`
            A list `dict`, each containing a PNGs or SVG and the `render_to` ID of the corresponding CanvasXpress.
        """
        format_arg = kwargs.get("format", [PNG_IMAGE])
        formats = format_arg if isinstance(format_arg, list) else [format_arg]

        json_renderer = CXJSON(self.canvas)
        reproducible_jsons = json_renderer.render()

        rendered_images: list = []

        for image_format in formats:
            if image_format not in [PNG_IMAGE, SVG_IMAGE]:
                raise ValueError(
                    "format must be one of PNG_IMAGE or SVG_IMAGE, or a list of each."
                )

            for json in reproducible_jsons:
                work_dir = "." # gettempdir()
                work_json_path = os.path.join(work_dir, "cx_data.json")
                work_image_path = os.path.join(work_dir, f"cx_image.{image_format}")

                with open(work_json_path, "w") as json_temp_file:
                    json_temp_file.write(json)

                result = subprocess.run(
                    [
                        "npx",
                        "canvasxpress",
                        image_format,
                        "-i",
                        work_json_path,
                        "-o",
                        work_image_path,
                    ],
                    shell=True,
                    capture_output=True,
                )
                if result.returncode == 0:

                    with open(work_image_path, "rb") as image_file:
                        image = base64.b64encode(image_file.read())

                    rendered_images.append(
                        {
                            "id": json.loads(json).get("render_to", "anonymous"),
                            "image_base64": image,
                        }
                    )

                    os.remove(work_image_path)

                os.remove(work_json_path)

        return reproducible_jsons
