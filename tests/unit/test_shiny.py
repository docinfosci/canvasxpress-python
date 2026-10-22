"""Tests for CanvasXpress Shiny integration."""

from unittest.mock import MagicMock, patch

import pytest

from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.shiny import output_canvasxpress, CXShinyWidget


CX_EXAMPLE = CanvasXpress(
    render_to="shiny-test-1",
    data={"y": {"data": [[1, 2, 3], [4, 5, 6]], "vars": ["A", "B"], "smps": ["s1", "s2", "s3"]}},
    config={"graphType": "Bar"},
)


class TestOutputCanvasXpress:
    """Test output_canvasxpress function."""

    def test_raises_for_none(self):
        with pytest.raises(ValueError):
            output_canvasxpress(None)

    def test_raises_for_invalid_type(self):
        with pytest.raises(TypeError):
            output_canvasxpress(123)

    def test_accepts_string_id(self):
        result = output_canvasxpress("my_output")
        assert result is not None

    def test_returns_taglist_with_css_js(self):
        result = output_canvasxpress("my_output")
        # Should be a ui.TagList containing head_content and output_ui
        assert hasattr(result, '__iter__')


class TestCxShinyWidget:
    """Test CXShinyWidget class."""

    def test_accepts_canvasxpress(self):
        widget = CXShinyWidget(CX_EXAMPLE)
        assert widget._canvas == CX_EXAMPLE

    def test_raises_for_none(self):
        with pytest.raises(ValueError):
            CXShinyWidget(None)

    def test_raises_for_invalid_type(self):
        with pytest.raises(TypeError):
            CXShinyWidget("not a chart")

    def test_repr_html_returns_string(self):
        """Test _repr_html_ returns an HTML string."""
        widget = CXShinyWidget(CX_EXAMPLE)
        html = widget._repr_html_()
        assert isinstance(html, str)
        assert len(html) > 0
        # Should contain CanvasXpress chart elements
        assert "canvasxpress" in html.lower() or "CanvasXpress" in html
