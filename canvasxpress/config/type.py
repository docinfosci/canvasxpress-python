import json
from abc import ABC, abstractmethod
from copy import deepcopy
from enum import Enum
from functools import total_ordering
from typing import Union, Any

from deepdiff import DeepDiff


@total_ordering
class CXConfig(ABC):
    """
    CXConfig provides the means by which CanvasXpress objects can be configured for
    customized rendering and interaction.
    """

    __label: str = ""
    """
    The configuration object's label.
    """

    @property
    def label(self) -> str:
        """
        Provides the label for the configuration.
        :returns: `str`
        """
        return self.__label

    @property
    @abstractmethod
    def value(self) -> Any:
        """
        Provides the value for the configuration.  Must be implemented by
        concrete classes.
        :returns: `Any`
            The relevant type of value.
        """
        pass

    @value.setter
    @abstractmethod
    def value(self, value: Any) -> None:
        """
        Sets the value of the configuration.  Must be implemented by concrete
        classes.
        :param value: `Any`
            The value to be accepted.  Will be more specific with concrete
            implementations, such as `str` for string configurations.
        """
        pass

    def __init__(
            self,
            label: str,
            value: Any
    ):
        """
        Initializes a new CXConfig object with a label and value.
        :param label: `str`
            The label for the configuration.
        :param value: `Any`
            The value for the configuration.  See the `value` property for the
            concrete implementation for allowed types.
        """
        if label is None:
            raise ValueError("label cannot be None")
        self.__label = label

    def __copy__(self) -> 'CXConfig':
        """
        *copy constructor* that provides a new CXConfig of the same type with
        the data referenced.
        :returns: `CXConfig` of the proper type
        """
        return self.__class__(
            self.label,
            self.value
        )

    def __deepcopy__(
            self,
            memo
    ):
        """
        *deepcopy constructor* that provides a new CXConfig of the same type with
        the a deepcopy of the data.
        :returns: `CXConfig` of the proper type
        """
        return self.__class__(
            self.label,
            deepcopy(self.value)
        )

    def __hash__(self) -> int:
        """
        Provides a hash proxy for the object as converted into its `repr` form.
        :returns: `int`
        """
        return hash(repr(self))

    def __lt__(
            self,
            other: 'CXConfig'
    ) -> bool:
        """
        *less than* comparison.  Also see `@total_ordering` in `functools`.
        :param other:
            `CXConfig` The object to compare.
        :returns: `bool`
            <ul>
            <li> If `other` is `None` then `False`
            <li> If `other` is not a `CXConfig` object then `False`
            <li> If `other` is a `CXConfig` object then True if label and value
                of `other` are less than that of `self`.
            </ul>
        """
        if other is None:
            return False

        if not isinstance(other, self.__class__):
            return False

        if self.label < other.label:
            return True

        elif self.label == other.label:
            if self.value < other.value:
                return True

            else:
                return False

    def __eq__(
            self,
            other: 'CXConfig'
    ) -> bool:
        """
        *equals* comparison.  Also see `@total_ordering` in `functools`.
        :param other:
            `CXConfig` The object to compare.
        :returns: `bool`
            <ul>
            <li> If `other` is `None` then `False`
            <li> If `other` is not a `CXConfig` object then `False`
            <li> If `other` is a `CXConfig` object then True if label and value
                of `other` are equal to that of `self`.
            </ul>
        """
        if other is None:
            return False

        if not isinstance(other, self.__class__):
            return False

        return (self.label == other.label) and (self.value == other.value)

    def __str__(self) -> str:
        """
        *str* function.  Converts the object into a JSON string.
        """
        return json.dumps(
            {
                "label": self.label,
                "value": self.value,
            }
        )

    def __repr__(self) -> str:
        """
        *repr* function.  Converts the CXConfig object into a pickle string
        that can be used with `eval` to establish a copy of the object.
        :returns: `str` An evaluatable representation of the object.
        """
        return f"{str(self.__class__).split('.')[-1][:-2]}(" \
               f" label='{self.label}'," \
               f" value={json.dumps(self.value)}" \
               f")"


class CXString(CXConfig):
    """
    A `CXConfig` object that manages `str` values.
    """
    __value: str = ""
    """
    The managed value.
    """

    @property
    def value(self) -> str:
        """
        Provides the value for the configuration.
        :returns: `str`
        """
        return self.__value

    @value.setter
    def value(self, value: Union[object, str]) -> None:
        """
        Sets the value of the configuration.
        :param value: `str`
            If `None` then an empty `str` will be used.
        """
        if value is None:
            self.__value = ""
        else:
            self.__value = str(value)

    def __init__(self, label: str, value: str):
        """
        Initializes the configuration with a `str` value.
        """
        super().__init__(label, value)
        self.value = value


class CXBool(CXConfig):
    """
    A `CXConfig` object that manages `bool` values.
    """
    __value: bool = False
    """
    The managed value.
    """

    @property
    def value(self) -> bool:
        """
        Provides the value for the configuration.
        :returns: `bool`
        """
        return self.__value

    @value.setter
    def value(self, value: Union[object, bool]) -> None:
        """
        Sets the value of the configuration.
        :param value: `bool`
            If `None` then `False` will be used.
        """
        if value is None:
            self.__value = False
        else:
            self.__value = bool(value)

    def __init__(self, label: str, value: bool):
        """
        Initializes the configuration with a `bool` value.
        """
        super().__init__(label, value)
        self.value = value

    def __str__(self) -> str:
        """
        *str* function.  Converts the object into a Javascript statement.
        """
        return str(
            {
                "label": self.label,
                "value": self.value,
            }
        )

    def __repr__(self) -> str:
        """
        *repr* function.  Converts the CXBool object into a pickle string
        that can be used with `eval` to establish a copy of the object.
        :returns: `str` An evaluatable representation of the object.
        """
        return f"{str(self.__class__).split('.')[-1][:-2]}(" \
               f" label='{self.label}'," \
               f" value={str(self.value)}" \
               f")"


class CXFloat(CXConfig):
    """
    A `CXConfig` object that manages `float` values.
    """
    __value: float = 0.0
    """
    The managed value.
    """

    @property
    def value(self) -> float:
        """
        Provides the value for the configuration.
        :returns: `float`
        """
        return self.__value

    @value.setter
    def value(self, value: Union[object, float]) -> None:
        """
        Sets the value of the configuration.
        :param value: `float`
            If `None` then `float(0.0)` will be used.
        """
        if value is None:
            self.__value = 0.0
        else:
            self.__value = float(value)

    def __init__(self, label: str, value: float):
        """
        Initializes the configuration with a `float` value.
        """
        super().__init__(label, value)
        self.__value = 0.0

        self.value = value


class CXInt(CXConfig):
    """
    A `CXConfig` object that manages `int` values.
    """
    __value: int = 0
    """
    The managed value.
    """

    @property
    def value(self) -> int:
        """
        Provides the value for the configuration.
        :returns: `int`
        """
        return self.__value

    @value.setter
    def value(self, value: Union[object, int]) -> None:
        """
        Sets the value of the configuration.
        :param value: `int`
            If `None` then `int(0)` will be used.
        """
        if value is None:
            self.__value = 0
        else:
            self.__value = int(value)

    def __init__(self, label: str, value: int):
        """
        Initializes the configuration with an `int` value.
        """
        super().__init__(label, value)
        self.__value = 0

        self.value = value


class CXDict(CXConfig):
    """
    A `CXConfig` object that manages `dict` values.
    """
    __value: dict = dict()
    """
    The managed value.
    """

    @property
    def value(self) -> dict:
        """
        Provides the value for the configuration.
        :returns: `dict`
        """
        return self.__value

    @value.setter
    def value(self, value: Union[dict, str, None]) -> None:
        """
        Sets the value of the configuration.
        :param value: `dict`
            If `None` then `dict()` will be used.
        """
        if value is None:
            self.__value = dict()

        elif isinstance(value, CXDict):
            self.__value = deepcopy(value.value)

        elif isinstance(value, str):
            candidate = json.loads(value)
            self.__value = candidate

        else:
            self.__value = deepcopy(value)

    def __init__(self, label: str, value: Union[dict, str, None]) -> None:
        """
        Initializes the CXData object with data.  Only dict or compatible data
        types are accepted.
        """
        super().__init__(label, value)
        self.value = value

    def __lt__(
            self,
            other: 'CXDict'
    ) -> bool:
        """
        *less than* comparison.  Also see `@total_ordering` in `functools`.
        :param other:
            `CXDict` The object to compare.
        :returns: `bool`
            <ul>
            <li> If `other` is `None` then `False`
            <li> If `other` is not a `CXDict` object then `False`
            <li> If `other` is a `CXDict` object then True if the label and
                value parts are less than that of self.
            </ul>
        """
        if other is None:
            return False

        if not isinstance(other, CXDict):
            return False

        if self.label < other.label:
            return True

        if self.label > other.label:
            return False

        else:
            delta: dict = DeepDiff(
                self.value,
                other.value,
                ignore_order=True
            )
            other_added: int = len(delta.get('dictionary_item_added', []))
            other_removed: int = len(delta.get('dictionary_item_removed', []))

            if (other_added - other_removed) == 0:
                for skey in self.value.keys():
                    if skey not in other.value.keys():
                        for okey in other.value.keys():
                            if skey < okey:
                                return True

                    elif self.value[skey] < other.value[skey]:
                        return True

                return False

            else:
                return (other_added - other_removed) > 0

    def __eq__(
            self,
            other: 'CXDict'
    ) -> bool:
        """
        *equals* comparison.  Also see `@total_ordering` in `functools`.
        :param other:
            `CXDict` The object to compare.
        :returns: `bool`
            <ul>
            <li> If `other` is `None` then `False`
            <li> If `other` is not a `CXDict` object then `False`
            <li> If `other` is a `CXDict` object then True if the label and
                value parts are equal to that of self.
            </ul>
        """
        if other is None:
            return False

        elif not isinstance(other, CXDict):
            return False

        elif self.label < other.label:
            return False

        elif self.label > other.label:
            return False

        else:
            delta: dict = DeepDiff(
                self.value,
                other.value,
                ignore_order=True
            )
            other_added: int = len(delta.get('dictionary_item_added', []))
            other_removed: int = len(delta.get('dictionary_item_removed', []))

            if (other_added - other_removed) == 0:
                for skey in self.value.keys():
                    if skey not in other.value.keys():
                        return False

                    elif self.value[skey] != other.value[skey]:
                        return False

                return True

            else:
                return False

    def __repr__(self) -> str:
        """
        *repr* function.  Converts the CXDict object into a pickle string
        that can be used with `eval` to establish a copy of the object.
        :returns: `str` An evaluatable representation of the object.
        """
        return f"CXDict(label='{self.label}', value={json.dumps(self.value)})"


class CXList(CXConfig):
    """
    A `CXConfig` object that manages `list` values.
    """
    __value: list = list()
    """
    The managed value.
    """

    @property
    def value(self) -> list:
        """
        Provides the value for the configuration.
        :returns: `list`
        """
        return self.__value

    @value.setter
    def value(self, value: Union[object, list]) -> None:
        """
        Sets the value of the configuration.
        :param value: `list`
            If `None` then `list()` will be used.
        """
        if value is None:
            self.__value = list()
        else:
            self.__value = list(value)

    def __init__(self, label: str, value: list):
        """
        Initializes the configuration with a `list` value.
        """
        super().__init__(label, value)
        self.__value = list()

        self.value = value


class CXRGBAColor(CXDict):
    """
    A `CXConfig` object that manages `str` Javascript rgba() values.
    """

    @staticmethod
    def is_color_str(value: str):
        """
        A static method that evaluates a given string to see if it represents a
        Javascript rgba() statement.
        :param value: `str`
            A string to evaluate.  A valid Javascript value has the form
            `rgba(r, g, b, a)` where RGB values are `int` from 0-255 and A is a
            `float` from 0.0 to 1.0.
        :returns: `bool`
            True if the string represents a Javascript rgba() statement.
        """
        if isinstance(value, str):
            if not value.startswith("rgba"):
                return False

            try:
                components = value.split(',')
                if len(components) != 4:
                    return False

                r = components[0].strip().split("rgba(")[1]
                g = components[1].strip()
                b = components[2].strip()
                a = components[3].strip().split(')')[0]

                for x in [int(r), int(g), int(b)]:
                    if (x < 0) or (x > 255):
                        return False
                for x in [float(a)]:
                    if (x < 0) or (x > 1):
                        return False

                return True

            except:
                return False

        else:
            return False

    @staticmethod
    def is_color_list(value: list):
        """
        A static method that evaluates a given list to see if it represents a
        Javascript rgba() statement.
        :param value: `list`
            A list to evaluate.  A valid Javascript value has the form
            `rgba(r, g, b, a)` where RGB values are `int` from 0-255 and A is a
            `float` from 0.0 to 1.0.
        :returns: `bool`
            True if the list represents a Javascript rgba() statement.
        """
        if isinstance(value, list):
            try:
                list_len = len(value)
                all_rgb_elements_int = all(
                    isinstance(x, int) for x in value[:3]
                )
                alpha_element_num = type(value[3]) in [int, float]
                if (not list_len == 4) or \
                        (not all_rgb_elements_int) or \
                        (not alpha_element_num):
                    return False

                for x in value[:3]:
                    if (x < 0) or (x > 255):
                        return False
                if (value[3] < 0) or (value[3] > 1):
                    return False

                return True

            except:
                return False

        else:
            return False

    @staticmethod
    def is_color_dict(value: dict):
        """
        A static method that evaluates a given dict to see if it represents a
        Javascript rgba() statement.
        :param value: `dict`
            A dict to evaluate.  A valid Javascript value has the form
            `rgba(r, g, b, a)` where RGB values are `int` from 0-255 and A is a
            `float` from 0.0 to 1.0.  For the dict to be valid its keys must be
            lower case r, g, b, and a characters.
        :returns: `bool`
            True if the dict represents a Javascript rgba() statement.
        """
        if isinstance(value, dict):
            list_len = len(value.keys())
            all_rgba_elements = all(
                x in ['r', 'g', 'b', 'a'] for x in value.keys()
            )
            all_rgb_elements_int = all(
                isinstance(value[x], int) for x in value.keys()
                if x in ['r', 'g', 'b']
            )
            alpha_element_num = type(value.get('a')) in [int, float]
            keys_rgba = all([j in ['r', 'g', 'b', 'a'] for j in [k for k in value.keys()]])
            if (not list_len == 4) or \
                    (not all_rgb_elements_int) or \
                    (not keys_rgba) or \
                    (not alpha_element_num) or \
                    (not all_rgba_elements):
                return False

            for key in value.keys():
                if key in ['r', 'g', 'b']:
                    if (value[key] < 0) or (value[key] > 255):
                        return False
                if key in ['a']:
                    if (value[key] < 0) or (value[key] > 1):
                        return False

            return True

        else:
            return False

    @CXDict.value.setter
    def value(self, value: Union['CXRGBAColor', dict, list, str]) -> None:
        """
        Sets the RGBA value from an existing `CXRGBAColor` object, or a `dict`,
        `list`, or `string` following the Javascript `rgba()` format.
        :param value: `Union['CXRGBAColor', dict, list, str]`
            The value to be accepted.  See the `is_color_*()` methods for
            acceptable formats.
        """
        if value is None:
            CXDict.value.fset(
                self,
                {
                    'r': 0,
                    'g': 0,
                    'b': 0,
                    'a': 1.0,
                }
            )

        elif type(value) not in [CXRGBAColor, list, dict, str]:
            raise TypeError(
                "value must be a dict of {'r': int, 'g': int, 'b': int, "
                "'a': float} or a list of [r, g, b, a] or a string of "
                "rgba(int,int,int,float)"
            )

        else:
            if isinstance(value, str):
                if not CXRGBAColor.is_color_str(value):
                    raise ValueError(
                        "str RGBA values must be in the format"
                        " rgb(int,int,int,float)"
                    )
                else:
                    components = value.split(',')
                    r = components[0].strip().split("rgba(")[1]
                    g = components[1].strip()
                    b = components[2].strip()
                    a = components[3].strip().split(')')[0]

                    candidate = {
                        'r': int(r),
                        'g': int(g),
                        'b': int(b),
                        'a': float(a),
                    }

            elif isinstance(value, list):
                if not CXRGBAColor.is_color_list(value):
                    raise ValueError(
                        "list RGBA values must be in the format"
                        " (int,int,int,float)"
                    )
                else:
                    candidate = {
                        'r': value[0],
                        'g': value[1],
                        'b': value[2],
                        'a': value[3],
                    }

            elif isinstance(value, dict):
                if not CXRGBAColor.is_color_dict(value):
                    raise ValueError(
                        "RGBA dict must have three int values for keys"
                        " 'r', 'g', 'b' and a float value for key 'a'"
                    )
                else:
                    candidate = dict(value)

            else:
                candidate = deepcopy(value.value)

            CXDict.value.fset(
                self,
                candidate
            )

    def __init__(
            self,
            label: str,
            value: Union['CXRGBAColor', dict, list, str]
    ):
        """
        Initializes a new CXRGBAColor object using the RGBA value from an
         existing `CXRGBAColor` object, or a `dict`, `list`, or `string`
         following the Javascript `rgba()` format.
        :param value: `Union['CXRGBAColor', dict, list, str]`
            The value to be accepted.  See the `is_color_*()` methods for
            acceptable formats.
        """
        super().__init__(label, {'r': 0, 'g': 0, 'b': 0, 'a': 1})
        self.value = value

    def __str__(self) -> str:
        """
        *str* function.  Converts the object into a JSON string.
        """
        r = self.value['r']
        g = self.value['g']
        b = self.value['b']
        a = self.value['a']
        return json.dumps(
            {
                "label": self.label,
                "value": f"rgba({r},{g},{b},{a})",
            }
        )

    def __repr__(self) -> str:
        """
        *repr* function.  Converts the CXRGBAColor object into a pickle string
        that can be used with `eval` to establish a copy of the object.
        :returns: `str` An evaluatable representation of the object.
        """
        r = self.value['r']
        g = self.value['g']
        b = self.value['b']
        a = self.value['a']
        return f"CXRGBAColor(" \
               f" label={json.dumps(self.label)}," \
               f" value='rgba({r},{g},{b},{a})'" \
               f")"


class CXRGBColor(CXDict):
    """
    A `CXConfig` object that manages `str` Javascript rgb() values.
    """

    @staticmethod
    def is_color_str(value: str):
        """
        A static method that evaluates a given string to see if it represents a
        Javascript rgb() statement.
        :param value: `str`
            A string to evaluate.  A valid Javascript value has the form
            `rgb(r, g, b)` where RGB values are `int` from 0-255.
        :returns: `bool`
            True if the string represents a Javascript rgb() statement.
        """
        if isinstance(value, str):
            if not value.startswith("rgb"):
                return False

            try:
                components = value.split(',')
                if len(components) != 3:
                    return False

                r = components[0].strip().split("rgb(")[1]
                g = components[1].strip()
                b = components[2].strip().split(')')[0]

                for x in [int(r), int(g), int(b)]:
                    if (x < 0) or (x > 255):
                        return False

                return True

            except:
                return False

        else:
            return False

    @staticmethod
    def is_color_list(value: list):
        """
        A static method that evaluates a given list to see if it represents a
        Javascript rgb() statement.
        :param value: `list`
            A list to evaluate.  A valid Javascript value has the form
            `rgb(r, g, b)` where RGB values are `int` from 0-255.
        :returns: `bool`
            True if the list represents a Javascript rgb() statement.
        """
        if isinstance(value, list):
            list_len = len(value)
            all_rgb_elements_int = all(
                isinstance(x, int) for x in value[:2]
            )
            if (not list_len == 3) or (not all_rgb_elements_int):
                return False

            for x in value[:3]:
                if (x < 0) or (x > 255):
                    return False

            return True

        else:
            return False

    @staticmethod
    def is_color_dict(value: dict):
        """
        A static method that evaluates a given dict to see if it represents a
        Javascript rgb() statement.
        :param value: `dict`
            A dict to evaluate.  A valid Javascript value has the form
            `rgba(r, g, b)` where RGB values are `int` from 0-255.  For the dict
             to be valid its keys must be lower case r, g, and b characters.
        :returns: `bool`
            True if the dict represents a Javascript rgb() statement.
        """
        if isinstance(value, dict):
            list_len = len(value.keys())
            all_rgb_elements = all(
                x in ['r', 'g', 'b', ] for x in value.keys()
            )
            all_rgb_elements_int = all(
                isinstance(value[x], int) for x in value.keys()
                if x in ['r', 'g', 'b']
            )
            keys_rgb = all([j in ['r', 'g', 'b'] for j in [k for k in value.keys()]])
            if (not list_len == 3) or \
                    (not all_rgb_elements) or \
                    (not all_rgb_elements_int) or \
                    (not keys_rgb):
                return False

            for key in value.keys():
                if key in ['r', 'g', 'b']:
                    if (value[key] < 0) or (value[key] > 255):
                        return False

            return True

        else:
            return False

    @CXDict.value.setter
    def value(self, value: Union['CXRGBColor', dict, list, str]) -> None:
        """
        Sets the RGB value from an existing `CXRGBColor` object, or a `dict`,
        `list`, or `string` following the Javascript `rgb()` format.
        :param value: `Union['CXRGBColor', dict, list, str]`
            The value to be accepted.  See the `is_color_*()` methods for
            acceptable formats.
        """
        if value is None:
            CXDict.value.fset(
                self,
                {
                    'r': 0,
                    'g': 0,
                    'b': 0,
                }
            )

        elif type(value) not in [CXRGBColor, list, dict, str]:
            raise TypeError(
                "value must be a dict of {'r': int, 'g': int, 'b': int}"
                " or a list of [r, g, b] or a string of "
                "rgb(int,int,int)"
            )

        else:
            if isinstance(value, str):
                if not CXRGBColor.is_color_str(value):
                    raise ValueError(
                        "str RGB values must be in the format"
                        " rgb(int,int,int)"
                    )
                else:
                    components = value.split(',')
                    r = components[0].strip().split("rgb(")[1]
                    g = components[1].strip()
                    b = components[2].strip().split(')')[0]

                    candidate = {
                        'r': int(r),
                        'g': int(g),
                        'b': int(b),
                    }

            elif isinstance(value, list):
                if not CXRGBColor.is_color_list(value):
                    raise ValueError(
                        "list RGB values must be in the format"
                        " (int,int,int)"
                    )
                else:
                    candidate = {
                        'r': value[0],
                        'g': value[1],
                        'b': value[2],
                    }

            elif isinstance(value, dict):
                if not CXRGBColor.is_color_dict(value):
                    raise ValueError(
                        "RGB dict must have three int values for keys"
                        " 'r', 'g', 'b'"
                    )
                else:
                    candidate = dict(value)

            else:
                candidate = deepcopy(value.value)

            CXDict.value.fset(
                self,
                candidate
            )

    def __init__(
            self,
            label: str,
            value: Union['CXRGBColor', dict, list, str]
    ):
        """
        Initializes a new CXRGBColor object using the RGB value from an
         existing `CXRGBColor` object, or a `dict`, `list`, or `string`
         following the Javascript `rgb()` format.
        :param value: `Union['CXRGBColor', dict, list, str]`
            The value to be accepted.  See the `is_color_*()` methods for
            acceptable formats.
        """
        super().__init__(label, {'r': 0, 'g': 0, 'b': 0})
        self.value = value

    def __str__(self) -> str:
        """
        *str* function.  Converts the object into a JSON string.
        """
        r = self.value['r']
        g = self.value['g']
        b = self.value['b']
        return json.dumps(
            {
                "label": self.label,
                "value": f"rgb({r},{g},{b})",
            }
        )

    def __repr__(self) -> str:
        """
        *repr* function.  Converts the CXRGBColor object into a pickle string
        that can be used with `eval` to establish a copy of the object.
        :returns: `str` An evaluatable representation of the object.
        """
        r = self.value['r']
        g = self.value['g']
        b = self.value['b']
        return f"CXRGBColor(" \
               f" label={json.dumps(self.label)}," \
               f" value='rgb({r},{g},{b})'" \
               f")"


class CXGraphTypeOptions(Enum):
    """
    A set of known chart types permitted for use with CanvasXpress objects.  If
    a chart not yet identified in this list is required then use a `CXString`
    object with the label `graphType` and the value set to the name of the
    chart to be used.
    """
    Area = "Area"
    AreaLine = "AreaLine"
    Bar = "Bar"
    BarLine = "BarLine"
    Boxplot = 'Boxplot'
    Bubble = 'Bubble'
    Chord = 'Chord'
    Circular = 'Circular'
    Contour = 'Contour'
    Correlation = 'Correlation'
    Dashboard = 'Dashboard'
    Density = 'Density'
    Donnut = 'Donnut'
    DotLine = 'DotLine'
    Dotplot = 'Dotplot'
    Facet = 'Facet'
    Fish = 'Fish'
    Gantt = 'Gantt'
    Genome = 'Genome'
    Heatmap = 'Heatmap'
    Histogram = 'Histogram'
    Kaplan_Meier = 'Kaplan - Meier'
    Layout = 'Layout'
    Line = 'Line'
    Map = 'Map'
    Meter = 'Meter'
    Network = 'Network'
    NonLinear_Fit = 'NonLinear - Fit'
    Oncoprint = 'Oncoprint'
    ParallelCoordinates = 'ParallelCoordinates'
    Pie = 'Pie'
    Radar = 'Radar'
    Remote_Graphs = 'Remote - Graphs'
    Ridge_Line = 'Ridge - Line'
    SPLOM = 'SPLOM'
    Sankey = 'Sankey'
    Scatter2D = 'Scatter2D'
    Scatter3D = 'Scatter3D'
    ScatterBubble2D = 'ScatterBubble2D'
    Stacked = 'Stacked'
    StackedLine = 'StackedLine'
    StackedPercent = 'StackedPercent'
    StackedPercentLine = 'StackedPercentLine'
    Sunburst = 'Sunburst'
    TCGA = 'TCGA'
    TagCloud = 'TagCloud'
    Tree = 'Tree'
    Treemap = 'Treemap'
    Venn = 'Venn'
    Violin = 'Violin'


class CXGraphType(CXString):
    """
    A CXString that is aware of CanvasXpress types of graphs, such as 'Bar'.
    """

    CX_ATTRIBUTE = "graphType"

    @CXString.value.setter
    def value(self, value: Union[CXGraphTypeOptions, str]) -> None:
        """
        Sets the value using a known CanvasXpress option.
        """
        if value is None:
            raise ValueError("value cannot be None.")

        elif isinstance(value, CXGraphTypeOptions):
            CXString.value.fset(self, value.value)

        elif str(value) not in list(map(str, CXGraphTypeOptions.__members__)):
            raise ValueError("value must be a known type.")

        else:
            CXString.value.fset(self, str(value))

    def set_custom_value(self, value: str):
        """
        Permits a js value to be set, such as if a new option is recently
        made available that the Python framework is yet to be aware of.
        :param value: `str`
            The string value to set.
        """
        CXString.value.fset(self, value)

    def __init__(
            self,
            type: Union[CXGraphTypeOptions, str] = CXGraphTypeOptions.Bar
    ):
        """
        Initializes a new CXGraphType object with a value corresponding to one
        of the values provided by `CXGraphTypeOptions`.
        """
        if isinstance(type, CXGraphTypeOptions):
            super().__init__(
                self.CX_ATTRIBUTE,
                type.value
            )

        else:
            super().__init__(
                self.CX_ATTRIBUTE,
                type
            )
