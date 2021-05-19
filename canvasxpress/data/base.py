from abc import abstractmethod, ABC
from typing import Union

from canvasxpress.data.convert import CXDictConvertable


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
    def validate(
            self,
            data: 'CXData'
    ) -> None:
        """
        Inspects a given `CXData` object to determine if it conforms to the
        expectations of the `CXDataProfile`'s configuration.  Issues are
        raised as `CXDataProfileException` instances.
        :param data: `CXData`
            The `CXData` instance to consider in the context of the
            `CXDataProfile`.
        :returns: `None`
            Raises `CXDataProfileException` if an issue with `data` exists in
            the context of the `CXDataProfile` instance.
        """
        pass

    @abstractmethod
    def convert_to_profile(
            self,
            data: 'CXData'
    ) -> dict:
        """
        Converts a given `CXData` instance into a dict suitable for use by
        `CanvasXpress` when creating data instructions for the JS object.
        """
        pass


class CXData(CXDictConvertable):
    """
    CXData defines an essential data class for managing data acquisiton,
    transformation, and introspection as required by the `CanvasXPress` class.
    """

    __profile: Union[None, CXDataProfile]
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

    @abstractmethod
    def __init__(self, data: Union[object, None]) -> None:
        """
        Initializes the CXData object with data.
        :param data: `Union[object, None]`
            Given an object or no data prepares a new CXData instance ready for
            use by a `CanvasXpress` object.
        """
        pass
