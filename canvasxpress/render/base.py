from abc import ABC, abstractmethod
from copy import copy
from typing import Any, List, Union

from canvasxpress.canvas import CanvasXpress


class CXRenderable(ABC):
    """
    CXRenderable is capable of rendering a CanvasXpress object to some kind of
    output or display device.
    """

    __cx: List[CanvasXpress] = list()
    """
    The CanvasXpress object to be managed by this CXRenderable.
    """

    @property
    def canvas(self) -> Union[List[CanvasXpress], CanvasXpress, None]:
        """
        Provides the tracked CanvasXpress object.
        :returns: `value: Union[List[CanvasXpress], CanvasXpress, None]`
            A `list` of `CanvasXpress` objects if multiple are tracked,
            or one `CanvasXpress object, or `None` if no objects are tracked.
        """
        if len(self.__cx) == 0:
            return None

        elif len(self.__cx) == 1:
            return self.__cx[0]

        else:
            return copy(self.__cx)

    @canvas.setter
    def canvas(
            self,
            value: Union[List[CanvasXpress], CanvasXpress, None]
    ):
        """
        Sets the CanvasXpress object to be tracked.
        :praram value: `value: Union[List[CanvasXpress], CanvasXpress, None]`
            A `list` of `CanvasXpress` objects if multiple are tracked,
            or one `CanvasXpress object, or `None` if no objects are to be
            tracked.
        """
        if value is None:
            self.__cx = list()

        elif isinstance(value, CanvasXpress):
            self.__cx = [value]

        elif isinstance(value, list):
            for v in value:
                if not isinstance(v, CanvasXpress):
                    raise TypeError("value must of type CanvasXpress")

            self.__cx = copy(value)

        else:
            raise TypeError("value must of type CanvasXpress")

    def __init__(
            self,
            *cx: Union[List[CanvasXpress], CanvasXpress, None]
    ):
        """
        Initializes a new `CXRenderable` object.
        :praram cx: `Union[List[CanvasXpress], CanvasXpress, None], ...`
            The `CanvasXpress` object(s) to be tracked.  See the `canvas`
            property, except that on initialization cx can be `None`.
            Multiple CanvasXpress objects are supported provided that
            they have distinct `render_to` targets.
        """
        charts = list()
        for arg in cx:
            if arg is None:
                pass

            if isinstance(arg, (list, tuple)):
                for item in arg:
                    if not isinstance(item, CanvasXpress):
                        raise TypeError(
                            "All cx members must be of type CanvasXpress"
                        )
                    else:
                        charts.append(item)

            elif isinstance(arg, CanvasXpress):
                charts.append(arg)

            else:
                raise TypeError(
                    "All cx members must be of type CanvasXpress"
                )

        self.canvas = charts

    @abstractmethod
    def render(
            self,
            **kwargs: Any
    ):
        """
        Renders the associated CanvasXpress object appropriate to the render_to.
        Not implemented.
        :param kwargs: `Any`
            Parameters specific to implementations are supported.  The essential
            render call should work with no extra parameters, and with
            parameters that do not apply to the implementation.
        """
        pass
