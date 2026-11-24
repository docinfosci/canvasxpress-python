"""Tests for the shared HTML/CSS/JS layer in canvasxpress.render.context."""

import json
import os
import tempfile
from pathlib import Path

import pytest

import canvasxpress
from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.context import (
    ANONYMOUS_NAME,
    FILL_JS,
    LIBRARY_LOADER,
    LIBRARY_MODES,
    LIBRARY_NONE,
    LIBRARY_TAGS,
    LOADER_JS,
    MAX_FILE_STEM,
    CXChartAssets,
    CXHtmlDocument,
    CXLibraryAssets,
    escape_script,
    fill_container_js,
    fill_options,
    page_file_name,
    script_element,
    temp_directory,
    write_html_file,
)

LICENSE_URL = "https://example.org/CanvasXpressLicense.js"


def _chart(render_to=None, width=500, height=500, **kwargs) -> CanvasXpress:
    return CanvasXpress(
        render_to=render_to,
        data={"y": {"vars": ["V1"], "smps": ["S1", "S2"], "data": [[1, 2]]}},
        config={"graphType": "Bar"},
        width=width,
        height=height,
        **kwargs,
    )


def _licensed_chart(render_to="licensed") -> CanvasXpress:
    chart = _chart(render_to)
    chart.license_url = LICENSE_URL
    return chart


class TestScriptHelpers:
    def test_escape_script_breaks_closing_tags(self):
        assert escape_script('var s = "</script><b>";') == 'var s = "<\\/script><b>";'
        assert escape_script("x = '</SCRIPT>'") == "x = '<\\/SCRIPT>'"

    def test_escape_script_leaves_other_code(self):
        code = "if (a < b) { c = '</div>'; }"
        assert escape_script(code) == code

    def test_script_element_wraps_escaped_code(self):
        html = script_element('"</script>"')
        assert html.startswith('<script type="text/javascript">')
        assert html.endswith("</script>")
        assert html.count("</script>") == 1


class TestLibraryAssets:
    def test_current_uses_canvasxpress_configuration(self):
        library = CXLibraryAssets.current()
        assert library.js_url == CanvasXpress.js_library_url()
        assert library.css_url == CanvasXpress.css_library_url()
        assert library.license_url is None

    def test_current_follows_cdn_edition(self):
        CanvasXpress.set_cdn_edition("48.3")
        try:
            assert "/48.3/" in CXLibraryAssets.current().js_url
        finally:
            CanvasXpress.set_cdn_edition(None)

    def test_tags_order_stylesheet_license_library(self):
        library = CXLibraryAssets("https://x/cx.js", "https://x/cx.css", LICENSE_URL)
        tags = library.tags()
        assert tags.index("cx.css") < tags.index(LICENSE_URL) < tags.index("cx.js")
        assert 'referrerpolicy="origin-when-cross-origin"' in tags

    def test_tags_without_license(self):
        library = CXLibraryAssets("https://x/cx.js", "https://x/cx.css")
        assert library.license_tag() == ""
        assert len(library.tags().splitlines()) == 2

    def test_urls_are_attribute_escaped(self):
        library = CXLibraryAssets('https://x/cx.js?a="1"&b=2', "https://x/cx.css")
        assert 'src="https://x/cx.js?a=&quot;1&quot;&amp;b=2"' in library.library_tag()

    def test_loader_js_loads_library_then_runs_code(self):
        library = CXLibraryAssets("https://x/cx.js", "https://x/cx.css", LICENSE_URL)
        js = library.loader_js("drawCharts();")
        assert js.startswith(LOADER_JS)
        expected = json.dumps(
            {
                "jsUrl": "https://x/cx.js",
                "cssUrl": "https://x/cx.css",
                "licenseUrl": LICENSE_URL,
            }
        )
        assert f"window.canvasxpress.loadLibrary({expected})" in js
        assert js.index("loadLibrary(") < js.index("drawCharts();")

    def test_loader_resource_defines_load_library(self):
        assert "namespace.loadLibrary = loadLibrary" in LOADER_JS

    def test_equality(self):
        assert CXLibraryAssets("a", "b") == CXLibraryAssets("a", "b")
        assert CXLibraryAssets("a", "b") != CXLibraryAssets("a", "b", LICENSE_URL)


class TestChartAssets:
    def test_from_canvas_named_chart(self):
        chart = CXChartAssets.from_canvas(_chart("my_chart", width=400, height=300))
        assert chart.target_id == "my_chart"
        assert 'id="my_chart"' in chart.canvas
        assert '"renderTo": "my_chart"' in chart.js
        assert (chart.width, chart.height) == (400, 300)
        assert chart.license_url is None

    def test_from_canvas_anonymous_chart_has_one_id(self):
        chart = CXChartAssets.from_canvas(_chart())
        assert chart.target_id.startswith("cX")
        assert f'id="{chart.target_id}"' in chart.canvas
        assert f'"renderTo": "{chart.target_id}"' in chart.js

    def test_from_canvas_target_id_does_not_change_chart(self):
        original = _chart("my_chart")
        chart = CXChartAssets.from_canvas(original, target_id="other")
        assert chart.target_id == "other"
        assert original.render_to == "my_chart"

    def test_from_canvas_license(self):
        assert CXChartAssets.from_canvas(_licensed_chart()).license_url == LICENSE_URL

    def test_from_canvas_rejects_other_types(self):
        with pytest.raises(TypeError):
            CXChartAssets.from_canvas("not a chart")

    def test_from_canvases_none_and_single(self):
        assert CXChartAssets.from_canvases(None) == []
        assert len(CXChartAssets.from_canvases(_chart("one"))) == 1

    def test_from_canvases_makes_ids_unique_without_changing_charts(self):
        first, second = _chart("same"), _chart("same")
        charts = CXChartAssets.from_canvases([first, second])
        assert charts[0].target_id == "same"
        assert charts[1].target_id.startswith("same_")
        assert first.render_to == second.render_to == "same"

    def test_from_canvases_compares_rendered_ids(self):
        # render_to drops "-", so both charts render as "ab".
        charts = CXChartAssets.from_canvases([_chart("a-b"), _chart("ab")])
        assert charts[0].target_id != charts[1].target_id

    def test_from_canvases_rejects_other_types(self):
        with pytest.raises(TypeError):
            CXChartAssets.from_canvases([_chart("one"), "bad"])


class TestHtmlDocument:
    def test_empty_document(self):
        document = CXHtmlDocument()
        assert document.charts == []
        assert document.layout_html() == ""
        assert document.fragment(LIBRARY_TAGS) == ""
        assert document.loader_js() == ""
        assert document.size == (0, 0)
        assert "<body>" in document.page()

    def test_columns_are_bounded(self):
        charts = [_chart(f"c{i}") for i in range(3)]
        assert CXHtmlDocument(charts, columns=0).columns == 1
        assert CXHtmlDocument(charts, columns=-2).columns == 1
        assert CXHtmlDocument(charts, columns=2).columns == 2
        assert CXHtmlDocument(charts, columns=10).columns == 3

    def test_rows_keep_chart_order(self):
        document = CXHtmlDocument([_chart(f"c{i}") for i in range(5)], columns=2)
        assert [[c.target_id for c in row] for row in document.rows()] == [
            ["c0", "c1"],
            ["c2", "c3"],
            ["c4"],
        ]

    def test_layout_is_a_grid_in_chart_order(self):
        document = CXHtmlDocument([_chart("first"), _chart("second")], columns=2, gap=7)
        layout = document.layout_html()
        assert "grid-template-columns: repeat(2, max-content)" in layout
        assert "gap: 7px" in layout
        assert layout.index('id="first"') < layout.index('id="second"')

    def test_size(self):
        document = CXHtmlDocument(
            [
                _chart("a", width=100, height=50),
                _chart("b", width=200, height=80),
                _chart("c", width=150, height=60),
            ],
            columns=2,
            gap=10,
        )
        assert document.size == (310, 150)

    def test_license_comes_from_first_licensed_chart(self):
        document = CXHtmlDocument([_chart("plain"), _licensed_chart()])
        assert document.library.license_url == LICENSE_URL

    def test_explicit_library(self):
        library = CXLibraryAssets("https://x/cx.js", "https://x/cx.css")
        document = CXHtmlDocument(_licensed_chart(), library=library)
        assert document.library is library

    def test_fragment_library_none(self):
        html = CXHtmlDocument(_licensed_chart()).fragment(LIBRARY_NONE)
        assert LICENSE_URL in html
        assert CanvasXpress.js_library_url() not in html
        assert "new CanvasXpress(" in html

    def test_fragment_library_tags(self):
        html = CXHtmlDocument(_chart("tagged")).fragment(LIBRARY_TAGS)
        assert html.index(CanvasXpress.js_library_url()) < html.index('id="tagged"')
        assert html.index('id="tagged"') < html.index("new CanvasXpress(")

    def test_fragment_library_loader(self):
        html = CXHtmlDocument(_chart("loaded")).fragment(LIBRARY_LOADER)
        assert f'src="{CanvasXpress.js_library_url()}"' not in html
        assert "window.canvasxpress.loadLibrary(" in html
        assert html.index('id="loaded"') < html.index("loadLibrary(")

    def test_fragment_rejects_unknown_mode(self):
        with pytest.raises(ValueError):
            CXHtmlDocument(_chart("x")).fragment("bogus")

    def test_chart_js_isolates_charts(self):
        js = CXHtmlDocument([_chart("one"), _chart("two")]).chart_js()
        assert 'console.error("CanvasXpress chart one failed:", error);' in js
        assert 'console.error("CanvasXpress chart two failed:", error);' in js

    def test_page(self):
        page = CXHtmlDocument([_chart("p1"), _chart("p2")], title="A & B").page()
        assert page.startswith("<!DOCTYPE html>")
        assert "<title>A &amp; B</title>" in page
        head, body = page.split("<body>")
        assert f'src="{CanvasXpress.js_library_url()}"' in head
        assert body.index('id="p1"') < body.index('id="p2"')
        assert body.index('id="p2"') < body.index("new CanvasXpress(")
        assert "@" not in page

    def test_page_escapes_script_end_in_data(self):
        chart = CanvasXpress(
            render_to="tricky",
            data={"y": {"vars": ["</script><b>x"], "smps": ["S1"], "data": [[1]]}},
        )
        page = CXHtmlDocument(chart).page()
        assert "</script><b>" not in page
        assert "<\\/script><b>x" in page


class TestFill:
    def test_off_by_default(self):
        document = CXHtmlDocument([_chart("one"), _chart("two")], columns=2)
        assert (document.fill_to_width, document.fill_to_height) == (False, False)
        assert document.fills is False
        layout = document.layout_html()
        assert "max-content" in layout
        assert "grid-template-rows" not in layout
        assert "fillContainer" not in document.page()
        assert "fillContainer" not in document.loader_js()

    def test_cells_are_identified_by_chart(self):
        layout = CXHtmlDocument([_chart("one"), _chart("one")]).layout_html()
        assert 'data-canvasxpress-cell="one"' in layout
        assert layout.count("data-canvasxpress-cell=") == 2

    def test_width_shares_full_width_between_columns(self):
        layout = CXHtmlDocument(
            [_chart("one"), _chart("two")], columns=2, fill_to_width=True
        ).layout_html()
        assert "grid-template-columns: repeat(2, minmax(0, 1fr))" in layout
        assert "width: 100%" in layout
        assert "max-content" not in layout
        assert "grid-template-rows" not in layout
        assert "height: 100%" not in layout

    def test_height_shares_full_height_between_rows(self):
        layout = CXHtmlDocument(
            [_chart(f"c{i}") for i in range(3)], columns=2, fill_to_height=True
        ).layout_html()
        assert "grid-template-rows: repeat(2, minmax(0, 1fr))" in layout
        assert "height: 100%" in layout
        assert "grid-template-columns: repeat(2, max-content)" in layout
        assert "width: 100%" not in layout

    def test_fill_options(self):
        assert fill_options(400, 300, True, False) == {
            "fillToWidth": True,
            "fillToHeight": False,
            "width": 400,
            "height": 300,
        }

    def test_fill_container_js(self):
        options = json.dumps(fill_options(400, 300, False, True))
        assert fill_container_js("my_chart", 400, 300, False, True) == (
            "window.canvasxpress.fillContainer("
            'document.querySelector("[data-canvasxpress-cell=\\"my_chart\\"]"), '
            f'"my_chart", {options});'
        )

    @pytest.mark.parametrize(
        "fill_to_width, fill_to_height", [(True, False), (False, True), (True, True)]
    )
    def test_page_defines_fill_then_fills_each_chart_after_creating_it(
        self, fill_to_width, fill_to_height
    ):
        page = CXHtmlDocument(
            [_chart("one", width=400, height=200), _chart("two", height=300)],
            fill_to_width=fill_to_width,
            fill_to_height=fill_to_height,
        ).page()
        body = page.split("<body>")[1]
        assert body.index("namespace.fillContainer = fillContainer") < body.index(
            "new CanvasXpress("
        )
        assert page.count("namespace.fillContainer = fillContainer") == 1
        for target_id, width, height in [("one", 400, 200), ("two", 500, 300)]:
            call = fill_container_js(
                target_id, width, height, fill_to_width, fill_to_height
            )
            assert call in body
            assert body.index(f'"renderTo": "{target_id}"') < body.index(call)

    def test_page_takes_window_height_only_when_filling_height(self):
        assert (
            "html, body { height: 100%"
            not in CXHtmlDocument(_chart("one"), fill_to_width=True).page()
        )
        page = CXHtmlDocument(_chart("one"), fill_to_height=True).page()
        head = page.split("<body>")[0]
        assert "html, body { height: 100%; margin: 0; }" in head

    def test_fills_duplicate_charts_by_their_unique_ids(self):
        document = CXHtmlDocument([_chart("same"), _chart("same")], fill_to_width=True)
        page = document.page()
        for chart in document.charts:
            assert f'data-canvasxpress-cell="{chart.target_id}"' in page
            assert fill_container_js(chart.target_id, 500, 500, True, False) in page

    def test_loader_and_fragments_include_fill(self):
        document = CXHtmlDocument(_chart("one"), fill_to_height=True)
        call = fill_container_js("one", 500, 500, False, True)

        js = document.loader_js()
        assert js.index("loadLibrary(") < js.index(FILL_JS) < js.index(call)
        for mode in LIBRARY_MODES:
            assert call in document.fragment(mode)

    def test_size_is_configured_size(self):
        document = CXHtmlDocument(
            _chart("one", width=400, height=300),
            fill_to_width=True,
            fill_to_height=True,
        )
        assert document.size == (400, 300)

    def test_fill_resource(self):
        assert "namespace.fillContainer = fillContainer" in FILL_JS
        assert "ResizeObserver" in FILL_JS
        assert "setDimensions(width, height)" in FILL_JS
        assert "options.fillToWidth" in FILL_JS
        assert "options.fillToHeight" in FILL_JS
        assert '"canvasxpress:resize"' in FILL_JS


class TestPageFileName:
    def test_named_and_anonymous_charts(self):
        assert page_file_name(["scatter"]) == "scatter.html"
        assert page_file_name([None]) == "anonymous.html"
        assert page_file_name([]) == "anonymous.html"

    def test_charts_are_joined_in_order(self):
        assert page_file_name(["scatter", "heatmap"]) == "scatter_heatmap.html"
        assert page_file_name(["scatter", None]) == "scatter_anonymous.html"

    def test_unsafe_characters_are_removed(self):
        assert page_file_name(["a/b\\c:d"]) == "abcd.html"
        assert page_file_name(["../"]) == "anonymous.html"
        assert page_file_name(["grafico_é"]) == "grafico_é.html"

    def test_long_names_are_shortened_and_kept_distinct(self):
        first = page_file_name(["a" * 60, "b" * 60])
        second = page_file_name(["a" * 60, "c" * 60])
        assert len(first) == MAX_FILE_STEM + len(".html")
        assert first.startswith("a" * 60 + "_")
        assert first != second

    def test_windows_device_names_are_avoided(self):
        assert page_file_name(["con"]) == "con_chart.html"
        assert page_file_name(["LPT1"]) == "LPT1_chart.html"
        assert page_file_name(["console"]) == "console.html"


class TestDocumentFileName:
    def test_uses_original_chart_names(self):
        document = CXHtmlDocument([_chart("same"), _chart("same"), _chart()])
        assert document.charts[1].target_id != "same"
        assert document.file_name == "same_same_anonymous.html"

    def test_anonymous_chart_name_is_stable(self):
        assert CXHtmlDocument(_chart()).file_name == "anonymous.html"
        assert CXHtmlDocument(_chart()).file_name == "anonymous.html"

    def test_chart_assets_name(self):
        assert CXChartAssets.from_canvas(_chart("named"), "other").name == "named"
        assert CXChartAssets.from_canvas(_chart()).name == ANONYMOUS_NAME


class TestTempDirectory:
    def test_is_private_folder_in_system_temp(self):
        directory = temp_directory()
        assert directory.is_dir()
        assert directory.parent == Path(tempfile.gettempdir())
        assert directory.name.startswith("canvasxpress-python")
        assert temp_directory() == directory

    def test_is_outside_the_package(self):
        package = Path(canvasxpress.__file__).parent.resolve()
        assert package not in temp_directory().resolve().parents

    @pytest.mark.skipif(not hasattr(os, "getuid"), reason="POSIX permissions only")
    def test_shared_folder_is_not_used(self, tmp_path, monkeypatch):
        monkeypatch.setattr(tempfile, "gettempdir", lambda: str(tmp_path))
        shared = temp_directory()
        shared.chmod(0o777)

        directory = temp_directory()
        assert directory != shared
        assert directory.stat().st_mode & 0o077 == 0


class TestWriteHtmlFile:
    def test_writes_file(self, tmp_path):
        path = write_html_file("<p>é</p>", tmp_path / "page.html")
        assert path == tmp_path / "page.html"
        assert path.read_text(encoding="utf-8") == "<p>é</p>"

    def test_directory_uses_file_name(self, tmp_path):
        path = write_html_file("<p>1</p>", tmp_path, "scatter.html")
        assert path == tmp_path / "scatter.html"

    def test_directory_defaults_to_anonymous_and_replaces(self, tmp_path):
        first = write_html_file("<p>1</p>", tmp_path)
        second = write_html_file("<p>2</p>", str(tmp_path))
        assert first == second == tmp_path / "anonymous.html"
        assert second.read_text(encoding="utf-8") == "<p>2</p>"
        assert len(list(tmp_path.iterdir())) == 1
