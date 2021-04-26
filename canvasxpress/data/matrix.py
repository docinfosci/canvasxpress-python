import csv
import json
from functools import total_ordering
from io import StringIO
from typing import Union

import pandas
from pandas import DataFrame

from canvasxpress.data.base import CXData


@total_ordering
class CXDataframeData(CXData):
    """
    A CXData class dedicated to processing Python DataFrame, matrix-structured
     data.
    """

    __data: DataFrame = DataFrame()
    """
    The data managed by an object of this class.
    """

    @property
    def dataframe(self) -> DataFrame:
        """
        Provides the data managed by the object.
        :returns: `DataFrame` The managed data.
        """
        return self.__data

    @dataframe.setter
    def dataframe(
            self,
            value: Union[DataFrame, None] = None
    ) -> None:
        """
        Sets the dataframe managed by the object.
        :param value: `Union[DataFrame, None]`
            `None` results in an empty `DataFrame`.  A deepcopy will be made of
            `DataFrame` values.
        """
        self.data = value

    @property
    def data(self) -> dict:
        """
        Provides the data managed by the object.
        :returns: `DataFrame` The managed data.
        """
        return self.render_to_dict()

    @data.setter
    def data(
            self,
            value: Union['CXDataframeData', DataFrame, dict, str, None] = None
    ) -> None:
        """
        Sets the dataframe managed by the object.
        :param value: `Union['CXDataframeData', DataFrame, dict, str, None]`
            `None` results in an empty `DataFrame`.  A deepcopy will be made of
            `DataFrame` or equivalent values.
        """
        if value is None:
            self.__data = DataFrame()

        elif not type(value) in [CXDataframeData, DataFrame, dict, str]:
            raise TypeError("value must be type DataFrame or compatible.")

        elif isinstance(value, CXDataframeData):
            self.__data = value.dataframe.copy(deep=True)

        elif isinstance(value, DataFrame):
            self.__data = value.copy(deep=True)

        elif isinstance(value, dict):
            self.__data = DataFrame.from_dict(value)

        else:
            # Try a JSON edition
            try:
                candidate_json = json.loads(value)
                candidate = DataFrame.from_dict(candidate_json)

            except:
                # Try to load a CSV or read it from memory
                try:
                    candidate = pandas.read_csv(
                        value,
                        index_col=False
                    )

                except:
                    candidate = pandas.read_csv(
                        StringIO(value),
                        index_col=False
                    )

            self.__data = DataFrame(candidate)

    def render_to_dict(self) -> dict:
        """
        Provides a dict representation of the data.
        :returns: `dict`
            The data in `dict` form.
        """
        return self.__data.to_dict(orient="list")

    def __init__(
            self,
            data: Union['CXDataframeData', DataFrame, dict, str, None] = None
    ) -> None:
        """
        Initializes the CXData object with data.  Only `DataFrame` or compatible
         data types are accepted.
        :param data: `Union['CXDataframeData', DataFrame, dict, str, None]`
            `None` to initialize with an empty `DataFrame`, or a `DataFrame`
            like object to assign mapped data.
        """
        super().__init__(data)
        self.dataframe = data

    def __copy__(self) -> 'CXDataframeData':
        """
        *copy constructor* that returns a copy of the CXDataframeData object.
        :returns: `CXDataframeData`
            A copy of the wrapping object.
        """
        return CXDataframeData(self.data)

    def __deepcopy__(
            self,
            memo
    ) -> 'CXDataframeData':
        """
        *deepcopy constructor* that returns a copy of the CXDataframeData object.
        :returns: `CXDataframeData` A copy of the wrapping object and deepcopy of
            the tracked data.
        """
        return CXDataframeData(self.data)

    def __lt__(
            self,
            other: 'CXDataframeData'
    ) -> bool:
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

        if type(other) is not CXDataframeData:
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

                return self.dataframe.lt(other.dataframe).all(
                    axis=None
                )

    def __eq__(
            self,
            other: 'CXDataframeData'
    ) -> bool:
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

        if type(other) is not CXDataframeData:
            return False

        else:
            self_c = self.dataframe.columns.unique()
            other_c = other.dataframe.columns.unique()

            if len(self_c) != len(other_c):
                return False

            if any([s not in other_c for s in self_c]):
                return False

            return self.dataframe.eq(other.dataframe).all(
                axis=None
            )

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
        candidate = f"CXDataframeData(" \
                    f"data=DataFrame.from_dict(" \
                    f"{json.dumps(self.render_to_dict())}, orient='columns'))"
        candidate = candidate.replace("Infinity", "float('inf')")
        candidate = candidate.replace("NaN", "float('nan')")

        return candidate


class CXCSVData(CXDataframeData):
    """
    A CXData class dedicated to processing Python CSV-based, matrix-structured
     data.
    """

    @property
    def csv(self) -> str:
        """
        Provides the data managed by the object.
        :returns: `str` The managed data.
        """
        candidate = self.dataframe.to_csv(
            index=False,
            quoting=csv.QUOTE_NONNUMERIC
        )
        candidate = candidate.replace('nan', '')
        return candidate

    @csv.setter
    def csv(
            self,
            value: str = None
    ) -> None:
        """
        Sets the CSV data managed by the object.
        :param value: `str`
            `None` results in an empty CSV.  A deepcopy will be made of
            valid CSV `str` values.
        """
        self.data = value

    def __init__(
            self,
            data: Union['CXCSVData', DataFrame, dict, str, None] = None
    ) -> None:
        """
        Initializes the CXData object with data.  Only CSV `str` or compatible
         data types are accepted.
        :param data: `Union['CXCSVData', DataFrame, dict, str, None]`
            `None` to initialize with an empty CSV, or a CSV `str`
            like object to assign mapped data.
        """
        super().__init__(data)

    def __str__(self) -> str:
        """
        *str* function.  Converts the CXCSVData object into a JSON
        representation.
        :returns" `str` JSON form of the `CXCSVData`.
        """
        return self.csv

    def __repr__(self) -> str:
        """
        *repr* function.  Converts the CXCSVData object into a pickle
         string that can be used with `eval` to establish a copy of the object.
        :returns: `str` An evaluatable representation of the object.
        """
        return f"CXCSVData(data={self.data})"
