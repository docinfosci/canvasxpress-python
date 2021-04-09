import csv
import json
from functools import total_ordering
from io import StringIO
from typing import Union

import pandas
from pandas import DataFrame, read_sql_query

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
        A property accessor for the data managed by the object.
        """
        return self.__data

    @dataframe.setter
    def dataframe(
            self,
            value: Union[DataFrame] = None
    ) -> None:
        self.data = value

    @property
    def data(self) -> dict:
        """
        A property accessor for the data managed by the object.
        """
        return self.render_to_dict()

    @data.setter
    def data(
            self,
            value: Union['CXDataframeData', DataFrame, dict, str, None] = None
    ) -> None:
        if (not isinstance(value, DataFrame)) and (value is None):
            raise TypeError("value cannot be None.")

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
        :return: The JSON as a str
        """
        return self.__data.to_dict(orient="list")

    def __init__(
            self,
            data: Union['CXDataframeData', DataFrame, dict, str, None] = None
    ) -> None:
        """
        Initializes the CXData object with data.  Only DataFrame or compatible
         data types are accepted.
        """
        super().__init__(data)
        self.__data = DataFrame()
        if data is not None:
            self.dataframe = data

    def __copy__(self):
        return CXDataframeData(self.data)

    def __deepcopy__(
            self,
            memo
    ):
        return CXDataframeData(self.data)

    def __lt__(
            self,
            other: 'CXDataframeData'
    ):
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
    ):
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
        return json.dumps(self.render_to_dict())

    def __repr__(self) -> str:
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
        A property accessor for the data managed by the object.
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
        self.data = value

    def __init__(
            self,
            data: Union['CXDataframeData', DataFrame, dict, str, None] = None
    ) -> None:
        """
        Initializes the CXData object with data.  Only DataFrame or compatible
         data types are accepted.
        """
        super().__init__(data)

    def __str__(self) -> str:
        return self.csv

    def __repr__(self) -> str:
        return f"CXCSVData(data={self.data})"
