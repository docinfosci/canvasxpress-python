import json
import uuid
from typing import Union, List

from canvasxpress.config.collection import CXConfigs
from canvasxpress.config.type import CXConfig
from canvasxpress.data.convert import CXHtmlConvertable
from canvasxpress.data.keypair import CXData, CXDictData
from canvasxpress.js.collection import CXEvents
from canvasxpress.js.function import CXEvent
from canvasxpress.util.template import render_from_template

CX_JS_TEMPLATE = \
    "var cX@cx_target_id@ = new CanvasXpress(@cx_json@);"

CX_CANVAS_TEMPLATE = \
    "<canvas id='@cx_target_id@' width='@cx_canvas_width@' height=" \
    "'@cx_canvas_height@' aspectRatio='@cx_canvas_ratio@' responsive='true'>"


class CanvasXpress(CXHtmlConvertable):
    """
    CXPress consolidates CanvasXpress behavior by representing a single chart
    renderable by CanvasXpress.
    """

    __target_id: str = None
    """
    __target_id is used by the JS renderTo param.
    """

    @property
    def target_id(self) -> str:
        """
        The ID of the CanvasXpress object's associated HTML components, such as
        the render canvas element.
        """
        return self.__target_id

    @target_id.setter
    def target_id(self, value: str) -> None:
        """
        Sets the target_id of the CanvasXpress instance.
        """
        if value is None:
            raise ValueError("value cannot be None")

        elif not isinstance(value, str):
            raise TypeError("value must be of type str")

        elif any(not s.isidentifier() for s in value):
            raise ValueError("value must be only alpha numeric")

        else:
            self.__target_id = value

    CHART_WIDTH_DEFAULT: int = 500
    """
    Default width in pixels of the chart when rendered, such as into HTML.
    """

    __chart_width: int = CHART_WIDTH_DEFAULT
    """
    Preferred width in pixels of the chart when rendered, such as into HTML.
    """

    @property
    def chart_width(self) -> int:
        """
        Provides the suggested canvas width.
        """
        return self.__chart_width

    @chart_width.setter
    def chart_width(self, value: int):
        if value is None:
            raise ValueError("chart_width cannot be None")

        elif not isinstance(value, int):
            raise TypeError("value must be of type int")

        elif value < 1:
            raise ValueError("chart_width cannot be less than 1 pixel")

        else:
            self.__chart_width = value

    CHART_HEIGHT_DEFAULT: int = 500
    """
    Default height in pixels of the chart when rendered, such as into HTML.
    """

    __chart_height: int = CHART_HEIGHT_DEFAULT
    """
    Preferred height in pixels of the chart when rendered, such as into HTML.
    """

    @property
    def chart_height(self) -> int:
        """
        Provides the suggested canvas height.
        """
        return self.__chart_height

    @chart_height.setter
    def chart_height(self, value: int):
        if value is None:
            raise ValueError("chart_height cannot be None")

        elif not isinstance(value, int):
            raise TypeError("value must be of type int")

        elif value < 1:
            raise ValueError("chart_height cannot be less than 1 pixel")

        else:
            self.__chart_height = value

    __data: CXData = None
    """
    _data is used by the JS data param, and it can be of numerous forms.  This
    class provides mapping mechanisms to translate Python objects into 
    structures usable by CanvasXpress.
    """

    @property
    def data(self) -> CXData:
        """
        Provides access to the CXData associated with this CanvasXpress chart.
        """
        return self.__data

    @data.setter
    def data(self, value: Union[CXData, dict, None]) -> None:
        """
        Sets the CXData associated with this CanvasXpress chart.
        """
        if value is None:
            self.__data = CXDictData()

        elif isinstance(value, CXData):
            self.__data = value

        elif isinstance(value, dict):
            self.__data = CXDictData(value)

        else:
            raise TypeError("data must be of type CXData or dict")

    __events: CXEvents = None
    """
    __events is used by the JS events param.
    """

    @property
    def events(self) -> CXEvents:
        return self.__events

    @events.setter
    def events(self, events: Union[CXEvents, list, None]) -> None:
        """
        Sets the CXEvents associated with this CanvasXpress chart.
        """
        if not events:
            self.__events = CXEvents()

        elif isinstance(events, CXEvents):
            self.__events = events

        elif isinstance(events, list):
            self.__events = CXEvents(*events)

        else:
            raise TypeError("value must be List[CXEvent] or CXEvents")

    __config: CXConfigs = None
    """
    __config is used to compose the configs settings for the CanvasXpress object.
    """

    @property
    def configs(self) -> CXConfigs:
        return self.__config

    @configs.setter
    def configs(self, value: Union[List[CXConfig], CXConfigs]):
        if value is None:
            self.__config = CXConfigs()

        elif isinstance(value, list):
            self.__config = CXConfigs(*value)

        elif isinstance(value, CXConfigs):
            self.__config = value

        else:
            raise TypeError("value must be List[CXConfig] or CXConfigs")

    def __init__(
            self,
            target_id: str = None,
            data: Union[CXData, dict] = None,
            events: Union[List[CXEvent], CXEvents] = None,
            configs: Union[List[CXConfig], CXConfigs] = None
    ) -> None:

        super().__init__()

        self.__target_id = str(uuid.uuid4())
        if target_id:
            self.__target_id = target_id

        self.data = data
        self.events = events
        self.configs = configs

    def render_to_html_parts(self) -> dict:
        """
        Converts the CanvasXpress object into HTML5 complant script.
        """
        canvasxpress = {
            'renderTo': self.target_id,
            'data': self.data.render_to_dict(),
            'configs': self.configs.render_to_dict(),
            'events': "js_events"
        }

        cx_js = render_from_template(
            CX_JS_TEMPLATE,
            {
                'cx_target_id': self.target_id,
                'cx_json': json.dumps(
                    canvasxpress,
                    indent=4
                )
            }
        )

        cx_js = cx_js.replace(
            '"js_events"', self.events.render_to_js(),
        )

        cx_canvas = render_from_template(
            CX_CANVAS_TEMPLATE,
            {
                'cx_target_id': self.target_id,
                'cx_canvas_width': self.chart_width,
                'cx_canvas_height': self.chart_height,
                'cx_canvas_ratio': "1:1",
            }
        )

        return {
            'cx_js': cx_js,
            'cx_canvas': cx_canvas
        }
