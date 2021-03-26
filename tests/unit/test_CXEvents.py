import json
from copy import copy, deepcopy

import pytest

from canvasxpress.js.collection import CXEvents
from canvasxpress.js.function import CXEvent


def test_CXEvents_init_blank():
    events = CXEvents()
    assert len(events.events) == 0


def test_CXEvents_init_cxevent_list():
    events = CXEvents(
        CXEvent(id="1", script="hi")
    )
    assert len(events.events) == 1


def test_CXEvents_init_junk():
    with pytest.raises(TypeError):
        events = CXEvents(
            [
                ("1", "hi")
            ]
        )


def test_CXEvents_copy():
    events1 = CXEvents(
        CXEvent(id="1", script="hi")
    )
    events2 = copy(events1)
    assert events1 == events2


def test_CXEvents_deepcopy():
    events1 = CXEvents(
        CXEvent(id="1", script="hi")
    )
    events2 = deepcopy(events1)
    assert events1 == events2


def test_CXEvents_add_event():
    event = CXEvent(id="1", script="hi")
    events = CXEvents()
    assert len(events.events) == 0

    events.add(event)
    assert len(events.events) == 1


def test_CXEvents_add_duplicate_event_non_unique():
    event = CXEvent(id="1", script="hi")
    events = CXEvents()
    assert len(events.events) == 0

    events.add(event)
    assert len(events.events) == 1

    events.add(event, False)
    assert len(events.events) == 2


def test_CXEvents_add_duplicate_event_unique():
    event = CXEvent(id="1", script="hi")
    events = CXEvents()
    assert len(events.events) == 0

    events.add(event)
    assert len(events.events) == 1

    with pytest.raises(ValueError):
        events.add(event)
    assert len(events.events) == 1


def test_CXEvents_add_None():
    events = CXEvents()
    assert len(events.events) == 0

    with pytest.raises(TypeError):
        events.add(None)
    assert len(events.events) == 0


def test_CXEvents_add_junk():
    events = CXEvents()
    assert len(events.events) == 0

    with pytest.raises(TypeError):
        events.add(123)
    assert len(events.events) == 0


def test_CXEvents_remove_event():
    event = CXEvent(id="1", script="hi")
    events = CXEvents()
    assert len(events.events) == 0

    events.add(event)
    assert len(events.events) == 1

    events.remove(event)
    assert len(events.events) == 0


def test_CXEvents_str_perspective():
    event = CXEvent(id="1", script="hi")
    events = CXEvents(event)

    events_str = str(events)
    assert events_str == json.dumps(events.render_to_dict())


def test_CXEvents_repr_perspective():
    event = CXEvent(id="1", script="hi")
    events = CXEvents(event)

    events_repr = repr(events)
    events_rep = eval(r"{}".format(events_repr))
    assert events_rep == events


def test_CXEvents_equality():
    events_a: CXEvents = CXEvents()
    events_b: CXEvents = CXEvents()

    assert events_a == events_b
    assert not events_a < events_b
    assert not events_a > events_b

    events_c: CXEvents = CXEvents(
        CXEvent("a", "a()")
    )

    assert events_a != events_c
    assert events_a < events_c
    assert events_c > events_a

    events_d: CXEvents = CXEvents(
        CXEvent("a", "a()")
    )

    assert events_c == events_d
    assert not events_c < events_d
    assert not events_c > events_d

    events_e: CXEvents = CXEvents(
        CXEvent("b", "b()")
    )

    assert events_a != events_e
    assert events_a < events_e
    assert events_e > events_a
    assert not events_a > events_e

    assert events_d != events_e
    assert events_d < events_e
    assert events_e > events_d
    assert not events_d > events_e

def test_CXEvents_equality_by_None():
    events: CXEvents = CXEvents()

    assert events != None
    assert not events < None
    assert events > None
    assert None < events


def test_CXEvents_equality_by_junk():
    events: CXEvent = CXEvents()
    junk_candidates: list = [0, "0", {"a": 0}, [0]]

    for junk in junk_candidates:
        assert events != junk
        assert not events < junk
        assert events > junk


def test_CXEvents_render_to_dict():
    event1 = CXEvent("1", "x = 0")
    event2 = CXEvent("2", "x = 1")

    events = CXEvents(event1, event2)
    functions = events.render_to_dict()

    assert isinstance(functions, dict)

    for event_id in functions.keys():
        for event in events.events:
            if event_id == event.id:
                assert event.render_to_js() == functions[event_id]
                break


def test_CXEvents_render_to_js():
    event1 = CXEvent("1", "x = 0")
    event2 = CXEvent("2", "x = 1")

    events = CXEvents(event1, event2)
    functions = events.render_to_js()

    assert isinstance(functions, str)

    for event_id in [event.id for event in events.events]:
        for event in events.events:
            if event_id == event.id:
                assert event.render_to_js() in functions
                break
