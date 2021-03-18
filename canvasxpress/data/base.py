from abc import abstractmethod
from typing import Union

from canvasxpress.data.convert import CXDictConvertable


class CXData(CXDictConvertable):
    """
    CXData defines an essential data class for managing data acquisiton,
    transformation, and introspection as required by the CXPress class.
    """

    @property
    @abstractmethod
    def data(self) -> dict:
        """
        A property accessor for the data managed by the object.  Regardless of
        the input data the returned data structure will be a dict-type for use
        with CanvasXpress.
        """
        pass

    @abstractmethod
    def __init__(self, data: Union[object, None]) -> None:
        """
        Initializes the CXData object with data.
        """
        pass
