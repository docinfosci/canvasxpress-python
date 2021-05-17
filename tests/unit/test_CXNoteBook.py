import pytest

from canvasxpress.canvas import CanvasXpress
from canvasxpress.config.collection import CXConfigs
from canvasxpress.config.type import CXGraphType, CXGraphTypeOptions, CXString, CXList, CXBool
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
                    "data": [[10, 35, 88]]
                }
            }
        ),
        config=CXConfigs(
            CXGraphType(CXGraphTypeOptions.Bar)
        )
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
        CXList("colors", ["rgba(0,104,139,0.5)", "rgba(205,0,0,0.5)", "rgba(64,64,64,0.5)"]),
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
            "\\nand alcoholic beverages for each of the 11 regions of Great Britain."
        ),
        CXList("xAxis", ["Alcohol"]),
        CXList("yAxis", ["Tobacco"]),
    )

    chart_configs \
        .set_param("sizeBy", "FC") \
        .set_param("plotBox", False)

    # An example event showing some information as the mouse moves
    chart_events = CXEvents(
        CXEvent(
            "click",
            """
            var s = 'click on var ' + o.y.vars[0] + ' and smp ' + o.y.smps[0];
            t.showInfoSpan(e, s);
            """
        )
    )

    chart_data = CXDictData(
        {
            "y": {
                "vars": ["Gene1"],
                "smps": ["Smp1", "Smp2", "Smp3"],
                "data": [[10, 35, 88]]
            }
        }
    )

    # The canvas, which uses earlier work
    chart = CanvasXpress(
        render_to="example_scatter2d",
        data=chart_data,
        config=chart_configs,
        events=chart_events
    )

    # Jupyter notebook requires components to render in their own containers -- so we provide one
    demo_nb = CXNoteBook(chart)
    demo_nb.render()
