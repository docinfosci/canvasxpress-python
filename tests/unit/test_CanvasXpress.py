import pytest

from canvasxpress.canvas import CanvasXpress
from canvasxpress.config.collection import CXConfigs
from canvasxpress.config.type import CXString
from canvasxpress.data.keypair import CXDictData
from canvasxpress.js.collection import CXEvents
from canvasxpress.js.function import CXEvent


def test_CanvasXpress_init():
    subject: CanvasXpress = CanvasXpress(
        render_to="this_is_a_test"
    )
    assert subject.render_to == "this_is_a_test"

    raw_sample = {'a': [1]}
    data_sample = CXDictData(raw_sample)
    subject: CanvasXpress = CanvasXpress(
        data=raw_sample
    )
    assert subject.data == data_sample
    subject: CanvasXpress = CanvasXpress(
        data=data_sample
    )
    assert subject.data == data_sample

    raw_sample = CXEvent("test", "x = 1")
    data_sample = CXEvents(raw_sample)
    subject: CanvasXpress = CanvasXpress(
        events=[raw_sample]
    )
    assert subject.events == data_sample
    subject: CanvasXpress = CanvasXpress(
        events=data_sample
    )
    assert subject.events == data_sample

    raw_sample = CXString("label", "value")
    data_sample = CXConfigs(raw_sample)
    subject: CanvasXpress = CanvasXpress(
        config=[raw_sample]
    )
    assert subject.config == data_sample
    subject: CanvasXpress = CanvasXpress(
        config=data_sample
    )
    assert subject.config == data_sample


def test_CanvasXpress_render_to():
    subject: CanvasXpress = CanvasXpress()
    subject.render_to = "this_is_a_test"
    assert subject.render_to == "this_is_a_test"

    with pytest.raises(ValueError):
        subject: CanvasXpress = CanvasXpress()
        subject.render_to = None

    with pytest.raises(TypeError):
        subject: CanvasXpress = CanvasXpress()
        subject.render_to = 1

    with pytest.raises(ValueError):
        subject: CanvasXpress = CanvasXpress()
        subject.render_to = "%*&*("


def test_CanvasXpress_chart_width():
    subject: CanvasXpress = CanvasXpress()
    subject.element_width = 10
    assert subject.element_width == 10

    with pytest.raises(ValueError):
        subject: CanvasXpress = CanvasXpress()
        subject.element_width = None

    with pytest.raises(TypeError):
        subject: CanvasXpress = CanvasXpress()
        subject.element_width = "test"

    with pytest.raises(ValueError):
        subject: CanvasXpress = CanvasXpress()
        subject.element_width = -1


def test_CanvasXpress_chart_height():
    subject: CanvasXpress = CanvasXpress()
    subject.element_height = 10
    assert subject.element_height == 10

    with pytest.raises(ValueError):
        subject: CanvasXpress = CanvasXpress()
        subject.element_height = None

    with pytest.raises(TypeError):
        subject: CanvasXpress = CanvasXpress()
        subject.element_height = "test"

    with pytest.raises(ValueError):
        subject: CanvasXpress = CanvasXpress()
        subject.element_height = -1


def test_CanvasXpress_data():
    subject: CanvasXpress = CanvasXpress()
    raw_sample = {'a': [1]}
    data_sample = CXDictData(raw_sample)

    subject.data = data_sample
    assert subject.data == data_sample

    subject.data = raw_sample
    assert subject.data == data_sample

    subject.data = None
    assert subject.data == CXDictData()

    with pytest.raises(TypeError):
        subject: CanvasXpress = CanvasXpress()
        subject.data = -1


def test_CanvasXpress_events():
    subject: CanvasXpress = CanvasXpress()
    raw_sample = CXEvent("test", "x = 1")
    data_sample = CXEvents(raw_sample)

    subject.events = data_sample
    assert subject.events == data_sample

    subject.events = [raw_sample]
    assert subject.events == data_sample

    subject.events = None
    assert subject.events == CXEvents()

    with pytest.raises(TypeError):
        subject: CanvasXpress = CanvasXpress()
        subject.events = -1


def test_CanvasXpress_config():
    subject: CanvasXpress = CanvasXpress()
    raw_sample = CXString("label", "value")
    data_sample = CXConfigs(raw_sample)

    subject.config = data_sample
    assert subject.config == data_sample

    subject.config = [raw_sample]
    assert subject.config == data_sample

    subject.config = None
    assert subject.config == CXConfigs()

    with pytest.raises(TypeError):
        subject: CanvasXpress = CanvasXpress()
        subject.config = -1


def test_CanvasXpress_license():
    subject: CanvasXpress = CanvasXpress()

    assert not subject.license_available
    with pytest.raises(ValueError):
        subject.license_url = "junk"

    assert not subject.license_available
    subject.license_url = "CanvasXpressLicense.js"
    assert subject.license_available

    assert subject.license_available
    subject.license_url = None
    assert not subject.license_available

    assert not subject.render_to_html_parts().get('cx_license')
    subject.license_url = "CanvasXpressLicense.js"
    assert subject.render_to_html_parts().get('cx_license')
    assert "CanvasXpressLicense.js" in subject.render_to_html_parts().get('cx_license')
