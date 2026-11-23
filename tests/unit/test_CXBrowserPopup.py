from unittest.mock import patch

from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.context import temp_directory
from canvasxpress.render.popup import CXBrowserPopup

CX_SIMPLE = CanvasXpress(
    render_to="popup_test",
    data={
        "y": {
            "data": [[1, 2, 3]],
            "vars": ["A"],
            "smps": ["X", "Y", "Z"],
        }
    },
    config={"graphType": "Bar"},
)


CX_SECOND = CanvasXpress(
    render_to="popup_test_2",
    data={
        "y": {
            "data": [[4, 5, 6]],
            "vars": ["B"],
            "smps": ["X", "Y", "Z"],
        }
    },
    config={"graphType": "Line"},
)


def test_cx_browser_popup_init_single():
    """Test CXBrowserPopup initialization with a single canvas."""
    popup = CXBrowserPopup(CX_SIMPLE)
    assert popup.canvas == CX_SIMPLE


def test_cx_browser_popup_init_multiple():
    """Test CXBrowserPopup initialization with multiple canvases."""
    popup = CXBrowserPopup(CX_SIMPLE, CX_SECOND)
    assert isinstance(popup.canvas, list)
    assert len(popup.canvas) == 2


def test_cx_browser_popup_init_none():
    """Test CXBrowserPopup initialization with None."""
    popup = CXBrowserPopup(None)
    assert popup.canvas is None


def test_cx_browser_popup_init_list():
    """Test CXBrowserPopup initialization with a list of canvases."""
    popup = CXBrowserPopup([CX_SIMPLE, CX_SECOND])
    assert isinstance(popup.canvas, list)


def test_cx_browser_popup_render_creates_html_file(tmp_path):
    """Test that render creates an HTML file in temp directory."""
    popup = CXBrowserPopup(CX_SIMPLE)

    with patch("canvasxpress.render.popup.webbrowser.open") as mock_open:
        popup.render()

    mock_open.assert_called_once()
    call_arg = mock_open.call_args[0][0]
    assert "file://" in call_arg
    assert ".html" in call_arg


def test_cx_browser_popup_render_handles_duplicate_render_to(tmp_path):
    """Test that render handles duplicate render_to values."""
    cx1 = CanvasXpress(
        render_to="same_id",
        data={"y": {"data": [[1]], "vars": ["A"], "smps": ["X"]}},
    )
    cx2 = CanvasXpress(
        render_to="same_id",
        data={"y": {"data": [[2]], "vars": ["B"], "smps": ["X"]}},
    )
    popup = CXBrowserPopup([cx1, cx2])

    with patch("canvasxpress.render.popup.webbrowser.open") as mock_open:
        popup.render()

    mock_open.assert_called_once()


def test_cx_browser_popup_render_with_columns(tmp_path):
    """Test that render respects the columns parameter."""
    cx1 = CanvasXpress(
        render_to="c1",
        data={"y": {"data": [[1]], "vars": ["A"], "smps": ["X"]}},
        width=200,
    )
    cx2 = CanvasXpress(
        render_to="c2",
        data={"y": {"data": [[2]], "vars": ["B"], "smps": ["X"]}},
        width=200,
    )
    popup = CXBrowserPopup([cx1, cx2])

    with patch("canvasxpress.render.popup.webbrowser.open") as mock_open:
        popup.render(columns=2)

    mock_open.assert_called_once()


def test_cx_browser_popup_render_with_zero_columns(tmp_path):
    """Test that render handles zero or negative columns."""
    popup = CXBrowserPopup(CX_SIMPLE)

    with patch("canvasxpress.render.popup.webbrowser.open") as mock_open:
        popup.render(columns=0)

    mock_open.assert_called_once()


def test_cx_browser_popup_render_with_negative_columns(tmp_path):
    """Test that render handles negative columns."""
    popup = CXBrowserPopup(CX_SIMPLE)

    with patch("canvasxpress.render.popup.webbrowser.open") as mock_open:
        popup.render(columns=-5)

    mock_open.assert_called_once()


def test_cx_browser_popup_render_single_no_copy(tmp_path):
    """Test that single canvas render doesn't modify original."""
    popup = CXBrowserPopup(CX_SIMPLE)
    original_id = CX_SIMPLE.render_to

    with patch("canvasxpress.render.popup.webbrowser.open"):
        popup.render()

    assert CX_SIMPLE.render_to == original_id


def test_cx_browser_popup_html_contains_expected_elements(tmp_path):
    """Test that rendered HTML contains expected elements."""
    popup = CXBrowserPopup(CX_SIMPLE)

    with patch("canvasxpress.render.popup.webbrowser.open") as mock_open:
        popup.render()

    mock_open.assert_called_once()
    call_args = mock_open.call_args[0][0]
    assert "file://" in call_args
    assert ".html" in call_args


def test_cx_browser_popup_render_license_handling(tmp_path):
    """Test that render handles license properly."""
    cx_with_license = CanvasXpress(
        render_to="licensed",
        data={"y": {"data": [[1]], "vars": ["A"], "smps": ["X"]}},
    )
    popup = CXBrowserPopup(cx_with_license)

    with patch("canvasxpress.render.popup.webbrowser.open") as mock_open:
        popup.render()

    mock_open.assert_called_once()


def test_cx_browser_popup_writes_page_that_survives_render():
    """The page stays on disk for the browser and holds every chart in order."""
    popup = CXBrowserPopup(CX_SIMPLE, CX_SECOND)

    with patch("canvasxpress.render.popup.webbrowser.open") as mock_open:
        page_path = popup.render(columns=2)

    url = mock_open.call_args[0][0]
    assert url.startswith("file://")
    assert url.endswith(page_path.name)
    assert page_path.exists()

    page = page_path.read_text(encoding="utf-8")
    page_path.unlink()
    assert page_path.parent == temp_directory()
    assert page_path.name == "popup_test_popup_test_2.html"
    assert page.startswith("<!DOCTYPE html>")
    assert CanvasXpress.js_library_url() in page
    assert "repeat(2, max-content)" in page
    assert page.index('id="popup_test"') < page.index('id="popup_test_2"')


def test_cx_browser_popup_rendering_again_replaces_page():
    """Rendering the same charts again reuses their page instead of adding one."""
    with patch("canvasxpress.render.popup.webbrowser.open"):
        first = CXBrowserPopup(CX_SIMPLE).render()
        second = CXBrowserPopup(CX_SIMPLE).render()

    second.unlink()
    assert first == second
    assert first.name == "popup_test.html"


def test_cx_browser_popup_anonymous_chart_page():
    """An anonymous chart's page is called anonymous.html, not a random ID."""
    chart = CanvasXpress(data={"y": {"data": [[1]], "vars": ["A"], "smps": ["X"]}})

    with patch("canvasxpress.render.popup.webbrowser.open"):
        page_path = CXBrowserPopup(chart).render()

    page_path.unlink()
    assert page_path.name == "anonymous.html"


def test_cx_browser_popup_fill():
    """The page has the charts follow the window in the dimensions asked for."""
    with patch("canvasxpress.render.popup.webbrowser.open"):
        fixed = CXBrowserPopup(CX_SIMPLE).render().read_text(encoding="utf-8")
        wide = CXBrowserPopup(CX_SIMPLE).render(fill_to_width=True)
        wide_page = wide.read_text(encoding="utf-8")
        tall = CXBrowserPopup(CX_SIMPLE).render(fill_to_height=True)
        tall_page = tall.read_text(encoding="utf-8")

    tall.unlink()
    assert "fillContainer(" not in fixed
    assert '"fillToWidth": true, "fillToHeight": false' in wide_page
    assert "html, body { height: 100%" not in wide_page
    assert '"fillToWidth": false, "fillToHeight": true' in tall_page
    assert "html, body { height: 100%" in tall_page
