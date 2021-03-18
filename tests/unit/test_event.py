import string
from copy import copy, deepcopy

import pytest
from hypothesis import given
from hypothesis.strategies import text

from canvasxpress.js.function import CXEvent


def test_event_init_blank():
    event = CXEvent()
    assert event.id == ""
    assert event.script == ""


@given(text(), text())
def test_event_init_values(id, script):
    event = CXEvent(id, script)
    assert event.id == id
    assert event.script == script


def test_event_set_id_none():
    event = CXEvent()
    with pytest.raises(TypeError):
        event.id = None


def test_event_set_script_none():
    event = CXEvent()
    with pytest.raises(TypeError):
        event.script = None


def test_event_set_id_int():
    event = CXEvent()
    event.id = 123
    assert event.id == "123"


@given(text(), text())
def test_copy_event(id, script):
    event1 = CXEvent(id, script)
    event2 = copy(event1)
    assert event1 == event2


@given(text(), text())
def test_deepcopy_event(id, script):
    event1 = CXEvent(id, script)
    event2 = deepcopy(event1)
    assert event1 == event2


@given(text(), text())
def test_event_str_perspective(id, script):
    event = CXEvent(id, script)
    event_str = str(event)
    assert event_str == f'"{event.id}": {event.render_to_js()}'


@given(
    text(alphabet=string.ascii_letters, min_size=5),
    text(alphabet=string.ascii_letters, min_size=5)
)
def test_event_repr_perspective(id, script):
    event = CXEvent(id, script)
    event_repr = repr(event)
    event_rep = eval(r"{}".format(event_repr))
    assert event_rep == event


@given(
    text(alphabet=string.ascii_letters, min_size=5),
    text(alphabet=string.ascii_letters, min_size=5)
)
def test_event_render_to_js(id, script):
    event = CXEvent(id, script)
    js = event.render_to_js()

    assert type(js) == str
    assert js.startswith("function(o, e, t){")
    assert js.endswith("}")
    assert js.find(event.script) >= 0
