import json
from copy import copy, deepcopy

import pytest

from canvasxpress.js.collection import CXEvents
from canvasxpress.js.function import CXEvent


def test_events_init_blank():
    events = CXEvents()
    assert len(events.events) == 0

def test_events_init_cxevent_list():
    events = CXEvents(
        CXEvent(id="1", script="hi")
    )
    assert len(events.events) == 1

def test_events_init_junk():
    with pytest.raises(TypeError):
        events = CXEvents(
            [
                ("1", "hi")
            ]
        )

def test_events_copy():
    events1 = CXEvents(
        CXEvent(id="1", script="hi")
    )
    events2 = copy(events1)
    assert events1 == events2

def test_events_deepcopy():
    events1 = CXEvents(
        CXEvent(id="1", script="hi")
    )
    events2 = deepcopy(events1)
    assert events1 == events2

def test_events_add_event():
    event = CXEvent(id="1", script="hi")
    events = CXEvents()
    assert len(events.events) == 0

    events.add(event)
    assert len(events.events) == 1

def test_events_add_duplicate_event_non_unique():
    event = CXEvent(id="1", script="hi")
    events = CXEvents()
    assert len(events.events) == 0

    events.add(event)
    assert len(events.events) == 1

    events.add(event, False)
    assert len(events.events) == 2

def test_events_add_duplicate_event_unique():
    event = CXEvent(id="1", script="hi")
    events = CXEvents()
    assert len(events.events) == 0

    events.add(event)
    assert len(events.events) == 1

    with pytest.raises(ValueError):
        events.add(event)
    assert len(events.events) == 1

def test_events_add_junk():
    events = CXEvents()
    assert len(events.events) == 0

    with pytest.raises(TypeError):
        events.add(123)
    assert len(events.events) == 0

def test_events_remove_event():
    event = CXEvent(id="1", script="hi")
    events = CXEvents()
    assert len(events.events) == 0

    events.add(event)
    assert len(events.events) == 1

    events.remove(event)
    assert len(events.events) == 0

def test_events_str_perspective():
    event = CXEvent(id="1", script="hi")
    events = CXEvents(event)

    events_str = str(events)
    assert events_str == json.dumps(events.render_to_dict())


def test_events_repr_perspective():
    event = CXEvent(id="1", script="hi")
    events = CXEvents(event)

    events_repr = repr(events)
    events_rep = eval(r"{}".format(events_repr))
    assert events_rep == events

def test_events_render_to_dict():
    event1 = CXEvent("1", "x = 0")
    event2 = CXEvent("2", "x = 1")

    events = CXEvents(event1, event2)
    functions = events.render_to_dict()

    assert type(functions) == dict

    for event_id in functions.keys():
        for event in events.events:
            if event_id == event.id:
                assert event.render_to_js() == functions[event_id]
                break
