from abc import ABC, abstractmethod
from copy import copy
from typing import Any, List, Union

from canvasxpress.canvas import CanvasXpress


class CXRenderAssociation(ABC):
    """
    CXRenderAssociation tracks a set of CanvasXpress objects that will be used to produce
    a domain- or container-specific rendering (e.g., for display in a Jupyter notebook).
    """

    __cx: List[CanvasXpress] = list()
    """The CanvasXpress objects to be managed by this CXRenderAssociation."""

    @property
    def canvas(self) -> Union[List[CanvasXpress], CanvasXpress, None]:
        """
        Provides the tracked CanvasXpress object(s).

        Returns:
            A list of CanvasXpress objects if multiple are tracked,
            a single CanvasXpress object, or None if no objects are tracked.
        """
        if len(self.__cx) == 0:
            return None

        elif len(self.__cx) == 1:
            return self.__cx[0]

        else:
            return copy(self.__cx)

    @canvas.setter
    def canvas(self, value: Union[List[CanvasXpress], CanvasXpress, None]):
        """
        Sets the CanvasXpress object(s) to be tracked.

        Args:
            value: A list of CanvasXpress objects if multiple are tracked,
                a single CanvasXpress object, or None if no objects are to be
                tracked.

        Raises:
            TypeError: If value is not None, a CanvasXpress instance, or a list
                of CanvasXpress instances.
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

    def __init__(self, *cx: Union[List[CanvasXpress], CanvasXpress, None]):
        """
        Initializes a new CXRenderAssociation object.

        Args:
            cx: The CanvasXpress object(s) to be tracked. See the `canvas`
                property, except that on initialization cx can be None.
                Multiple CanvasXpress objects are supported provided that
                they have distinct `render_to` targets.

        Raises:
            TypeError: If any cx member is not a CanvasXpress instance.
        """
        charts = list()
        for arg in cx:
            if arg is None:
                continue

            if isinstance(arg, (list, tuple)):
                for item in arg:
                    if not isinstance(item, CanvasXpress):
                        raise TypeError("All cx members must be of type CanvasXpress")
                    else:
                        charts.append(item)

            elif isinstance(arg, CanvasXpress):
                charts.append(arg)

            else:
                raise TypeError("All cx members must be of type CanvasXpress")

        self.canvas = charts


class CXRenderable(CXRenderAssociation):
    """
    CXRenderable is capable of rendering a CanvasXpress object to some kind of
    output or display device.
    """

    def __init__(self, *cx: Union[List[CanvasXpress], CanvasXpress, None]):
        """
        Initializes a new CXRenderable object.

        Args:
            cx: The CanvasXpress object(s) to be tracked. See the `canvas`
                property, except that on initialization cx can be None.
                Multiple CanvasXpress objects are supported provided that
                they have distinct `render_to` targets.

        Raises:
            TypeError: If any cx member is not a CanvasXpress instance.
        """
        super().__init__(*cx)

    @abstractmethod
    def render(self, **kwargs: Any):
        """
        Renders the associated CanvasXpress object appropriate to the render_to.

        Note:
            This method is not implemented. Subclasses must provide an implementation.

        Args:
            kwargs: Parameters specific to implementations are supported.
                The essential render call should work with no extra parameters,
                and with parameters that do not apply to the implementation.
        """
        pass


class CXRenderFactory(CXRenderAssociation):
    """
    CXRenderFactory produces objects for use in a container or framework that understand how
    to cooperate with the framework to produce CanvasXpress illustrations.
    """

    def __init__(self, *cx: Union[List[CanvasXpress], CanvasXpress, None]):
        """
        Initializes a new CXRenderFactory object.

        Args:
            cx: The CanvasXpress object(s) to be tracked. See the `canvas`
                property, except that on initialization cx can be None.
                Multiple CanvasXpress objects are supported provided that
                they have distinct `render_to` targets.

        Raises:
            TypeError: If any cx member is not a CanvasXpress instance.
        """
        super().__init__(*cx)

    @abstractmethod
    def render_all(self, **kwargs: Any) -> List[object]:
        """
        Provides a list of objects that can be used by the target domain or container
        to create CanvasXpress illustrations or instantiations.

        Note:
            This method is not implemented. Subclasses must provide an implementation.

        Args:
            kwargs: Parameters specific to implementations are supported.
                The essential render call should work with no extra parameters,
                and with parameters that do not apply to the implementation.

        Returns:
            A list of objects usable by the target domain or container.
        """
        pass
