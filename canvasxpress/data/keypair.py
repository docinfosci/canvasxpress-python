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

        elif not isinstance(value, dict):
            raise TypeError("value must be type dict or compatible.")

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

        if data == None:
            self.__data = dict()

        elif not isinstance(data, dict):
            raise TypeError("data must be of type dict or compatible")

        else:
            self.__data = deepcopy(data)

    def __copy__(self):
        return CXDictData(self.data)

    def __deepcopy__(
            self,
            memo
    ):
        return CXDictData(self.data)

    def __hash__(self):
        return hash(repr(self))

    def __lt__(
            self,
            other: 'CXDictData'
    ):
        if not object:
            return False

        if type(other) is not CXDictData:
            return False

        if self is other:
            return False

        else:
            delta: dict = DeepDiff(
                self.data,
                other.data,
                ignore_order=True
            )
            other_added: int = len(delta.get('dictionary_item_added', []))
            other_removed: int = len(delta.get('dictionary_item_removed', []))

            return (other_added - other_removed) < 0

    def __eq__(
            self,
            other: 'CXDictData'
    ):
        if not object:
            return False

        if type(other) is not CXDictData:
            return False

        if self is other:
            return True

        else:
            delta: dict = DeepDiff(
                self.data,
                other.data,
                ignore_order=True
            )
            other_added: int = len(delta.get('dictionary_item_added', []))
            other_removed: int = len(delta.get('dictionary_item_removed', []))

            return (other_added - other_removed) == 0

    def __str__(self) -> str:
        return json.dumps(self.data)

    def __repr__(self) -> str:
        return f"CXDictData(data={json.dumps(self.data)})"


class CXJSONData(CXDictData):
    """
    A CXData class dedicated to processing JSON data.
    """

    @property
    def data(self) -> str:
        """
        A property accessor for the data managed by the object.
        """
        return json.dumps(
            self.__data,
            indent=4
        )

    @CXDictData.data.setter
    def data(self, value: Union[dict, str]) -> None:
        if value == None:
            raise TypeError("value cannot be None.")

        elif not isinstance(value, dict):
            try:
                candidate = json.loads(value)
                super().data = candidate

            except Exception as e:
                raise TypeError(
                    f"value must be type JSON or compatible: {e}"
                )

        else:
            super().data = json.loads(value)

    def __init__(self, data: Union[dict, str, None] = None) -> None:
        """
        Initializes the CXData object with data.  Only dict or compatible data
        types are accepted.
        """
        super().__init__(data)

    def __copy__(self):
        return CXJSONData(self.data)

    def __deepcopy__(
            self,
            memo
    ):
        return CXJSONData(self.data)

    def __hash__(self):
        return hash(repr(self))

    def __lt__(
            self,
            other: 'CXJSONData'
    ):
        if not object:
            return False

        if not isinstance(other, CXJSONData):
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
            other: 'CXJSONData'
    ):
        if not object:
            return False

        if type(other) is not CXJSONData:
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
        return json.dumps(
            self.data,
            indent=4
        )

    def __repr__(self) -> str:
        return f"CXJSONData(data={json.dumps(self.data)})"
