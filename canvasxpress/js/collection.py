import json
from copy import copy, deepcopy
from functools import total_ordering
from typing import List

from canvasxpress.data.convert import CXJavascriptConvertable
from canvasxpress.js.function import CXEvent


@total_ordering
class CXEvents(CXJavascriptConvertable):
    """
    CXEvents represents a Javascript script that can be associated with a
    CanvasXpress object.

    For example, when defining a CanvasXpress object Javascript could be
    added for reactive feedback via:

    ```python
    chart_events = CXEvents(
        CXEvent(
            "click",
            '''
            var s = 'click on var ' + o.y.vars[0] + ' and smp ' + o.y.smps[0];
            t.showInfoSpan(e, s);
            '''
        )
    )
    chart = CanvasXpress(
        events=chart_events
    )
    ```

    Also see the [CanvasXpress documentation](https://www.canvasxpress.org/docs.html#events)
    or `CXEvent` for additional information.
    """

    __events: List[CXEvent] = list()
    """
    The `CXEvent` objects tracked by this instance.
    """

    @property
    def events(self) -> List[CXEvent]:
        """
        Provides a non-associated list of the associated CXEvents.
        :returns: `List[CXEvent]` A list of zero or more CXEvent objects.
        """
        return copy(self.__events)

    def has(self, event: CXEvent) -> bool:
        """
        Indicates if the `CXEvent` is a member.
        :param event: The `CXEvent` to consider.
        :returns: `bool` True if `event` is a member.
        """
        return event in self.events

    def add(self, event: CXEvent, unique: bool = True) -> None:
        """
        Adds the specified CXEvent.  If the CXEvent must be unique then an Error
        is raised if an react is already presenbt with the same ID.
        :param event:
            `CXEvent` The event to add to the collection.  Cannot be `None`.
        :param unique:
            `bool` True if `event` must not already be a part of the collection.
        """
        if not event:
            raise TypeError("event cannot be None.")

        if not isinstance(event, CXEvent):
            raise TypeError("react must be of type CXEvent.")

        if unique and self.has(event):
            raise ValueError(
                f"A CXEvent of ID '{event.id}' is already part "
                f"of this CXEvent object."
            )

        self.__events.append(event)

    def remove(self, event: CXEvent) -> bool:
        """
        Removes the specified object from the list.
        :param event: The CXEvent object to remove from the list if it is
            already included.
        :returns: True if the CXEvent was removed.  False indicates that the
            object was not a member.
        """
        if self.has(event):
            for associated_event in self.__events:
                if associated_event == event:
                    self.__events.remove(event)
            return True

        else:
            return False

    def render_to_dict(self) -> dict:
        """
        Provides a dict with each js properly formatted as JS within.
        :returns: `dict`
        Given:
        ```python
        event1 = CXEvent("f1", "x = 0")
        event2 = CXEvent("f2", "x = 1")
        events = CXEvents(event1, event2)
        functions = events.render_to_dict()
        ```
        Then the value of `functions` would be:
        ```python
        {
            "f1": function(o, e, t){x = 0},
            "f2": function(o, e, t){x = 1}
        }
        ```
        """

        events = dict()
        for event in self.events:
            events[event.id] = event.render_to_js()

        return events

    def render_to_js(self) -> str:
        """
        Converts the object into HTML5 complant script.
        :returns: 'str'
        Given:
        ```python
        event1 = CXEvent("f1", "x = 0")
        event2 = CXEvent("f2", "x = 1")
        events = CXEvents(event1, event2)
        functions = events.render_to_js()
        ```
        Then the value of `functions` would be:
        ```text
        {
            'f1': 'function(o, e, t){x = 0}',
            'f2': 'function(o, e, t){x = 1}',
        }
        ```
        """
        events = dict()
        for event in self.events:
            events[event.id] = f"js_{event.id}"

        html = json.dumps(events).replace('"', "'")
        for event in self.events:
            html = html.replace(f"'js_{event.id}'", event.render_to_js())

        return html

    def __init__(self, *events):
        """
        Initializes a new CXEvents object.
        :param events:
            A multiple value parameter by which zero or more `CXEvent` objects
            may be provided.  Also see `add()` for how individual objects are
            processed.

            For example:
        ```python
        event1 = CXEvent("f1", "x = 0")
        event2 = CXEvent("f2", "x = 1")
        events = CXEvents(event1, event2)
        ```
        """
        super().__init__()

        self.__events = list()
        if events:
            for event in events:
                self.add(event)

    def __copy__(self):
        """
        *copy* constructor.  Returns the `CXEvent` objects within a new `CXEvents`
        object.
        """
        return CXEvents(*self.events)

    def __deepcopy__(self, memo):
        """
        *deepcopy* constructor.  Returns a deep copy of `CXEvent` objects within
        a new `CXEvents` object.
        """
        return CXEvents(*([deepcopy(event) for event in self.events]))

    def __lt__(self, other: "CXEvents"):
        """
        *less than* comparison.  Also see `@total_ordering` in `functools`.
        :param other:
            `CXEvent` The object to compare.
        :returns: `bool`
            <ul>
            <li> If `other` is `None` then `False`
            <li> If `other` is not a `CXEvents` object then False
            <li> If `other` is a `CXEvents` object then True of all `CXEvent`
                objects are also less than the events tracked by `self`.
            </ul>
        """
        if other is None:
            return False

        if not isinstance(other, CXEvents):
            return False

        else:
            if (len(self.events) + len(other.events)) == 0:
                return False

            if len(self.events) == len(other.events):
                for event in self.events:
                    for oevent in other.events:
                        if not event < oevent:
                            return False
                return True

            else:
                return len(self.events) < len(other.events)

    def __eq__(self, other: "CXEvents"):
        """
        *equals* comparison.  Also see `@total_ordering` in `functools`.
        :param other:
            `CXEvent` The object to compare.
        :returns: `bool`
            <ul>
            <li> If `other` is `None` then `False`
            <li> If `other` is not a `CXEvents` object then False
            <li> If `other` is a `CXEvents` object then True of all `CXEvent`
                objects are also equal to the events tracked by `self`.
            </ul>
        """
        if other is None:
            return False

        if not isinstance(other, CXEvents):
            return False

        else:
            if len(self.events) == len(other.events):
                for event in self.events:
                    for oevent in other.events:
                        if not event == oevent:
                            return False
                return True

            else:
                return len(self.events) == len(other.events)

    def __str__(self) -> str:
        """
        *str* function.  Converts the CXEvents object into a JSON list of
        `CXEvent` objects also converted into JSON representations.
        :returns" `str` JSON form of the collection.
        """
        return json.dumps(self.render_to_dict())

    def __repr__(self) -> str:
        """
        *repr* function.  Converts the CXEvents object into a pickle string
        that can be used with `eval` to establish a copy of the object.
        :returns: `str` An evaluatable representation of the object.
        """
        event_rep_list = ", ".join([repr(event) for event in self.events])
        rep_candidate = f"CXEvents(" f"{event_rep_list}" f")"
        return rep_candidate
