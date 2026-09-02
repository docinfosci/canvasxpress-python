import html
import json
from abc import ABC, abstractmethod
from copy import deepcopy
from enum import Enum
from functools import total_ordering
from typing import Union, Any

from deepdiff import DeepDiff
from deprecated import deprecated


@total_ordering
class CXConfig(ABC):
    """CXConfig provides the means by which CanvasXpress objects can be
    configured for customized rendering and interaction."""

    __label: str = ""
    """The configuration object's label."""

    __extra: tuple = ()
    """Additional trailing elements beyond `label` and `value` that were
    imported when the configuration was created from a multi-element list."""

    @property
    def extra(self) -> tuple:
        """Provides any trailing elements beyond `label` and `value` that were
        originally imported with the configuration.

        Returns:
            `tuple`: The trailing elements, if any, otherwise an empty `tuple`.
        """
        return self.__extra

    @extra.setter
    def extra(self, extra: Union[tuple, list]) -> None:
        """Sets the trailing elements associated with the configuration.

        Args:
            extra: `Union[tuple, list]` The trailing elements to associate.
        """
        if extra is None:
            self.__extra = ()
        else:
            self.__extra = tuple(extra)

    @property
    def label(self) -> str:
        """Provides the label for the configuration.

        Returns:
            `str`: The label for the configuration.
        """
        return self.__label

    @property
    @abstractmethod
    def value(self) -> Any:
        """Provides the value for the configuration. Must be implemented by
        concrete classes.

        Returns:
            `Any`: The relevant type of value.
        """
        pass

    @value.setter
    @abstractmethod
    def value(self, value: Any) -> None:
        """Sets the value of the configuration. Must be implemented by
        concrete classes.

        Args:
            value: `Any` The value to be accepted. Will be more specific with
                concrete implementations, such as `str` for string
                configurations.
        """
        pass

    def render(self) -> dict:
        """Renders the value in a form suitable for use in preparing Javascript.
        Typically, this will be the native `value`.

        Returns:
            `dict`: A version of the `value` most appropriate for use in
            preparing the Javascript rendering.
        """
        return {self.label: self.value}

    def __init__(self, label: str, value: Any):
        """Initializes a new CXConfig object with a label and value.

        Args:
            label: `str` The label for the configuration.
            value: `Any` The value for the configuration. See the `value`
                property for the concrete implementation for allowed types.
        """
        if label is None:
            raise ValueError("label cannot be None")
        self.__label = label

    def __copy__(self) -> "CXConfig":
        """*copy constructor* that provides a new CXConfig of the same type
        with the data referenced.

        Returns:
            `CXConfig` of the proper type
        """
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        """*deepcopy constructor* that provides a new CXConfig of the same
        type with a deepcopy of the data.

        Returns:
            `CXConfig` of the proper type
        """
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def __hash__(self) -> int:
        """Provides a hash proxy for the object as converted into its `repr`
        form.

        Returns:
            `int`: The hash value of the object's repr form.
        """
        return hash(repr(self))

    def __lt__(self, other: "CXConfig") -> bool:
        """*less than* comparison. Also see `@total_ordering` in `functools`.

        Args:
            other: `CXConfig` The object to compare.

        Returns:
            `bool`: True if self is less than other. False if `other` is
                `None`, if `other` is not a `CXConfig` object of the same
                class, or if label/value of `other` is not less than `self`.
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

    def __eq__(self, other: "CXConfig") -> bool:
        """*equals* comparison. Also see `@total_ordering` in `functools`.

        Args:
            other: `CXConfig` The object to compare.

        Returns:
            `bool`: True if self equals other. False if `other` is `None`,
                if `other` is not a `CXConfig` object of the same class, or
                if label/value of `other` is not equal to `self`.
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
        """*repr* function. Converts the CXConfig object into a pickle string
        that can be used with `eval` to establish a copy of the object.

        Returns:
            `str`: An evaluatable representation of the object.
        """
        return (
            f"{str(self.__class__).split('.')[-1][:-2]}("
            f" label='{self.label}',"
            f" value={json.dumps(self.value)}"
            f")"
        )


class CXString(CXConfig):
    """A `CXConfig` object that manages `str` values."""

    __value: str = ""
    """The managed value."""

    @property
    def value(self) -> str:
        """Provides the value for the configuration.

        Returns:
            `str`: The string value for the configuration.
        """
        return self.__value

    @value.setter
    def value(self, value: Union[object, str]) -> None:
        """Sets the value of the configuration.

        Args:
            value: `str` If `None` then an empty `str` will be used.
        """
        if value is None:
            self.__value = ""
        else:
            self.__value = str(value)

    def __init__(self, label: str, value: str):
        """Initializes the configuration with a `str` value.

        Args:
            label: `str` The label for the configuration.
            value: `str` The string value for the configuration.
        """
        super().__init__(label, value)
        self.value = value


class CXNone(CXConfig):
    """A `CXConfig` object that manages `None` values."""

    __value: Any = None
    """The managed value."""

    @property
    def value(self) -> None:
        """Provides the value for the configuration.

        Returns:
            `None`: Always returns None.
        """
        return self.__value

    @value.setter
    def value(self, value=None) -> None:
        """Sets the value of the configuration.

        Args:
            value: `None` Only None can be used.
        """
        if value is not None:
            raise ValueError("CXNone only accepts None values")

        self.__value = None

    def __init__(self, label: str, value=None):
        """Initializes the configuration with a None value.

        Args:
            label: `str` The label for the configuration.
            value: `None` The None value for the configuration.
        """
        super().__init__(label, value)
        self.value = value


class CXBool(CXConfig):
    """A `CXConfig` object that manages `bool` values."""

    __value: bool = False
    """The managed value."""

    @property
    def value(self) -> bool:
        """Provides the value for the configuration.

        Returns:
            `bool`: The boolean value for the configuration.
        """
        return self.__value

    @value.setter
    def value(self, value: Union[object, bool]) -> None:
        """Sets the value of the configuration.

        Args:
            value: `bool` If `None` then `False` will be used.
        """
        if value is None:
            self.__value = False
        else:
            self.__value = bool(value)

    def __init__(self, label: str, value: bool):
        """Initializes the configuration with a `bool` value.

        Args:
            label: `str` The label for the configuration.
            value: `bool` The boolean value for the configuration.
        """
        super().__init__(label, value)
        self.value = value

    def __str__(self) -> str:
        """*str* function. Converts the object into a Javascript statement.

        Returns:
            `str`: JSON string representation of the label and value.
        """
        return str(
            {
                "label": self.label,
                "value": self.value,
            }
        )

    def __repr__(self) -> str:
        """*repr* function. Converts the CXBool object into a pickle string
        that can be used with `eval` to establish a copy of the object.

        Returns:
            `str`: An evaluatable representation of the object.
        """
        return (
            f"{str(self.__class__).split('.')[-1][:-2]}("
            f" label='{self.label}',"
            f" value={str(self.value)}"
            f")"
        )


class CXFloat(CXConfig):
    """A `CXConfig` object that manages `float` values."""

    __value: float = 0.0
    """The managed value."""

    @property
    def value(self) -> float:
        """Provides the value for the configuration.

        Returns:
            `float`: The float value for the configuration.
        """
        return self.__value

    @value.setter
    def value(self, value: Union[object, float]) -> None:
        """Sets the value of the configuration.

        Args:
            value: `float` If `None` then `float(0.0)` will be used.
        """
        if value is None:
            self.__value = 0.0
        else:
            self.__value = float(value)

    def __init__(self, label: str, value: float):
        """Initializes the configuration with a `float` value.

        Args:
            label: `str` The label for the configuration.
            value: `float` The float value for the configuration.
        """
        super().__init__(label, value)
        self.__value = 0.0

        self.value = value


class CXInt(CXConfig):
    """A `CXConfig` object that manages `int` values."""

    __value: int = 0
    """The managed value."""

    @property
    def value(self) -> int:
        """Provides the value for the configuration.

        Returns:
            `int`: The integer value for the configuration.
        """
        return self.__value

    @value.setter
    def value(self, value: Union[object, int]) -> None:
        """Sets the value of the configuration.

        Args:
            value: `int` If `None` then `int(0)` will be used.
        """
        if value is None:
            self.__value = 0
        else:
            self.__value = int(value)

    def __init__(self, label: str, value: int):
        """Initializes the configuration with an `int` value.

        Args:
            label: `str` The label for the configuration.
            value: `int` The integer value for the configuration.
        """
        super().__init__(label, value)
        self.__value = 0

        self.value = value


class CXDict(CXConfig):
    """A `CXConfig` object that manages `dict` values."""

    __value: dict = dict()
    """The managed value."""

    @property
    def value(self) -> dict:
        """Provides the value for the configuration.

        Returns:
            `dict`: The dictionary value for the configuration.
        """
        return self.__value

    @value.setter
    def value(self, value: Union[dict, str, None]) -> None:
        """Sets the value of the configuration.

        Args:
            value: `dict` If `None` then `dict()` will be used.
        """
        if value is None:
            self.__value = dict()

        elif isinstance(value, CXDict):
            self.__value = deepcopy(value.value)

        elif isinstance(value, str):
            candidate = json.loads(html.unescape(value).replace("&nl;", '"<br>"'))
            self.__value = candidate

        else:  # remove html entities from string values
            clean_value = {}
            for k, v in value.items():
                clean_value[k] = v
                if isinstance(v, str):
                    clean_value[k] = html.unescape(v).replace("&nl;", '"<br>"')
            self.__value = deepcopy(clean_value)

    def __init__(self, label: str, value: Union[dict, str, None]) -> None:
        """Initializes the CXData object with data. Only dict or compatible
        data types are accepted.

        Args:
            label: `str` The label for the configuration.
            value: `Union[dict, str, None]` The dictionary, string, or None
                value for the configuration.
        """
        super().__init__(label, value)
        self.value = value

    def __lt__(self, other: "CXDict") -> bool:
        """*less than* comparison. Also see `@total_ordering` in `functools`.

        Args:
            other: `CXDict` The object to compare.

        Returns:
            `bool`: True if self is less than other.
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
            delta: dict = DeepDiff(self.value, other.value, ignore_order=True)
            other_added: int = len(delta.get("dictionary_item_added", []))
            other_removed: int = len(delta.get("dictionary_item_removed", []))

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

    def __eq__(self, other: "CXDict") -> bool:
        """*equals* comparison. Also see `@total_ordering` in `functools`.

        Args:
            other: `CXDict` The object to compare.

        Returns:
            `bool`: True if self equals other.
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
            delta: dict = DeepDiff(self.value, other.value, ignore_order=True)
            other_added: int = len(delta.get("dictionary_item_added", []))
            other_removed: int = len(delta.get("dictionary_item_removed", []))

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
        """*repr* function. Converts the CXDict object into a pickle string
        that can be used with `eval` to establish a copy of the object.

        Returns:
            `str`: An evaluatable representation of the object.
        """
        return f"CXDict(label='{self.label}', value={json.dumps(self.value)})"


class CXList(CXConfig):
    """A `CXConfig` object that manages `list` values."""

    __value: list = list()
    """
    The managed value.
    """

    @property
    def value(self) -> list:
        """Provides the value for the configuration.

        Returns:
            `list`: The list value for the configuration.
        """
        return self.__value

    @value.setter
    def value(self, value: Union[object, list]) -> None:
        """Sets the value of the configuration.

        Args:
            value: `list` If `None` then `list()` will be used.
        """
        if value is None:
            self.__value = list()
        else:
            self.__value = list(value)

    def __init__(self, label: str, value: list):
        """Initializes the configuration with a `list` value.

        Args:
            label: `str` The label for the configuration.
            value: `list` The list value for the configuration.
        """
        super().__init__(label, value)
        self.__value = list()

        self.value = value


class CXGraphWeight(CXConfig):
    """A `CXConfig` object that manages and normalizes `CXGraphWeight list` values."""

    __value: list = list()
    """The managed value."""

    def is_graph_weight_list(label: str, value: list):
        """A static method that evaluates a given list and label to check
        if it represents a graph weight list.

        Args:
            label: `str` A string representing the value label (e.g.
                "ringGraphWeight"). It must contain the word "weight".
            value: `list` A list to evaluate. It must be:
                - a non-empty list
                - all its values are numeric
                - summation of its values is 100 or 1

        Returns:
            `bool`: True if all conditions are valid.
        """
        valid_label = False
        if label is not None:
            valid_label = "weight" in label.lower()
        valid_list = True

        if valid_label:
            if value is None:
                valid_list = False
            elif not isinstance(value, list):
                valid_list = False
            elif not all(isinstance(x, (int, float)) for x in value):
                valid_list = False
            elif sum(value) != 100 and sum(value) != 1:
                valid_list = False

        return valid_label and valid_list

    @property
    def value(self) -> list:
        """Provides the value for the configuration.

        Returns:
            `list`: The list value for the configuration.
        """
        return self.__value

    @value.setter
    def value(self, value: Union[object, list]) -> None:
        """Sets the value of the configuration.

        Args:
            value: `list` If `None` then `list()` will be used.
        """
        # return empty value if the weight list or its sum is invalid
        final_value = list()

        # normalize graph weight only if it has non normalized and valid weight list
        if value is not None and all(isinstance(x, (int, float)) for x in value):
            if sum(value) == 100:
                final_value = [x / 100 for x in value]
            elif sum(value) == 1:
                final_value = value

        self.__value = final_value

    def __init__(self, label: str, value: list):
        """Initializes the configuration with a `list` value.

        Args:
            label: `str` The label for the configuration.
            value: `list` The list value for the configuration.
        """
        super().__init__(label, value)
        self.__value = list()

        self.value = value


@deprecated(action="ignore")
class CXRGBAColor(CXDict):
    """A `CXConfig` object that manages `str` Javascript rgba() values."""

    @staticmethod
    def is_color_str(value: str):
        """A static method that evaluates a given string to see if it represents
        a Javascript rgba() statement.

        Args:
            value: `str` A string to evaluate. A valid Javascript value has the
                form `rgba(r, g, b, a)` where RGB values are `int` from 0-255
                and A is a `float` from 0.0 to 1.0.

        Returns:
            `bool`: True if the string represents a Javascript rgba() statement.
        """
        if isinstance(value, str):
            if not value.startswith("rgba"):
                return False

            try:
                components = value.split(",")
                if len(components) != 4:
                    return False

                r = components[0].strip().split("rgba(")[1]
                g = components[1].strip()
                b = components[2].strip()
                a = components[3].strip().split(")")[0]

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
        """A static method that evaluates a given list to see if it represents
        a Javascript rgba() statement.

        Args:
            value: `list` A list to evaluate. A valid Javascript value has the
                form `rgba(r, g, b, a)` where RGB values are `int` from 0-255
                and A is a `float` from 0.0 to 1.0.

        Returns:
            `bool`: True if the list represents a Javascript rgba() statement.
        """
        if isinstance(value, list):
            try:
                list_len = len(value)
                all_rgb_elements_int = all(isinstance(x, int) for x in value[:3])
                alpha_element_num = type(value[3]) in [int, float]
                if (
                    (not list_len == 4)
                    or (not all_rgb_elements_int)
                    or (not alpha_element_num)
                ):
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
        """A static method that evaluates a given dict to see if it represents
        a Javascript rgba() statement.

        Args:
            value: `dict` A dict to evaluate. A valid Javascript value has the
                form `rgba(r, g, b, a)` where RGB values are `int` from 0-255
                and A is a `float` from 0.0 to 1.0. For the dict to be valid
                its keys must be lower case r, g, b, and a characters.

        Returns:
            `bool`: True if the dict represents a Javascript rgba() statement.
        """
        if isinstance(value, dict):
            list_len = len(value.keys())
            all_rgba_elements = all(x in ["r", "g", "b", "a"] for x in value.keys())
            all_rgb_elements_int = all(
                isinstance(value[x], int) for x in value.keys() if x in ["r", "g", "b"]
            )
            alpha_element_num = type(value.get("a")) in [int, float]
            keys_rgba = all(
                [j in ["r", "g", "b", "a"] for j in [k for k in value.keys()]]
            )
            if (
                (not list_len == 4)
                or (not all_rgb_elements_int)
                or (not keys_rgba)
                or (not alpha_element_num)
                or (not all_rgba_elements)
            ):
                return False

            for key in value.keys():
                if key in ["r", "g", "b"]:
                    if (value[key] < 0) or (value[key] > 255):
                        return False
                if key in ["a"]:
                    if (value[key] < 0) or (value[key] > 1):
                        return False

            return True

        else:
            return False

    @CXDict.value.setter
    def value(self, value: Union["CXRGBAColor", dict, list, str]) -> None:
        """Sets the RGBA value from an existing `CXRGBAColor` object, or a
        `dict`, `list`, or `string` following the Javascript `rgba()` format.

        Args:
            value: `Union['CXRGBAColor', dict, list, str]` The value to be
                accepted. See the `is_color_*()` methods for acceptable formats.
        """
        if value is None:
            CXDict.value.fset(
                self,
                {
                    "r": 0,
                    "g": 0,
                    "b": 0,
                    "a": 1.0,
                },
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
                    components = value.split(",")
                    r = components[0].strip().split("rgba(")[1]
                    g = components[1].strip()
                    b = components[2].strip()
                    a = components[3].strip().split(")")[0]

                    candidate = {
                        "r": int(r),
                        "g": int(g),
                        "b": int(b),
                        "a": float(a),
                    }

            elif isinstance(value, list):
                if not CXRGBAColor.is_color_list(value):
                    raise ValueError(
                        "list RGBA values must be in the format" " (int,int,int,float)"
                    )
                else:
                    candidate = {
                        "r": value[0],
                        "g": value[1],
                        "b": value[2],
                        "a": value[3],
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

            CXDict.value.fset(self, candidate)

    def render(self) -> Any:
        """Renders the value in a form suitable for use in preparing Javascript.
        Typically, this will be the native `value`.

        Returns:
            `Any`: A version of the `value` most appropriate for use in
            preparing the Javascript rendering.
        """
        r = self.value["r"]
        g = self.value["g"]
        b = self.value["b"]
        a = self.value["a"]
        return {self.label: f"rgba({r},{g},{b},{a})"}

    def __init__(self, label: str, value: Union["CXRGBAColor", dict, list, str]):
        """Initializes a new CXRGBAColor object using the RGBA value from an
        existing `CXRGBAColor` object, or a `dict`, `list`, or `string`
        following the Javascript `rgba()` format.

        Args:
            label: `str` The label for the configuration.
            value: `Union['CXRGBAColor', dict, list, str]` The value to be
                accepted. See the `is_color_*()` methods for acceptable formats.
        """
        super().__init__(label, {"r": 0, "g": 0, "b": 0, "a": 1})
        self.value = value

    def __str__(self) -> str:
        """*str* function. Converts the object into a JSON string.

        Returns:
            `str`: JSON string representation of the rendered value.
        """
        return json.dumps(self.render())

    def __repr__(self) -> str:
        """*repr* function. Converts the CXRGBAColor object into a pickle
        string that can be used with `eval` to establish a copy of the object.

        Returns:
            `str`: An evaluatable representation of the object.
        """
        r = self.value["r"]
        g = self.value["g"]
        b = self.value["b"]
        a = self.value["a"]
        return (
            f"CXRGBAColor("
            f" label={json.dumps(self.label)},"
            f" value='rgba({r},{g},{b},{a})'"
            f")"
        )


@deprecated(action="ignore")
class CXRGBColor(CXDict):
    """A `CXConfig` object that manages `str` Javascript rgb() values."""

    @staticmethod
    def is_color_str(value: str):
        """A static method that evaluates a given string to see if it represents
        a Javascript rgb() statement.

        Args:
            value: `str` A string to evaluate. A valid Javascript value has the
                form `rgb(r, g, b)` where RGB values are `int` from 0-255.

        Returns:
            `bool`: True if the string represents a Javascript rgb() statement.
        """
        if isinstance(value, str):
            if not value.startswith("rgb"):
                return False

            try:
                components = value.split(",")
                if len(components) != 3:
                    return False

                r = components[0].strip().split("rgb(")[1]
                g = components[1].strip()
                b = components[2].strip().split(")")[0]

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
        """A static method that evaluates a given list to see if it represents
        a Javascript rgb() statement.

        Args:
            value: `list` A list to evaluate. A valid Javascript value has the
                form `rgb(r, g, b)` where RGB values are `int` from 0-255.

        Returns:
            `bool`: True if the list represents a Javascript rgb() statement.
        """
        if isinstance(value, list):
            list_len = len(value)
            all_rgb_elements_int = all(isinstance(x, int) for x in value[:2])
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
        """A static method that evaluates a given dict to see if it represents
        a Javascript rgb() statement.

        Args:
            value: `dict` A dict to evaluate. A valid Javascript value has the
                form `rgb(r, g, b)` where RGB values are `int` from 0-255.
                For the dict to be valid its keys must be lower case r, g,
                and b characters.

        Returns:
            `bool`: True if the dict represents a Javascript rgb() statement.
        """
        if isinstance(value, dict):
            list_len = len(value.keys())
            all_rgb_elements = all(
                x
                in [
                    "r",
                    "g",
                    "b",
                ]
                for x in value.keys()
            )
            all_rgb_elements_int = all(
                isinstance(value[x], int) for x in value.keys() if x in ["r", "g", "b"]
            )
            keys_rgb = all([j in ["r", "g", "b"] for j in [k for k in value.keys()]])
            if (
                (not list_len == 3)
                or (not all_rgb_elements)
                or (not all_rgb_elements_int)
                or (not keys_rgb)
            ):
                return False

            for key in value.keys():
                if key in ["r", "g", "b"]:
                    if (value[key] < 0) or (value[key] > 255):
                        return False

            return True

        else:
            return False

    @CXDict.value.setter
    def value(self, value: Union["CXRGBColor", dict, list, str]) -> None:
        """Sets the RGB value from an existing `CXRGBColor` object, or a
        `dict`, `list`, or `string` following the Javascript `rgb()` format.

        Args:
            value: `Union['CXRGBColor', dict, list, str]` The value to be
                accepted. See the `is_color_*()` methods for acceptable formats.
        """
        if value is None:
            CXDict.value.fset(
                self,
                {
                    "r": 0,
                    "g": 0,
                    "b": 0,
                },
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
                        "str RGB values must be in the format" " rgb(int,int,int)"
                    )
                else:
                    components = value.split(",")
                    r = components[0].strip().split("rgb(")[1]
                    g = components[1].strip()
                    b = components[2].strip().split(")")[0]

                    candidate = {
                        "r": int(r),
                        "g": int(g),
                        "b": int(b),
                    }

            elif isinstance(value, list):
                if not CXRGBColor.is_color_list(value):
                    raise ValueError(
                        "list RGB values must be in the format" " (int,int,int)"
                    )
                else:
                    candidate = {
                        "r": value[0],
                        "g": value[1],
                        "b": value[2],
                    }

            elif isinstance(value, dict):
                if not CXRGBColor.is_color_dict(value):
                    raise ValueError(
                        "RGB dict must have three int values for keys" " 'r', 'g', 'b'"
                    )
                else:
                    candidate = dict(value)

            else:
                candidate = deepcopy(value.value)

            CXDict.value.fset(self, candidate)

    def render(self) -> dict:
        """Renders the value in a form suitable for use in preparing Javascript.
        Typically, this will be the native `value`.

        Returns:
            `dict`: A version of the `value` most appropriate for use in
            preparing the Javascript rendering.
        """
        r = self.value["r"]
        g = self.value["g"]
        b = self.value["b"]
        return {self.label: f"rgb({r},{g},{b})"}

    def __init__(self, label: str, value: Union["CXRGBColor", dict, list, str]):
        """Initializes a new CXRGBColor object using the RGB value from an
        existing `CXRGBColor` object, or a `dict`, `list`, or `string`
        following the Javascript `rgb()` format.

        Args:
            label: `str` The label for the configuration.
            value: `Union['CXRGBColor', dict, list, str]` The value to be
                accepted. See the `is_color_*()` methods for acceptable formats.
        """
        super().__init__(label, {"r": 0, "g": 0, "b": 0})
        self.value = value

    def __str__(self) -> str:
        """*str* function. Converts the object into a JSON string.

        Returns:
            `str`: JSON string representation of the rendered value.
        """
        return json.dumps(self.render())

    def __repr__(self) -> str:
        """*repr* function. Converts the CXRGBColor object into a pickle
        string that can be used with `eval` to establish a copy of the object.

        Returns:
            `str`: An evaluatable representation of the object.
        """
        r = self.value["r"]
        g = self.value["g"]
        b = self.value["b"]
        return (
            f"CXRGBColor("
            f" label={json.dumps(self.label)},"
            f" value='rgb({r},{g},{b})'"
            f")"
        )


class CXGraphTypeOptions(Enum):
    """A set of known chart types permitted for use with CanvasXpress objects.
    If a chart not yet identified in this list is required then use a `CXString`
    object with the label `graphType` and the value set to the name of the
    chart to be used."""

    Area = "Area"
    AreaLine = "AreaLine"
    Bar = "Bar"
    BarLine = "BarLine"
    Boxplot = "Boxplot"
    Bubble = "Bubble"
    Chord = "Chord"
    Circular = "Circular"
    Contour = "Contour"
    Correlation = "Correlation"
    Dashboard = "Dashboard"
    Density = "Density"
    Donnut = "Donnut"
    DotLine = "DotLine"
    Dotplot = "Dotplot"
    Facet = "Facet"
    Fish = "Fish"
    Gantt = "Gantt"
    Genome = "Genome"
    Heatmap = "Heatmap"
    Histogram = "Histogram"
    Kaplan_Meier = "Kaplan - Meier"
    Layout = "Layout"
    Line = "Line"
    Map = "Map"
    Meter = "Meter"
    Network = "Network"
    NonLinear_Fit = "NonLinear - Fit"
    Oncoprint = "Oncoprint"
    ParallelCoordinates = "ParallelCoordinates"
    Pie = "Pie"
    Radar = "Radar"
    Remote_Graphs = "Remote - Graphs"
    Ridge_Line = "Ridge - Line"
    SPLOM = "SPLOM"
    Sankey = "Sankey"
    Scatter2D = "Scatter2D"
    Scatter3D = "Scatter3D"
    ScatterBubble2D = "ScatterBubble2D"
    Stacked = "Stacked"
    StackedLine = "StackedLine"
    StackedPercent = "StackedPercent"
    StackedPercentLine = "StackedPercentLine"
    Sunburst = "Sunburst"
    TCGA = "TCGA"
    TagCloud = "TagCloud"
    Tree = "Tree"
    Treemap = "Treemap"
    Venn = "Venn"
    Violin = "Violin"


class CXGraphType(CXString):
    """A CXString that is aware of CanvasXpress types of graphs, such as 'Bar'."""

    CX_ATTRIBUTE = "graphType"

    @CXString.value.setter
    def value(self, value: Union[CXGraphTypeOptions, str]) -> None:
        """Sets the value using a known CanvasXpress option.

        Args:
            value: `Union[CXGraphTypeOptions, str]` A known CanvasXpress graph
                type option.
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
        """Permits a js value to be set, such as if a new option is recently
        made available that the Python framework is yet to be aware of.

        Args:
            value: `str` The string value to set.
        """
        CXString.value.fset(self, value)

    def render(self) -> dict:
        """Renders the value in a form suitable for use in preparing Javascript.
        Typically, this will be the native `value`.

        Returns:
            `dict`: A version of the `value` most appropriate for use in
            preparing the Javascript rendering.
        """
        return {self.label: self.value}

    def __init__(self, type: Union[CXGraphTypeOptions, str] = CXGraphTypeOptions.Bar):
        """Initializes a new CXGraphType object with a value corresponding to
        one of the values provided by `CXGraphTypeOptions`.

        Args:
            type: `Union[CXGraphTypeOptions, str]` A known CanvasXpress graph
                type option or a string value.
        """
        if isinstance(type, CXGraphTypeOptions):
            super().__init__(self.CX_ATTRIBUTE, type.value)

        else:
            super().__init__(self.CX_ATTRIBUTE, type)
