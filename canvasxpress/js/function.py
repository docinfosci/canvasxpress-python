import json
from copy import copy, deepcopy
from functools import total_ordering

from canvasxpress.data.convert import CXJavascriptConvertable
from canvasxpress.util.template import render_from_template

_CX_EVENT_TEMPLATE = "function(o, e, t){@cx_js_script@}"
"""
_CX_EVENT_TEMPLATE provides the function format expected by CanvasXpress.
"""


@total_ordering
class CXEvent(CXJavascriptConvertable):
    """
    CXEvent is a `CXJavascriptConvertable` that represents Javascript source to
    be associated with a CanvasXpress object.

    CanvasXpress provides hook functions for various events that are called as
    those events occur for the `div` element containing the rendered chart.
    The format is:

    ```javascript
    "event-name": function(o, e, t) {
        event code
    }
    ```

    With the following as an example:

    ```javascript
    "mousemove": function(o, e, t) {
        t.showInfoSpan(e, '<pre>' + t.prettyJSON(o) + '</pre>');
    }
    ```

    CXEvent handles the function template, so the developer only needs to supply
    the event name and the source.  Given the above example, the following
    creates the equivalent CXEvent:

    ```python
    event = CXEvent(
        id="mousemove",
        script="t.showInfoSpan(e, '<pre>' + t.prettyJSON(o) + '</pre>');"
    )
    ```

    No validations is performed for `id` or `script`.

    Read the [CanvasXpress documentation](https://www.canvasxpress.org/docs.html#events)
    for additional information.  Also see `CXEvents`.
    """

    __id: str = ""
    """
    The triggering JS react, such as mousemove.
    """

    __script: str = ""
    """
    The script to be placed inside of the CanvasXpress react function, which
    takes the general form:
    
    function(o, e, t) {
        // script logic goes here
    };
    """

    @property
    def id(self) -> str:
        """
        Provides access to the react ID.
        :returns: The ID as a string.
        """
        return self.__id

    @id.setter
    def id(self, value: str) -> None:
        """
        Sets the react ID, which is a keyword recognized by CanvasXpress.
        :param value: `str`
            The ID, which must be a string compliant object.  Cannot be `None`.
        """
        if value == None:
            raise TypeError("value cannot be None")
        else:
            self.__id = str(value)

    @property
    def script(self) -> str:
        """
        Provides access to the react script.
        :returns: `str` The Javascript source.
        """
        return self.__script

    @script.setter
    def script(self, value: str) -> None:
        """
        Sets the react script, which is logic that goes inside of the react
        function.  Functions take the form:

        ```javascript
        function(o, e, t) {
            // script logic goes here
        };
        ```

        The script can be assumed to have access to all DOM elements as proper,
        and it will be provided the parameters o, e, and t.  Read the
        [CanvasXpress documentation](https://www.canvasxpress.org/docs.html#events)
        for additional information.

        :param value: `str`
            The ID, which must be a UTF-8 string compliant object.
        """
        if value == None:
            raise TypeError("value cannot be None")
        else:
            self.__script = str(value)

    def render_to_js(self) -> str:
        """
        Converts the object into HTML5 complant script.
        :returns: 'str'
        Given:
        ```python
        event1 = CXEvent("f1", "x = 0")
        function = event1.render_to_js()
        ```
        Then the value of `function` would be:
        ```text
        'f1': 'function(o, e, t){x = 0}
        ```
        """
        cx_js = self.script
        cx_js_func = render_from_template(
            _CX_EVENT_TEMPLATE,
            {
                "cx_js_script": cx_js,
            },
        )
        return cx_js_func

    def __init__(self, id: str = "", script: str = ""):
        """
        Initializes a new CXEvent object.
        :param id: `str`
            The ID of the react, such as mousemove.  Also see property `id`.
        :param script: `str`
            The script logic for the react.  Also see property `script`.
        """
        super().__init__()

        self.id = id
        self.script = script

    def __copy__(self):
        """
        *copy* constructor.  Returns a new `CXEvent` object.
        """
        return CXEvent(id=copy(self.id), script=copy(self.script))

    def __deepcopy__(self, memo):
        """
        *deepcopy* constructor.  Returns a new `CXEvent` object.
        """
        return CXEvent(id=deepcopy(self.id), script=deepcopy(self.script))

    def __lt__(self, other: "CXEvent") -> bool:
        """
        *less than* comparison.  Also see `@total_ordering` in `functools`.
        :param other:
            `CXEvent` The object to compare.
        :returns: `bool`
            <ul>
            <li> If `other` is `None` then `False`
            <li> If `other` is not a `CXEvent` object then `False`
            <li> If `other` is a `CXEvent` object then True if id and string of
                `other` are less than that of `self`.
            </ul>
        """
        if other is None:
            return False

        if not isinstance(other, CXEvent):
            return False

        else:
            if self.id < other.id:
                return True
            elif self.id == other.id:
                return self.script < other.script
            else:
                return False

    def __eq__(self, other: "CXEvent") -> bool:
        """
        *equal* comparison.  Also see `@total_ordering` in `functools`.
        :param other:
            `CXEvent` The object to compare.
        :returns: `bool`
            <ul>
            <li> If `other` is `None` then `False`
            <li> If `other` is not a `CXEvent` object then `False`
            <li> If `other` is a `CXEvent` object then True if id and string of
                `other` are equal to that of `self`.
            </ul>
        """
        if other is None:
            return False

        if not isinstance(other, CXEvent):
            return False

        else:
            return (self.id == other.id) and (self.script == other.script)

    def __str__(self) -> str:
        """
        *str* function.  Converts the object into a Javascript statement.
        """
        return f'"{self.id}": {self.render_to_js()}'

    @staticmethod
    def __clean_string(value: str) -> str:
        """
        Adjusts characters problematic for Javascript conversion.
        :param value: `str` The value to clean.
        :returns: `str` The cleaned value.
        """
        candidate = json.dumps(value)[1:-1]

        escape_chars = [("\\", "\\\\"), ('"', '\\"'), ("\n", "\\n")]
        for escape in escape_chars:
            candidate = candidate.replace(escape[0], escape[1])

        return candidate

    def __repr__(self) -> str:
        """
        *repr* function.  Converts the CXEvent object into a pickle string
        that can be used with `eval` to establish a copy of the object.
        :returns: `str` An evaluatable representation of the object.
        """
        clean_id = CXEvent.__clean_string(self.id)
        clean_script = CXEvent.__clean_string(self.script)
        rep_candidate = f"CXEvent(" f'id="{clean_id}", ' f'script="{clean_script}"' f")"
        return rep_candidate
