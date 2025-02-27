from abc import abstractmethod, ABC
from typing import Union

from canvasxpress.data.convert import CXDictConvertable

Y = "y"
X = "x"
Z = "z"
VENN = "venn"

VARS = "vars"
SMPS = "smps"
DATA = "data"
CORS = "cors"
LEGEND = "legend"
NODES = "nodes"


class CXData(CXDictConvertable):
    """
    CXData defines an essential data class for managing data acquisiton,
    transformation, and introspection as required by the `CanvasXPress` class.
    """

    @property
    @abstractmethod
    def data(self) -> dict:
        """
        A property accessor for the data managed by the object.  Regardless of
        the input data the returned data structure will be a dict-type for use
        with CanvasXpress.
        :returns: `dict`
            A dictionary representing a data map suitable for use with a chart.
        """
        pass

    @abstractmethod
    def get_raw_dict_form(self) -> dict:
        """
        Provides a simple dict perspective of the data with no metadata or other
        contextual transformations performed.  For example, if the data is
        natively in `dict` form then it would be passed-through with no
        modification or enhancement.
        :returns: `dict`
            The `dict` perspective of the data with as little modification or
            interpretation as is reasonable.
        """
        pass

    @abstractmethod
    def __init__(self, data: Union[object, None]) -> None:
        """
        Initializes the CXData object with data.
        :param data: `Union[object, None]`
            Given an object or no data prepares a new CXData instance ready for
            use by a `CanvasXpress` object.
        """
        pass


class CXDataProfileException(ValueError):
    """
    CXDataProfileException is used by CXDataProfile to describe validation
    errors when considering CXData objects in the context of CXDataProfile
    objects.
    """

    pass


class CXKeyPairData(CXData):
    """
    CXKeyPairData is a marker class to indicate that the data managed will be
    generally of the structure key-pair.  A `dict` is an example of key-pair
    data.
    """

    pass


class CXMatrixData(CXData):
    """
    CXMatrixData is a marker class to indicate that the data management will be
    generally of the structure matrix or tabular.  A spreadsheet is an example
    of matrix data.
    """

    pass
