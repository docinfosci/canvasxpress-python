<a name="canvasxpress"></a>
# canvasxpress

<a name="canvasxpress.util"></a>
# canvasxpress.util

<a name="canvasxpress.util.template"></a>
# canvasxpress.util.template

<a name="canvasxpress.util.template.render_from_template"></a>
#### render\_from\_template

```python
render_from_template(template: str, data: dict) -> str
```

Updates the template text with the provided data.

**Arguments**:

- `template`: The name of the template file
- `data`: the dict of str values with which to update the template text
:returns The adjusted template text

<a name="canvasxpress.config"></a>
# canvasxpress.config

<a name="canvasxpress.config.type"></a>
# canvasxpress.config.type

<a name="canvasxpress.config.type.CXConfig"></a>
## CXConfig Objects

```python
@total_ordering
class CXConfig(ABC)
```

CXConfig provides the means by which CanvasXpress objects can be configured for
customized rendering and interaction.

<a name="canvasxpress.config.type.CXDict"></a>
## CXDict Objects

```python
class CXDict(CXConfig)
```

<a name="canvasxpress.config.type.CXDict.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(label: str, value: Union[dict, str, None]) -> None
```

Initializes the CXData object with data.  Only dict or compatible data
types are accepted.

<a name="canvasxpress.config.type.CXGraphType"></a>
## CXGraphType Objects

```python
class CXGraphType(CXString)
```

Notes the legal CanvasXpress types of graphs, such as 'Bar'.

<a name="canvasxpress.config.type.CXGraphType.value"></a>
#### value

```python
 | @CXString.value.setter
 | value(value: Union[CXGraphTypeOptions, str]) -> None
```

Sets the value using a known CanvasXpress option.

<a name="canvasxpress.config.type.CXGraphType.set_custom_value"></a>
#### set\_custom\_value

```python
 | set_custom_value(value: str)
```

Permits a js value to be set, such as if a new option is recently
made available that the Python framework is yet to be aware of.

**Arguments**:

- `value`: The string value to set.

<a name="canvasxpress.config.collection"></a>
# canvasxpress.config.collection

<a name="canvasxpress.config.collection.CXConfigs"></a>
## CXConfigs Objects

```python
@total_ordering
class CXConfigs(CXDictConvertable)
```

CXConfigs provides support for addressing CXConfig values.

<a name="canvasxpress.config.collection.CXConfigs.set_param"></a>
#### set\_param

```python
 | set_param(label: str, value: Any) -> 'CXConfigs'
```

Adds a parameter to the configs.  Attempts to infer the kind of param to
add, and if a type can be deduced then an appropriate CXConfig is used.
If a type cannot be inferred the a text type is assumed.

<a name="canvasxpress.config.collection.CXConfigs.merge_configs"></a>
#### merge\_configs

```python
 | @classmethod
 | merge_configs(cls, configs: List[CXConfig]) -> dict
```

Given a list of CXConfig objects, a dictionary of unique attributes is
generated and provided.

**Returns**:

A dict of zero or more keys representing the CXConfigs.

<a name="canvasxpress.js"></a>
# canvasxpress.js

<a name="canvasxpress.js.collection"></a>
# canvasxpress.js.collection

<a name="canvasxpress.js.collection.CXEvents"></a>
## CXEvents Objects

```python
@total_ordering
class CXEvents(CXJavascriptConvertable)
```

CXEvents represents a set of CXEvent objects and can render them properly
for inclusion with a CanvasXpress object.

<a name="canvasxpress.js.collection.CXEvents.events"></a>
#### events

```python
 | @property
 | events() -> List[CXEvent]
```

A non-associated list of the CXEvents associated with this object.

<a name="canvasxpress.js.collection.CXEvents.has"></a>
#### has

```python
 | has(event: CXEvent)
```

Indicates if the react is a member.

**Arguments**:

- `event`: The object to consider

<a name="canvasxpress.js.collection.CXEvents.add"></a>
#### add

```python
 | add(event: CXEvent, unique: bool = True) -> None
```

Adds the specified react.  If the react must be unique then an Error
is raised if an react is already presenbt with the same ID.

<a name="canvasxpress.js.collection.CXEvents.remove"></a>
#### remove

```python
 | remove(event: CXEvent) -> bool
```

Removes the specified object from the list.

**Arguments**:

- `event`: The CXEvent object to remove from the list if it is
    already included.

**Returns**:

True if the react was removed.  False indicates that the
    object was not a member.

<a name="canvasxpress.js.collection.CXEvents.render_to_dict"></a>
#### render\_to\_dict

```python
 | render_to_dict() -> dict
```

Provides a dict with each js properly formatted as JS within.

<a name="canvasxpress.js.collection.CXEvents.render_to_js"></a>
#### render\_to\_js

```python
 | render_to_js() -> str
```

Converts the object into HTML5 complant script.

<a name="canvasxpress.js.collection.CXEvents.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(*events)
```

Establishes a new CXEvents object.

**Arguments**:

- `events`: A list of CXEvents to associate.

<a name="canvasxpress.js.function"></a>
# canvasxpress.js.function

<a name="canvasxpress.js.function.CXEvent"></a>
## CXEvent Objects

```python
@total_ordering
class CXEvent(CXJavascriptConvertable)
```

CXEvent represents a Javascript script that can be associated with a
CanvasXpress object.

<a name="canvasxpress.js.function.CXEvent.id"></a>
#### id

```python
 | @property
 | id() -> str
```

Provides access to the react ID.

**Returns**:

The ID as a string.

<a name="canvasxpress.js.function.CXEvent.id"></a>
#### id

```python
 | @id.setter
 | id(value: str) -> None
```

Sets the react ID, which is a keyword recognized by CanvasXpress.

**Arguments**:

- `value`: The ID, which must be a string compliant object.

<a name="canvasxpress.js.function.CXEvent.script"></a>
#### script

```python
 | @property
 | script() -> str
```

Provides access to the react script.

**Returns**:

The script as a string.

<a name="canvasxpress.js.function.CXEvent.script"></a>
#### script

```python
 | @script.setter
 | script(value: str) -> None
```

Sets the react script, which is logic that goes inside of the react
function.  Functions take the form:

function(o, e, t) {
    // script logic goes here
};

The script can be assumed to have access to all DOM elements as proper,
and it will be provided the parameters o, e, and t.  Read more about
react functions on the CanvasXpress.org site.

**Arguments**:

- `value`: The ID, which must be a UTF-8 string compliant object.

<a name="canvasxpress.js.function.CXEvent.render_to_js"></a>
#### render\_to\_js

```python
 | render_to_js() -> str
```

Converts the object into HTML5 complant script.

<a name="canvasxpress.js.function.CXEvent.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(id: str = "", script: str = "")
```

Provides a new CXEvent object.

**Arguments**:

- `id`: The ID of the react, such as mousemove.
- `script`: The script logic for the react.

<a name="canvasxpress.render"></a>
# canvasxpress.render

<a name="canvasxpress.render.base"></a>
# canvasxpress.render.base

<a name="canvasxpress.render.base.CXRenderable"></a>
## CXRenderable Objects

```python
class CXRenderable(ABC)
```

CXRenderable is capable of rendering a CanvasXpress object to some kind of
output or display device.

<a name="canvasxpress.render.base.CXRenderable.render"></a>
#### render

```python
 | @abstractmethod
 | render()
```

Renders the associated CanvasXpress object appropriate to the target.

<a name="canvasxpress.render.jupyter"></a>
# canvasxpress.render.jupyter

<a name="canvasxpress.render.jupyter.CXNoteBook"></a>
## CXNoteBook Objects

```python
class CXNoteBook(CXRenderable)
```

<a name="canvasxpress.render.jupyter.CXNoteBook.render"></a>
#### render

```python
 | render()
```

Renders the provided CanvasXpress object appropriate for display in
an IPython (e.g., Jupyter NoteBook/Lab) environment.

**Arguments**:

- `cx`: A valid CanvasXpress object.

<a name="canvasxpress.data"></a>
# canvasxpress.data

<a name="canvasxpress.data.matrix"></a>
# canvasxpress.data.matrix

<a name="canvasxpress.data.matrix.CXDataframeData"></a>
## CXDataframeData Objects

```python
@total_ordering
class CXDataframeData(CXData)
```

A CXData class dedicated to processing Python DataFrame, matrix-structured
 data.

<a name="canvasxpress.data.matrix.CXDataframeData.dataframe"></a>
#### dataframe

```python
 | @property
 | dataframe() -> DataFrame
```

A property accessor for the data managed by the object.

<a name="canvasxpress.data.matrix.CXDataframeData.data"></a>
#### data

```python
 | @property
 | data() -> dict
```

A property accessor for the data managed by the object.

<a name="canvasxpress.data.matrix.CXDataframeData.render_to_dict"></a>
#### render\_to\_dict

```python
 | render_to_dict() -> dict
```

Provides a dict representation of the data.

**Returns**:

The JSON as a str

<a name="canvasxpress.data.matrix.CXDataframeData.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(data: Union['CXDataframeData', DataFrame, dict, str, None] = None) -> None
```

Initializes the CXData object with data.  Only DataFrame or compatible
 data types are accepted.

<a name="canvasxpress.data.matrix.CXCSVData"></a>
## CXCSVData Objects

```python
class CXCSVData(CXDataframeData)
```

A CXData class dedicated to processing Python CSV-based, matrix-structured
 data.

<a name="canvasxpress.data.matrix.CXCSVData.csv"></a>
#### csv

```python
 | @property
 | csv() -> str
```

A property accessor for the data managed by the object.

<a name="canvasxpress.data.matrix.CXCSVData.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(data: Union['CXDataframeData', DataFrame, dict, str, None] = None) -> None
```

Initializes the CXData object with data.  Only DataFrame or compatible
 data types are accepted.

<a name="canvasxpress.data.convert"></a>
# canvasxpress.data.convert

<a name="canvasxpress.data.convert.CXHtmlConvertable"></a>
## CXHtmlConvertable Objects

```python
class CXHtmlConvertable(ABC)
```

CXHtmlConvertable represents an object that can be converted into HTML.

<a name="canvasxpress.data.convert.CXHtmlConvertable.render_to_html_parts"></a>
#### render\_to\_html\_parts

```python
 | @abstractmethod
 | render_to_html_parts() -> str
```

Converts the object into HTML5 complant script.

<a name="canvasxpress.data.convert.CXDictConvertable"></a>
## CXDictConvertable Objects

```python
class CXDictConvertable(ABC)
```

CXDictConvertable represents an object that can be converted into a dict.

<a name="canvasxpress.data.convert.CXDictConvertable.render_to_dict"></a>
#### render\_to\_dict

```python
 | @abstractmethod
 | render_to_dict() -> dict
```

Converts the object into HTML5 complant script.

<a name="canvasxpress.data.convert.CXJavascriptConvertable"></a>
## CXJavascriptConvertable Objects

```python
class CXJavascriptConvertable(ABC)
```

CXJavascriptConvertable represents an object that can be converted into JS.

<a name="canvasxpress.data.convert.CXJavascriptConvertable.render_to_js"></a>
#### render\_to\_js

```python
 | @abstractmethod
 | render_to_js() -> str
```

Converts the object into HTML5 complant script.

<a name="canvasxpress.data.keypair"></a>
# canvasxpress.data.keypair

<a name="canvasxpress.data.keypair.CXDictData"></a>
## CXDictData Objects

```python
@total_ordering
class CXDictData(CXData)
```

A CXData class dedicated to processing Python dict-structured data.

<a name="canvasxpress.data.keypair.CXDictData.data"></a>
#### data

```python
 | @property
 | data() -> dict
```

A property accessor for the data managed by the object.

<a name="canvasxpress.data.keypair.CXDictData.render_to_dict"></a>
#### render\_to\_dict

```python
 | render_to_dict() -> dict
```

Provides a dict representation of the data.

**Returns**:

The JSON as a str

<a name="canvasxpress.data.keypair.CXDictData.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(data: Union[dict, None] = None) -> None
```

Initializes the CXData object with data.  Only dict or compatible data
types are accepted.

<a name="canvasxpress.data.keypair.CXJSONData"></a>
## CXJSONData Objects

```python
class CXJSONData(CXDictData)
```

A CXData class dedicated to processing JSON data.

<a name="canvasxpress.data.keypair.CXJSONData.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(data: Union[dict, str, None] = None) -> None
```

Initializes the CXData object with data.  Only dict or compatible data
types are accepted.

<a name="canvasxpress.data.base"></a>
# canvasxpress.data.base

<a name="canvasxpress.data.base.CXData"></a>
## CXData Objects

```python
class CXData(CXDictConvertable)
```

CXData defines an essential data class for managing data acquisiton,
transformation, and introspection as required by the CXPress class.

<a name="canvasxpress.data.base.CXData.data"></a>
#### data

```python
 | @property
 | @abstractmethod
 | data() -> dict
```

A property accessor for the data managed by the object.  Regardless of
the input data the returned data structure will be a dict-type for use
with CanvasXpress.

<a name="canvasxpress.data.base.CXData.__init__"></a>
#### \_\_init\_\_

```python
 | @abstractmethod
 | __init__(data: Union[object, None]) -> None
```

Initializes the CXData object with data.

<a name="canvasxpress.canvas"></a>
# canvasxpress.canvas

<a name="canvasxpress.canvas.CanvasXpress"></a>
## CanvasXpress Objects

```python
class CanvasXpress(CXHtmlConvertable)
```

CXPress consolidates CanvasXpress behavior by representing a single chart
renderable by CanvasXpress.

<a name="canvasxpress.canvas.CanvasXpress.target_id"></a>
#### target\_id

```python
 | @property
 | target_id() -> str
```

The ID of the CanvasXpress object's associated HTML components, such as
the render canvas element.

<a name="canvasxpress.canvas.CanvasXpress.target_id"></a>
#### target\_id

```python
 | @target_id.setter
 | target_id(value: str) -> None
```

Sets the target_id of the CanvasXpress instance.

<a name="canvasxpress.canvas.CanvasXpress.CHART_WIDTH_DEFAULT"></a>
#### CHART\_WIDTH\_DEFAULT

Default width in pixels of the chart when rendered, such as into HTML.

<a name="canvasxpress.canvas.CanvasXpress.chart_width"></a>
#### chart\_width

```python
 | @property
 | chart_width() -> int
```

Provides the suggested canvas width.

<a name="canvasxpress.canvas.CanvasXpress.CHART_HEIGHT_DEFAULT"></a>
#### CHART\_HEIGHT\_DEFAULT

Default height in pixels of the chart when rendered, such as into HTML.

<a name="canvasxpress.canvas.CanvasXpress.chart_height"></a>
#### chart\_height

```python
 | @property
 | chart_height() -> int
```

Provides the suggested canvas height.

<a name="canvasxpress.canvas.CanvasXpress.data"></a>
#### data

```python
 | @property
 | data() -> CXData
```

Provides access to the CXData associated with this CanvasXpress chart.

<a name="canvasxpress.canvas.CanvasXpress.data"></a>
#### data

```python
 | @data.setter
 | data(value: Union[CXData, dict, None]) -> None
```

Sets the CXData associated with this CanvasXpress chart.

<a name="canvasxpress.canvas.CanvasXpress.events"></a>
#### events

```python
 | @events.setter
 | events(events: Union[CXEvents, list, None]) -> None
```

Sets the CXEvents associated with this CanvasXpress chart.

<a name="canvasxpress.canvas.CanvasXpress.render_to_html_parts"></a>
#### render\_to\_html\_parts

```python
 | render_to_html_parts() -> dict
```

Converts the CanvasXpress object into HTML5 complant script.

