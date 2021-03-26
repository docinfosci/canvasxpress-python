import collections
import json
from copy import copy, deepcopy
from functools import total_ordering
from typing import List

from canvasxpress.data.convert import CXJavascriptConvertable
from canvasxpress.js.function import CXEvent


@total_ordering
class CXEvents(CXJavascriptConvertable):
    """
    CXEvents represents a set of CXEvent objects and can render them properly
    for inclusion with a CanvasXpress object.
    """

    __events: List[CXEvent] = list()
    """
    The react objects tracked by this instance.
    """

    @property
    def events(self) -> List[CXEvent]:
        """
        A non-associated list of the CXEvents associated with this object.
        """
        return copy(self.__events)

    def has(
            self,
            event: CXEvent
    ):
        """
        Indicates if the react is a member.
        :param event: The object to consider
        """
        return event in self.events

    def add(
            self,
            event: CXEvent,
            unique: bool = True
    ) -> None:
        """
        Adds the specified react.  If the react must be unique then an Error
        is raised if an react is already presenbt with the same ID.
        """
        if not event:
            raise TypeError("react cannot be None.")

        if not isinstance(event, CXEvent):
            raise TypeError("react must be of type CXEvent.")

        if unique and self.has(event):
            raise ValueError(
                f"A CXEvent of ID '{event.id}' is already part "
                f"of this CXEvent object."
            )

        self.__events.append(event)

    def remove(
            self,
            event: CXEvent
    ) -> bool:
        """
        Removes the specified object from the list.
        :param event: The CXEvent object to remove from the list if it is
            already included.
        :returns: True if the react was removed.  False indicates that the
            object was not a member.
        """
        event_removed = False
        for associated_event in self.__events:
            if associated_event == event:
                self.__events.remove(event)
                event_removed = True

        return event_removed

    def render_to_dict(self) -> dict:
        """
        Provides a dict with each js properly formatted as JS within.
        """

        events = dict()
        for event in self.events:
            events[event.id] = event.render_to_js()

        return events

    def render_to_js(self) -> str:
        """
        Converts the object into HTML5 complant script.
        """
        events = dict()
        for event in self.events:
            events[event.id] = f"js_{event.id}"

        html = json.dumps(
            events,
            indent=8
        )
        for event in self.events:
            html = html.replace(
                f'"js_{event.id}"',
                event.render_to_js()
            )

        return html

    def __init__(self, *events):
        """
        Establishes a new CXEvents object.
        :param events: A list of CXEvents to associate.
        """
        self.__events = list()
        if events:
            for event in events:
                self.add(event)

    def __copy__(self):
        return CXEvents(
            *self.events
        )

    def __deepcopy__(
            self,
            memo
    ):
        return CXEvents(
            *([deepcopy(event) for event in self.events])
        )

    def __lt__(
            self,
            other: 'CXEvents'
    ):
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

    def __eq__(
            self,
            other: 'CXEvents'
    ):
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
        return json.dumps(
            self.render_to_dict()
        )

    def __repr__(self) -> str:
        event_rep_list = ", ".join([repr(event) for event in self.events])
        rep_candidate = f'CXEvents(' \
                        f'{event_rep_list}' \
                        f')'
        return rep_candidate
