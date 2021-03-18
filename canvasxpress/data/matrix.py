import csv
import json
from functools import total_ordering
from io import StringIO
from typing import Union

from deepdiff import DeepDiff
from pandas import DataFrame, read_csv, read_sql_query

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
    def data(self) -> DataFrame:
        """
        A property accessor for the data managed by the object.
        """
        return self.__data

    @data.setter
    def data(self, value: DataFrame) -> None:
        if value == None:
            raise TypeError("value cannot be None.")

        elif not isinstance(value, DataFrame):
            raise TypeError("value must be type DataFrame or compatible.")

        else:
            self.__data = value.copy(deep=True)

    def render_to_dict(self) -> dict:
        """
        Provides a dict representation of the data.
        :return: The JSON as a str
        """
        return self.data.to_dict(orient="list")

    def __init__(self, data: Union[DataFrame, None] = None) -> None:
        """
        Initializes the CXData object with data.  Only DataFrame or compatible
         data types are accepted.
        """
        super().__init__(data)

        if data == None:
            self.__data = DataFrame()

        elif not isinstance(data, DataFrame):
            raise TypeError("data must be of type DataFrame or compatible")

        else:
            self.__data = data.copy(deep=True)

    def __copy__(self):
        return CXDataframeData(self.data)

    def __deepcopy__(
            self,
            memo
    ):
        return CXDataframeData(self.data)

    def __hash__(self):
        return hash(repr(self))

    def __lt__(
            self,
            other: 'CXDataframeData'
    ):
        if not object:
            return False

        if type(other) is not CXDataframeData:
            return False

        if self is other:
            return False

        else:
            delta: dict = DeepDiff(
                self.render_to_dict(),
                other.render_to_dict(),
                ignore_order=True
            )
            other_added: int = len(delta.get('dictionary_item_added', []))
            other_removed: int = len(delta.get('dictionary_item_removed', []))

            return (other_added - other_removed) < 0

    def __eq__(
            self,
            other: 'CXDataframeData'
    ):
        if not object:
            return False

        if type(other) is not CXDataframeData:
            return False

        if self is other:
            return True

        else:
            delta: dict = DeepDiff(
                self.render_to_dict(),
                other.render_to_dict(),
                ignore_order=True
            )
            other_added: int = len(delta.get('dictionary_item_added', []))
            other_removed: int = len(delta.get('dictionary_item_removed', []))

            return (other_added - other_removed) == 0

    def __str__(self) -> str:
        return json.dumps(self.render_to_dict())

    def __repr__(self) -> str:
        return f"CXDataframeData(data=" \
               f"DataFrame.from_dict({json.dumps(self.render_to_dict())})" \
               f")"


class CXCSVData(CXDataframeData):
    """
    A CXData class dedicated to processing Python CSV-based, matrix-structured
     data.
    """

    @property
    def data(self) -> str:
        """
        A property accessor for the data managed by the object.
        """
        csv_data: StringIO = StringIO()
        self.__data.to_csv(
            csv_data,
            index=False,
            quoting=csv.QUOTE_NONNUMERIC
        )
        return str(csv_data)

    @data.setter
    def data(self, value: str) -> None:
        if value == None:
            raise TypeError("value cannot be None.")

        elif not isinstance(value, str):
            raise TypeError("value must be type str or compatible.")

        else:
            self.__data = read_csv(value)

    def __init__(self, data: Union[DataFrame, None] = None) -> None:
        """
        Initializes the CXData object with data.  Only DataFrame or compatible
         data types are accepted.
        """
        super().__init__(data)

        if data == None:
            self.__data = DataFrame()

        elif not isinstance(data, str):
            raise TypeError("data must be of type str or compatible")

        else:
            self.__data = read_csv(data)

    def __str__(self) -> str:
        return self.data

    def __repr__(self) -> str:
        return f"CXCSVData(data={self.data})"


class CXSQLData(CXDataframeData):
    """
    A CXData class dedicated to processing Python SQL-based, matrix-structured
     data.
    """

    @CXDataframeData.data.setter
    def data(self, value: dict) -> None:
        if value == None:
            raise TypeError("value cannot be None.")

        elif not isinstance(value, dict):
            raise TypeError("value must be type dict or compatible.")

        else:
            if not value.get('sql') or not value.get('con'):
                raise ValueError("value must have members sql and con")

            self.__data = read_sql_query(
                sql=value['sql'],
                con=value['con']
            )

    def __init__(self, data: Union[dict, None] = None) -> None:
        """
        Initializes the CXData object with data.  Only DataFrame or compatible
         data types are accepted.
        """
        super().__init__(data)

        if data == None:
            self.__data = DataFrame()

        elif not isinstance(data, dict):
            raise TypeError("data must be of dict str or compatible")

        else:
            if not data.get('sql') or not data.get('con'):
                raise ValueError("data must have members sql and con")

            self.__data = read_sql_query(
                sql=data['sql'],
                con=data['con']
            )
