import json
import uuid
from typing import Union, List

from pandas import DataFrame
from deprecated import deprecated

from canvasxpress.config.collection import CXConfigs
from canvasxpress.config.type import CXConfig, CXGraphTypeOptions
from canvasxpress.data.base import CXData, CXProfiledData
from canvasxpress.data.convert import CXHtmlConvertable
from canvasxpress.data.keypair import CXDictData, CXJSONData
from canvasxpress.data.matrix import CXDataframeData, CXCSVData
from canvasxpress.data.profile import (
    CXVennProfile,
    CXStandardProfile,
    CXNetworkProfile,
    CXGenomeProfile,
    CXRawProfile,
)
from canvasxpress.data.text import CXTextData
from canvasxpress.js.collection import CXEvents
from canvasxpress.js.function import CXEvent
from canvasxpress.util.template import render_from_template

_CX_JS_TEMPLATE = "var cX@cx_target_id@ = new CanvasXpress(@cx_json@); @cx_functions@"
"""
The template for declaring a CanvasXpress Javascript object using data
from the Python edition.
"""

_CX_LICENSE_TEMPLATE = "<script src='@cx_license@' type='text/javascript'></script>"
"""
The template for declaring a CanvasXpress license file so that charts do 
not create_element with unlicensed watermarks.
"""

_CX_REPR_TEMPLATE = """CanvasXpress(
    render_to="@render_to@",
    data=@data@,
    config=@config@,
    width=@width@,
    height=@height@,
    events=@events@,
    after_render=@after_render@,
    other_init_params=@other_init_params@
)
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

    __target_id: Union[str, None] = None
    """
    __target_id is used by the JS renderTo param.  None indicates that the object is anonymous.
    """

    @property
    def anonymous(self) -> bool:
        """
        Indicates whether the object is anonymous.  If `True`, then `render_to()` will result in a one-time random
        ID string being returned for use in contexts such as rapidly changing React environments.  If `False`, then
        the ID string returned is the one set for the object by the developer.
        :returns: `bool` `True` if the object is anonymous; otherwise `False`.
        """
        return self.__target_id is None

    @property
    def render_to(self) -> Union[str, None]:
        """
        The ID of the CanvasXpress object's associated HTML components, such as
        the create_element canvas element.  Sets the `id` attribute of the `<canvas>`
        element.
        :returns: `str` The ID, if configured; `None` if anonymous.
        """
        return (
            str(uuid.uuid4()).replace("-", "") if self.anonymous else self.__target_id
        )

    @render_to.setter
    def render_to(self, value: Union[str, None]) -> None:
        """
        Sets the render_to of the CanvasXpress instance.  Sets the `id`
        attribute of the `<canvas>` element.
        :param value:
            `str` The ID to be associated.  Cannot be `None`, and
            must be alphanumeric.  Non-alphanumeric characters will
            be removed, except for `_`, and if the remaining string
            is empty then a UUID4 will be substituted.  This is to preserve JS
            compatibility during rendering. `None` can also be provided to
            indicate that this object should be anonymous, such as for use
            in rapidly changing React interfaces.
        """
        if not isinstance(value, str) and value is not None:
            raise TypeError("value must be of type str or None")

        elif value is not None:
            candidate = ""
            for c in value:
                if c.isalnum() or c == "_":
                    candidate += c
            if candidate == "":
                candidate = str(uuid.uuid4()).replace("-", "")

        else:
            candidate = value

        self.__target_id = candidate

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
                    "CanvasXpress license files must be named "
                    "'CanvasXpressLicense.js'"
                )

            else:
                self.__license_url = candidate

    __cdn_edition: Union[str, None] = None
    """
    The edition of CanvasXpress to use.  None indicates that the latest edition available shall be used.
    Used as a class variable.
    """

    @classmethod
    def cdn_edition(cls) -> Union[str, None]:
        """
        Indicates the version of CanvasXpress being used.

        :returns: `Union[str, None]`: The Javascript CDN version used or None if the latest.
        """
        return cls.__cdn_edition

    @classmethod
    def set_cdn_edition(cls, value) -> None:
        """
        Sets the version of the Javascript CDN to use when generating HTML or React components.  See thr CDN page
        for CanvasXpress to identify the versions available: https://cdnjs.com/libraries/canvasXpress.

        :param value:
            `Union[str, None]` The CDN version, such as `38.1`, or None if the latest version is preferred.
        """
        cls.__cdn_edition = None if value is None else str(value)

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
        influences create_element containers for contexts such as Jupyter Notebooks.
        :returns: `int` The width
        """
        return self.__chart_width

    @width.setter
    def width(self, value: int):
        """
        Sets the preferred Web element width when rendered. Added to the
        `<canvas>` element, and also influences create_element containers for contexts
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
        influences create_element containers for contexts such as Jupyter Notebooks.
        :returns: `int` The pixel count
        """
        return self.__chart_height

    @height.setter
    def height(self, value: int):
        """
        Sets the preferred Web element height when rendered.  Added to the
        `<canvas>` element, and also influences create_element containers for contexts
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
    def data(self, value: Union[CXData, dict, DataFrame, str, None]) -> None:
        """
        Sets the CXData associated with this CanvasXpress chart.
        :param value: `Union[CXData, dict, DataFrame, str, None]`
            An object translatable into a CXData type. If the object is an
            instance of CXData then it will be tracked by the CanvasXpress
            object; otherwise, a new CXData object will be created to manage
            the content.
        """
        if value is None:
            self.__data = CXDictData()

        elif isinstance(value, CXData):
            self.__data = value

        elif isinstance(value, dict):
            self.__data = CXDictData(value)

        elif isinstance(value, DataFrame):
            self.__data = CXDataframeData(value)

        elif isinstance(value, str):
            try:
                json.loads(value)
                self.__data = CXJSONData(value)

            except Exception:
                if (value.find(",") >= 0 or value.find("\t") >= 0) and value.find(
                    "\n"
                ) >= 0:
                    self.__data = CXCSVData(value)

                else:
                    self.__data = CXTextData(value)

        else:
            raise TypeError(
                "data must be of type CXData, dict, DataFrame, str, or None"
            )

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
        self, value: Union[List[CXConfig], List[tuple], List[list], dict, CXConfigs]
    ):
        """
        Sets the CXConfigs associated with this CanvasXpress chart.
        :param value: `Union[
                List[CXConfig],
                List[tuple],
                List[list],
                dict,
                CXConfigs
            ]`
            An object translatable into a CXConfigs type.  If the object is an
            instance of CXConfigs then it will be
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
        self, value: Union[List[CXConfig], List[tuple], List[list], dict, CXConfigs]
    ):
        """
        Sets the CXConfigs associated with this CanvasXpress chart's afterRender
        property.
        :param value: `Union[List[CXConfig], List[tuple], dict, CXConfigs,
            CXConfigs]`
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
    def other_init_params(self) -> CXConfigs:
        """
        Provides access to additional parameters that will be used with the
        `CanvasXpress` for Javascript constructor, such as `afterRencderInit`.

        :returns: `CXConfigs`
            `CXConfig` objects to be provided as additional Javascript
            constructor parameter values.
        """
        return self.__canvas_attributes

    @other_init_params.setter
    def other_init_params(
        self, value: Union[List[CXConfig], List[tuple], List[list], dict, CXConfigs]
    ):
        """
        Set the additional parameters to be used with the `CanvasXpress` for
        Javascript constructor, such as `afterRencderInit`. The following
        parameters will be ignored and the properties for this class should
        be used instead due to Python tier functionality useful to the
        developer:

        * `renderTo`: Use `CanvasXpress.render_to`
        * `data`: Use `CanvasXpress.data`
        * `config`: Use `CanvasXpress.config`
        * `afterRender`: Use `CanvasXpress.after_render`
        * `width`: Use `CanvasXpress.width`
        * `height`: Use `CanvasXpress.height`

        :param value: `Union[List[CXConfig], List[tuple], List[list], dict,
            CXConfigs]`
            An object translatable into a CXConfigs type.  If the object is an
            instance of CXConfigs then it will be tracked by the CanvasXpress
            object; otherwise, a new CXConfigs object will be created to manage
            the content.
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
                "value must be one of List[CXConfig], List[tuple], List[list], "
                "dict, CXConfigs"
            )

        # Clean override properties
        disallowed_attributes = [
            "id",
            "width",
            "height",
            "data",
            "config",
            "afterRender",
            "renderTo",
        ]
        for attribute in disallowed_attributes:
            self.other_init_params.remove(attribute)

    @classmethod
    def from_reproducible_json(
        cls, cx_json: str, include_factory: bool = False, include_system: bool = False
    ) -> "CanvasXpress":
        """
        Initializes a new `CanvasXpress` object using a reproducable research
        JSON saved from a CanvasXpress chart rendered in a Web browser.

        :param cx_json: `str`
            A valid reproducable research JSON typical of those created by
            CanvasXpress when running a Web browser.

        :param include_factory: `bool`
            Default `False`.  If `False` remove the `factory` attribute.

        :param include_system: `bool`
            Default `False`.  If `False` remove the `system` attribute.

        :returns: `CanvasXpress`
            Returns a new `CanvasXpress` object will all properties filled using
            the information provided by the reproducable research JSON.
        """
        try:
            cx_json_dict = json.loads(cx_json)

            if not include_factory:
                if cx_json_dict.get("factory"):
                    del cx_json_dict["factory"]

            if not include_system:
                if cx_json_dict.get("system"):
                    del cx_json_dict["system"]

            cx_render_to = cx_json_dict.get("renderTo")
            cx_data = cx_json_dict.get("data")
            cx_config = cx_json_dict.get("config")
            cx_after_render = cx_json_dict.get("afterRender")
            cx_width = cx_json_dict.get("width", 500)
            cx_height = cx_json_dict.get("height", 500)
            cx_other_init_params = [
                (str(param), cx_json_dict[param])
                for param in cx_json_dict.keys()
                if param
                not in [
                    "id",
                    "width",
                    "height",
                    "data",
                    "config",
                    "afterRender",
                    "renderTo",
                ]
            ]

            # Capure and remove setDimensions width, height
            setDimensions_indexes = list()
            for instruction_index, instruction in enumerate(cx_after_render):
                if isinstance(instruction, list):
                    if len(instruction) >= 2:
                        if instruction[0] == "setDimensions":
                            dimensions = instruction[1]
                            if isinstance(dimensions, list):
                                if len(dimensions) >= 2:
                                    if isinstance(dimensions[0], int):
                                        cx_width = dimensions[0]
                                    if isinstance(dimensions[1], int):
                                        cx_height = dimensions[1]
                            setDimensions_indexes.append(instruction_index)

            for index in reversed(setDimensions_indexes):
                del cx_after_render[index]

            candidate = CanvasXpress(
                render_to=cx_render_to,
                data=cx_data,
                config=cx_config,
                after_render=cx_after_render,
                other_init_params=cx_other_init_params,
                width=int(cx_width),
                height=int(cx_height),
            )

            return candidate

        except Exception as e:
            raise ValueError(
                "cx_json must be a valid CanvasXpress reproducable" " research JSON"
            )

    def __init__(
        self,
        render_to: str = None,
        data: Union[CXData, dict, DataFrame, str, None] = None,
        events: Union[List[CXEvent], CXEvents] = None,
        config: Union[List[CXConfig], List[tuple], dict, CXConfigs] = None,
        after_render: Union[List[CXConfig], List[tuple], dict, CXConfigs] = None,
        other_init_params: Union[List[CXConfig], List[tuple], dict, CXConfigs] = None,
        width: int = CHART_WIDTH_DEFAULT,
        height: int = CHART_HEIGHT_DEFAULT,
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
        :param other_init_params: See the 'other_init_params` property
        :param width: See the `width` property
        :param height: See the `height` property
        """

        super().__init__()

        self.render_to = render_to
        self.data = data
        self.events = events
        self.config = config
        self.after_render = after_render
        self.other_init_params = other_init_params
        self.width = width
        self.height = height

    def update_data_profile(
        self, data: CXData, fix_missing_profile: bool, match_profile_to_graphtype: bool
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
                            CXGraphTypeOptions.Venn.value: CXVennProfile(),
                            CXGraphTypeOptions.Network.value: CXNetworkProfile(),
                            CXGraphTypeOptions.Genome.value: CXGenomeProfile(),
                        }

                        if special_types.get(graphType.value):
                            if not isinstance(
                                data.profile, type(special_types[graphType.value])
                            ):
                                data.profile = special_types[graphType.value]

                        else:
                            if not isinstance(data.profile, CXStandardProfile):
                                data.profile = CXStandardProfile()

    def prepare_html_element_parts(
        self,
        fix_missing_profile: bool = True,
        match_profile_to_graphtype: bool = True,
    ) -> dict:
        """
        Converts the CanvasXpress object into CanvasXpress element components in
        anticipation of further use in renderable objects or conversion into HTML.

        If the associated `CXData` is a type of `CXProfiledData` and a profile
        has yet to be assigned then a profile can be assigned according to the
        `CXConfig` labelled `graphType`.  If a profile is assigned but is not
        `CXRawProfile` then the `graphType` can be reassessed, and if
        appropriate a new profile better aligned to the data can be provided.

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

        :returns: `dict` A map of values in anticipation of further conversion
            into html or a renderable.
        """
        self.update_data_profile(
            self.data,
            fix_missing_profile,
            match_profile_to_graphtype,
        )

        cx_element_params = {
            "renderTo": self.render_to,
            "data": self.data.render_to_dict(config=self.config),
            "config": self.config.render_to_dict(),
            "afterRender": self.after_render.render_to_list(),
            "otherParams": self.other_init_params.render_to_dict(),
            "events": "js_events",
            "width": self.width,
            "height": self.height,
        }

        # Support unique data without JSON data structure
        if cx_element_params["data"].get("raw"):
            cx_element_params["data"] = cx_element_params["data"]["raw"]

        cx_element_params["events"] = self.events.render_to_js()

        return cx_element_params

    def render_to_html_parts(
        self,
        fix_missing_profile: bool = True,
        match_profile_to_graphtype: bool = True,
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
                <!-- 1. DOM element where the visualization will be appear -->
                {{canvas_element|safe}}

                <!-- 2. Include the CanvasXpress library -->
                <link
                    href='https://www.canvasxpress.org/dist/canvasXpress.css'
                    rel='stylesheet' type='text/css'/>
                <script
                    src='https://www.canvasxpress.org/dist/canvasXpress.min.js'
                    type='text/javascript'>
                </script>

                <!-- 3. Include script to initialize object -->
                <script type="text/javascript">
                    onReady(function () {
                        {{bar_graph|safe}}
                    })
                </script>
            </body>
        </html>
        ```

        A flask function could create_element a page with a chart such as:
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
        self.update_data_profile(
            self.data, fix_missing_profile, match_profile_to_graphtype
        )

        primary_params = {
            "renderTo": self.render_to,
            "data": self.data.render_to_dict(config=self.config),
            "config": self.config.render_to_dict(),
            "events": "js_events",
        }
        secondary_params = self.other_init_params.render_to_dict()
        canvasxpress = {**primary_params, **secondary_params}
        after_render_functions = []
        for fx in self.after_render.render_to_list():
            params = [json.dumps(p) for p in fx[1]]
            after_render_functions.append(
                f"CanvasXpress.$('{self.render_to}').{fx[0]}({', '.join(params)})"
            )

        # Support unique data without JSON data structure
        if canvasxpress["data"].get("raw"):
            canvasxpress["data"] = canvasxpress["data"]["raw"]

        cx_js = render_from_template(
            _CX_JS_TEMPLATE,
            {
                "cx_target_id": self.render_to,
                "cx_json": json.dumps(canvasxpress),
                "cx_functions": "\n" + "; ".join(after_render_functions) + ";\n",
            },
        )

        cx_js = cx_js.replace(
            '"js_events"',
            self.events.render_to_js(),
        )

        canvas_configs = CXConfigs(
            {
                "id": self.render_to,
                "width": self.width,
                "height": self.height,
            }
        )
        cx_canvas = (
            "<canvas "
            + " ".join(
                [
                    f"{str(config.label)}={json.dumps(config.value)}"
                    for config in canvas_configs.configs
                ]
            )
            + "></canvas>"
        )

        cx_license = render_from_template(
            _CX_LICENSE_TEMPLATE, {"cx_license": self.license_url}
        )

        cx_web_data = dict()
        cx_web_data["cx_js"] = cx_js
        cx_web_data["cx_canvas"] = cx_canvas
        if self.license_available:
            cx_web_data["cx_license"] = cx_license

        return cx_web_data

    def __str__(self) -> str:
        """
        *str* function.  Converts the `CanvasXpress` object into a JSON
         representation.
        :returns" `str`
            JSON form of the `CanvasXpress` object.
        """
        data = str(type(self.data)).split(".")[-1][:-2] if self.data else "None"

        return (
            f"CanvasXpress ({hex(id(self))}):"
            f" render_to '{self.render_to}';"
            f" data <{data}>;"
            f" config {len(self.config.configs)} item(s);"
            f" after_render {len(self.after_render.configs)} item(s));"
            f" other_init_params"
            f" {len(self.other_init_params.configs)} item(s);"
            f" events {len(self.events.events)} function(s)."
        )

    def __repr__(self) -> str:
        """
        *repr* function.  Converts the `CanvasXpress` object into a pickle
        string that can be used with `eval` to establish a copy of the object.
        :returns: `str` An evaluatable representation of the object.
        """

        normalized_data = self.data.render_to_dict(config=self.config)
        if normalized_data.get("raw"):
            normalized_data = normalized_data["raw"]
        str_data = json.dumps(normalized_data)
        str_data_parts = str_data.split("\n")
        str_data = "\n".join(["    " + line for line in str_data_parts])[4:]

        str_config = json.dumps(self.config.render_to_dict())
        str_config_parts = str_config.split("\n")
        str_config = "\n".join(["    " + line for line in str_config_parts])[4:]

        str_after_render = json.dumps(self.after_render.render_to_list())
        str_after_render_parts = str_after_render.split("\n")
        str_after_render = "\n".join(
            ["    " + line for line in str_after_render_parts]
        )[4:]

        str_other_init_params = json.dumps(
            self.other_init_params.render_to_dict(), indent=4
        )
        str_other_init_params_parts = str_other_init_params.split("\n")
        str_other_init_params = "\n".join(
            ["    " + line for line in str_other_init_params_parts]
        )[4:]

        repr_str = (
            _CX_REPR_TEMPLATE.replace("@render_to@", self.render_to)
            .replace("@data@", str_data)
            .replace("@config@", str_config)
            .replace("@width@", json.dumps(self.width))
            .replace("@height@", json.dumps(self.height))
            .replace("@events@", repr(self.events))
            .replace("@after_render@", str_after_render)
            .replace("@other_init_params@", str_other_init_params)
            .replace("true", "True")
            .replace("false", "False")
            .replace("null", "None")
        )

        return repr_str
