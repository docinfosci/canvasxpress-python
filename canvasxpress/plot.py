from typing import Any, Union

from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.environment import (
    get_target_context,
    CONTEXT_RSTUDIO,
    CONTEXT_SHINY,
    CONTEXT_DASH,
    CONTEXT_JUPYTER,
    CONTEXT_STREAMLIT,
    CONTEXT_BROWSER,
)
from canvasxpress.render.image import CXImage
from canvasxpress.render.json import CXJSON
from canvasxpress.render.popup import CXBrowserPopup

# Track the runtime context
_g_contexts_imported: list = []
_g_context = get_target_context()

# Pre-load Jupyter JS and CSS.
if _g_context == CONTEXT_JUPYTER:
    if not _g_context in _g_contexts_imported:
        from canvasxpress.render.jupyter import CXNoteBook

        CXNoteBook.display_canvasxpress_header()


def convert_from_reproducible_json(json: str) -> Union[None, CanvasXpress]:
    """
    Accepts a str with a reproducible JSON and returns a CanvasXpress object.
    """
    return CanvasXpress.from_reproducible_json(json)


def convert_to_reproducible_json(canvas: CanvasXpress) -> str:
    """
    Converts the CanvasXpress object into a reproducible JSON string.
    """
    return CXJSON.render_to_json(canvas)


def convert_to_image(canvas: CanvasXpress, type: str = "png") -> Union[None, bytes]:
    """
    Converts the CanvasXpress object to an image of the specified type.
    """
    converter = CXImage(canvas)
    candidates = converter.render(format=type)
    for conversion in candidates:
        if conversion.get("image", {}).get("format") == type:
            return conversion.get("image", {}).get("binary")


def show_in_browser(canvas: CanvasXpress) -> None:
    """
    Opens a browser and displays the canvas.
    """
    plotter = CXBrowserPopup(canvas)
    plotter.render()


def graph(canvas: CanvasXpress) -> Any:
    """
    Displays the CanvasXpress object as a visualized chart in a manner appropriate to the running context.

    To override an assumed context the ENV variable `CANVASXPRESS_TARGET_CONTEXT` can be set to one of the following
    values, in which case `show` will attempt to illustrate the chart of the set target.

    - rstudio
    - shiny
    - jupyter
    - dash
    - streamlit
    - browser

    :returns: An `object` or `None` depending on the target context.  In the case of `browser` a popup browser will
        be launched.`
    """
    if _g_context == CONTEXT_RSTUDIO:
        if not _g_context in _g_contexts_imported:
            from canvasxpress.render.shiny import CXShinyWidget

        plotter = CXShinyWidget(canvas)
        plotter._repr_rstudio_viewer_()

    elif _g_context == CONTEXT_SHINY:
        if not _g_context in _g_contexts_imported:
            from canvasxpress.render.shiny import CXShinyWidget

        plotter = CXShinyWidget(canvas)
        return plotter

    elif _g_context == CONTEXT_DASH:
        if not _g_context in _g_contexts_imported:
            from canvasxpress.render.dash import CXElementFactory

        plotter = CXElementFactory()
        return plotter.render(canvas)

    elif _g_context == CONTEXT_JUPYTER:
        if not _g_context in _g_contexts_imported:
            from canvasxpress.render.jupyter import CXNoteBook

        plotter = CXNoteBook(canvas)
        return plotter.render()

    elif _g_context == CONTEXT_STREAMLIT:
        if not _g_context in _g_contexts_imported:
            from canvasxpress.render import streamlit

        streamlit.plot(canvas)

    elif _g_context == CONTEXT_BROWSER:
        plotter = CXBrowserPopup(canvas)
        plotter.render()

    else:
        return """
        show() cannot identify the target context.  Either explicitly use a module from canvasxpress.render to 
        illustrate the CanvasXpress object, which requires the proper canvasxpress package option to be installed 
        (for example, pip install canvasxpress[shiny]) or set the environment variable CANVASXPRESS_TARGET_CONTEXT 
        to be one of rstudio, shiny, jupyter, streamlit, dash, or browser.
        """
