import json
from copy import deepcopy
from functools import total_ordering
from typing import Set, List, Any

from canvasxpress.config.type import CXConfig, CXString, CXInt, CXFloat, CXBool, \
    CXList, CXDict, CXRGBColor, CXRGBAColor
from canvasxpress.data.convert import CXDictConvertable


@total_ordering
class CXConfigs(CXDictConvertable):
    """
    CXConfigs provides support for addressing CXConfig values.
    """

    __configs: List[CXConfig] = None

    def __init__(self, *configs):
        self.__configs: List[CXConfig] = list()
        for config in configs:
            self.add(config)

    def add(self, config: CXConfig) -> 'CXConfigs':
        if config is None:
            raise ValueError("configs cannot be None.")

        if not isinstance(config, CXConfig):
            raise TypeError("configs must be a type of CXConfig.")

        if config not in self.__configs:
            self.__configs.append(config)

        return self

    def set_param(
            self,
            label: str,
            value: Any
    ) -> 'CXConfigs':
        """
        Adds a parameter to the configs.  Attempts to infer the kind of param to
        add, and if a type can be deduced then an appropriate CXConfig is used.
        If a type cannot be inferred the a text type is assumed.
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
    def configs(self) -> Set[CXConfig]:
        return self.__configs

    def render_to_dict(self) -> dict:
        return CXConfigs.merge_configs(
            list(self.__configs)
        )

    @classmethod
    def merge_configs(
            cls,
            configs: List[CXConfig]
    ) -> dict:
        """
        Given a list of CXConfig objects, a dictionary of unique attributes is
        generated and provided.
        :returns: A dict of zero or more keys representing the CXConfigs.
        """
        if configs is None:
            unique_configs = set()
        else:
            unique_configs = set(configs)

        dict_configs = dict()
        for config in unique_configs:
            dict_configs[config.label] = config.value

        return dict_configs

    def __copy__(self):
        return CXConfigs(
            *self.configs
        )

    def __deepcopy__(
            self,
            memo
    ):
        return CXConfigs(
            *([deepcopy(config) for config in self.configs])
        )

    def __lt__(
            self,
            other: 'CXConfigs'
    ):
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
    ):
        if other is None:
            return False

        if not isinstance(other, CXConfigs):
            return False

        else:
            if len(self.configs) == len(other.configs):
                for config in self.configs:
                    for oconfig in other.configs:
                        if not config == oconfig:
                            return False
                return True

            else:
                return len(self.configs) == len(other.configs)

    def __str__(self) -> str:
        return json.dumps(
            self.render_to_dict()
        )

    def __repr__(self) -> str:
        config_rep_list = ", ".join([repr(config) for config in self.configs])
        rep_candidate = f'CXConfigs(' \
                        f'{config_rep_list}' \
                        f')'
        return rep_candidate
