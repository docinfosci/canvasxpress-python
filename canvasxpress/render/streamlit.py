import inspect
from pathlib import Path

import streamlit

from canvasxpress.canvas import CanvasXpress

cx_iframe_padding = 50
util_dir = Path(__file__).parent.parent / "util"


def load_template(filename: str) -> str:
    """
    Load a template file from the util directory.

    Args:
        filename: Name of the template file.

    Returns:
        The template file content as a string.
    """
    return (util_dir / filename).read_text()


cx_expand_override_js = load_template("streamlit_expand_override.js")
cx_chart_init_template = load_template("streamlit_chart_init.js")
cx_html_template = load_template("streamlit_html_template.html")


def get_chart_display_code(cx_chart: CanvasXpress) -> tuple:
    """
    Get the HTML display code and iframe dimensions for rendering a CanvasXpress
    object in a Streamlit application.

    Args:
        cx_chart: The CanvasXpress object to be rendered.

    Returns:
        Tuple of (cx_html, cx_iframe_width, cx_iframe_height) with HTML string and iframe
        dimensions in pixels.

    Raises:
        TypeError: If cx_chart is not a CanvasXpress object.
    """
    if cx_chart is None or not isinstance(cx_chart, CanvasXpress):
        raise TypeError("Argument 'cx_chart' is not a CanvasXpress object")

    html_parts = cx_chart.render_to_html_parts()
    canvases = html_parts["cx_canvas"]
    js_functions = cx_chart_init_template.replace("@code@", html_parts["cx_js"])
    js_functions = js_functions.replace("@cx_target_id@", cx_chart.render_to)

    cx_license_html = ""
    if html_parts.get("cx_license"):
        cx_license_html = html_parts["cx_license"]

    css_url = CanvasXpress.css_library_url()
    js_url = CanvasXpress.js_library_url()

    cx_html = (
        cx_html_template.replace("@canvases@", canvases)
        .replace("@canvasxpress_license@", cx_license_html)
        .replace("@js_functions@", js_functions)
        .replace("@css_url@", css_url)
        .replace("@js_url@", js_url)
        .replace("@expand_override@", cx_expand_override_js)
    )

    cx_iframe_width = cx_chart.width + cx_iframe_padding
    cx_iframe_height = cx_chart.height + cx_iframe_padding

    return cx_html, cx_iframe_width, cx_iframe_height


def render_with_streamlit_html(cx_html: str, cx_width: int, cx_height: int) -> bool:
    """
    Render HTML using streamlit.html with unsafe_allow_javascript.

    Args:
        cx_html: HTML string to render.
        cx_width: Width in pixels.
        cx_height: Height in pixels.

    Returns:
        True if rendering succeeded, False otherwise.
    """
    success = False

    if hasattr(streamlit, "html"):
        html_func = getattr(streamlit, "html")
        signature = inspect.signature(html_func)
        if "unsafe_allow_javascript" in signature.parameters:
            html_func(cx_html, unsafe_allow_javascript=True)
            success = True

    return success


def render_with_streamlit_iframe(cx_html: str, cx_width: int, cx_height: int) -> bool:
    """
    Render HTML using streamlit.iframe with data URL.

    Args:
        cx_html: HTML string to render.
        cx_width: Width in pixels.
        cx_height: Height in pixels.

    Returns:
        True if rendering succeeded, False otherwise.
    """
    success = False

    if hasattr(streamlit, "iframe"):
        import base64

        html_bytes = cx_html.encode("utf-8")
        b64 = base64.b64encode(html_bytes).decode("utf-8")
        data_url = f"data:text/html;base64,{b64}"

        streamlit.iframe(data_url, width=cx_width, height=cx_height)
        success = True

    return success


render_functions = (
    render_with_streamlit_html,
    render_with_streamlit_iframe,
)


def plot(cx_chart: CanvasXpress) -> None:
    """
    Renders the provided CanvasXpress object for display in a Streamlit application.

    Args:
        cx_chart: The CanvasXpress object to be rendered.

    Raises:
        TypeError: If cx_chart is not a CanvasXpress object.
    """
    result = None

    if cx_chart is None:
        result = None

    elif not isinstance(cx_chart, CanvasXpress):
        raise TypeError("Argument 'cx_chart' is not a CanvasXpress object")

    else:
        cx_html, cx_iframe_width, cx_iframe_height = get_chart_display_code(cx_chart)

        for render_function in render_functions:
            if render_function(cx_html, cx_iframe_width, cx_iframe_height):
                break

        result = None

    return result
