import pytest

from canvasxpress.canvas import CanvasXpress
from canvasxpress.render.streamlit import _get_chart_display_code, plot


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
    assert not "@" in html


def test_invalid_chart_argument():
    with pytest.raises(TypeError):
        plot(cx="abc")


def test_none_chart_argument():
    assert plot(cx=None) is None
