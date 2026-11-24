import pytest

from canvasxpress.canvas import CanvasXpress
from canvasxpress.config.collection import CXConfigs
from canvasxpress.config.type import (
    CXBool,
    CXGraphType,
    CXGraphTypeOptions,
    CXList,
    CXString,
)
from canvasxpress.data.keypair import CXDictData
from canvasxpress.js.collection import CXEvents
from canvasxpress.js.function import CXEvent
from canvasxpress.render.jupyter import CXNoteBook


def test_CXNoteBook_render():
    chart: CanvasXpress = CanvasXpress(
        render_to="canvasId",
        data=CXDictData(
            {
                "y": {
                    "vars": ["Gene1"],
                    "smps": ["Smp1", "Smp2", "Smp3"],
                    "data": [[10, 35, 88]],
                }
            }
        ),
        config=CXConfigs(CXGraphType(CXGraphTypeOptions.Bar)),
    )

    notebook: CXNoteBook = CXNoteBook(chart)

    try:
        notebook.render()

    except Exception as e:
        pytest.fail(f"Unexpected {e} when calling CXNoteBook.render()")


def test_CXNoteBook_render_complex():
    # A chart configuration is managed distinct from the associated chart, and it
    # can be reused across multiple chart objects.  A CXConfig object can be
    # initialized with a set of CXConfig objects or, later, objects can be added via
    # add() or set_param().  These functions support chaining.
    chart_configs = CXConfigs(
        CXGraphType(CXGraphTypeOptions.Scatter2D),
        CXString("axisAlgorithm", "rPretty"),
        CXString("backgroundType", "window"),
        CXString("backgroundWindow", "rgb(238,238,238)"),
        CXString("colorBy", "Group"),
        CXList(
            "colors", ["rgba(0,104,139,0.5)", "rgba(205,0,0,0.5)", "rgba(64,64,64,0.5)"]
        ),
        CXBool("showTransition", False),
        CXString("theme", "CanvasXpress"),
        CXString("showLoessFit", True),
        CXBool("legendBox", True),
        CXString("legendBoxColor", "rgb(0,0,0)"),
        CXBool("legendInside", True),
        CXString("legendPosition", "bottomRight"),
        CXBool("showConfidenceIntervals", False),
        CXBool("showDecorations", True),
        CXBool("showTransition", False),
        CXList("sizes", [4, 14, 16, 18]),
        CXString(
            "title",
            "Average weekly household spending, in British pounds, on tobacco products"
            "\\nand alcoholic beverages for each of the 11 regions of Great Britain.",
        ),
        CXList("xAxis", ["Alcohol"]),
        CXList("yAxis", ["Tobacco"]),
    )

    chart_configs.set_param("sizeBy", "FC").set_param("plotBox", False)

    # An example event showing some information as the mouse moves
    chart_events = CXEvents(
        CXEvent(
            "click",
            """
            var s = 'click on var ' + o.y.vars[0] + ' and smp ' + o.y.smps[0];
            t.showInfoSpan(e, s);
            """,
        )
    )

    chart_data = CXDictData(
        {
            "y": {
                "vars": ["Gene1"],
                "smps": ["Smp1", "Smp2", "Smp3"],
                "data": [[10, 35, 88]],
            }
        }
    )

    # The canvas, which uses earlier work
    chart = CanvasXpress(
        render_to="example_scatter2d",
        data=chart_data,
        config=chart_configs,
        events=chart_events,
    )

    # Jupyter notebook requires components to create_element in their own containers -- so we provide one
    demo_nb = CXNoteBook(chart)
    demo_nb.render()


def test_complex_chart_arrangements():
    # Define a CX bar chart with some basic data
    chart1 = CanvasXpress(
        render_to="dict_chart",
        data=CXDictData(
            {
                "y": {
                    "vars": ["Gene1"],
                    "smps": ["Smp1", "Smp2", "Smp3"],
                    "data": [[10, 35, 88]],
                },
            }
        ),
        config=CXConfigs(CXGraphType(CXGraphTypeOptions.Area)),
    )

    chart2 = CanvasXpress(
        render_to="dict_chart",
        data=CXDictData(
            {
                "y": {
                    "vars": ["Gene1"],
                    "smps": ["Smp1", "Smp2", "Smp3"],
                    "data": [[10, 35, 88]],
                },
            }
        ),
        config=CXConfigs(CXGraphType(CXGraphTypeOptions.Bar)),
    )

    chart3 = CanvasXpress(
        render_to="dict_chart",
        data=CXDictData(
            {
                "y": {"smps": ["Smp1", "Smp2", "Smp3"], "data": [[10, 35, 88]]},
            }
        ),
        config=CXConfigs(CXGraphType(CXGraphTypeOptions.Area)),
    )

    chart4 = CanvasXpress(
        render_to="dict_chart",
        data=CXDictData(
            {
                "vars": ["Gene1"],
                "smps": ["Smp1", "Smp2", "Smp3"],
                "data": [[10, 35, 88]],
            }
        ),
        config=CXConfigs(CXGraphType(CXGraphTypeOptions.Bar)),
    )

    nb = CXNoteBook([chart1, chart2, chart3, chart4])
    nb.render()
    nb.render(columns=1)
    nb.render(columns=2)
    nb.render(columns=3)
    nb.render(columns=4)
    nb.render(columns=5)


def _named_chart(render_to):
    return CanvasXpress(
        render_to=render_to,
        data=CXDictData({"y": {"vars": ["Gene1"], "smps": ["Smp1"], "data": [[10]]}}),
        config=CXConfigs(CXGraphType(CXGraphTypeOptions.Bar)),
    )


def test_CXNoteBook_render_returns_layout_then_loader():
    from IPython.display import HTML, Javascript

    content = CXNoteBook(_named_chart("nb_one"), _named_chart("nb_two")).render(
        columns=2
    )

    assert isinstance(content[0], HTML)
    assert isinstance(content[1], Javascript)
    assert 'id="nb_one"' in content[0].data
    assert "repeat(2, max-content)" in content[0].data
    assert "window.canvasxpress.loadLibrary(" in content[1].data
    assert "nb_two" in content[1].data


def test_CXNoteBook_render_does_not_change_duplicate_charts():
    first, second = _named_chart("nb_same"), _named_chart("nb_same")
    content = CXNoteBook([first, second]).render()

    assert first.render_to == second.render_to == "nb_same"
    assert content[0].data.count('id="nb_same') == 2


def test_CXNoteBook_render_none():
    assert CXNoteBook(None).render() == []


def test_CXNoteBook_render_output_file(tmp_path):
    output_file = tmp_path / "chart.html"
    content = CXNoteBook(_named_chart("nb_file")).render(output_file=str(output_file))

    assert len(content) == 2
    page = output_file.read_text(encoding="utf-8")
    assert page.startswith("<!DOCTYPE html>")
    assert 'id="nb_file"' in page
    assert CanvasXpress.js_library_url() in page


def test_CXNoteBook_render_output_directory(tmp_path):
    notebook = CXNoteBook(_named_chart("nb_one"), _named_chart("nb_two"))
    notebook.render(output_file=str(tmp_path))
    notebook.render(output_file=str(tmp_path))

    assert [path.name for path in tmp_path.iterdir()] == ["nb_one_nb_two.html"]


def test_CXNoteBook_render_debug():
    from IPython.display import Code

    content = CXNoteBook(_named_chart("nb_debug")).render(debug=True)

    assert isinstance(content, Code)
    assert "nb_debug" in content.data


def test_CXNoteBook_fill():
    fixed = CXNoteBook(_named_chart("nb_fixed")).render()
    wide = CXNoteBook(_named_chart("nb_wide")).render(fill_to_width=True)
    tall = CXNoteBook(_named_chart("nb_tall")).render(fill_to_height=True)

    assert "fillContainer(" not in fixed[1].data
    assert "grid-template-columns: repeat(1, minmax(0, 1fr))" in wide[0].data
    assert '"fillToWidth": true, "fillToHeight": false' in wide[1].data
    assert "grid-template-rows: repeat(1, minmax(0, 1fr))" in tall[0].data
    assert '"fillToWidth": false, "fillToHeight": true' in tall[1].data


def test_CXNoteBook_fill_output_file(tmp_path):
    output_file = tmp_path / "chart.html"
    CXNoteBook(_named_chart("nb_fill")).render(
        fill_to_width=True, fill_to_height=True, output_file=str(output_file)
    )

    page = output_file.read_text(encoding="utf-8")
    assert '"fillToWidth": true, "fillToHeight": true' in page
    assert "html, body { height: 100%" in page
