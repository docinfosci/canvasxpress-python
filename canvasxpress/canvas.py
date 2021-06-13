import json
import uuid
from typing import Union, List

from deprecated import deprecated

from canvasxpress.config.collection import CXConfigs
from canvasxpress.config.type import CXConfig, CXGraphTypeOptions
from canvasxpress.data.base import CXData, CXProfiledData
from canvasxpress.data.convert import CXHtmlConvertable
from canvasxpress.data.keypair import CXDictData
from canvasxpress.data.profile import CXVennProfile, CXStandardProfile, \
    CXNetworkProfile, CXGenomeProfile, CXRawProfile
from canvasxpress.js.collection import CXEvents
from canvasxpress.js.function import CXEvent
from canvasxpress.util.template import render_from_template

_CX_JS_TEMPLATE = \
    "var cX@cx_target_id@ = new CanvasXpress(@cx_json@);"
"""
The template for declaring a CanvasXpress Javascript object using data
from the Python edition.
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
    def render_to(self) -> str:
        """
        The ID of the CanvasXpress object's associated HTML components, such as
        the render canvas element.  Sets the `id` attribute of the `<canvas>`
        element.
        :returns: `str` The ID
        """
        return self.__target_id

    @render_to.setter
    def render_to(self, value: str) -> None:
        """
        Sets the render_to of the CanvasXpress instance.  Sets the `id`
        attribute of the `<canvas>` element.
        :param value:
            `str` The ID to be associated.  Cannot be `None`, and
            must be alphanumeric.
        """
        if value is None:
            raise ValueError("value cannot be None")

        elif not isinstance(value, str):
            raise TypeError("value must be of type str")

        elif not value.isidentifier():
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
                raise ValueError(
                    "CanvasXpress license files must be named 'CanvasXpressLicense.js'")

            else:
                self.__license_url = candidate

    CHART_WIDTH_DEFAULT: int = 500
    """
    Default width of the chart when rendered, such as into HTML.
    """

    __chart_width: int = CHART_WIDTH_DEFAULT
    """
    Preferred width of the chart when rendered, such as into HTML.
    """

    @property
    def width(self) -> int:
        """
        Indicates the preferred <canvas> Web element width when rendered.  This
        property is used to facilitate integration with Web containers such
        as Jupyter notebooks. Added to the `<canvas>` element, and also
        influences render containers for contexts such as Jupyter Notebooks.
        :returns: `int` The width
        """
        return self.__chart_width

    @width.setter
    def width(self, value: int):
        """
        Sets the preferred Web element width when rendered. Added to the
        `<canvas>` element, and also influences render containers for contexts
        such as Jupyter Notebooks.
        :param value: `int`
            The pixel count.  Cannot be `None` or less than `1`.
        """
        if value is None:
            raise ValueError("element_width cannot be None")

        elif not isinstance(value, int):
            raise TypeError("element_width must be an int.")

        elif value < 1:
            raise ValueError("element_width cannot be less than 1 pixel")

        else:
            self.__chart_width = value

    CHART_HEIGHT_DEFAULT: int = 500
    """
    Default height of the chart in pixels when rendered, such as into HTML.
    """

    __chart_height: int = CHART_HEIGHT_DEFAULT
    """
    Preferred height of the chart in pixels when rendered, such as into HTML.
    """

    @property
    def height(self) -> int:
        """
        Indicates the preferred Web element height when rendered.  This
        property is used to facilitate integration with Web containers such
        as Jupyter notebooks.  Added to the `<canvas>` element, and also
        influences render containers for contexts such as Jupyter Notebooks.
        :returns: `int` The pixel count
        """
        return self.__chart_height

    @height.setter
    def height(self, value: int):
        """
        Sets the preferred Web element height when rendered.  Added to the
        `<canvas>` element, and also influences render containers for contexts
        such as Jupyter Notebooks.
        :param value: `int`
        """
        if value is None:
            raise ValueError("element_height cannot be None")

        elif not isinstance(value, int):
            raise TypeError("element_height must be an int.")

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
    def config(self) -> CXConfigs:
        """
        Provides access to the CXConfigs associated with this CanvasXpress chart.
        :returns: `CXConfigs` The config to be associated with the chart.
        """
        return self.__config

    @config.setter
    def config(
            self,
            value: Union[
                List[CXConfig], List[tuple], dict, CXConfigs, CXConfigs
            ]
    ):
        """
        Sets the CXConfigs associated with this CanvasXpress chart.
        :param value: `Union[List[CXConfig], List[tuple], dict, CXConfigs, CXConfigs]`
            An object translatable into a CXConfigs
            type.  If the object is an instance of CXConfigs then it will be
            tracked by the CanvasXpress object; otherwise, a new CXConfigs
            object will be created to manage the content.
        """
        if value is None:
            self.__config = CXConfigs()

        elif isinstance(value, list):
            self.__config = CXConfigs(*value)

        elif isinstance(value, dict):
            self.__config = CXConfigs(value)

        elif isinstance(value, CXConfigs):
            self.__config = value

        else:
            raise TypeError(
                "value must be one of Union[List[CXConfig], List[tuple], "
                "dict, CXConfigs, CXConfigs]"
            )

    __after_render: CXConfigs = None
    """
    __after_render is used to compose the afterRender settings for the 
    CanvasXpress object.
    """

    @property
    def after_render(self) -> CXConfigs:
        """
        Provides access to the CXConfigs associated with this CanvasXpress
        chart's afterRender property.
        :returns: `CXConfigs`
            The after_render configuration to be associated with the chart.
        """
        return self.__after_render

    @after_render.setter
    def after_render(
            self,
            value: Union[
                List[CXConfig], List[tuple], dict, CXConfigs, CXConfigs
            ]
    ):
        """
        Sets the CXConfigs associated with this CanvasXpress chart's afterRender
        property.
        :param value: `Union[List[CXConfig], List[tuple], dict, CXConfigs, CXConfigs]`
            An object translatable into a CXConfigs
            type.  If the object is an instance of CXConfigs then it will be
            tracked by the CanvasXpress object; otherwise, a new CXConfigs
            object will be created to manage the content.
        """
        if value is None:
            self.__after_render = CXConfigs()

        elif isinstance(value, list):
            self.__after_render = CXConfigs(*value)

        elif isinstance(value, dict):
            self.__after_render = CXConfigs(value)

        elif isinstance(value, CXConfigs):
            self.__after_render = value

        else:
            raise TypeError(
                "value must be one of Union[List[CXConfig], List[tuple], "
                "dict, CXConfigs, CXConfigs]"
            )

    __canvas_attributes = CXConfigs()
    """
    __canvas_attributes modify the <canvas> element generated by this object.
    """

    @property
    def canvas(self) -> CXConfigs:
        """
        Provides access to the attributes to be used with the `<canvas>`
        element generated by this object.  Each element is tracked as a CXConfig
        object.  Note that `id`, `width`, and `height` are uniquely set using
        the respective `id`, `width`, and `height` properties of this
        `CanvasXpress` object due to their mandatory nature.
        :returns: `CXConfigs`
            The element attributes as CXConfig entries to be associated with
            the `<canvas>` element.
        """
        return self.__canvas_attributes

    @canvas.setter
    def canvas(
            self,
            value: Union[
                List[CXConfig], List[tuple], dict, CXConfigs, CXConfigs
            ]
    ):
        """
        Sets the attributes to be incorporated into the `<canvas>` element
        generated by this object.  Each element is tracked as a CXConfig
        object. <br><br>
        Note that `id`, `width`, and `height` are uniquely set using
        the respective `id`, `width`, and `height` properties of this
        `CanvasXpress` object due to their mandatory nature, and values for such
        will not be kept in the `canvas` configs.

        :param value: `Union[List[CXConfig], List[tuple], dict, CXConfigs, CXConfigs]`
            An object translatable into a CXConfigs
            type.  If the object is an instance of CXConfigs then it will be
            tracked by the CanvasXpress object; otherwise, a new CXConfigs
            object will be created to manage the content.
        """
        if value is None:
            self.__canvas_attributes = CXConfigs()

        elif isinstance(value, list):
            self.__canvas_attributes = CXConfigs(*value)

        elif isinstance(value, dict):
            self.__canvas_attributes = CXConfigs(value)

        elif isinstance(value, CXConfigs):
            self.__canvas_attributes = value

        else:
            raise TypeError(
                "value must be one of Union[List[CXConfig], List[tuple], "
                "dict, CXConfigs, CXConfigs]"
            )

        # Clean override properties
        disallowed_attributes = ['id', 'width', 'height']
        for attribute in disallowed_attributes:
            self.canvas.remove(attribute)

    def __init__(
            self,
            render_to: str = None,
            data: Union[CXData, dict] = None,
            events: Union[List[CXEvent], CXEvents] = None,
            config: Union[List[CXConfig], List[tuple], dict, CXConfigs] = None,
            after_render: Union[
                List[CXConfig], List[tuple], dict, CXConfigs
            ] = None,
            canvas: Union[List[CXConfig], List[tuple], dict, CXConfigs] = None,
            width: int = CHART_WIDTH_DEFAULT,
            height: int = CHART_HEIGHT_DEFAULT
    ) -> None:
        """
        Initializes a new CanvasXpress object.  Default values are provided for
        all parameters if values are not specified; otherwise the arguments are
        treated as if an appropriate setter were used.
        :param render_to: See `render_to` property, except that on default
            initialization the object will be assigned an UUID4 value.
        :param data: See the `data` property
        :param events: See the `events` property
        :param config: See the `config` property
        :param after_render: See the `after_render` property
        :param canvas: See the 'canvas` property
        :param width: See the `width` property
        :param height: See the `height` property
        """

        super().__init__()

        if render_to:
            self.__target_id = render_to

        else:
            self.__target_id = str(uuid.uuid4())

        self.data = data
        self.events = events
        self.config = config
        self.after_render = after_render
        self.canvas = canvas
        self.width = width
        self.height = height

    def update_data_profile(
            self,
            data: CXData,
            fix_missing_profile: bool,
            match_profile_to_graphtype: bool
    ):
        """
        Inspects the `CXData` object to see if it is a `CXProfiledData` object.
        If so, then `fix_missing_profile` and `match_profile_to_graphtype` are
        evaluated to determine if profile adjustments are to be made, and then
        applied if/as appropriate.

        :param data: `CXData`
            The data to inspect.  Only `CXProfiledData` objects will be 
            modified.
            
        :param fix_missing_profile: `bool`
            Defaults to `True`.  If `True` then CXData used for the chart will
            be provided with a data profile appropriate to the `graphType`
            (or CXStandardProfile if no graphType is provided).  If `False`
            then no profile will be applied to those data objects without
            profiles.

        :param match_profile_to_graphtype: `bool`
            Defaults to `True`.  If `True` then the `graphType` will be
            inspected and an appropriate data profile will be applied to
            the data object.  If a profile of an appropriate type is already
            associated then nothing is changed.  If a CXRawProfile is associated
            then no change is made regardless of the paranmeter value.
            Missing profiles are ignored unless fix_missing_profile is also
            `True`.  If `False` then no change to the data profile will be made
            if a profile is already associated with the data object.
        """
        if isinstance(data, CXProfiledData):
            if fix_missing_profile and not data.profile:
                data.profile = CXStandardProfile

            if match_profile_to_graphtype and data.profile:
                if not isinstance(data.profile, CXRawProfile):
                    graphType = self.config.get_param("graphType")
                    if not graphType:
                        if not isinstance(data.profile, CXStandardProfile):
                            data.profile = CXStandardProfile()

                    else:
                        special_types = {
                            CXGraphTypeOptions.Venn.value:
                                CXVennProfile(),
                            CXGraphTypeOptions.Network.value:
                                CXNetworkProfile(),
                            CXGraphTypeOptions.Genome.value:
                                CXGenomeProfile()
                        }

                        if special_types.get(graphType.value):
                            if not isinstance(
                                    data.profile,
                                    type(special_types[graphType.value])
                            ):
                                data.profile = special_types[
                                    graphType.value
                                ]

                        else:
                            if not isinstance(data.profile, CXStandardProfile):
                                data.profile = CXStandardProfile()
                                
    def render_to_html_parts(
            self,
            fix_missing_profile: bool = True,
            match_profile_to_graphtype: bool = True
    ) -> dict:
        """
        Converts the CanvasXpress object into HTML5 complant script.

        If the associated `CXData` is a type of `CXProfiledData` and a profile
        has yet to be assigned then a profile can be assigned according to the
        `CXConfig` labelled `graphType`.  If a profile is assigned but is not
        `CXRawProfile` then the `graphType` can be reassessed, and if
        appropriate a new profile better aligned to the data can be provided.

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

        :param fix_missing_profile: `bool`
            Defaults to `True`.  If `True` then CXData used for the chart will
            be provided with a data profile appropriate to the `graphType`
            (or CXStandardProfile if no graphType is provided).  If `False`
            then no profile will be applied to those data objects without
            profiles.

        :param match_profile_to_graphtype: `bool`
            Defaults to `True`.  If `True` then the `graphType` will be
            inspected and an appropriate data profile will be applied to
            the data object.  If a profile of an appropriate type is already
            associated then nothing is changed.  If a CXRawProfile is associated
            then no change is made regardless of the paranmeter value.
            Missing profiles are ignored unless fix_missing_profile is also
            `True`.  If `False` then no change to the data profile will be made
            if a profile is already associated with the data object.
        """
        # For profiled data types, ensure a profile is assigned for rendering
        self.update_data_profile(
            self.data,
            fix_missing_profile,
            match_profile_to_graphtype
        )

        canvasxpress = {
            'renderTo': self.render_to,
            'data': self.data.render_to_dict(
                config=self.config
            ),
            'config': self.config.render_to_dict(),
            'afterRender': self.after_render.render_to_list(),
            'events': "js_events"
        }

        # Support unique data without JSON data structure
        if canvasxpress['data'].get('raw'):
            canvasxpress['data'] = canvasxpress['data']['raw']

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

        canvas_configs = CXConfigs(
            {
                'id': self.render_to,
                'width': self.width,
                'height': self.height,
            }
        )
        canvas_configs.add(
            self.canvas.render_to_dict()
        )
        cx_canvas = "<canvas " + \
                    " ".join(
                        [
                            f"{str(config.label)}={json.dumps(config.value)}"
                            for config in canvas_configs.configs
                        ]
                    ) + \
                    "></canvas>"

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
