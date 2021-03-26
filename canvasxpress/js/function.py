import json
from copy import copy, deepcopy
from functools import total_ordering

from canvasxpress.data.convert import CXJavascriptConvertable
from canvasxpress.util.template import render_from_template

CX_EVENT_TEMPLATE = "function(o, e, t){@cx_js_script@}"


@total_ordering
class CXEvent(CXJavascriptConvertable):
    """
    CXEvent represents a Javascript script that can be associated with a
    CanvasXpress object.
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
    def id(
            self,
            value: str
    ) -> None:
        """
        Sets the react ID, which is a keyword recognized by CanvasXpress.
        :param value: The ID, which must be a string compliant object.
        """
        if value == None:
            raise TypeError("value cannot be None")
        else:
            self.__id = str(value)

    @property
    def script(self) -> str:
        """
        Provides access to the react script.
        :returns: The script as a string.
        """
        return self.__script

    @script.setter
    def script(
            self,
            value: str
    ) -> None:
        """
        Sets the react script, which is logic that goes inside of the react
        function.  Functions take the form:

        function(o, e, t) {
            // script logic goes here
        };

        The script can be assumed to have access to all DOM elements as proper,
        and it will be provided the parameters o, e, and t.  Read more about
        react functions on the CanvasXpress.org site.

        :param value: The ID, which must be a UTF-8 string compliant object.
        """
        if value == None:
            raise TypeError("value cannot be None")
        else:
            self.__script = str(value)

    def render_to_js(self) -> str:
        """
        Converts the object into HTML5 complant script.
        """
        cx_js = self.script
        cx_js_func = render_from_template(
            CX_EVENT_TEMPLATE,
            {
                'cx_js_script': cx_js,
            }
        )
        return cx_js_func

    def __init__(
            self,
            id: str = "",
            script: str = ""
    ):
        """
        Provides a new CXEvent object.
        :param id: The ID of the react, such as mousemove.
        :param script: The script logic for the react.
        """
        self.id = id
        self.script = script

    def __copy__(self):
        return CXEvent(
            id=copy(self.id),
            script=copy(self.script)
        )

    def __deepcopy__(
            self,
            memo
    ):
        return CXEvent(
            id=deepcopy(self.id),
            script=deepcopy(self.script)
        )

    def __lt__(
            self,
            other: 'CXEvent'
    ):
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

    def __eq__(
            self,
            other: 'CXEvent'
    ):
        if other is None:
            return False

        if not isinstance(other, CXEvent):
            return False

        else:
            return (self.id == other.id) and (self.script == other.script)

    def __str__(self) -> str:
        return f'"{self.id}": {self.render_to_js()}'

    @staticmethod
    def __clean_string(value: str) -> str:
        candidate = json.dumps(value)[1:-1]

        escape_chars = [
            ('\\', '\\\\'),
            ('"', '\\"'),
            ('\n', '\\n')
        ]
        for escape in escape_chars:
            candidate = candidate.replace(escape[0], escape[1])

        return candidate

    def __repr__(self) -> str:
        clean_id = CXEvent.__clean_string(self.id)
        clean_script = CXEvent.__clean_string(self.script)
        rep_candidate = f'CXEvent(' \
                        f'id="{clean_id}", ' \
                        f'script="{clean_script}"' \
                        f')'
        return rep_candidate
