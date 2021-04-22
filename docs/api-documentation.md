<a name="canvasxpress"></a>
# canvasxpress

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/__init__.py#L2)

<a name="canvasxpress.util"></a>
# canvasxpress.util

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/util/__init__.py#L2)

<a name="canvasxpress.util.template"></a>
# canvasxpress.util.template

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/util/template.py#L1)

<a name="canvasxpress.util.template.render_from_template"></a>
#### render\_from\_template

```python
render_from_template(template: str, data: dict) -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/util/template.py#L1)

Updates the template text with the provided data.

**Arguments**:

- `template`: The name of the template file
- `data`: the dict of str values with which to update the template text
:returns The adjusted template text

<a name="canvasxpress.config"></a>
# canvasxpress.config

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/config/__init__.py#L2)

<a name="canvasxpress.config.type"></a>
# canvasxpress.config.type

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/config/type.py#L1)

<a name="canvasxpress.config.type.CXConfig"></a>
## CXConfig Objects

```python
@total_ordering
class CXConfig(ABC)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/config/type.py#L12)

CXConfig provides the means by which CanvasXpress objects can be configured for
customized rendering and interaction.

<a name="canvasxpress.config.type.CXDict"></a>
## CXDict Objects

```python
class CXDict(CXConfig)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/config/type.py#L200)

<a name="canvasxpress.config.type.CXDict.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(label: str, value: Union[dict, str, None]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/config/type.py#L222)

Initializes the CXData object with data.  Only dict or compatible data
types are accepted.

<a name="canvasxpress.config.type.CXGraphType"></a>
## CXGraphType Objects

```python
class CXGraphType(CXString)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/config/type.py#L756)

Notes the legal CanvasXpress types of graphs, such as 'Bar'.

<a name="canvasxpress.config.type.CXGraphType.value"></a>
#### value

```python
 | @CXString.value.setter
 | value(value: Union[CXGraphTypeOptions, str]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/config/type.py#L764)

Sets the value using a known CanvasXpress option.

<a name="canvasxpress.config.type.CXGraphType.set_custom_value"></a>
#### set\_custom\_value

```python
 | set_custom_value(value: str)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/config/type.py#L780)

Permits a js value to be set, such as if a new option is recently
made available that the Python framework is yet to be aware of.

**Arguments**:

- `value`: The string value to set.

<a name="canvasxpress.config.collection"></a>
# canvasxpress.config.collection

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/config/collection.py#L1)

<a name="canvasxpress.config.collection.CXConfigs"></a>
## CXConfigs Objects

```python
@total_ordering
class CXConfigs(CXDictConvertable)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/config/collection.py#L11)

CXConfigs provides support for addressing CXConfig values.

<a name="canvasxpress.config.collection.CXConfigs.set_param"></a>
#### set\_param

```python
 | set_param(label: str, value: Any) -> 'CXConfigs'
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/config/collection.py#L35)

Adds a parameter to the configs.  Attempts to infer the kind of param to
add, and if a type can be deduced then an appropriate CXConfig is used.
If a type cannot be inferred the a text type is assumed.

<a name="canvasxpress.config.collection.CXConfigs.merge_configs"></a>
#### merge\_configs

```python
 | @classmethod
 | merge_configs(cls, configs: List[CXConfig]) -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/config/collection.py#L151)

Given a list of CXConfig objects, a dictionary of unique attributes is
generated and provided.

**Returns**:

A dict of zero or more keys representing the CXConfigs.

<a name="canvasxpress.js"></a>
# canvasxpress.js

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/js/__init__.py#L2)

<a name="canvasxpress.js.collection"></a>
# canvasxpress.js.collection

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/js/collection.py#L1)

<a name="canvasxpress.js.collection.CXEvents"></a>
## CXEvents Objects

```python
@total_ordering
class CXEvents(CXJavascriptConvertable)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/js/collection.py#L12)

CXEvents represents a set of CXEvent objects and can render them properly
for inclusion with a CanvasXpress object.

<a name="canvasxpress.js.collection.CXEvents.events"></a>
#### events

```python
 | @property
 | events() -> List[CXEvent]
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/js/collection.py#L24)

A non-associated list of the CXEvents associated with this object.

<a name="canvasxpress.js.collection.CXEvents.has"></a>
#### has

```python
 | has(event: CXEvent)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/js/collection.py#L30)

Indicates if the react is a member.

**Arguments**:

- `event`: The object to consider

<a name="canvasxpress.js.collection.CXEvents.add"></a>
#### add

```python
 | add(event: CXEvent, unique: bool = True) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/js/collection.py#L40)

Adds the specified react.  If the react must be unique then an Error
is raised if an react is already presenbt with the same ID.

<a name="canvasxpress.js.collection.CXEvents.remove"></a>
#### remove

```python
 | remove(event: CXEvent) -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/js/collection.py#L63)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/js/collection.py#L82)

Provides a dict with each js properly formatted as JS within.

<a name="canvasxpress.js.collection.CXEvents.render_to_js"></a>
#### render\_to\_js

```python
 | render_to_js() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/js/collection.py#L93)

Converts the object into HTML5 complant script.

<a name="canvasxpress.js.collection.CXEvents.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(*events)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/js/collection.py#L113)

Establishes a new CXEvents object.

**Arguments**:

- `events`: A list of CXEvents to associate.

<a name="canvasxpress.js.function"></a>
# canvasxpress.js.function

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/js/function.py#L1)

<a name="canvasxpress.js.function.CXEvent"></a>
## CXEvent Objects

```python
@total_ordering
class CXEvent(CXJavascriptConvertable)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/js/function.py#L12)

CXEvent represents a Javascript script that can be associated with a
CanvasXpress object.

<a name="canvasxpress.js.function.CXEvent.id"></a>
#### id

```python
 | @property
 | id() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/js/function.py#L34)

Provides access to the react ID.

**Returns**:

The ID as a string.

<a name="canvasxpress.js.function.CXEvent.id"></a>
#### id

```python
 | @id.setter
 | id(value: str) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/js/function.py#L42)

Sets the react ID, which is a keyword recognized by CanvasXpress.

**Arguments**:

- `value`: The ID, which must be a string compliant object.

<a name="canvasxpress.js.function.CXEvent.script"></a>
#### script

```python
 | @property
 | script() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/js/function.py#L56)

Provides access to the react script.

**Returns**:

The script as a string.

<a name="canvasxpress.js.function.CXEvent.script"></a>
#### script

```python
 | @script.setter
 | script(value: str) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/js/function.py#L64)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/js/function.py#L87)

Converts the object into HTML5 complant script.

<a name="canvasxpress.js.function.CXEvent.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(id: str = "", script: str = "")
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/js/function.py#L100)

Provides a new CXEvent object.

**Arguments**:

- `id`: The ID of the react, such as mousemove.
- `script`: The script logic for the react.

<a name="canvasxpress.render"></a>
# canvasxpress.render

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/render/__init__.py#L2)

<a name="canvasxpress.render.base"></a>
# canvasxpress.render.base

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/render/base.py#L1)

<a name="canvasxpress.render.base.CXRenderable"></a>
## CXRenderable Objects

```python
class CXRenderable(ABC)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/render/base.py#L7)

CXRenderable is capable of rendering a CanvasXpress object to some kind of
output or display device.

<a name="canvasxpress.render.base.CXRenderable.render"></a>
#### render

```python
 | @abstractmethod
 | render()
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/render/base.py#L38)

Renders the associated CanvasXpress object appropriate to the target.

<a name="canvasxpress.render.jupyter"></a>
# canvasxpress.render.jupyter

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/render/jupyter.py#L1)

<a name="canvasxpress.render.jupyter.CXNoteBook"></a>
## CXNoteBook Objects

```python
class CXNoteBook(CXRenderable)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/render/jupyter.py#L11)

<a name="canvasxpress.render.jupyter.CXNoteBook.render"></a>
#### render

```python
 | render()
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/render/jupyter.py#L19)

Renders the provided CanvasXpress object appropriate for display in
an IPython (e.g., Jupyter NoteBook/Lab) environment.

**Arguments**:

- `cx`: A valid CanvasXpress object.

<a name="canvasxpress.data"></a>
# canvasxpress.data

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/data/__init__.py#L2)

<a name="canvasxpress.data.matrix"></a>
# canvasxpress.data.matrix

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/data/matrix.py#L1)

<a name="canvasxpress.data.matrix.CXDataframeData"></a>
## CXDataframeData Objects

```python
@total_ordering
class CXDataframeData(CXData)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/data/matrix.py#L14)

A CXData class dedicated to processing Python DataFrame, matrix-structured
 data.

<a name="canvasxpress.data.matrix.CXDataframeData.dataframe"></a>
#### dataframe

```python
 | @property
 | dataframe() -> DataFrame
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/data/matrix.py#L26)

A property accessor for the data managed by the object.

<a name="canvasxpress.data.matrix.CXDataframeData.data"></a>
#### data

```python
 | @property
 | data() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/data/matrix.py#L40)

A property accessor for the data managed by the object.

<a name="canvasxpress.data.matrix.CXDataframeData.render_to_dict"></a>
#### render\_to\_dict

```python
 | render_to_dict() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/data/matrix.py#L88)

Provides a dict representation of the data.

**Returns**:

The JSON as a str

<a name="canvasxpress.data.matrix.CXDataframeData.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(data: Union['CXDataframeData', DataFrame, dict, str, None] = None) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/data/matrix.py#L95)

Initializes the CXData object with data.  Only DataFrame or compatible
 data types are accepted.

<a name="canvasxpress.data.matrix.CXCSVData"></a>
## CXCSVData Objects

```python
class CXCSVData(CXDataframeData)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/data/matrix.py#L183)

A CXData class dedicated to processing Python CSV-based, matrix-structured
 data.

<a name="canvasxpress.data.matrix.CXCSVData.csv"></a>
#### csv

```python
 | @property
 | csv() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/data/matrix.py#L190)

A property accessor for the data managed by the object.

<a name="canvasxpress.data.matrix.CXCSVData.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(data: Union['CXDataframeData', DataFrame, dict, str, None] = None) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/data/matrix.py#L208)

Initializes the CXData object with data.  Only DataFrame or compatible
 data types are accepted.

<a name="canvasxpress.data.convert"></a>
# canvasxpress.data.convert

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/data/convert.py#L1)

<a name="canvasxpress.data.convert.CXHtmlConvertable"></a>
## CXHtmlConvertable Objects

```python
class CXHtmlConvertable(ABC)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/data/convert.py#L4)

CXHtmlConvertable represents an object that can be converted into HTML.

<a name="canvasxpress.data.convert.CXHtmlConvertable.render_to_html_parts"></a>
#### render\_to\_html\_parts

```python
 | @abstractmethod
 | render_to_html_parts() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/data/convert.py#L10)

Converts the object into HTML5 complant script.

<a name="canvasxpress.data.convert.CXDictConvertable"></a>
## CXDictConvertable Objects

```python
class CXDictConvertable(ABC)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/data/convert.py#L17)

CXDictConvertable represents an object that can be converted into a dict.

<a name="canvasxpress.data.convert.CXDictConvertable.render_to_dict"></a>
#### render\_to\_dict

```python
 | @abstractmethod
 | render_to_dict() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/data/convert.py#L23)

Converts the object into HTML5 complant script.

<a name="canvasxpress.data.convert.CXJavascriptConvertable"></a>
## CXJavascriptConvertable Objects

```python
class CXJavascriptConvertable(ABC)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/data/convert.py#L30)

CXJavascriptConvertable represents an object that can be converted into JS.

<a name="canvasxpress.data.convert.CXJavascriptConvertable.render_to_js"></a>
#### render\_to\_js

```python
 | @abstractmethod
 | render_to_js() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/data/convert.py#L36)

Converts the object into HTML5 complant script.

<a name="canvasxpress.data.keypair"></a>
# canvasxpress.data.keypair

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/data/keypair.py#L1)

<a name="canvasxpress.data.keypair.CXDictData"></a>
## CXDictData Objects

```python
@total_ordering
class CXDictData(CXData)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/data/keypair.py#L12)

A CXData class dedicated to processing Python dict-structured data.

<a name="canvasxpress.data.keypair.CXDictData.data"></a>
#### data

```python
 | @property
 | data() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/data/keypair.py#L23)

A property accessor for the data managed by the object.

<a name="canvasxpress.data.keypair.CXDictData.render_to_dict"></a>
#### render\_to\_dict

```python
 | render_to_dict() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/data/keypair.py#L43)

Provides a dict representation of the data.

**Returns**:

The JSON as a str

<a name="canvasxpress.data.keypair.CXDictData.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(data: Union[dict, None] = None) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/data/keypair.py#L50)

Initializes the CXData object with data.  Only dict or compatible data
types are accepted.

<a name="canvasxpress.data.keypair.CXJSONData"></a>
## CXJSONData Objects

```python
class CXJSONData(CXDictData)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/data/keypair.py#L143)

A CXData class dedicated to processing JSON data.

<a name="canvasxpress.data.keypair.CXJSONData.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(data: Union[dict, str, None] = None) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/data/keypair.py#L168)

Initializes the CXData object with data.  Only dict or compatible data
types are accepted.

<a name="canvasxpress.data.base"></a>
# canvasxpress.data.base

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/data/base.py#L1)

<a name="canvasxpress.data.base.CXData"></a>
## CXData Objects

```python
class CXData(CXDictConvertable)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/data/base.py#L7)

CXData defines an essential data class for managing data acquisiton,
transformation, and introspection as required by the CXPress class.

<a name="canvasxpress.data.base.CXData.data"></a>
#### data

```python
 | @property
 | @abstractmethod
 | data() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/data/base.py#L15)

A property accessor for the data managed by the object.  Regardless of
the input data the returned data structure will be a dict-type for use
with CanvasXpress.

<a name="canvasxpress.data.base.CXData.__init__"></a>
#### \_\_init\_\_

```python
 | @abstractmethod
 | __init__(data: Union[object, None]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/data/base.py#L24)

Initializes the CXData object with data.

<a name="canvasxpress.canvas"></a>
# canvasxpress.canvas

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/canvas.py#L1)

<a name="canvasxpress.canvas.CanvasXpress"></a>
## CanvasXpress Objects

```python
class CanvasXpress(CXHtmlConvertable)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/canvas.py#L24)

CXPress consolidates CanvasXpress behavior by representing a single chart
renderable by CanvasXpress.

<a name="canvasxpress.canvas.CanvasXpress.target_id"></a>
#### target\_id

```python
 | @property
 | target_id() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/canvas.py#L36)

The ID of the CanvasXpress object's associated HTML components, such as
the render canvas element.

<a name="canvasxpress.canvas.CanvasXpress.target_id"></a>
#### target\_id

```python
 | @target_id.setter
 | target_id(value: str) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/canvas.py#L44)

Sets the target_id of the CanvasXpress instance.

<a name="canvasxpress.canvas.CanvasXpress.CHART_WIDTH_DEFAULT"></a>
#### CHART\_WIDTH\_DEFAULT

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/canvas.py#L86)

Default width in pixels of the chart when rendered, such as into HTML.

<a name="canvasxpress.canvas.CanvasXpress.chart_width"></a>
#### chart\_width

```python
 | @property
 | chart_width() -> int
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/canvas.py#L97)

Provides the suggested canvas width.

<a name="canvasxpress.canvas.CanvasXpress.CHART_HEIGHT_DEFAULT"></a>
#### CHART\_HEIGHT\_DEFAULT

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/canvas.py#L117)

Default height in pixels of the chart when rendered, such as into HTML.

<a name="canvasxpress.canvas.CanvasXpress.chart_height"></a>
#### chart\_height

```python
 | @property
 | chart_height() -> int
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/canvas.py#L128)

Provides the suggested canvas height.

<a name="canvasxpress.canvas.CanvasXpress.data"></a>
#### data

```python
 | @property
 | data() -> CXData
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/canvas.py#L156)

Provides access to the CXData associated with this CanvasXpress chart.

<a name="canvasxpress.canvas.CanvasXpress.data"></a>
#### data

```python
 | @data.setter
 | data(value: Union[CXData, dict, None]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/canvas.py#L163)

Sets the CXData associated with this CanvasXpress chart.

<a name="canvasxpress.canvas.CanvasXpress.events"></a>
#### events

```python
 | @events.setter
 | events(events: Union[CXEvents, list, None]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/canvas.py#L189)

Sets the CXEvents associated with this CanvasXpress chart.

<a name="canvasxpress.canvas.CanvasXpress.render_to_html_parts"></a>
#### render\_to\_html\_parts

```python
 | render_to_html_parts() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/a9d6adbacc7f6b084c083c15de0aff7851180764/canvasxpress/canvas.py#L246)

Converts the CanvasXpress object into HTML5 complant script.

