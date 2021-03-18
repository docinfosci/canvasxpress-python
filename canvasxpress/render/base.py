from abc import ABC, abstractmethod
from typing import Union

from canvasxpress.canvas import CanvasXpress


class CXRenderable(ABC):
    """
    CXRenderable is capable of rendering a CanvasXpress object to some kind of
    output or display device.
    """

    __cx: CanvasXpress = None

    @property
    def canvas(self) -> CanvasXpress:
        return self.__cx

    @canvas.setter
    def canvas(self, value: CanvasXpress):
        if value is None:
            raise ValueError("value cannot be None")

        elif not isinstance(value, CanvasXpress):
            raise TypeError("value must of type CanvasXpress")

        else:
            self.__cx = value

    def __init__(
            self,
            cx: CanvasXpress
    ):
        __cx = None
        self.canvas = cx

    @abstractmethod
    def render(self):
        """
        Renders the associated CanvasXpress object appropriate to the target.
        """
        pass
