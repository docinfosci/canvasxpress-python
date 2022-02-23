import json

from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.dash import CXDashElementFactory
from cxdash import CXDashElement

_g_cx = CanvasXpress(
    render_to="area1",
    data={
        "y": {
            "data": [[10, 100, 70, 130, 60]],
            "vars": ["A"],
            "smps": ["S1", "S2", "S3", "S4", "S5"],
        }
    },
    config={
        "colorScheme": "GGPlot",
        "colors": ["rgb(248,118,109)"],
        "graphOrientation": "vertical",
        "graphType": "Area",
        "histogramStackRatio": 1,
        "objectBorderColor": False,
        "showLegend": False,
        "smpLabelRotate": 90,
        "smpTitle": "time",
        "xAxis": ["A"],
    },
    width=613,
    height=613,
)


def test_convert():
    factory: CXDashElementFactory = CXDashElementFactory()

    dash_element: CXDashElement = factory.convert(_g_cx)
    converted_properties = _g_cx.prepare_html_element_parts()

    assert dash_element.id == converted_properties["renderTo"]
    assert dash_element.width == str(converted_properties["width"])
    assert dash_element.height == str(converted_properties["height"])
    assert dash_element.config == json.dumps(converted_properties["config"])
    assert dash_element.events == converted_properties["events"]


def test_renderables():
    factory: CXDashElementFactory = CXDashElementFactory(_g_cx)

    dash_element: CXDashElement = factory.renderables()[0]
    converted_properties = _g_cx.prepare_html_element_parts()

    assert dash_element.id == converted_properties["renderTo"]
    assert dash_element.width == str(converted_properties["width"])
    assert dash_element.height == str(converted_properties["height"])
    assert dash_element.config == json.dumps(converted_properties["config"])
    assert dash_element.events == converted_properties["events"]
