import os
import subprocess
import json
from typing import Any, Union, List
from tempfile import gettempdir
from pathlib import Path

from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.base import CXRenderable
from canvasxpress.render.json import CXJSON

PNG_IMAGE: str = "png"
SVG_IMAGE: str = "svg"


def install_cx_in_nodejs() -> None:
    """
    Installs the canvasxpress-cli NodeJS package if it is not available.
    """
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


def nodejs_modules_path() -> Path:
    """
    Returns the path to the NodeJS' modules installation.
    :returns: `str`
        The path for the NodeJS' modules installation.
    """
    install_cx_in_nodejs()
    search_path = Path(os.path.abspath(__file__)).parent
    while search_path != "":
        test_path = Path(search_path, "node_modules")
        if test_path.exists():
            return test_path
        else:
            if search_path == search_path.root:
                raise RuntimeError("node_modules is not available.")
            else:
                search_path = search_path.parent


def render_html_as_image(url: str) -> list:
    """
    Renders a Web page with CanvasXpress chart declarations into one image per chart.
    :param url: `str`
        The URL to the HTML.  Can be file:// or http[s]://.
    :param format: `str`
        A `str` or list indicating whether PNG or SVG images should be produced.
    :returns: `list`
        A `list[dict]` of image data, if any.
    """
    formats = format if isinstance(format, list) else [format]

    rendered_images: list = []
    for image_format in formats:
        if image_format not in [PNG_IMAGE, SVG_IMAGE]:
            raise ValueError(
                "format must be one of PNG_IMAGE or SVG_IMAGE, or a list of each."
            )

        work_dir = Path(gettempdir()) / "canvasxpress-python"
        work_dir.mkdir(exist_ok=True)
        work_image_path = work_dir

        result = subprocess.run(
            [
                f"{CX_NODEJS_PATH} {image_format} -i {url} -o {work_image_path}",
            ],
            shell=True,
            capture_output=True,
        )
        if result.returncode == 0:

            image_file_options = list(work_image_path.glob(f"**/*.{image_format}"))
            for image_file_path in image_file_options:
                with open(Path(image_file_path), "rb") as image_file:
                    image: bytes = image_file.read()
                image_file_path.unlink()
                rendered_images.append(
                    {
                        "id": url,
                        "image": {
                            "binary": image,
                            "format": image_format,
                        },
                    }
                )

    return rendered_images


CX_NODEJS_PATH: Path = nodejs_modules_path() / "canvasxpress-cli/bin/canvasxpress"


class CXImage(CXRenderable):
    """
    CXPng is a `CXRenderable` that renders `CanvasXpress` objects into PNG images without the need for a Web session
    at the client code level.  NodeJS must be installed in the system, and the Python process must have permission
    to interact with NodeJS.
    """

    def __init__(self, *cx: Union[List[CanvasXpress], CanvasXpress, None]):
        """
        Initializes a new `CXNoteBook` object.
        :param cx: `Union[List[CanvasXpress], CanvasXpress, None], ...`
            The `CanvasXpress` object(s) to be tracked.  See the `canvas`
            property, except that on initialization cx can be `None`.
            Multiple CanvasXpress objects are supported provided that
            they have distinct `render_to` targets.
        """
        super().__init__(*cx)

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

            for reproducible_json in reproducible_jsons:
                work_dir = Path(gettempdir()) / "canvasxpress-python"
                work_dir.mkdir(exist_ok=True)
                work_json_path = Path(work_dir, "cx_data.json")
                work_image_path = work_dir

                with open(work_json_path, "w") as json_temp_file:
                    json_temp_file.write(reproducible_json)

                result = subprocess.run(
                    [
                        f"{CX_NODEJS_PATH} {image_format} -i {work_json_path} -o {work_image_path}",
                    ],
                    shell=True,
                    capture_output=True,
                )
                work_json_path.unlink()
                if result.returncode == 0:

                    image_file_options = list(
                        work_image_path.glob(f"**/*.{image_format}")
                    )
                    for image_file_path in image_file_options:
                        with open(Path(image_file_path), "rb") as image_file:
                            image: bytes = image_file.read()
                        image_file_path.unlink()
                        rendered_images.append(
                            {
                                "id": json.loads(reproducible_json).get(
                                    "renderTo", "anonymous"
                                ),
                                "image": {
                                    "binary": image,
                                    "format": image_format,
                                },
                            }
                        )

        return rendered_images
