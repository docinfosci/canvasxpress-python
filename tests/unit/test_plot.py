import json
import os
from unittest.mock import patch, MagicMock

import pytest

from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import (
    convert_to_reproducible_json,
    convert_from_reproducible_json,
    convert_to_image,
    show_in_browser,
    graph,
)


CX_SIMPLE = CanvasXpress(
    render_to="test_chart",
    data={
        "y": {
            "data": [[1, 2, 3], [4, 5, 6]],
            "vars": ["A", "B"],
            "smps": ["X", "Y", "Z"],
        }
    },
    config={"graphType": "Bar"},
)


def test_convert_to_reproducible_json_returns_string():
    """Test that convert_to_reproducible_json returns a valid JSON string."""
    result = convert_to_reproducible_json(CX_SIMPLE)
    assert isinstance(result, str)
    parsed = json.loads(result)
    assert "renderTo" in parsed
    assert parsed["renderTo"] == "test_chart"
    assert "data" in parsed
    assert "config" in parsed


def test_convert_to_reproducible_json_contains_data():
    """Test that the converted JSON contains the chart data."""
    result = convert_to_reproducible_json(CX_SIMPLE)
    parsed = json.loads(result)
    assert "y" in parsed["data"]
    assert parsed["data"]["y"]["vars"] == ["A", "B"]
    assert parsed["data"]["y"]["smps"] == ["X", "Y", "Z"]


def test_convert_to_reproducible_json_contains_config():
    """Test that the converted JSON contains the chart config."""
    result = convert_to_reproducible_json(CX_SIMPLE)
    parsed = json.loads(result)
    assert parsed["config"]["graphType"] == "Bar"


def test_convert_from_reproducible_json_valid():
    """Test that convert_from_reproducible_json creates a CanvasXpress object."""
    json_str = convert_to_reproducible_json(CX_SIMPLE)
    result = convert_from_reproducible_json(json_str)
    assert isinstance(result, CanvasXpress)
    assert result.render_to == "test_chart"


def test_convert_from_reproducible_json_invalid():
    """Test that convert_from_reproducible_json raises for invalid JSON."""
    with pytest.raises(ValueError):
        convert_from_reproducible_json("not valid json")


def test_convert_from_reproducible_json_empty():
    """Test that convert_from_reproducible_json raises for empty string."""
    with pytest.raises(ValueError):
        convert_from_reproducible_json("")


def test_convert_to_image_returns_none_when_no_nodejs():
    """Test that convert_to_image returns None when node.js is not available."""
    result = convert_to_image(CX_SIMPLE, type="png")
    assert result is None  # May be None if node.js not available


def test_convert_to_image_invalid_type():
    """Test that convert_to_image raises for invalid type."""
    with pytest.raises(ValueError):
        convert_to_image(CX_SIMPLE, type="invalid")


def test_show_in_browser_creates_popup(tmp_path):
    """Test that show_in_browser creates a CXBrowserPopup without errors."""
    with patch("canvasxpress.render.popup.webbrowser.open") as mock_open:
        show_in_browser(CX_SIMPLE)
        mock_open.assert_called_once()


def test_graph_raises_runtime_error_for_unknown_context():
    """Test that graph raises RuntimeError for unknown context."""
    with patch("canvasxpress.plot._g_context", None):
        with pytest.raises(RuntimeError) as exc_info:
            graph(CX_SIMPLE)
        assert "cannot identify the target context" in str(exc_info.value)


def test_graph_browser_context_with_kwargs(tmp_path):
    """Test that graph in browser context passes kwargs correctly."""
    with patch("canvasxpress.plot._g_context", "browser"):
        with patch("canvasxpress.render.popup.webbrowser.open") as mock_open:
            graph(CX_SIMPLE, debug=True)
            mock_open.assert_called_once()


def test_graph_dash_context():
    """Test that graph in dash context returns CXDashElement."""
    with patch("canvasxpress.plot._g_context", "dash"):
        with patch("canvasxpress.render.dash.CXElementFactory") as mock_factory:
            mock_instance = MagicMock()
            mock_factory.return_value = mock_instance
            mock_instance.render.return_value = "dash_element"
            result = graph(CX_SIMPLE)
            assert result == "dash_element"
            mock_instance.render.assert_called_once_with(CX_SIMPLE)


def test_graph_jupyter_context():
    """Test that graph in jupyter context calls display."""
    with patch("canvasxpress.plot._g_context", "jupyter"):
        with patch("canvasxpress.render.jupyter.CXNoteBook") as mock_notebook:
            mock_instance = MagicMock()
            mock_notebook.return_value = mock_instance
            mock_instance.render.return_value = "html_content"
            with patch("IPython.core.display_functions.display") as mock_display:
                graph(CX_SIMPLE)
                mock_display.assert_called_once()


def test_graph_streamlit_context():
    """Test that graph in streamlit context calls streamlit.plot."""
    with patch("canvasxpress.plot._g_context", "streamlit"):
        with patch("canvasxpress.render.streamlit.plot") as mock_plot:
            graph(CX_SIMPLE)
            mock_plot.assert_called_once_with(CX_SIMPLE)


def test_graph_shiny_context():
    """Test that graph in shiny context returns CXShinyWidget."""
    with patch("canvasxpress.plot._g_context", "shiny"):
        with patch("canvasxpress.render.shiny.CXShinyWidget") as mock_widget:
            mock_instance = MagicMock()
            mock_widget.return_value = mock_instance
            result = graph(CX_SIMPLE)
            assert result == mock_instance


def test_graph_rstudio_context():
    """Test that graph in rstudio context calls _repr_rstudio_viewer_."""
    with patch("canvasxpress.plot._g_context", "rstudio"):
        with patch("canvasxpress.render.shiny.CXShinyWidget") as mock_widget:
            mock_instance = MagicMock()
            mock_widget.return_value = mock_instance
            graph(CX_SIMPLE)
            mock_instance._repr_rstudio_viewer_.assert_called_once()
