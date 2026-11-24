from typing import Any, Union

from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.environment import (
    CONTEXT_BROWSER,
    CONTEXT_DASH,
    CONTEXT_JUPYTER,
    CONTEXT_RSTUDIO,
    CONTEXT_SHINY,
    CONTEXT_STREAMLIT,
    CONTEXT_UNKNOWN,
    get_target_context,
)
from canvasxpress.render.image import CXImage
from canvasxpress.render.json import CXJSON
from canvasxpress.render.popup import CXBrowserPopup

# Track the runtime context
_g_context = get_target_context()


def convert_from_reproducible_json(json: str) -> Union[None, CanvasXpress]:
    """Accepts a str with a reproducible JSON and returns a CanvasXpress object.

    Args:
        json: `str` A valid reproducible research JSON string.

    Returns:
        `Union[None, CanvasXpress]`: A CanvasXpress object constructed from
        the JSON, or None if the JSON is invalid.
    """
    return CanvasXpress.from_reproducible_json(json)


def convert_to_reproducible_json(canvas: CanvasXpress) -> str:
    """Converts the CanvasXpress object into a reproducible JSON string.

    Args:
        canvas: `CanvasXpress` The CanvasXpress object to convert.

    Returns:
        `str`: A reproducible JSON string representation of the canvas.
    """
    return CXJSON.render_to_json(canvas)


def convert_to_image(canvas: CanvasXpress, type: str = "png") -> Union[None, bytes]:
    """Converts the CanvasXpress object to an image of the specified type.

    Args:
        canvas: `CanvasXpress` The CanvasXpress object to convert.
        type: `str` The image format (e.g., 'png', 'jpg'). Defaults to 'png'.

    Returns:
        `Union[None, bytes]`: The image binary data, or None if conversion
        fails.
    """
    converter = CXImage(canvas)
    candidates = converter.render(format=type)
    for conversion in candidates:
        if conversion.get("image", {}).get("format") == type:
            return conversion.get("image", {}).get("binary")


def show_in_browser(canvas: CanvasXpress) -> None:
    """Opens a browser and displays the canvas.

    Args:
        canvas: `CanvasXpress` The CanvasXpress object to display.
    """
    plotter = CXBrowserPopup(canvas)
    plotter.render()


def graph(
    canvas: CanvasXpress,
    debug: bool = False,
    fill_to_width: bool = False,
    fill_to_height: bool = False,
    **kwargs: Any,
) -> Any:
    """Displays the CanvasXpress object as a visualized chart in a manner
    appropriate to the running context.

    To override an assumed context the ENV variable
    `CANVASXPRESS_TARGET_CONTEXT` can be set to one of the following values,
    in which case `graph` will attempt to illustrate the chart of the set
    target.

    - rstudio
    - shiny
    - jupyter
    - dash
    - streamlit
    - browser

    By default a chart is drawn at the `width` and `height` it was configured
    with. `fill_to_width` and `fill_to_height` instead size the chart to the
    element that holds it, such as a notebook output area, a Streamlit or Dash
    column, a Shiny card, the RStudio viewer pane or the browser window, and
    redraw it whenever that element is resized, including when a sidebar or
    expander changes the layout without the window resizing. Each dimension is
    chosen separately; one that is not filled keeps its configured size, and a
    filled one starts at its configured size until the container is measured.

    - `fill_to_width` follows the container's width. Almost every container has
      a width to give, so this works wherever the chart is placed.
    - `fill_to_height` follows the container's height. Most containers take
      their height from their content, which leaves no height to fill, so it
      only has an effect where the container's height is set by the layout:
      the browser window (`browser` and the RStudio viewer), a Streamlit
      `st.container(height=...)`, a Dash element with a fixed or flex height, or
      a fillable Shiny card. Elsewhere, such as a notebook output, the chart
      keeps its configured height rather than growing.

    This is provided by the canvasxpress package for live Python framework
    contexts and is separate from CanvasXpress's own `resizable` setting, which
    lets a user resize a chart by dragging it. Leave both off for a chart that
    must keep its size, such as one drawn wider than its container to be
    scrolled.

    Args:
        canvas: `CanvasXpress` The CanvasXpress object to display.
        debug: `bool` Whether to enable debug mode. Defaults to False.
        fill_to_width: `bool` Whether the chart follows the width of its
            container as it is resized, rather than keeping the width it was
            configured with. Defaults to False.
        fill_to_height: `bool` Whether the chart follows the height of its
            container as it is resized, rather than keeping the height it was
            configured with. Only has an effect where the container's height is
            set by the layout rather than by its content. Defaults to False.
        **kwargs: Additional keyword arguments passed to the renderer.

    Returns:
        `Any`: An object or None depending on the target context. In the
        case of `browser` a popup browser will be launched.
    """
    # A Dash app can only be detected once it exists, which is usually after this
    # module is imported. At import such an app is then seen as unknown, or as
    # Streamlit when Streamlit is merely installed, so detect again for those.
    _context = _g_context
    if _context in (CONTEXT_UNKNOWN, CONTEXT_STREAMLIT):
        _context = get_target_context()

    if _context == CONTEXT_RSTUDIO:
        from canvasxpress.render.shiny import CXShinyWidget

        plotter = CXShinyWidget(
            canvas, fill_to_width=fill_to_width, fill_to_height=fill_to_height
        )
        plotter._repr_rstudio_viewer_()

    elif _context == CONTEXT_SHINY:
        from canvasxpress.render.shiny import CXShinyWidget

        plotter = CXShinyWidget(
            canvas, fill_to_width=fill_to_width, fill_to_height=fill_to_height
        )
        return plotter

    elif _context == CONTEXT_DASH:
        from canvasxpress.render.dash import CXElementFactory

        plotter = CXElementFactory()
        return plotter.render(
            canvas, fill_to_width=fill_to_width, fill_to_height=fill_to_height
        )

    elif _context == CONTEXT_JUPYTER:
        from IPython.core.display_functions import display

        from canvasxpress.render.jupyter import CXNoteBook

        plotter = CXNoteBook(canvas)
        content = plotter.render(
            debug=debug,
            fill_to_width=fill_to_width,
            fill_to_height=fill_to_height,
            **kwargs,
        )
        if isinstance(content, list):
            for element in content:
                display(element)
        else:
            display(content)

    elif _context == CONTEXT_STREAMLIT:
        from canvasxpress.render import streamlit

        streamlit.plot(
            canvas,
            key=kwargs.get("key"),
            fill_to_width=fill_to_width,
            fill_to_height=fill_to_height,
        )

    elif _context == CONTEXT_BROWSER:
        plotter = CXBrowserPopup(canvas)
        plotter.render(
            fill_to_width=fill_to_width, fill_to_height=fill_to_height, **kwargs
        )

    else:
        raise RuntimeError(
            "show() cannot identify the target context. Either explicitly use a module "
            "from canvasxpress.render to illustrate the CanvasXpress object, which requires "
            "the proper canvasxpress package option to be installed (for example, pip install "
            "canvasxpress[shiny]) or set the environment variable CANVASXPRESS_TARGET_CONTEXT "
            "to be one of rstudio, shiny, jupyter, streamlit, dash, or browser."
        )
