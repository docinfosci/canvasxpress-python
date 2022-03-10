import string
from copy import copy, deepcopy

import pytest
from hypothesis import given
from hypothesis.strategies import text

from canvasxpress.js.function import CXEvent


def test_CXEvent_init_blank():
    event = CXEvent()
    assert event.id == ""
    assert event.script == ""


@given(text(), text())
def test_CXEvent_init_values(id, script):
    event = CXEvent(id, script)
    assert event.id == id
    assert event.script == script


def test_CXEvent_set_id_none():
    event = CXEvent()
    with pytest.raises(TypeError):
        event.id = None


def test_CXEvent_set_script_none():
    event = CXEvent()
    with pytest.raises(TypeError):
        event.script = None


def test_CXEvent_set_id_int():
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
def test_CXEvent_str_perspective(id, script):
    event = CXEvent(id, script)
    event_str = str(event)
    assert event_str == f'"{event.id}": {event.render_to_js()}'


@given(
    text(alphabet=string.ascii_letters, min_size=5),
    text(alphabet=string.ascii_letters, min_size=5),
)
def test_CXEvent_repr_perspective(id, script):
    event = CXEvent(id, script)
    event_repr = repr(event)
    event_rep = eval(r"{}".format(event_repr))
    assert event_rep == event


@given(
    text(alphabet=string.ascii_letters, min_size=5),
    text(alphabet=string.ascii_letters, min_size=5),
)
def test_CXEvent_render_to_js(id, script):
    event = CXEvent(id, script)
    js = event.render_to_js()

    assert type(js) == str
    assert js.startswith("function(o, e, t){")
    assert js.endswith("}")
    assert js.find(event.script) >= 0


def test_CXEvent_equality_by_script():
    event_a: CXEvent = CXEvent("a", "a()")
    event_b: CXEvent = CXEvent("a", "b()")

    assert event_a < event_b
    assert event_a != event_b
    assert event_b > event_a


def test_CXEvent_equality_by_id():
    event_a: CXEvent = CXEvent("a", "a()")
    event_b: CXEvent = CXEvent("b", "a()")

    assert event_a < event_b
    assert event_a != event_b
    assert event_b > event_a


def test_CXEvent_equality_by_None():
    event: CXEvent = CXEvent("a", "a()")

    assert not event < None
    assert event != None
    assert event > None
    assert None < event


def test_CXEvent_equality_by_junk():
    event_a: CXEvent = CXEvent("a", "a()")
    event_b: int = 0

    assert not event_a < event_b
    assert event_a != event_b
    assert not event_b > event_a
