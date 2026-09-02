import json
from copy import copy, deepcopy
from functools import total_ordering
from typing import List

from canvasxpress.data.convert import CXJavascriptConvertable
from canvasxpress.js.function import CXEvent


@total_ordering
class CXEvents(CXJavascriptConvertable):
    """
    A collection of CXEvent objects for Javascript scripts associated with a
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
    """The `CXEvent` objects tracked by this instance."""

    @property
    def events(self) -> List[CXEvent]:
        """Provides a non-associated list of the associated CXEvents.

        Returns:
            `List[CXEvent]` A list of zero or more CXEvent objects.
        """
        return copy(self.__events)

    def has(self, event: CXEvent) -> bool:
        """Indicates if the `CXEvent` is a member.

        Args:
            event: The `CXEvent` to consider.

        Returns:
            `bool` True if `event` is a member.
        """
        return event in self.events

    def add(self, event: CXEvent, unique: bool = True) -> None:
        """Adds the specified CXEvent. If the CXEvent must be unique then an Error
        is raised if a react is already present with the same ID.

        Args:
            event: `CXEvent` The event to add to the collection. Cannot be `None`.
            unique: `bool` True if `event` must not already be part of the collection.
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
        """Removes the specified object from the list.

        Args:
            event: The CXEvent object to remove from the list if it is
                already included.

        Returns:
            True if the CXEvent was removed. False indicates that the
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
        """Provides a dict with each JS properly formatted as JS within.

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

        Returns:
            `dict` A dictionary mapping event IDs to their JS function bodies.
        """

        events = dict()
        for event in self.events:
            events[event.id] = event.render_to_js()

        return events

    def render_to_js(self) -> str:
        """Converts the object into HTML5 compliant script.

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

        Returns:
            `str` A JSON-like string of event IDs mapped to JS function code.
        """
        events = dict()
        for event in self.events:
            events[event.id] = f"js_{event.id}"

        html = json.dumps(events).replace('"', "'")
        for event in self.events:
            html = html.replace(f"'js_{event.id}'", event.render_to_js())

        if html == "{}":
            html = "null"

        return html

    def __init__(self, *events):
        """Initializes a new CXEvents object.

        Args:
            events: A variable number of `CXEvent` objects to add. Also see
                `add()` for how individual objects are processed.

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
        """Creates a shallow copy of this CXEvents object.

        Returns:
            A new `CXEvents` object containing copies of the `CXEvent` objects
            within this instance.
        """
        return CXEvents(*self.events)

    def __deepcopy__(self, memo):
        """Creates a deep copy of this CXEvents object.

        Args:
            memo: The memoization dictionary for deepcopy.

        Returns:
            A new `CXEvents` object containing deep copies of the `CXEvent`
            objects within this instance.
        """
        return CXEvents(*([deepcopy(event) for event in self.events]))

    def __lt__(self, other: "CXEvents"):
        """Less than comparison. Also see `@total_ordering` in `functools`.

        Args:
            other: `CXEvents` The object to compare.

        Returns:
            `bool` True if `other` is a `CXEvents` object and all `CXEvent`
            objects are less than the events tracked by `other`, otherwise
            False.
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
        """Equals comparison. Also see `@total_ordering` in `functools`.

        Args:
            other: `CXEvents` The object to compare.

        Returns:
            `bool` True if `other` is a `CXEvents` object with the same length
            as `self` and all events are equal, otherwise False.
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
        """Converts the CXEvents object into a JSON list of `CXEvent` objects
        also converted into JSON representations.

        Returns:
            `str` JSON form of the collection.
        """
        return json.dumps(self.render_to_dict())

    def __repr__(self) -> str:
        """Converts the CXEvents object into a pickle string that can be used
        with `eval` to establish a copy of the object.

        Returns:
            `str` An evaluatable representation of the object.
        """
        event_rep_list = ", ".join([repr(event) for event in self.events])
        rep_candidate = f"CXEvents(" f"{event_rep_list}" f")"
        return rep_candidate
