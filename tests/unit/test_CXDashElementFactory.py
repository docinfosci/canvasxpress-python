import json
import os

import pytest

import canvasxpress
from canvasxpress.canvas import CanvasXpress
from canvasxpress.config.collection import CXConfigs
from canvasxpress.config.type import CXList
from canvasxpress.render.dash import CXDashElement, CXElementFactory

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
    factory: CXElementFactory = CXElementFactory()

    dash_element: CXDashElement = factory.render(_g_cx)
    converted_properties = _g_cx.prepare_html_element_parts()

    assert dash_element.id == converted_properties["renderTo"]
    assert dash_element.width == str(converted_properties["width"])
    assert dash_element.height == str(converted_properties["height"])
    assert dash_element.config == json.dumps(converted_properties["config"])
    assert dash_element.events == converted_properties["events"]


def test_renderables():
    factory: CXElementFactory = CXElementFactory(_g_cx)

    dash_element: CXDashElement = factory.render_all()[0]
    converted_properties = _g_cx.prepare_html_element_parts()

    assert dash_element.id == converted_properties["renderTo"]
    assert dash_element.width == str(converted_properties["width"])
    assert dash_element.height == str(converted_properties["height"])
    assert dash_element.config == json.dumps(converted_properties["config"])
    assert dash_element.events == converted_properties["events"]


def test_render_library_urls():
    dash_element = CXElementFactory.render(_g_cx)

    assert dash_element.js_url == CanvasXpress.js_library_url()
    assert dash_element.css_url == CanvasXpress.css_library_url()
    assert dash_element.license_url is None


def test_render_after_render():
    chart = CanvasXpress(
        render_to="pie",
        data={"y": {"vars": ["V1"], "smps": ["S1"], "data": [[1]]}},
        after_render=CXConfigs(CXList("createPie", ["Gender"])),
    )
    dash_element = CXElementFactory.render(chart)

    assert json.loads(dash_element.after_render) == [["createPie", ["Gender"]]]


def test_element_requires_id():
    with pytest.raises(TypeError):
        CXDashElement(data="{}")


def test_element_dash_serialization():
    dash_element = CXElementFactory.render(_g_cx)
    plotly_json = dash_element.to_plotly_json()

    assert plotly_json["namespace"] == "canvasxpress"
    assert plotly_json["type"] == "CXDashElement"
    assert plotly_json["props"]["id"] == "area1"


def test_component_javascript_is_registered():
    """Dash serves component JavaScript listed by the component's top-level package."""
    paths = [dist["relative_package_path"] for dist in canvasxpress._js_dist]

    assert paths == [
        "render/resources/canvasxpress-loader.js",
        "render/resources/canvasxpress-fill.js",
        "render/resources/canvasxpress-react.js",
        "render/resources/canvasxpress-dash.js",
    ]
    package_dir = os.path.dirname(canvasxpress.__file__)
    for dist in canvasxpress._js_dist:
        assert dist["namespace"] == "canvasxpress"
        resource = os.path.join(package_dir, dist["relative_package_path"])
        with open(resource, encoding="utf-8") as fh:
            assert "root.canvasxpress" in fh.read()


def test_render_fill():
    element = CXElementFactory.render(_g_cx)
    assert (element.fill_to_width, element.fill_to_height) == (False, False)

    element = CXElementFactory.render(_g_cx, fill_to_width=True)
    assert (element.fill_to_width, element.fill_to_height) == (True, False)

    element = CXElementFactory.render(_g_cx, fill_to_height=True)
    props = element.to_plotly_json()["props"]
    assert (props["fill_to_width"], props["fill_to_height"]) == (False, True)


def test_render_all_fill():
    elements = CXElementFactory(_g_cx, _g_cx).render_all(
        fill_to_width=True, fill_to_height=True
    )
    assert [(e.fill_to_width, e.fill_to_height) for e in elements] == [
        (True, True),
        (True, True),
    ]


def test_react_wrapper_fills_container_after_creating_chart():
    package_dir = os.path.dirname(canvasxpress.__file__)
    resources = os.path.join(package_dir, "render", "resources")
    with open(os.path.join(resources, "canvasxpress-react.js"), encoding="utf-8") as fh:
        react = fh.read()
    with open(os.path.join(resources, "canvasxpress-dash.js"), encoding="utf-8") as fh:
        dash_js = fh.read()

    assert react.index("new CanvasXpress(") < react.index("fillContainer(host")
    assert "fillToHeight: props.fillToHeight" in react
    assert "stopFill()" in react
    assert "fillToWidth: Boolean(props.fill_to_width)" in dash_js
