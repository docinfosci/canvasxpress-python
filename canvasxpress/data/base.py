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
        """"
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


class CXDataProfile(ABC):
    """
    CXDataProfile assists with CXData translations into CanvasXpress JSON data
    formats, such as documented at
    [CanvasXpress.org](https://www.canvasxpress.org/docs.html#data).
    """

    @abstractmethod
    def render_to_profiled_dict(
            self,
            data: CXData,
            **kwargs
    ) -> dict:
        """
        Converts a given `CXData` instance into a dict suitable for use by
        `CanvasXpress` when creating data instructions for the JS object.
        """
        pass


class CXProfiledData(CXData):
    """
    CXData defines an essential data class for managing data acquisiton,
    transformation, and introspection as required by the `CanvasXPress` class.
    """

    __profile: Union[None, CXDataProfile] = None
    """
    `__profile` tracks the CXDataProfile instance by which the data will be 
    further adjusted into a CanvasXpress JSON data format.
    """

    @property
    def profile(self) -> Union[None, CXDataProfile]:
        """
        Provides the `CXDataProfile` associated with the `CXData` instance.
        :returns: `Union[None, CXDataProfile]`
            The `CXDataProfile` if one is associated, otherwise `None`.
        """
        return self.__profile

    @profile.setter
    def profile(
            self,
            profile: Union[None, CXDataProfile]
    ) -> None:
        """
        Sets the `CXDataProfile` associated with the `CXData` instance.  The
        default associated profile is `CXStandardProfile`, which supports the
        most typical CanvasXpress JSON data format for plotting.  To avoid the
        use of a profile and pass only a basic raw JSON edition of the instance
        to CanvasXpress set the profile to `None`.

        :param profile: `Union[None, CXDataProfile]`
            The profile to use when transforming the `CXData` instance into a
            CanvasXpress JSON data object.  Use `None` to avoid any
            transformation beyond the essential conversion of the instance into
            a JSON-like form.  For example, with `None` if the data tracked is
            a dict then the renderer would simply pass the data through.
        """
        self.__profile = profile

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

    def __init__(
            self,
            data: Union[object, None],
            profile: Union[CXDataProfile, None] = None
    ) -> None:
        """
        Initializes the CXData object with data.
        :param data: `Union[object, None]`
            Given an object or no data prepares a new CXData instance ready for
            use by a `CanvasXpress` object.
        :param profile: `Union[CXDataProfile, None]`
            Specify the desired profile object to facilitate transformation of
            data into a CanvasXpress JSON data object.  `None` to avoid use of
            a profile.
        """
        self.profile = profile


class CXKeyPairData(CXProfiledData):
    """
    CXKeyPairData is a marker class to indicate that the data managed will be
    generally of the structure key-pair.  A `dict` is an example of key-pair
    data.
    """
    pass


class CXMatrixData(CXProfiledData):
    """
    CXMatrixData is a marker class to indicate that the data management will be
    generally of the structure matrix or tabular.  A spreadsheet is an example
    of matrix data.
    """
    pass
