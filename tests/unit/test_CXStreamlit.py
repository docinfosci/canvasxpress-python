import json
import pytest
import inspect

from canvasxpress.canvas import CanvasXpress
from canvasxpress.config.collection import CXConfigs
from canvasxpress.config.type import CXGraphType
from canvasxpress.render.streamlit import (
    get_chart_display_code,
    render_with_streamlit_html,
    render_with_streamlit_iframe,
    render_functions,
    plot,
)

# Example chart for testing
# https://www.canvasxpress.org/examples/bar-1.html
cx_example = CanvasXpress(
    render_to="bar1",
    data={
        "y": {
            "data": [[4, 5, 4, 4, 7]],
            "smps": ["Cat 1", "Cat 2", "Cat 3", "Cat 4", "Cat 5"],
            "vars": ["Var 1"],
        }
    },
    config={
        "graphOrientation": "vertical",
        "graphType": "Bar",
        "showLegend": False,
        "smpTextRotate": 90,
        "smpTitle": "Categories",
        "title": "Bar graph with a single series",
        "xAxis": ["Var 1"],
        "xAxisTitle": "Var 1",
    },
)


def test_CXStreamlit_get_chart_display_code_valid_input():
    """
    Test that get_chart_display_code returns valid HTML and dimensions for a valid chart.
    """
    cx_html, cx_iframe_width, cx_iframe_height = get_chart_display_code(
        cx_chart=cx_example
    )

    assert isinstance(cx_html, str)
    assert isinstance(cx_iframe_width, int)
    assert isinstance(cx_iframe_height, int)

    # Check that all template placeholders have been replaced
    assert "@" not in cx_html


def test_CXStreamlit_get_chart_display_code_invalid_input():
    """
    Test that get_chart_display_code raises TypeError for invalid input.
    """
    for sample in [1, "1", [12, 13], 4.5]:
        with pytest.raises(TypeError) as exc_info:
            get_chart_display_code(cx_chart=sample)
        assert "not a CanvasXpress object" in str(exc_info.value)


def test_CXStreamlit_get_chart_display_code_none_input():
    """
    Test that get_chart_display_code raises TypeError for None input.
    """
    with pytest.raises(TypeError) as exc_info:
        get_chart_display_code(cx_chart=None)
    assert "not a CanvasXpress object" in str(exc_info.value)


def test_CXStreamlit_html_contains_canvas_element():
    """
    Test that the generated HTML contains the canvas element with correct ID.
    """
    cx_html, cx_iframe_width, cx_iframe_height = get_chart_display_code(
        cx_chart=cx_example
    )
    assert 'id="bar1"' in cx_html
    assert "<canvas" in cx_html


def test_CXStreamlit_html_contains_canvasxpress_libraries():
    """
    Test that the generated HTML includes CanvasXpress CSS and JS library references.
    """
    cx_html, cx_iframe_width, cx_iframe_height = get_chart_display_code(
        cx_chart=cx_example
    )
    assert "canvasXpress.css" in cx_html
    assert "canvasXpress.min.js" in cx_html


def test_CXStreamlit_html_contains_chart_initialization():
    """
    Test that the generated HTML contains the chart initialization JavaScript.
    """
    cx_html, cx_iframe_width, cx_iframe_height = get_chart_display_code(
        cx_chart=cx_example
    )
    assert "new CanvasXpress" in cx_html
    assert "renderTo" in cx_html
    assert "bar1" in cx_html


def test_CXStreamlit_html_contains_expand_override():
    """
    Test that the generated HTML includes the expand override JavaScript.
    """
    cx_html, cx_iframe_width, cx_iframe_height = get_chart_display_code(
        cx_chart=cx_example
    )
    assert "initExpand" in cx_html
    assert "CanvasXpress.prototype.expand" in cx_html


def test_CXStreamlit_expand_override_creates_popup():
    """
    Test that the expand override JavaScript opens a popup window with reproducible JSON.
    """
    cx_html, cx_iframe_width, cx_iframe_height = get_chart_display_code(
        cx_chart=cx_example
    )

    # Check expand override has window.open for popup
    assert "window.open" in cx_html
    assert "_blank" in cx_html
    assert "getReproducibleJSON" in cx_html
    assert "JSON.stringify" in cx_html


def test_CXStreamlit_expand_override_popup_has_toolbar():
    """
    Test that the expand popup window preserves toolbar configuration.
    """
    cx_html, cx_iframe_width, cx_iframe_height = get_chart_display_code(
        cx_chart=cx_example
    )
    assert "showToolbar" in cx_html
    assert "showToolbar = true" in cx_html


def test_CXStreamlit_expand_override_chart_container():
    """
    Test that the expand popup has a chart container div for click-to-close.
    """
    cx_html, cx_iframe_width, cx_iframe_height = get_chart_display_code(
        cx_chart=cx_example
    )
    assert "chartContainer" in cx_html


def test_CXStreamlit_iframe_dimensions_include_padding():
    """
    Test that iframe dimensions include the padding.
    """
    cx_html, cx_iframe_width, cx_iframe_height = get_chart_display_code(
        cx_chart=cx_example
    )

    expected_width = 500 + 50
    expected_height = 500 + 50

    assert cx_iframe_width == expected_width
    assert cx_iframe_height == expected_height


def test_CXStreamlit_plot_valid_chart():
    """
    Test that plot returns None for a valid chart (no exception).
    """
    result = plot(cx_chart=cx_example)
    assert result is None


def test_CXStreamlit_plot_invalid_chart():
    """
    Test that plot raises TypeError for invalid chart argument.
    """
    with pytest.raises(TypeError, match="not a CanvasXpress object"):
        plot(cx_chart="abc")


def test_CXStreamlit_plot_none_chart():
    """
    Test that plot returns None for None chart argument.
    """
    assert plot(cx_chart=None) is None


def test_CXStreamlit_html_structure_complete():
    """
    Test that the generated HTML has all required structural elements.
    """
    cx_html, cx_iframe_width, cx_iframe_height = get_chart_display_code(
        cx_chart=cx_example
    )

    required_elements = [
        "canvasXpress.css",
        "canvasXpress.min.js",
        "<canvas",
        "new CanvasXpress",
        "initExpand",
        "initChart",
        "cx_initialized_",
    ]

    for element in required_elements:
        assert element in cx_html, f"Missing required element: {element}"


def test_CXStreamlit_custom_render_to_preserved():
    """
    Test that custom render_to ID is preserved in HTML output.
    """
    custom_chart = CanvasXpress(
        render_to="my_custom_chart",
        data={"y": {"vars": ["A"], "smps": ["S1"], "data": [[1]]}},
        config={"graphType": "Bar"},
    )

    cx_html, cx_iframe_width, cx_iframe_height = get_chart_display_code(
        cx_chart=custom_chart
    )
    assert 'id="my_custom_chart"' in cx_html
    assert "my_custom_chart" in cx_html


def test_CXStreamlit_different_charts_produce_different_html():
    """
    Test that different charts produce different HTML.
    """
    chart1 = CanvasXpress(
        render_to="chart1",
        data={"y": {"vars": ["A"], "smps": ["S1"], "data": [[1]]}},
        config={"graphType": "Bar"},
    )
    chart2 = CanvasXpress(
        render_to="chart2",
        data={"y": {"vars": ["B"], "smps": ["S1"], "data": [[2]]}},
        config={"graphType": "Line"},
    )

    html1, width1, height1 = get_chart_display_code(cx_chart=chart1)
    html2, width2, height2 = get_chart_display_code(cx_chart=chart2)

    assert html1 != html2


def test_CXStreamlit_expand_override_debug_logging():
    """
    Test that expand override includes debug console logging.
    """
    cx_html, cx_iframe_width, cx_iframe_height = get_chart_display_code(
        cx_chart=cx_example
    )
    assert "console.log" in cx_html
    assert "Expand button clicked" in cx_html


def test_CXStreamlit_expand_override_popup_focus():
    """
    Test that expand popup focuses the window for key capture.
    """
    cx_html, cx_iframe_width, cx_iframe_height = get_chart_display_code(
        cx_chart=cx_example
    )
    assert "window.focus()" in cx_html
    assert "popup.focus()" in cx_html


def test_CXStreamlit_init_chart_polling():
    """
    Test that chart initialization polls for CanvasXpress availability.
    """
    cx_html, cx_iframe_width, cx_iframe_height = get_chart_display_code(
        cx_chart=cx_example
    )
    assert "setTimeout(initChart, 50)" in cx_html


def test_CXStreamlit_expand_override_resize_handler():
    """
    Test that expand popup includes resize handler for responsive chart.
    """
    cx_html, cx_iframe_width, cx_iframe_height = get_chart_display_code(
        cx_chart=cx_example
    )
    assert "addEventListener" in cx_html
    assert "resize" in cx_html
    assert "setDimensions" in cx_html
    assert "window.innerWidth" in cx_html
    assert "window.innerHeight" in cx_html


def test_CXStreamlit_multiple_charts_independent():
    """
    Test that multiple charts get independent initialization guards.
    """
    chart1 = CanvasXpress(
        render_to="chart1",
        data={"y": {"vars": ["A"], "smps": ["S1"], "data": [[1]]}},
        config={"graphType": "Bar"},
    )
    chart2 = CanvasXpress(
        render_to="chart2",
        data={"y": {"vars": ["B"], "smps": ["S1"], "data": [[2]]}},
        config={"graphType": "Line"},
    )

    html1, width1, height1 = get_chart_display_code(cx_chart=chart1)
    html2, width2, height2 = get_chart_display_code(cx_chart=chart2)

    assert "chart1" in html1
    assert "chart2" in html2
    assert 'globalKey = "cx_initialized_" + chartId' in html1
    assert 'globalKey = "cx_initialized_" + chartId' in html2
    assert "chart1" in html1
    assert "chart2" in html2


def test_CXStreamlit_get_chart_display_code_returns_tuple():
    """
    Test that get_chart_display_code returns a tuple of (html, width, height).
    """
    result = get_chart_display_code(cx_chart=cx_example)

    assert isinstance(result, tuple)
    assert len(result) == 3

    cx_html, cx_iframe_width, cx_iframe_height = result
    assert isinstance(cx_html, str)
    assert isinstance(cx_iframe_width, int)
    assert isinstance(cx_iframe_height, int)


def test_CXStreamlit_plot_none_returns_none():
    """
    Test that plot with None returns None.
    """
    assert plot(cx_chart=None) is None


def test_CXStreamlit_render_with_streamlit_html_signature():
    """
    Test that render_with_streamlit_html has correct signature.
    """
    signature = inspect.signature(render_with_streamlit_html)
    params = list(signature.parameters.keys())
    assert params == ["cx_html", "cx_width", "cx_height"]


def test_CXStreamlit_render_with_streamlit_iframe_signature():
    """
    Test that render_with_streamlit_iframe has correct signature.
    """
    signature = inspect.signature(render_with_streamlit_iframe)
    params = list(signature.parameters.keys())
    assert params == ["cx_html", "cx_width", "cx_height"]
