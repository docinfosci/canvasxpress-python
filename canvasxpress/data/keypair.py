import json
from copy import deepcopy
from functools import total_ordering
from typing import Union

from deepdiff import DeepDiff

from canvasxpress.data.base import CXData


@total_ordering
class CXDictData(CXData):
    """
    A CXData class dedicated to processing Python dict-structured data.
    """

    __data: dict = dict()
    """
    The data managed by an object of this class.
    """

    @property
    def data(self) -> dict:
        """
        A property accessor for the data managed by the object.
        """
        return self.__data

    @data.setter
    def data(self, value: dict) -> None:
        if value == None:
            raise TypeError("value cannot be None.")

        elif not type(value) in [dict, CXDictData]:
            raise TypeError("value must be type dict or compatible.")

        elif isinstance(value, CXDictData):
            self.__data = deepcopy(value.data)

        else:
            self.__data = deepcopy(value)

    def render_to_dict(self) -> dict:
        """
        Provides a dict representation of the data.
        :return: The JSON as a str
        """
        return deepcopy(self.data)

    def __init__(self, data: Union[dict, None] = None) -> None:
        """
        Initializes the CXData object with data.  Only dict or compatible data
        types are accepted.
        """
        super().__init__(data)
        self.__data = dict()

        if data is not None:
            self.data = data

    def __copy__(self):
        return CXDictData(self.data)

    def __deepcopy__(
            self,
            memo
    ):
        return CXDictData(self.data)

    def __lt__(
            self,
            other: 'CXDictData'
    ):
        if other is None:
            return False

        if not isinstance(other, CXDictData):
            return False

        else:
            delta: dict = DeepDiff(
                self.data,
                other.data,
                ignore_order=True
            )
            other_added: int = len(delta.get('dictionary_item_added', []))
            other_removed: int = len(delta.get('dictionary_item_removed', []))

            if (other_added - other_removed) == 0:
                for skey in self.data.keys():
                    if not skey in other.data.keys():
                        for okey in other.data.keys():
                            if skey < okey:
                                return True

                    elif self.data[skey] < other.data[skey]:
                        return True

                return False

            else:
                return (other_added - other_removed) > 0

    def __eq__(
            self,
            other: 'CXDictData'
    ):
        if other is None:
            return False

        if not isinstance(other, CXDictData):
            return False

        else:
            delta: dict = DeepDiff(
                self.data,
                other.data,
                ignore_order=True
            )
            other_added: int = len(delta.get('dictionary_item_added', []))
            other_removed: int = len(delta.get('dictionary_item_removed', []))

            if (other_added - other_removed) == 0:
                for skey in self.data.keys():
                    if not skey in other.data.keys():
                        return False

                    elif self.data[skey] != other.data[skey]:
                        return False

                return True

            else:
                return False

    def __str__(self) -> str:
        return json.dumps(self.data)

    def __repr__(self) -> str:
        return f"CXDictData(data={json.dumps(self.data)})"


class CXJSONData(CXDictData):
    """
    A CXData class dedicated to processing JSON data.
    """

    @property
    def json(self) -> str:
        return str(self)

    @json.setter
    def json(self, value: Union[dict, str]) -> None:
        self.data = value

    @CXDictData.data.setter
    def data(self, value: Union[dict, str]) -> None:
        if isinstance(value, CXJSONData):
            CXDictData.data.fset(self, value.data)

        elif isinstance(value, str):
            candidate = json.loads(value)
            CXDictData.data.fset(self, candidate)

        else:
            CXDictData.data.fset(self, value)

    def __init__(self, data: Union[dict, str, None] = None) -> None:
        """
        Initializes the CXData object with data.  Only dict or compatible data
        types are accepted.
        """
        super().__init__()
        if data is not None:
            self.json = data

    def __copy__(self):
        return CXJSONData(self.data)

    def __deepcopy__(
            self,
            memo
    ):
        return CXJSONData(self.data)

    def __repr__(self) -> str:
        return f"CXJSONData(data={str(self.data)})"
