from typing import Any

from canvasxpress.canvas import CanvasXpress
from canvasxpress.render import streamlit
from canvasxpress.render.dash import CXElementFactory
from canvasxpress.render.environment import (
    get_target_context,
    CONTEXT_RSTUDIO,
    CONTEXT_SHINY,
    CONTEXT_DASH,
    CONTEXT_JUPYTER,
    CONTEXT_STREAMLIT,
    CONTEXT_BROWSER,
)
from canvasxpress.render.jupyter import CXNoteBook
from canvasxpress.render.popup import CXBrowserPopup
from canvasxpress.render.shiny import CXShinyWidget


def show_in_browser(canvas: CanvasXpress) -> None:
    """
    Opens a browser and displays the canvas.
    """
    plotter = CXBrowserPopup(canvas)
    plotter.render()


def show(canvas: CanvasXpress) -> Any:
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
    context = get_target_context()

    if context == CONTEXT_RSTUDIO:
        plotter = CXShinyWidget(canvas)
        plotter._repr_rstudio_viewer_()

    elif context == CONTEXT_SHINY:
        plotter = CXShinyWidget(canvas)
        return plotter

    elif context == CONTEXT_DASH:
        plotter = CXElementFactory()
        return plotter.render(canvas)

    elif context == CONTEXT_JUPYTER:
        plotter = CXNoteBook(canvas)
        return plotter.render()

    elif context == CONTEXT_STREAMLIT:
        return streamlit.plot(canvas)

    elif context == CONTEXT_BROWSER:
        plotter = CXBrowserPopup(canvas)
        plotter.render()

    else:
        return """
        show() cannot identify the target context.  Either explicitly use a module from canvasxpress.render to 
        illustrate the CanvasXpress object, which requires the proper canvasxpress package option to be installed 
        (for example, pip install canvasxpress[shiny]) or set the environment variable CANVASXPRESS_TARGET_CONTEXT 
        to be one of rstudio, shiny, jupyter, streamlit, dash, or browser.
        """
