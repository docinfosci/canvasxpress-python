from abc import ABC, abstractmethod

from canvasxpress.canvas import CanvasXpress


class CXRenderable(ABC):
    """
    CXRenderable is capable of rendering a CanvasXpress object to some kind of
    output or display device.
    """

    __cx: CanvasXpress = None
    """
    The CanvasXpress object to be managed by this CXRenderable.
    """

    @property
    def canvas(self) -> CanvasXpress:
        """
        Provides the tracked CanvasXpress object.
        :returns: The `CanvasXpress` object if tracked, or `None` if not object
            is yet associated with the CXRenderable.
        """
        return self.__cx

    @canvas.setter
    def canvas(self, value: CanvasXpress):
        """
        Sets the CanvasXpress object to be tracked.
        :praram value:
            The `CanvasXpress` object to be tracked.  Cannot be `None`.
        """
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
        """
        Initializes a new CXRenderable object.
        :praram cx:
            The `CanvasXpress` object to be tracked.  See the `canvas`
            property, except that on initialization cx can be `None`.
        """
        self.__cx = cx
        if cx is not None:
            self.__cx = cx

    @abstractmethod
    def render(self):
        """
        Renders the associated CanvasXpress object appropriate to the render_to.
        Not implemented.
        """
        pass
