import pytest

from canvasxpress.canvas import CanvasXpress
from canvasxpress.config.collection import CXConfigs
from canvasxpress.data.url import CXUrlData


def test_set_valid_url():

    samples = [
        "https://www.canvasxpress.org/data/cX-basic-dat.txt"
    ]
    for sample in samples:
        CXUrlData(sample)


def test_set_invalid_url():
    samples = [
        "snarf",
        "/test/that"
    ]
    for sample in samples:
        with pytest.raises(ValueError):
            CXUrlData(sample)

def test_data():
    candidate = CXUrlData("https://www.canvasxpress.org/data/cX-basic-dat.txt")
    result = candidate.data
    assert isinstance(result, dict)
    for key in result:
        assert key in [
            'scheme', 'netloc', 'path', 'query', 'fragment', 'username',
            'password', 'hostname', 'port', 'params'
        ]

def test_set_data():
    sample = "https://www.canvasxpress.org/data/cX-basic-dat.txt"
    candidate = CXUrlData(sample)

    valid_url = candidate.data
    candidate.data = valid_url

    with pytest.raises(ValueError):
        candidate.data = None

    with pytest.raises(TypeError):
        candidate.data = 123

def test_render_to_dict():
    sample = "https://www.canvasxpress.org/data/cX-basic-dat.txt"
    candidate = CXUrlData(sample)
    result = candidate.render_to_dict()
    assert result == {
        'raw': sample
    }

def test_get_raw_dict_form():
    sample = "https://www.canvasxpress.org/data/cX-basic-dat.txt"
    candidate = CXUrlData(sample)
    result = candidate.get_raw_dict_form()
    assert result == {
        'raw': sample
    }

def test_get_url():
    sample = "https://www.canvasxpress.org/data/cX-basic-dat.txt"
    candidate = CXUrlData(sample)
    result = candidate.url
    assert result == sample

def test_set_url():
    sample = "https://www.canvasxpress.org"
    candidate = CXUrlData("https://www.pypi.org")
    candidate.url = sample
    result = candidate.url
    assert result == sample

def test_canvasxpress_conversion():
    url_data = CXUrlData("https://www.pypi.org")

    chart_options = CXConfigs()
    chart_options \
        .set_param("title", "Tooth Growth") \
        .set_param("smpLabelRotate", 90) \
        .set_param("graphType", "Boxplot") \
        .set_param("graphOrientation", "vertical") \
        .set_param("metaData", {"dose": True}) \
        .set_param("groupingFactors", ["dose"])

    chart = CanvasXpress(
        data=url_data,
        config=chart_options
    )
    parts = chart.render_to_html_parts()
    assert '"data": "https://www.pypi.org"' in parts['cx_js']
