import json
from typing import Union

from canvasxpress.data.base import CXData


class CXTextData(CXData):
    """
    `CXTextData` is a `CXData` class that provides plain-text data directly to
    the CanvasXpress for Javascript object.  In this manner, the Python tier
    makes no assumptions about the data content and permits the Javascript tier
    to address any required adjustments in order to properly display the data
    within a chart.  If the data is erroneously formatted then the only
    feedback will be at the Javascript tier.
    """

    __raw_text = ""
    """
    `__raw_text` tracks a block of text to be passed directly to the 
    CanvasXpress for Javascript constructor.
    """

    @property
    def text(self) -> str:
        """
        Returns the raw text form of the data.
        :returns: `str`
            The text to be provided to CanvasXpress.
        """
        return self.__raw_text

    @text.setter
    def text(self, value: str) -> None:
        """
        Sets the text to be provided to CanvasXpress.
        :param value: `str`
            The text to provide as-is to CanvasXpress.  `None` will be
            converted to an empty `str`.  Values of type other than `str`
            will be converted using `str()`.
        """
        if value is None:
            self.__raw_text = ""

        elif isinstance(value, str):
            self.__raw_text = value

        else:
            self.__raw_text = str(value)

    @property
    def data(self) -> dict:
        """
        A property accessor for the data managed by the object.  Regardless of
        the input data the returned data structure will be a dict-type for use
        with CanvasXpress.
        :returns: `dict`
            A dictionary representing a data map suitable for use with a chart.
        """
        return self.get_raw_dict_form()

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
        try:
            # Check the data as a JSON object.  If the JSON object equates to
            # a dict, list, or str then pass the Python form along as it will be
            # converted back into a string as part of the HTML render.  For
            # anything else treat the content as a standard string to be
            # passed along.

            candidate = {"raw": json.loads(self.text)}
            if isinstance(candidate["raw"], (dict, list, str)):
                return {"raw": json.loads(self.text)}
            else:
                return {"raw": self.text}

        except Exception as e:
            return {"raw": self.text}

    def render_to_dict(self, **kwargs) -> dict:
        """
        Converts the object into a dict representation.
        :returns: `dict`
            A dictionary representation of the object, such as what might be
            needed for a JSON export.
        """
        return self.get_raw_dict_form()

    def __init__(self, data: Union[object, None] = None) -> None:
        """
        Initializes the CXData object with data.
        :param data: `Union[object, None]`
            Given an object or no data prepares a new CXData instance ready for
            use by a `CanvasXpress` object.
        """
        self.text = data
