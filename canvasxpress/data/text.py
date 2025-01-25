import csv
import json
from typing import Union

from pandas import DataFrame

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


class CXDataframeData(CXTextData):
    """
    `CXDataframeData` is a `CXTextData` class that provides plain-text data directly to
    the CanvasXpress for Javascript object by converting a Pandas DataFrame into a text matrix.
    """

    __data: DataFrame = DataFrame()
    """
    The data managed by an object of this class.
    """

    __delimiter: str = ","
    """
    The delimiter to use when convert to a CSV or TSV.
    """

    @property
    def delimiter(self) -> str:
        """
        Provides the delimiter (separator) used when creating the text matrix.
        """
        return self.__delimiter

    @delimiter.setter
    def delimiter(self, value) -> None:
        """
        Sets the delimiter to the desired value.  Must be CSV or TSV compliant.
        """
        if not isinstance(value, str):
            raise TypeError(
                "The delimiter must be a single character str bearing a comma or tab."
            )

        if value not in [",", "\t"]:
            raise ValueError(
                "The delimiter must be a single character str bearing a comma or tab."
            )

        else:
            self.__delimiter = value

    @property
    def dataframe(self) -> DataFrame:
        """
        Provides the data managed by the object.
        :returns: `DataFrame` The managed data.
        """
        return self.__data

    @dataframe.setter
    def dataframe(self, value: Union[DataFrame, None] = None) -> None:
        """
        Sets the dataframe managed by the object.
        :param value: `Union[DataFrame, None]`
            `None` results in an empty `DataFrame`.  A deepcopy will be made of
            `DataFrame` values.
        """

        if value is not None and not isinstance(value, DataFrame):
            raise TypeError("The value of dataframe must be a valid DataFrame or None.")

        self.dataframe = value

        if self.dataframe is None:
            self.text = None

        else:
            self.text = self.dataframe.to_csv(
                index=False,
                sep=self.delimiter,
                quoting=csv.QUOTE_NONNUMERIC,
            )

    @property
    def text(self) -> str:
        return super().text

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

    def __init__(
        self,
        data: Union[DataFrame, None] = None,
        delimiter: str = ",",
    ) -> None:
        """
        Initializes the CXDataFrameData object with data.
        :param data: `Union[DataFrame, None]`
            Given an DataFrame or no data prepares a new CXDataFrameData instance ready for
            use by a `CanvasXpress` object.
        :param delimiter: `str`
            A single character `str` with a comma or tab as the value.  The default is a comma.
        """
        super().__init__(None)
        self.delimiter = delimiter
        self.dataframe = data

    def __copy__(self) -> "CXDataframeData":
        """
        *copy constructor* that returns a copy of the CXDataframeData object.
        :returns: `CXDataframeData`
            A copy of the wrapping object.
        """
        return self.__class__(self.dataframe)

    def __deepcopy__(self, memo) -> "CXDataframeData":
        """
        *deepcopy constructor* that returns a copy of the CXDataframeData object.
        :returns: `CXDataframeData` A copy of the wrapping object and deepcopy of
            the tracked data.
        """
        return self.__class__(self.data)

    def __lt__(self, other: "CXDataframeData") -> bool:
        """
        *less than* comparison.  Also see `@total_ordering` in `functools`.
        :param other:
            `CXDataframeData` The object to compare.
        :returns: `bool`
            <ul>
            <li> If `other` is `None` then `False`
            <li> If `other` is not a `CXDataframeData` object then False
            <li> If `other` is a `CXDataframeData` object then True of all
                `CXDataframeData` aspects are also less than the data tracked by
                `self`.
            </ul>
        """
        if other is None:
            return False

        if not isinstance(other, CXDataframeData):
            return False

        else:
            self_c = self.dataframe.columns.unique()
            other_c = other.dataframe.columns.unique()

            if len(self_c) < len(other_c):
                return True

            elif len(self_c) > len(other_c):
                return False

            else:
                for i in [s for s in self_c if s not in other_c]:
                    if any([i < o for o in other_c]):
                        return True

                return self.dataframe.lt(other.dataframe).all(axis=None)

    def __eq__(self, other: "CXDataframeData") -> bool:
        """
        *equals* comparison.  Also see `@total_ordering` in `functools`.
        :param other:
            `CXDataframeData` The object to compare.
        :returns: `bool`
            <ul>
            <li> If `other` is `None` then `False`
            <li> If `other` is not a `CXDataframeData` object then False
            <li> If `other` is a `CXDataframeData` object then True of all
                `CXDataframeData` aspects are also less than the data tracked by
                `self`.
            </ul>
        """
        if other is None:
            return False

        if not isinstance(other, CXDataframeData):
            return False

        else:
            self_c = self.dataframe.columns.unique()
            other_c = other.dataframe.columns.unique()

            if len(self_c) != len(other_c):
                return False

            if any([s not in other_c for s in self_c]):
                return False

            return self.dataframe.eq(other.dataframe).all(axis=None)

    def __str__(self) -> str:
        """
        *str* function.  Converts the CXDataframeData object into a JSON
        representation.
        :returns" `str` JSON form of the `CXDataframeData`.
        """
        return json.dumps(self.render_to_dict())

    def __repr__(self) -> str:
        """
        *repr* function.  Converts the CXDataframeData object into a pickle
         string that can be used with `eval` to establish a copy of the object.
        :returns: `str` An evaluatable representation of the object.
        """
        candidate = (
            f"CXDataframeData("
            f"data=pandas.read_csv("
            f'StringIO("""{self.text}"""),'
            f"index_col=0))"
        )
        candidate = candidate.replace("Infinity", "float('inf')")
        candidate = candidate.replace("NaN", "float('nan')")

        return candidate
