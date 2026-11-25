"""Tests for CanvasXpress Shiny integration."""

import sys
import types
from unittest.mock import MagicMock, patch

import pytest

from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.shiny import (
    CXShinyWidget,
    _as_fill_item,
    output_canvasxpress,
)

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

    def test_repr_html_uses_page_library_and_includes_license(self):
        chart = CanvasXpress(render_to="shiny_licensed", data={"y": {"data": [[1]]}})
        chart.license_url = "https://example.org/CanvasXpressLicense.js"
        html = CXShinyWidget(chart)._repr_html_()
        assert "https://example.org/CanvasXpressLicense.js" in html
        assert CanvasXpress.js_library_url() not in html
        assert 'id="shiny_licensed"' in html


class TestCxShinyWidgetFill:
    def test_off_by_default(self):
        html = CXShinyWidget(CX_EXAMPLE)._repr_html_()
        assert "fillContainer(" not in html
        assert "html-fill-item" not in html

    def test_fill_to_width(self):
        html = CXShinyWidget(CX_EXAMPLE, fill_to_width=True)._repr_html_()
        assert "grid-template-columns: repeat(1, minmax(0, 1fr))" in html
        assert '"fillToWidth": true, "fillToHeight": false' in html
        assert "html-fill-item" not in html

    def test_fill_to_height_fills_a_fillable_container(self):
        html = CXShinyWidget(CX_EXAMPLE, fill_to_height=True)._repr_html_()
        assert '"fillToWidth": false, "fillToHeight": true' in html
        assert "html-fill-item" in html

    def test_output_fill(self):
        assert "html-fill-item" not in str(output_canvasxpress("plain"))
        filled = str(output_canvasxpress("filled", fill=True))
        assert "html-fill-item" in filled
        assert "html-fill-container" in filled


class TestAsFillItem:
    def test_uses_shiny_fill_when_available(self):
        from shiny import ui

        result = _as_fill_item(ui.div("hi"))
        assert "html-fill-item" in str(result)

    def test_fallback_when_shiny_has_no_fill(self, monkeypatch):
        from shiny import ui

        monkeypatch.setattr(ui, "fill", None, raising=False)
        result = _as_fill_item(ui.div("hi"))
        assert result.attrs["style"] == "height: 100%;"


class TestCxShinyWidgetRStudioViewer:
    def test_raises_without_rpy2(self):
        with patch.dict(sys.modules, {"rpy2": None, "rpy2.robjects": None}):
            with pytest.raises(RuntimeError, match="rpy2"):
                CXShinyWidget(CX_EXAMPLE)._repr_rstudio_viewer_()

    def test_opens_page_in_rstudio_viewers(self):
        fake_robjects = MagicMock()
        fake_rpy2 = types.ModuleType("rpy2")
        fake_rpy2.robjects = fake_robjects

        with patch.dict(
            sys.modules, {"rpy2": fake_rpy2, "rpy2.robjects": fake_robjects}
        ):
            CXShinyWidget(CX_EXAMPLE)._repr_rstudio_viewer_()

        fake_robjects.r.assert_called_once()
