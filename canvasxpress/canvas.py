import json
import uuid
from typing import Union, List

from deprecated import deprecated

from canvasxpress.config.collection import CXConfigs
from canvasxpress.config.type import CXConfig
from canvasxpress.data.convert import CXHtmlConvertable
from canvasxpress.data.keypair import CXData, CXDictData
from canvasxpress.js.collection import CXEvents
from canvasxpress.js.function import CXEvent
from canvasxpress.util.template import render_from_template

_CX_JS_TEMPLATE = \
    "var cX@cx_target_id@ = new CanvasXpress(@cx_json@);"
"""
The template for declaring a CanvasXpress Javascript object using data
from the Python edition.
"""

_CX_CANVAS_TEMPLATE = \
    "<canvas id='@cx_target_id@' width='@cx_canvas_width@' height=" \
    "'@cx_canvas_height@' aspectRatio='@cx_canvas_ratio@' responsive='true'>"
"""
The template for declaring an HTML div element that will be replaced with a
CanvasXpress chart on HTML execution.
"""

_CX_LICENSE_TEMPLATE = \
    "<script src='@cx_license@' type='text/javascript'></script>"
"""
The template for declaring a CanvasXpress license file so that charts do 
not render with unlicensed watermarks.
"""


class CanvasXpress(CXHtmlConvertable):
    """
    CanvasXpress acts as a proxy to the Javascript CanvasXpress object, and in
    general use remains similar to its Javascript counterpart.

    Assuming a flask function that returns a rendered page using the data from
    a CanvasXpress object:

    ```python
    @app.route('/pythonexample')
    def get_simple_chart() -> str:
        chart: CanvasXpress = CanvasXpress(
            render_to="example_chart",
            data=CXDictData(
                {
                    "y": {
                    "vars": ["Gene1"],
                    "smps": ["Smp1", "Smp2", "Smp3"],
                    "data": [[10, 35, 88]],
                }
            ),
            config=CXConfigs(
                CXGraphType(CXGraphTypeOptions.Bar)
            )
        )

        html_parts = chart.render_to_html_parts()

        return render_template(
            "bar.html",
            canvas_element=html_parts["cx_canvas"],
            bar_graph=html_parts["cx_js"]
        )
    ```
    """

    __target_id: str = None
    """
    __target_id is used by the JS renderTo param.
    """

    @property
    @deprecated(
        reason="As part of improved alignment with CanvasXpress for JS, use the"
               " render_to property instead."
    )
    def target_id(self) -> str:
        """
        DEPRECATED - Use render_to instead.
        """
        return self.render_to

    @target_id.setter
    @deprecated(
        reason="As part of improved alignment with CanvasXpress for JS, use the"
               " render_to property instead."
    )
    def target_id(self, value: str) -> None:
        """
        DEPRECATED - Use render_to instead.
        """
        self.render_to = value

    @property
    def render_to(self) -> str:
        """
        The ID of the CanvasXpress object's associated HTML components, such as
        the render canvas element.
        :returns: `str` The ID
        """
        return self.__target_id

    @render_to.setter
    def render_to(self, value: str) -> None:
        """
        Sets the render_to of the CanvasXpress instance.
        :param value:
            `str` The ID to be associated.  Cannot be `None`, and
            must be alphanumeric.
        """
        if value is None:
            raise ValueError("value cannot be None")

        elif not isinstance(value, str):
            raise TypeError("value must be of type str")

        elif any(not s.isidentifier() for s in value):
            raise ValueError("value must be only alpha numeric")

        else:
            self.__target_id = value

    __license_url: Union[str, None] = None
    """
    Location of the CanvasXpressLicense.js file for use in rendering.
    """

    @property
    def license_available(self) -> bool:
        """
        Indicates if a license is associated with the CanvasXpress object.
        :returns: `True` if a license file URL has been set.
        """
        return self.__license_url is not None

    @property
    def license_url(self) -> str:
        """
        Returns the location of the license file associated with the
        CanvasXpress object.
        :returns: `str` URL of the file or `None` if no file is associated.
        """
        return self.__license_url

    @license_url.setter
    def license_url(self, value: str) -> None:
        """
        Sets the location of the license file to be associated with the
        CanvasXpress object.
        :param value:
            `str` The path to the license file or `None` if a previously set URL
            is no longer valid.
        """
        if value is None:
            self.__license_url = None

        else:
            candidate = str(value)
            if "CanvasXpressLicense.js" not in candidate:
                raise ValueError("CanvasXpress license files must be named 'CanvasXpressLicense.js'")

            else:
                self.__license_url = candidate

    CHART_WIDTH_DEFAULT: int = 500
    """
    Default width in pixels of the chart when rendered, such as into HTML.
    """

    __chart_width: int = CHART_WIDTH_DEFAULT
    """
    Preferred width in pixels of the chart when rendered, such as into HTML.
    """

    @property
    @deprecated(
        reason="To avoid confusion with CanvasXpress JS attributes, this"
               "property has been renamed.  Use element_width instead."
    )
    def chart_width(self) -> int:
        """
        DEPRECATED - use element_width.
        """
        return self.element_width

    @chart_width.setter
    @deprecated(
        reason="To avoid confusion with CanvasXpress JS attributes, this"
               "property has been renamed.  Use element_width instead."
    )
    def chart_width(self, value: int):
        """
        DEPRECATED - use element_width.
        """
        self.element_width = value

    @property
    def element_width(self) -> int:
        """
        Indicates the preferred Web element width when rendered.  This is
        distinct from the CanvasXpress JS `width` attribute; the Python
        property is used to facilitate integration with Web containers such
        as Jupyter notebooks.
        :returns: `int` The pixel count
        """
        return self.__chart_width

    @element_width.setter
    def element_width(self, value: int):
        """
        Sets the preferred Web element width when rendered.
        :param value:
            `int` The pixel count.  Cannot be `None` or less than `1`.
        """
        if value is None:
            raise ValueError("element_width cannot be None")

        elif not isinstance(value, int):
            raise TypeError("value must be of type int")

        elif value < 1:
            raise ValueError("element_width cannot be less than 1 pixel")

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
    @deprecated(
        reason="To avoid confusion with CanvasXpress JS attributes, this"
               "property has been renamed.  Use element_height instead."
    )
    def chart_height(self) -> int:
        """
        DEPRECATED - use element_height.
        """
        return self.element_height

    @chart_height.setter
    @deprecated(
        reason="To avoid confusion with CanvasXpress JS attributes, this"
               "property has been renamed.  Use element_height instead."
    )
    def chart_height(self, value: int):
        """
        DEPRECATED - use element_height.
        """
        self.element_height = value

    @property
    def element_height(self) -> int:
        """
        Indicates the preferred Web element height when rendered.  This is
        distinct from the CanvasXpress JS `height` attribute; the Python
        property is used to facilitate integration with Web containers such
        as Jupyter notebooks.
        :returns: `int` The pixel count
        """
        return self.__chart_height

    @element_height.setter
    def element_height(self, value: int):
        """
        Sets the preferred Web element height when rendered.
        :param value:
            `int` The pixel count.  Cannot be `None` or less than `1`.
        """
        if value is None:
            raise ValueError("element_height cannot be None")

        elif not isinstance(value, int):
            raise TypeError("value must be of type int")

        elif value < 1:
            raise ValueError("element_height cannot be less than 1 pixel")

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
        :returns: `CXData` The data to be associated with the chart.
        """
        return self.__data

    @data.setter
    def data(self, value: Union[CXData, dict, None]) -> None:
        """
        Sets the CXData associated with this CanvasXpress chart.
        :param value:
            `CXData, dict, None` An object translatable into a CXData type.
            If the object is an instance of CXData then it will be tracked
            by the CanvasXpress object; otherwise, a new CXData object will
            be created to manage the content.
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
        """
        Provides access to the CXEvents associated with this CanvasXpress chart.
        :returns: `CXEvents` The events to be associated with the chart.
        """
        return self.__events

    @events.setter
    def events(self, events: Union[CXEvents, List[CXEvent], None]) -> None:
        """
        Sets the CXEvents associated with this CanvasXpress chart.
        :param events:
            `CXEvents, List[CXEvent], None` An object translatable into a
            CXEvents type.  If the object is an instance of CXEvents then it
            will be tracked by the CanvasXpress object; otherwise, a new
            CXEvents object will be created to manage the content.
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
    __config is used to compose the config settings for the CanvasXpress object.
    """

    @property
    @deprecated(
        reason="As part of improved alignment with CanvasXpress for JS, use the"
               " config property instead."
    )
    def configs(self) -> CXConfigs:
        """
        DEPRECATED - Use config instead.
        """
        return self.config

    @configs.setter
    @deprecated(
        reason="As part of improved alignment with CanvasXpress for JS, use the"
               " config property instead."
    )
    def configs(self, value: Union[List[CXConfig], CXConfigs]):
        """
        DEPRECATED - Use config instead.
        """
        self.config = value

    @property
    def config(self) -> CXConfigs:
        """
        Provides access to the CXConfigs associated with this CanvasXpress chart.
        :returns: `CXConfigs` The config to be associated with the chart.
        """
        return self.__config

    @config.setter
    def config(self, value: Union[List[CXConfig], CXConfigs]):
        """
        Sets the CXConfigs associated with this CanvasXpress chart.
        :param value:
            `List[CXConfig], CXConfigs` An object translatable into a CXConfigs
            type.  If the object is an instance of CXConfigs then it will be
            tracked by the CanvasXpress object; otherwise, a new CXConfigs
            object will be created to manage the content.
        """
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
            render_to: str = None,
            data: Union[CXData, dict] = None,
            events: Union[List[CXEvent], CXEvents] = None,
            config: Union[List[CXConfig], CXConfigs] = None
    ) -> None:
        """
        Initializes a new CanvasXpress object.  Default values are provided for
        all parameters if values are not specified; otherwise the arguments are
        treated as if an appropriate setter were used.
        :param render_to: See `render_to` property, except that on default
            initialization the object will be assigned an UUID4 value.
        :param data: See `data` property
        :param events: See `events` property
        :param config: See `config` property
        """

        super().__init__()

        self.__target_id = str(uuid.uuid4())
        if render_to:
            self.__target_id = render_to

        self.data = data
        self.events = events
        self.config = config

    def render_to_html_parts(self) -> dict:
        """
        Converts the CanvasXpress object into HTML5 complant script.
        :returns: `dict` A map of values appropriate for use in HTML, such as
            via a jinja template typical of flask apps.

        Assuming a jinja template such as this:
        ```html
        <html>
            <head>
                <meta charset="UTF-8">
                <title>Flask CanvasXpress Example</title>
            </head>
            <body>
                <!-- 1. DOM element where the visualization will be displayed -->
                {{canvas_element|safe}}

                <!-- 2. Include the CanvasXpress library -->
                <link href='https://www.canvasxpress.org/dist/canvasXpress.css' rel='stylesheet' type='text/css'/>
                <script src='https://www.canvasxpress.org/dist/canvasXpress.min.js' type='text/javascript'></script>

                <!-- 3. Include script to initialize object -->
                <script type="text/javascript">
                    onReady(function () {
                        {{bar_graph|safe}}
                    })
                </script>
            </body>
        </html>
        ```

        A flask function could render a page with a chart such as:
        ```python
        @app.route('/pythonexample')
        def get_simple_chart() -> str:
            chart: CanvasXpress = CanvasXpress(
                render_to="example_chart",
                data=CXDictData(
                    {
                        "y": {
                        "vars": ["Gene1"],
                        "smps": ["Smp1", "Smp2", "Smp3"],
                        "data": [[10, 35, 88]],
                    }
                ),
                config=CXConfigs(
                    CXGraphType(CXGraphTypeOptions.Bar)
                )
            )

            html_parts = chart.render_to_html_parts()

            return render_template(
                "bar.html",
                canvas_element=html_parts["cx_canvas"],
                bar_graph=html_parts["cx_js"]
            )
        ```
        """
        canvasxpress = {
            'renderTo': self.render_to,
            'data': self.data.render_to_dict(),
            'config': self.config.render_to_dict(),
            'events': "js_events"
        }

        cx_js = render_from_template(
            _CX_JS_TEMPLATE,
            {
                'cx_target_id': self.render_to,
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
            _CX_CANVAS_TEMPLATE,
            {
                'cx_target_id': self.render_to,
                'cx_canvas_width': self.element_width,
                'cx_canvas_height': self.element_height,
                'cx_canvas_ratio': "1:1",
            }
        )

        cx_license = render_from_template(
            _CX_LICENSE_TEMPLATE,
            {
                'cx_license': self.license_url
            }
        )

        cx_web_data = dict()
        cx_web_data['cx_js'] = cx_js
        cx_web_data['cx_canvas'] = cx_canvas
        if self.license_available:
            cx_web_data['cx_license'] = cx_license

        return cx_web_data
