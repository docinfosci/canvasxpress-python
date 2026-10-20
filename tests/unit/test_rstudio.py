"""Tests for CanvasXpress HTML rendering (RStudio/HTML context)."""

import pytest

from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.rstudio import CXHtml


CX_EXAMPLE = CanvasXpress(
    render_to="rstudio-test-1",
    data={"y": {"data": [[1, 2, 3], [4, 5, 6]], "vars": ["A", "B"], "smps": ["s1", "s2", "s3"]}},
    config={"graphType": "Heatmap"},
)


class TestCxHtmlInit:
    """Test CXHtml.__init__ constructor."""

    def test_accepts_single_canvasxpress(self):
        html = CXHtml(CX_EXAMPLE)
        assert html.canvas == CX_EXAMPLE

    def test_accepts_list_of_canvasxpress(self):
        html = CXHtml([CX_EXAMPLE])
        # CXRenderable unwraps single-element lists to the single object
        assert html.canvas == CX_EXAMPLE

    def test_accepts_none(self):
        html = CXHtml(None)
        assert html.canvas is None

    def test_raises_for_non_canvasxpress(self):
        with pytest.raises(TypeError):
            CXHtml("not a chart")

    def test_raises_for_invalid_in_list(self):
        with pytest.raises(TypeError):
            CXHtml([CX_EXAMPLE, "bad"])


class TestCxHtmlRender:
    """Test CXHtml.render() method."""

    def test_render_returns_html_object(self):
        html = CXHtml(CX_EXAMPLE)
        result = html.render()
        # Returns IPython.display.HTML object
        assert hasattr(result, 'data') or hasattr(result, '_repr_html_')

    def test_render_html_contains_chart(self):
        html = CXHtml(CX_EXAMPLE)
        result = html.render()
        # The HTML should contain the CanvasXpress chart
        html_data = result.data if hasattr(result, 'data') else str(result)
        assert "CanvasXpress" in html_data or "canvasxpress" in html_data.lower()

    def test_render_with_none_canvas(self):
        html = CXHtml(None)
        result = html.render()
        # Should return HTML object even with None canvas
        assert hasattr(result, 'data') or hasattr(result, '_repr_html_')

    def test_render_with_multiple_charts(self):
        second = CanvasXpress(
            render_to="rstudio-test-2",
            data={"y": {"data": [[1, 2], [3, 4]]}},
        )
        html = CXHtml([CX_EXAMPLE, second])
        result = html.render()
        assert hasattr(result, 'data') or hasattr(result, '_repr_html_')

    def test_render_with_columns(self):
        html = CXHtml(CX_EXAMPLE)
        result = html.render(columns=2)
        assert hasattr(result, 'data') or hasattr(result, '_repr_html_')

    def test_render_with_debug(self):
        """Test that debug=True returns HTML and debug code."""
        html = CXHtml(CX_EXAMPLE)
        result = html.render(debug=True)
        # Returns HTML object
        assert hasattr(result, 'data') or hasattr(result, '_repr_html_')


class TestCxHtmlDisplayCanvasxpressHeader:
    """Test CXHtml.display_canvasxpress_header method."""

    def test_returns_html_string(self):
        html = CXHtml(CX_EXAMPLE)
        result = html.display_canvasxpress_header()
        assert isinstance(result, str)

    def test_header_contains_css(self):
        html = CXHtml(CX_EXAMPLE)
        result = html.display_canvasxpress_header()
        assert "stylesheet" in result.lower() or "css" in result.lower()

    def test_header_contains_js(self):
        html = CXHtml(CX_EXAMPLE)
        result = html.display_canvasxpress_header()
        assert "script" in result.lower() or "js" in result.lower()


class TestCxHtmlDisplayDebugCode:
    """Test CXHtml.display_debug_code method."""

    def test_display_debug_code_returns_prettified_html(self):
        html = CXHtml(CX_EXAMPLE)
        result = html.display_debug_code("<div><p>test</p></div>")
        assert isinstance(result, str)
        # BeautifulSoup prettify adds indentation
        assert "\n" in result or "  " in result

    def test_display_debug_code_handles_script_tags(self):
        html = CXHtml(CX_EXAMPLE)
        result = html.display_debug_code('<script>console.log("hello");</script>')
        assert isinstance(result, str)
        assert "script" in result.lower()


class TestCxHtmlGetChartDisplayCode:
    """Test CXHtml.get_chart_display_code method."""

    def test_single_chart(self):
        html = CXHtml(CX_EXAMPLE)
        code = html.get_chart_display_code(columns=1)
        assert isinstance(code, str)
        assert len(code) > 0

    def test_multiple_columns(self):
        html = CXHtml(CX_EXAMPLE)
        code = html.get_chart_display_code(columns=3)
        assert isinstance(code, str)

    def test_none_canvas_returns_empty_table(self):
        html = CXHtml(None)
        code = html.get_chart_display_code(columns=1)
        assert isinstance(code, str)
        assert "<table>" in code or code == ""


class TestCxHtmlDisplayCharts:
    """Test CXHtml.display_charts method."""

    def test_display_charts_returns_code(self):
        html = CXHtml(CX_EXAMPLE)
        code = '<div>test</div>'
        result = html.display_charts(code, output_file=None)
        assert result == code

    def test_display_charts_with_output_file(self, tmp_path):
        html = CXHtml(CX_EXAMPLE)
        code = '<div>test</div>'
        output_file = tmp_path / "test_output.html"
        result = html.display_charts(code, output_file=str(output_file))
        assert result == code
        assert output_file.exists()
        assert output_file.read_text() == code

    def test_display_charts_with_directory_output(self, tmp_path):
        html = CXHtml(CX_EXAMPLE)
        code = '<div>test</div>'
        result = html.display_charts(code, output_file=str(tmp_path))
        assert result == code
