from typing import Any

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
from canvasxpress.render.popup import CXBrowserPopup


def show_in_browser(canvas: CanvasXpress) -> None:
    """
    Opens a browser and displays the canvas.
    """
    plotter = CXBrowserPopup(canvas)
    plotter.render()


_contexts_imported: list = []


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
    context = get_target_context()

    if context == CONTEXT_RSTUDIO:
        if not context in _contexts_imported:
            from canvasxpress.render.shiny import CXShinyWidget

        plotter = CXShinyWidget(canvas)
        plotter._repr_rstudio_viewer_()

    elif context == CONTEXT_SHINY:
        if not context in _contexts_imported:
            from canvasxpress.render.shiny import CXShinyWidget

        plotter = CXShinyWidget(canvas)
        return plotter

    elif context == CONTEXT_DASH:
        if not context in _contexts_imported:
            from canvasxpress.render.dash import CXElementFactory

        plotter = CXElementFactory()
        return plotter.render(canvas)

    elif context == CONTEXT_JUPYTER:
        if not context in _contexts_imported:
            from canvasxpress.render.jupyter import CXNoteBook

        plotter = CXNoteBook(canvas)
        return plotter.render()

    elif context == CONTEXT_STREAMLIT:
        if not context in _contexts_imported:
            from canvasxpress.render import streamlit

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
