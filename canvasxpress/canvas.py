import json
import uuid
from typing import Union, List

from canvasxpress.config.type import CXType
from canvasxpress.config.collection import CXConfigs
from canvasxpress.data.convert import CXHtmlConvertable
from canvasxpress.data.keypair import CXData, CXDictData
from canvasxpress.js.collection import CXEvents
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

    DEFAULT_WIDTH: int = 600
    DEFAULT_HEIGHT: int = 600

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

    @property
    def width(self) -> int:
        """
        Provides the suggested canvas width.
        """
        return self.DEFAULT_WIDTH

    @property
    def height(self) -> int:
        """
        Provides the suggested canvas height.
        """
        return self.DEFAULT_HEIGHT

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
    def data(self, data: Union[CXData, dict, None]) -> None:
        """
        Sets the CXData associated with this CanvasXpress chart.
        """
        if not data:
            self.__data = CXDictData()

        elif isinstance(data, CXData):
            self.__data = data

        elif isinstance(data, dict):
            self.__data = CXDictData(data)

        else:
            raise ValueError("data must be None or of type CXData.")

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
            self.__events = CXEvents(events)

        else:
            raise ValueError("events must be None or of type CXEvents.")

    __config: CXConfigs = None
    """
    __config is used to compose the config settings for the CanvasXpress object.
    """

    @property
    def config(self) -> CXConfigs:
        return self.__config

    @config.setter
    def config(self, value: Union[List[CXType], CXConfigs]):
        if isinstance(value, list):
            self.__config = CXConfigs(value)

        elif isinstance(value, CXConfigs):
            self.__config = value

        elif value is None:
            self.__config = CXConfigs()

        else:
            raise TypeError("value must be List[CXType] or CXConfigs")

    def __init__(
            self,
            target_id: str = None,
            data: CXData = None,
            events: CXEvents = None,
            config: Union[List[CXType], CXConfigs] = None
    ) -> None:

        super().__init__()

        self.__target_id = str(uuid.uuid4())
        if target_id:
            self.__target_id = target_id

        self.data = data
        self.events = events
        self.config = config

    def render_to_html_parts(self) -> dict:
        """
        Converts the CanvasXpress object into HTML5 complant script.
        """
        config: dict = None

        canvasxpress = {
            'renderTo': self.target_id,
            'data': self.data.render_to_dict(),
            'config': self.config.render_to_dict(),
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
                'cx_canvas_width': self.DEFAULT_WIDTH,
                'cx_canvas_height': self.DEFAULT_HEIGHT,
                'cx_canvas_ratio': "1:1",
            }
        )

        return {
            'cx_js': cx_js,
            'cx_canvas': cx_canvas
        }
