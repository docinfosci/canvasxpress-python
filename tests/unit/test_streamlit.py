import pytest

from canvasxpress.canvas import CanvasXpress
from canvasxpress.config.collection import CXConfigs
from canvasxpress.config.type import CXList
from canvasxpress.render import streamlit as cx_streamlit
from canvasxpress.render.streamlit import (
    _get_chart_component_data,
    _get_chart_display_code,
    plot,
)


def _bar_chart(**kwargs) -> CanvasXpress:
    return CanvasXpress(
        data={
            "y": {
                "vars": ["Gene1"],
                "smps": ["Smp1", "Smp2", "Smp3"],
                "data": [[10, 35, 88]],
            }
        },
        config={"graphType": "Bar"},
        **kwargs,
    )


def test_component_data_anonymous_chart():
    data = _get_chart_component_data(_bar_chart())

    assert set(data.keys()) == {
        "target_id",
        "placeholder_id",
        "canvas",
        "js",
        "js_url",
        "css_url",
        "license_url",
        "width",
        "height",
        "fill_to_width",
        "fill_to_height",
    }
    assert data["target_id"].startswith("cX")
    # The canvas and JS reference the chart only through the placeholder ID,
    # which the browser replaces with the target ID.
    assert f'id="{data["placeholder_id"]}"' in data["canvas"]
    assert f'"renderTo": "{data["placeholder_id"]}"' in data["js"]
    assert data["target_id"] not in data["canvas"]
    assert data["target_id"] not in data["js"]
    assert data["js_url"] == CanvasXpress.js_library_url()
    assert data["css_url"] == CanvasXpress.css_library_url()
    assert data["license_url"] is None
    assert (data["width"], data["height"]) == (500, 500)
    assert data["fill_to_width"] is False
    assert data["fill_to_height"] is False


def test_component_data_named_chart():
    chart = _bar_chart(render_to="my_chart")
    data = _get_chart_component_data(chart)

    assert data["target_id"] == "my_chart"
    # Rendering does not change the caller's chart.
    assert chart.render_to == "my_chart"
    # Stable across reruns, so an unchanged chart is not remounted.
    assert data == _get_chart_component_data(chart)


def test_component_data_after_render_uses_placeholder():
    chart = _bar_chart(
        render_to="my_chart",
        after_render=CXConfigs(CXList("createPie", ["Gender"])),
    )
    data = _get_chart_component_data(chart)
    assert f"CanvasXpress.$('{data['placeholder_id']}').createPie" in data["js"]


def test_plot_repeated_chart_gets_generated_keys(monkeypatch):
    """Mounting the same chart twice worked with iframes and must still work."""
    from streamlit.errors import (
        StreamlitDuplicateElementId,
        StreamlitDuplicateElementKey,
    )

    mounted_ids = set()
    mounted_keys = []

    def fake_component(data, width, height, key=None):
        if key is None:
            element_id = repr(sorted(data.items()))
            if element_id in mounted_ids:
                raise StreamlitDuplicateElementId("bidi_component")
            mounted_ids.add(element_id)
        else:
            if key in mounted_keys:
                raise StreamlitDuplicateElementKey(key)
        mounted_keys.append(key)

    monkeypatch.setattr(cx_streamlit, "_cx_component", fake_component)

    chart = _bar_chart(render_to="my_chart")
    for _ in range(3):
        plot(chart)

    assert mounted_keys == [None, "canvasxpress_my_chart_2", "canvasxpress_my_chart_3"]


def test_plot_explicit_key_is_not_retried(monkeypatch):
    from streamlit.errors import StreamlitDuplicateElementKey

    def fake_component(data, width, height, key=None):
        raise StreamlitDuplicateElementKey(key)

    monkeypatch.setattr(cx_streamlit, "_cx_component", fake_component)

    with pytest.raises(StreamlitDuplicateElementKey):
        plot(_bar_chart(), key="taken")


def test_plot_uses_v2_component(monkeypatch):
    calls = []
    monkeypatch.setattr(
        cx_streamlit, "_cx_component", lambda **kwargs: calls.append(kwargs)
    )

    plot(_bar_chart(render_to="my_chart"), key="chart-key")

    assert len(calls) == 1
    assert calls[0]["key"] == "chart-key"
    assert calls[0]["data"]["target_id"] == "my_chart"


def test_plot_falls_back_to_iframe(monkeypatch):
    import streamlit.components.v1 as components

    calls = []
    monkeypatch.setattr(cx_streamlit, "_cx_component", None)
    monkeypatch.setattr(
        components, "html", lambda html, **kwargs: calls.append((html, kwargs))
    )

    plot(_bar_chart(width=400, height=300))

    assert len(calls) == 1
    assert calls[0][1] == {"width": 450, "height": 350}


def test_valid_chart_argument():
    chart: CanvasXpress = CanvasXpress(
        data={
            "y": {
                "vars": ["Gene1"],
                "smps": ["Smp1", "Smp2", "Smp3"],
                "data": [[10, 35, 88]],
            }
        },
        config={
            "graphType": "Bar",
            "smpTitle": "Samples",
            "xAxis": ["V1"],
            "xAxisTitle": "Value",
        },
    )

    html, iframe_width, iframe_height = _get_chart_display_code(cx=chart)
    assert type(html) == str
    assert type(iframe_width) == int
    assert type(iframe_height) == int

    # check that template strings "@canvases@", etc. have all been replaced
    assert "@" not in html


def test_invalid_chart_argument():
    with pytest.raises(TypeError):
        plot(cx="abc")


def test_none_chart_argument():
    assert plot(cx=None) is None


def test_iframe_page_loads_library_before_chart():
    html, _, _ = _get_chart_display_code(_bar_chart(render_to="iframe_chart"))

    assert html.startswith("<!DOCTYPE html>")
    assert html.index(CanvasXpress.js_library_url()) < html.index('id="iframe_chart"')
    assert html.index('id="iframe_chart"') < html.index("new CanvasXpress(")


def test_component_js_uses_shared_loader():
    from canvasxpress.render.context import LOADER_JS

    assert cx_streamlit._cx_component_js.startswith(LOADER_JS)
    assert "window.canvasxpress" in cx_streamlit._cx_component_js
    assert ".loadLibrary(" in cx_streamlit._cx_component_js


def test_component_data_license():
    chart = _bar_chart(render_to="licensed")
    chart.license_url = "https://example.org/CanvasXpressLicense.js"

    data = _get_chart_component_data(chart)

    assert data["license_url"] == "https://example.org/CanvasXpressLicense.js"


def test_plot_fill_sizes_component(monkeypatch):
    calls = []
    monkeypatch.setattr(
        cx_streamlit, "_cx_component", lambda **kwargs: calls.append(kwargs)
    )

    plot(_bar_chart(render_to="fixed"), key="fixed")
    plot(_bar_chart(render_to="wide"), key="wide", fill_to_width=True)
    plot(_bar_chart(render_to="tall", height=300), key="tall", fill_to_height=True)

    sizes = [(call["width"], call["height"]) for call in calls]
    assert sizes == [
        ("content", "content"),
        ("stretch", "content"),
        ("content", "stretch"),
    ]
    assert [
        (call["data"]["fill_to_width"], call["data"]["fill_to_height"])
        for call in calls
    ] == [(False, False), (True, False), (False, True)]
    assert calls[2]["data"]["height"] == 300


def test_plot_fill_iframe_takes_container_width_but_not_height(monkeypatch):
    import streamlit.components.v1 as components

    calls = []
    monkeypatch.setattr(cx_streamlit, "_cx_component", None)
    monkeypatch.setattr(
        components, "html", lambda html, **kwargs: calls.append((html, kwargs))
    )

    plot(
        _bar_chart(render_to="filled", width=400, height=300),
        fill_to_width=True,
        fill_to_height=True,
    )

    html, kwargs = calls[0]
    assert kwargs == {"width": None, "height": 350}
    assert '"fillToWidth": true, "fillToHeight": false' in html
    assert "html, body { height: 100%" not in html


def test_component_js_fills_container_after_creating_chart():
    from canvasxpress.render.context import FILL_JS

    js = cx_streamlit._cx_component_js
    assert FILL_JS in js
    assert js.index("new Function(chartJs)()") < js.index(
        "window.canvasxpress.fillContainer(root"
    )
    assert "fillToHeight: data.fill_to_height" in js
    assert "stopFilling(instance)" in js
