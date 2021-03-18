import json
from abc import ABC, abstractmethod
from enum import Enum
from typing import Union


class CXType(ABC):
    """
    CXType provides the means by which CanvasXpress objects can be configured for
    customized rendering and interaction.
    """

    __label: str = ""

    @property
    def label(self) -> str:
        return self.__label

    @property
    @abstractmethod
    def value(self):
        pass

    @value.setter
    @abstractmethod
    def value(self, value: object) -> None:
        pass

    def __init__(
            self,
            label: str,
            value: object
    ):
        if label is None:
            raise ValueError("label cannot be None")
        else:
            self.__label = label

    def __copy__(self):
        return CXType(
            self.label,
            self.value
        )

    def __deepcopy__(
            self,
            memo
    ):
        return self.__copy__()

    def __hash__(self):
        return hash(repr(self))

    def __lt__(
            self,
            other: 'CXType'
    ):
        if not object:
            return False

        if type(other) is not CXType:
            return False

        if self is other:
            return False

        else:
            if self.label < other.label:
                return True
            elif self.label == other.label:
                if self.value < other.value:
                    return True

            return False

    def __eq__(
            self,
            other: 'CXType'
    ):
        if not object:
            return False

        if type(other) is not CXType:
            return False

        if self is other:
            return False

        else:
            return (self.label == other.label) and (self.value == other.value)

    def __str__(self) -> str:
        return json.dumps(
            {
                "label": self.label,
                "value": self.value,
            }
        )

    def __repr__(self) -> str:
        return f"{str(self.__class__).split('.')[-1][:-2]}(" \
               f" label={json.dumps(self.label)}," \
               f" value={json.dumps(self.value)}" \
               f")"


class CXString(CXType):
    __value: str = ""

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value: Union[object, str]) -> None:
        if value is None:
            self.__value = ""
        else:
            self.__value = str(value)

    def __init__(self, label: str, value: str):
        super().__init__(label, value)
        self.__value = ""

        self.value = value


class CXBool(CXType):
    __value: bool = False

    @property
    def value(self) -> bool:
        return self.__value

    @value.setter
    def value(self, value: Union[object, bool]) -> None:
        if value is None:
            self.__value = False
        else:
            self.__value = bool(value)

    def __init__(self, label: str, value: bool):
        super().__init__(label, value)
        self.__value = False

        self.value = value


class CXFloat(CXType):
    __value: float = 0.0

    @property
    def value(self) -> float:
        return self.__value

    @value.setter
    def value(self, value: Union[object, float]) -> None:
        if value is None:
            self.__value = 0.0
        else:
            self.__value = float(value)

    def __init__(self, label: str, value: float):
        super().__init__(label, value)
        self.__value = 0.0

        self.value = value


class CXInt(CXType):
    __value: int = 0

    @property
    def value(self) -> int:
        return self.__value

    @value.setter
    def value(self, value: Union[object, int]) -> None:
        if value is None:
            self.__value = 0
        else:
            self.__value = int(value)

    def __init__(self, label: str, value: int):
        super().__init__(label, value)
        self.__value = 0

        self.value = value


class CXDict(CXType):
    __value: dict = dict()

    @property
    def value(self) -> dict:
        return self.__value

    @value.setter
    def value(self, value: Union[object, dict]) -> None:
        if value is None:
            self.__value = dict()
        else:
            self.__value = dict(value)

    def __init__(self, label: str, value: dict):
        super().__init__(label, value)
        self.__value = dict()

        self.value = value


class CXList(CXType):
    __value: list = list()

    @property
    def value(self) -> list:
        return self.__value

    @value.setter
    def value(self, value: Union[object, list]) -> None:
        if value is None:
            self.__value = list()
        else:
            self.__value = list(value)

    def __init__(self, label: str, value: list):
        super().__init__(label, value)
        self.__value = list()

        self.value = value


class CXRGBAColor(CXType):
    __value: dict = {
        'r': 0,
        'g': 0,
        'b': 0,
        'a': 1.0,
    }

    @staticmethod
    def is_color_str(value: str):
        if isinstance(value, str):
            if not value.startswith("rgba"):
                return False

            components = value.split(',')
            r = components[0].strip().split("rgba(")[1]
            g = components[1].strip()
            b = components[1].strip()
            a = components[2].strip().split(')')[0]
            if not all(x.isdigit() for x in [r, g, b, a]):
                return False

            for x in [int(r), int(g), int(b)]:
                if (x < 0) or (x > 255):
                    return False
            for x in [float(a)]:
                if (x < 0) or (x > 1):
                    return False

            return True

        else:
            return False

    @staticmethod
    def is_color_list(value: list):
        if isinstance(value, list):
            list_len = len(value)
            all_elements_int = all(isinstance(x, int) for x in value)
            if (list_len != 4) or (not all_elements_int):
                return False

            for x in value[:3]:
                if (x < 0) or (x > 255):
                    return False
            if (value[3] < 0) or (value[3] > 1):
                return False

            return True

        else:
            return False

    @staticmethod
    def is_color_dict(value: dict):
        if isinstance(value, dict):
            list_len = len(value)
            all_elements_int = all(
                isinstance(value[x], int) for x in value.keys()
            )
            keys_rgb = all(
                (x in ["rgba"]) for x in value.keys()
            )
            if (list_len != 4) or (not all_elements_int) or (not keys_rgb):
                return False

            candidate = dict(value)
            for k in candidate.keys():
                if k not in ['r', 'g', 'b', 'a']:
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

    @property
    def value(self) -> dict:
        return self.__value

    @value.setter
    def value(self, value: Union[object, dict, list, str]) -> None:
        if value is None:
            self.__value = {
                'r': 0,
                'g': 0,
                'b': 0,
                'a': 1.0,
            }
        elif type(value) not in [list, dict, str]:
            raise TypeError(
                "value must be a dict of {'r': int, 'g': int, 'b': int, "
                "'a': float} or a list of [r, g, b, a] or a string of "
                "rgba(int,int,int,float)"
            )

        else:
            candidate = None

            if isinstance(value, str):
                if not CXRGBAColor.is_color_str(value):
                    raise ValueError(
                        "str RGBA values must be in the format"
                        " rgb(int,int,int,float)"
                    )
                else:
                    components = value.split(',')
                    r = components[0].strip().split("rgb(")[1]
                    g = components[1].strip()
                    b = components[1].strip()
                    a = components[2].strip().split(')')[0]

                    candidate = {
                        'r': int(r),
                        'g': int(g),
                        'b': int(b),
                        'a': float(a),
                    }

            if isinstance(value, list):
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

            if isinstance(value, dict):
                if not CXRGBAColor.is_color_dict(value):
                    raise ValueError(
                        "RGB dict must have three int values for keys"
                        " 'r', 'g', 'b' and a float value for key 'a'"
                    )
                else:
                    candidate = dict(value)

            self.__value = candidate

    def __init__(self, label: str, value: int):
        super().__init__(label, value)
        self.__value = {
            'r': 0,
            'g': 0,
            'b': 0,
            'a': 1.0,
        }

        self.value = value

    def __str__(self) -> str:
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
        r = self.value['r']
        g = self.value['g']
        b = self.value['b']
        a = self.value['a']
        return f"CXRGBColor(" \
               f" label={json.dumps(self.label)}," \
               f" value='rgba({r},{g},{b},{a})'" \
               f")"


class CXRGBColor(CXType):
    __value: dict = {
        'r': 0,
        'g': 0,
        'b': 0
    }

    @staticmethod
    def is_color_str(value: str):
        if isinstance(value, str):
            if not value.startswith("rgb"):
                return False

            components = value.split(',')
            r = components[0].strip().split("rgb(")[1]
            g = components[1].strip()
            b = components[2].strip().split(')')[0]
            if not all(x.isdigit() for x in [r, g, b]):
                return False

            for x in [int(r), int(g), int(b)]:
                if (x < 0) or (x > 255):
                    return False

            return True

        else:
            return False

    @staticmethod
    def is_color_list(value: list):
        if isinstance(value, list):
            list_len = len(value)
            all_elements_int = all(isinstance(x, int) for x in value)
            if (list_len != 3) or (not all_elements_int):
                return False

            for x in value:
                if (x < 0) or (x > 255):
                    return False

            return True

        else:
            return False

    @staticmethod
    def is_color_dict(value: dict):
        if isinstance(value, dict):
            list_len = len(value)
            all_elements_int = all(
                isinstance(value[x], int) for x in value.keys()
            )
            keys_rgb = all(
                (x in ["rgb"]) for x in value.keys()
            )
            if (list_len != 3) or (not all_elements_int) or (not keys_rgb):
                return False

            candidate = dict(value)
            for k in candidate.keys():
                if k not in ['r', 'g', 'b']:
                    return False

            for key in value.keys():
                if (value[key] < 0) or (value[key] > 255):
                    return False

            return True

        else:
            return False

    @property
    def value(self) -> dict:
        return self.__value

    @value.setter
    def value(self, value: Union[object, dict, list, str]) -> None:
        if value is None:
            self.__value = {
                'r': 0,
                'g': 0,
                'b': 0,
            }
        elif type(value) not in [list, dict, str]:
            raise TypeError(
                "value must be a dict of {'r': int, 'g': int, 'b': int}"
                " or a list of [r, g, b] or a string of rgb(int,int,int)"
            )

        else:
            candidate = None

            if isinstance(value, str):
                if not CXRGBColor.is_color_str(value):
                    raise ValueError(
                        "str RGB values must be in the format rgb(int,int,int)"
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

            if isinstance(value, list):
                if not CXRGBColor.is_color_list(value):
                    raise ValueError("RGB list must have three int values")
                else:
                    candidate = {
                        'r': value[0],
                        'g': value[1],
                        'b': value[2],
                    }

            if isinstance(value, dict):
                if not CXRGBColor.is_color_dict(value):
                    raise ValueError(
                        "RGB dict must have three int values for keys"
                        " 'r', 'g', 'b'"
                    )
                else:
                    candidate = dict(value)

            self.__value = candidate

    def __init__(self, label: str, value: int):
        super().__init__(label, value)
        self.__value = {
            'r': 0,
            'g': 0,
            'b': 0,
        }

        self.value = value

    def __str__(self) -> str:
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
        r = self.value['r']
        g = self.value['g']
        b = self.value['b']
        return f"CXRGBColor(" \
               f" label={json.dumps(self.label)}," \
               f" value='rgb({r},{g},{b})'" \
               f")"


class CXGraphTypeOptions(Enum):
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
    Density = 'Density'
    Donnut = 'Donnut'
    DotLine = 'DotLine'
    Dotplot = 'Dotplot'
    Facet = 'Facet'
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
    Notes the legal CanvasXpress types of graphs, such as 'Bar'.
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
        :param value: The string value to set.
        """
        CXString.value.fset(self, value)

    def __init__(
            self,
            type: Union[CXGraphTypeOptions, str] = CXGraphTypeOptions.Bar
    ):
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
