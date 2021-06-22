import json
from copy import deepcopy
from functools import total_ordering
from typing import List, Any, Union

from canvasxpress.config.type import CXConfig, CXString, CXInt, CXFloat, CXBool, \
    CXList, CXDict, CXRGBColor, CXRGBAColor
from canvasxpress.data.convert import CXDictConvertable, CXListConvertable


@total_ordering
class CXConfigs(
    CXDictConvertable,
    CXListConvertable
):
    """
    CXConfigs provides support for addressing a collection of `CXConfig` values.
    """

    __configs: List[CXConfig] = None
    """
    The `CXConfig` objects associated with this collection.
    """

    def __init__(self, *configs: Union[CXConfig, tuple, dict, list]):
        """
        Initializes a new `CXConfigs` object with zero or more `CXConfig`
        objects.

        Example:
        ```python
        configs = CXConfigs(
            CXString("colorScheme", "ColorSpectrum"),
            ("lineType", "spline"),
            { "objectColorTransparency": 0.3 }
        )
        ```

        :param configs: `Union[CXConfig, tuple, dict], ...`
            A list of zero or more `CXConfig` objects to associate.
        """
        self.__configs: List[CXConfig] = list()
        for config in configs:
            self.add(config)

    def remove(self, label: str) -> Union[CXConfig, None]:
        """
        Removes the CXConfig if found, and if found the removed config is
        provided.
        :param label: 'str`
            The label of the CXConfig to remove.
        :returns: `Union[CXConfig, None]`
            If a CXConfig is removed then it is returned, otherwise None.
        """
        candidate = None
        for config in self.configs:
            if str(label) == config.label:
                candidate = config
                self.configs.remove(config)
                break

        return candidate

    def add(self, config: Union[CXConfig, tuple, dict, list]) -> 'CXConfigs':
        """
        Adds the specified configuration to the collection.  This method
        supports chaining for efficient additions of `CXConfig` objects.

        Example:
        ```python
        configs = CXConfigs()
        configs \
            .add(CXString("colorScheme", "ColorSpectrum") \
            .add(("lineType", "spline")) \
            .add({ "objectColorTransparency": 0.3 })
        ```

        :param config: `Union[CXConfig, tuple, dict, list]`
            The `CXConfig` to associate.  Cannot be `None`.  `tuple` an d`list`
            config values are expected to be two elements in length, with the
            first representing the label and the second representing the value.
            The label portion will be converted to a string using `str`.
        """
        if config is None:
            raise ValueError("configs cannot be None.")

        elif isinstance(config, dict):
            for param in config.keys():
                self.set_param(
                    str(param),
                    config.get(param)
                )

        elif isinstance(config, (tuple, list)):
            if len(config) > 0:
                if isinstance(config[0], (tuple, list)):
                    for item in config:
                        self.add(item)

                else:
                    if len(config) < 2:
                        raise ValueError(
                            "list and tuple config representations of "
                            "configuration parameters must have two elements: "
                            "the first is the label, and the second is the "
                            "value."
                        )
                    self.set_param(
                        str(config[0]),
                        config[1]
                    )

        elif isinstance(config, CXConfig):
            if config not in self.__configs:
                self.__configs.append(config)

        else:
            raise TypeError("configs must be a type of CXConfig.")

        return self

    def get_param(
            self,
            label: str
    ) -> Union[CXConfig, None]:
        """
        Provides the CXConfig with the indicated label.
        :param label: `str`
            The name of the congig to find.
        :returns: `Union[CXConfig, None]`
            The CXConfig or None if such a labelled item is not associated.
        """
        candidate = None
        for config in self.configs:
            if config.label == label:
                candidate = config
                break

        return candidate

    def set_param(
            self,
            label: str,
            value: Any
    ) -> 'CXConfigs':
        """
        Adds a parameter to the configs.  Attempts to infer the kind of param to
        add, and if a type can be deduced then an appropriate CXConfig is used.
        If a type cannot be inferred the a text type is assumed. This method
        supports chaining for efficient additions of `CXConfig` objects.

        Example:
        ```python
        configs = CXConfigs()
        configs \
            .set_param("1", "rgb(3, 172, 198)") \
            .set_param("2", 2) \
            .set_param("3", True)
        ```

        :param value: `Any`
            The parameter to infer and associate.  Cannot be `None`.  Defaults
            to `str` if the type cannot otherwise be deduced.
        """
        if (label is None) or (value is None):
            raise ValueError("Neither label nor value can be None.")

        else:
            existing_config_used = False
            for config in self.configs:
                if config.label == label:
                    if not isinstance(config.value, type(value)):
                        raise ValueError(
                            f"CXConfig {repr(config)} is already a member and"
                            f" has a different type than what is provided."
                            f" Remove the existing CXConfig object first or use"
                            f" the same type."
                        )
                    else:
                        config.value = value
                        existing_config_used = True
                        break

            if not existing_config_used:
                value_type = type(value)
                if value_type is int:
                    candidate = CXInt(
                        label,
                        value
                    )
                elif value_type is float:
                    candidate = CXFloat(
                        label,
                        value
                    )
                elif value_type is bool:
                    candidate = CXBool(
                        label,
                        value
                    )
                elif value_type is dict:
                    if CXRGBAColor.is_color_dict(value):
                        candidate = CXRGBAColor(
                            label,
                            value
                        )
                    elif CXRGBColor.is_color_dict(value):
                        candidate = CXRGBColor(
                            label,
                            value
                        )
                    else:
                        candidate = CXDict(
                            label,
                            value
                        )
                elif value_type is list:
                    if CXRGBAColor.is_color_list(value):
                        candidate = CXRGBAColor(
                            label,
                            value
                        )
                    elif CXRGBColor.is_color_list(value):
                        candidate = CXRGBColor(
                            label,
                            value
                        )
                    else:
                        candidate = CXList(
                            label,
                            value
                        )
                elif value_type is set:
                    set_persona: set = value
                    candidate = CXList(
                        label,
                        list(set_persona)
                    )
                else:
                    if CXRGBAColor.is_color_str(value):
                        candidate = CXRGBAColor(
                            label,
                            value
                        )
                    elif CXRGBColor.is_color_str(value):
                        candidate = CXRGBColor(
                            label,
                            value
                        )
                    else:
                        candidate = CXString(
                            label,
                            value
                        )

                self.add(candidate)

            return self

    @property
    def configs(self) -> List[CXConfig]:
        """
        Provides access to the list of associated `CXConfig` objects.
        :returns: `List[CXConfig]`
        """
        return self.__configs

    def render_to_dict(self) -> dict:
        """
        Provides a `dict` representation of the configuration values.
        :returns: `dict`
            A `dict` representing the configuration values arranged as a map
            of keys and values.

            Given:
            ```python
            configs = CXConfigs()
            configs \
                .set_param("1", "rgb(3, 172, 198)") \
                .set_param("2", 2) \
                .set_param("3", True)
            ```

            Then `render_to_dict()` results in:
            ```python
            {
                "1": "rgb(3, 172, 198)",
                "2": 2,
                "3": True,
            }
            ```
        """
        return CXConfigs.merge_configs(self.configs)

    def render_to_list(
            self,
            **kwargs
    ) -> list:
        """
        Provides a `list` representation of the configuration values.
        :returns: `list`
            A `list` representing the configuration values arranged as a map
            of keys and values.

            Given:
            ```python
            configs = CXConfigs()
            configs \
                .set_param("1", "rgb(3, 172, 198)") \
                .set_param("2", 2) \
                .set_param("3", True)
            ```

            Then `render_to_list()` results in:
            ```python
            [
                ["1", "rgb(3, 172, 198)"],
                ["2": 2],
                ["3": True],
            ]
            ```
        """
        configs = self.render_to_dict()
        return [
            [
                str(key),               # function name
                configs[key]            # list of parameter values
            ]
            for key in configs.keys()
        ]


    @classmethod
    def merge_configs(
            cls,
            configs: List[CXConfig]
    ) -> dict:
        """
        Given a list of CXConfig objects, a dictionary of unique attributes is
        generated and provided.
        :returns: `dict`
            A dict of zero or more keys representing the CXConfigs.
        """
        unique_configs = list()
        if not configs is None:
            for config in configs:
                if not config in unique_configs:
                    unique_configs.append(config)

        dict_configs = dict()
        for config in unique_configs:
            dict_configs = {
                **dict_configs,
                **(config.render())
            }

        return dict_configs

    def __copy__(self) -> 'CXConfigs':
        """
        *copy* constructor.  Returns the `CXConfig` objects within a new
        `CXConfigs` object.
        """
        return CXConfigs(
            *self.configs
        )

    def __deepcopy__(
            self,
            memo
    ) -> 'CXConfigs':
        """
        *deepcopy* constructor.  Returns a deepcopy of the `CXConfig` objects
         within a new `CXConfigs` object.
        """
        return CXConfigs(
            *([deepcopy(config) for config in self.configs])
        )

    def __lt__(
            self,
            other: 'CXConfigs'
    ) -> bool:
        """
        *less than* comparison.  Also see `@total_ordering` in `functools`.
        :param other:
            `CXConfigs` The object to compare.
        :returns: `bool`
            <ul>
            <li> If `other` is `None` then `False`
            <li> If `other` is not a `CXConfigs` object then False
            <li> If `other` is a `CXConfigs` object then True of all `CXConfig`
                objects are also less than the events tracked by `self`.
            </ul>
        """
        if other is None:
            return False

        if not isinstance(other, CXConfigs):
            return False

        else:
            if (len(self.configs) + len(other.configs)) == 0:
                return False

            if len(self.configs) == len(other.configs):
                for config in self.configs:
                    for oconfig in other.configs:
                        if not config < oconfig:
                            return False
                return True

            else:
                return len(self.configs) < len(other.configs)

    def __eq__(
            self,
            other: 'CXConfigs'
    ) -> bool:
        """
        *equals* comparison.  Also see `@total_ordering` in `functools`.
        :param other:
            `CXConfigs` The object to compare.
        :returns: `bool`
            <ul>
            <li> If `other` is `None` then `False`
            <li> If `other` is not a `CXConfigs` object then False
            <li> If `other` is a `CXConfigs` object then True of all `CXConfig`
                objects are also equal to the events tracked by `self`.
            </ul>
        """
        if other is None:
            return False

        if not isinstance(other, CXConfigs):
            return False

        else:
            if len(self.configs) == len(other.configs):
                for config in self.configs:
                    alt_config = other.get_param(config.label)
                    if alt_config is None:
                        return False
                    if alt_config.value != config.value:
                        return False

                return True

            else:
                return len(self.configs) == len(other.configs)

    def __str__(self) -> str:
        """
        *str* function.  Converts the `CXConfigs` object into a JSON
         representation.
        :returns" `str`
            JSON form of the collection.
        """
        return json.dumps(
            self.render_to_dict()
        )

    def __repr__(self) -> str:
        """
        *repr* function.  Converts the `CXConfigs` object into a pickle string
        that can be used with `eval` to establish a copy of the object.
        :returns: `str` An evaluatable representation of the object.
        """
        config_rep_list = ", ".join([repr(config) for config in self.configs])
        rep_candidate = f'CXConfigs(' \
                        f'{config_rep_list}' \
                        f')'
        return rep_candidate
