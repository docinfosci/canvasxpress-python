import json
from copy import deepcopy
from functools import total_ordering
from typing import Union

import requests
from deepdiff import DeepDiff

from canvasxpress.data.base import CXKeyPairData, CXDataProfile


@total_ordering
class CXDictData(CXKeyPairData):
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
        Provides a reference to the dict tracked by the object.
        :returns: `dict`
            The associated dictionary, with zero or more keys as appropriate.
        """
        return self.__data

    @data.setter
    def data(self, value: dict) -> None:
        """
        Sets the data associated with the object.
        :param value: `dict`
            The dictionary to be tracked by the object.  `None` will result in
            an empty dict.  A deep copy will be made of a valid `CXDict` or
            `dict` provided.
        """
        if value == None:
            self.__data = dict()

        elif not type(value) in [dict, CXDictData]:
            raise TypeError("value must be type dict or compatible.")

        elif isinstance(value, CXDictData):
            self.__data = deepcopy(value.data)

        else:
            self.__data = deepcopy(value)

    def get_raw_dict_form(self) -> dict:
        """
        Provides a simple dict perspective of the data with no metadata or other
        contextual transformations performed.  For example, if the data is
        natively in `dict` form then it would be passed-through with no
        modification or enhancement.

        This implementation provides matrix data formatted in a `dict` object
        with `DataFrame.to_dict('split')` behaviour.

        :returns: `dict`
            The `dict` perspective of the data with as little modification or
            interpretation as is reasonable.
        """
        return deepcopy(self.data)

    def render_to_dict(self, **kwargs) -> dict:
        """
        Provides a dict representation of the data.
        :returns: `dict`
            The data in `dict` form.
        """
        if self.profile:
            candidate = self.profile.render_to_profiled_dict(self)

        else:
            candidate = self.get_raw_dict_form()

        return candidate

    def __init__(
        self, data: Union[dict, None] = None, profile: Union[CXDataProfile, None] = None
    ) -> None:
        """
        Initializes the CXData object with data.  Only dict or compatible data
        types are accepted.
        :param data: `Union[dict, None]`
            `None` to initialize with an empty dictionary, or a `dict`-like
            object to assign mapped data.
        :param profile: `Union[CXDataProfile, None]`
            Specify the desired profile object to facilitate transformation of
            data into a CanvasXpress JSON data object.  `None` to avoid use of
            a profile.
        """
        super().__init__(data, profile)
        self.data = data

    def __copy__(self) -> "CXDictData":
        """
        *copy constructor* that returns a copy of the CXDictData object.
        :returns: `CXDictData` A copy of the wrapping object.
        """
        return self.__class__(self.data)

    def __deepcopy__(self, memo) -> "CXDictData":
        """
        *deepcopy constructor* that returns a copy of the CXDictData object.
        :returns: `CXDictData` A copy of the wrapping object and deepcopy of
            the tracked data.
        """
        return self.__class__(deepcopy(self.data))

    def __lt__(self, other: "CXDictData") -> bool:
        """
        *less than* comparison.  Also see `@total_ordering` in `functools`.
        :param other:
            `CXDictData` The object to compare.
        :returns: `bool`
            <ul>
            <li> If `other` is `None` then `False`
            <li> If `other` is not a `CXDictData` object then False
            <li> If `other` is a `CXDictData` object then True of all
                `CXDictData` objects are also less than the data tracked by
                `self`.
            </ul>
        """
        if other is None:
            return False

        if not isinstance(other, CXDictData):
            return False

        else:
            delta: dict = DeepDiff(self.data, other.data, ignore_order=True)
            other_added: int = len(delta.get("dictionary_item_added", []))
            other_removed: int = len(delta.get("dictionary_item_removed", []))

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

    def __eq__(self, other: "CXDictData") -> bool:
        """
        *equals* comparison.  Also see `@total_ordering` in `functools`.
        :param other:
            `CXDictData` The object to compare.
        :returns: `bool`
            <ul>
            <li> If `other` is `None` then `False`
            <li> If `other` is not a `CXDictData` object then False
            <li> If `other` is a `CXDictData` object then True of all
                `CXDictData` objects are also equal to the data tracked by
                `self`.
            </ul>
        """
        if other is None:
            return False

        if not isinstance(other, CXDictData):
            return False

        else:
            delta: dict = DeepDiff(self.data, other.data, ignore_order=True)
            other_added: int = len(delta.get("dictionary_item_added", []))
            other_removed: int = len(delta.get("dictionary_item_removed", []))

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
        """
        *str* function.  Converts the CXDictData object into a JSON
        representation.
        :returns" `str` JSON form of the `CXDictData`.
        """
        return json.dumps(self.data)

    def __repr__(self) -> str:
        """
        *repr* function.  Converts the CXDictData object into a pickle string
        that can be used with `eval` to establish a copy of the object.
        :returns: `str` An evaluatable representation of the object.
        """
        return f"CXDictData(data={json.dumps(self.data)})"


class CXJSONData(CXDictData):
    """
    A CXData class dedicated to processing JSON data.
    """

    @property
    def json(self) -> str:
        """
        Provides a copy of the JSON tracked by the object.
        :returns: `str`
            The associated JSON, with zero or more keys as appropriate.
        """
        return str(self)

    @json.setter
    def json(self, value: Union[dict, str]) -> None:
        """
        Sets the data associated with the object.
        :param value: `str`
            The JSON to be tracked by the object.  `None` will result in
            an empty JSON.  If `value` is URL beginning with *http/s*
            then `json` will attempt to download the data.
        """
        if isinstance(value, str) and value.lower().startswith("http"):
            try:
                result = requests.get(value, allow_redirects=True)
                self.data = result.json()

            except Exception as e:
                raise ValueError(
                    "Detected URL but cannot access JSON data at endpoint."
                )

        else:
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

    def __init__(
        self,
        data: Union[dict, str, None] = None,
        profile: Union[CXDataProfile, None] = None,
    ) -> None:
        """
        Initializes the CXData object with data.  Only dict or compatible data
        types are accepted.
        :param data: `Union[dict, str, None]`
            `None` to initialize with an empty JSON, or a JSON/`dict`-like
            object to assign mapped data.
        :param profile: `Union[CXDataProfile, None]`
            Specify the desired profile object to facilitate transformation of
            data into a CanvasXpress JSON data object.  `None` to avoid use of
            a profile.
        """
        super().__init__(data, profile)

    def __copy__(self) -> "CXJSONData":
        """
        *copy constructor* that returns a copy of the CXDictData objct.
        :returns: `CXDictData` A copy of the wrapping object.
        """
        return CXJSONData(self.data)

    def __deepcopy__(self, memo) -> "CXJSONData":
        """
        *deepcopy constructor* that returns a copy of the CXJSONData object.
        :returns: `CXJSONData` A copy of the wrapping object and deepcopy of
            the tracked data.
        """
        return CXJSONData(self.data)

    def __repr__(self) -> str:
        """
        *repr* function.  Converts the CXJSONData object into a pickle string
        that can be used with `eval` to establish a copy of the object.
        :returns: `str` An evaluatable representation of the object.
        """
        return f"CXJSONData(data={str(self.data)})"
