<a name="canvasxpress"></a>
# canvasxpress

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/__init__.py#L1)

The CanvasXpress package provides Python friendly management of the Javascript-
based [CanvasXpress](https://www.canvasxpress.org) library.  For an overview
and detailed instructions about CanvasXpress specifically please visit the site.

<a name="canvasxpress.util"></a>
# canvasxpress.util

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/util/__init__.py#L2)

<a name="canvasxpress.util.example"></a>
# canvasxpress.util.example

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/util/example/__init__.py#L2)

<a name="canvasxpress.util.example.generator"></a>
# canvasxpress.util.example.generator

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/util/example/generator.py#L1)

<a name="canvasxpress.util.example.generator.generate_canvasxpress_code_from_json_file"></a>
#### generate\_canvasxpress\_code\_from\_json\_file

```python
generate_canvasxpress_code_from_json_file(cx_json_path: str, document_includes: bool = True, document_render: bool = True, document_jupyter_render=False) -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/util/example/generator.py#L4)

Generates a string with a CanvasXPress in Python declaration using a
CanvasXpress reproducible research JSON stored in a file.

**Arguments**:

    A valid path to the reproducible JSON text from which a CanvasXPress
    object is to be built and then converted into example code.
    Default `True`.  Indicate if include headers should be prefixed.
    Default `True`.  Indicate if rendering should be included in the
    example code.
    Default `False`.  Indicate if Jupyter rendering should be performed;
    otherwise, popup rendering will suffixed.
- `cx_json_path`: `str`
- `document_includes`: `bool`
- `document_render`: `bool`
- `document_jupyter_render`: `bool`

**Returns**:

`str`

<a name="canvasxpress.util.example.generator.generate_canvasxpress_code_from_json"></a>
#### generate\_canvasxpress\_code\_from\_json

```python
generate_canvasxpress_code_from_json(cx_json: str, document_includes: bool = True, document_render: bool = True, document_jupyter_render=False) -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/util/example/generator.py#L38)

Generates a string with a CanvasXPress in Python declaration using a
CanvasXpress reproducible research JSON.

**Arguments**:

    The reproducible JSON text from which a CanvasXPress object is to be
    built and then converted into example code.
    Default `True`.  Indicate if include headers should be prefixed.
    Default `True`.  Indicate if rendering should be included in the
    example code.
    Default `False`.  Indicate if Jupyter rendering should be performed;
    otherwise, popup rendering will suffixed.
- `cx_json`: `str`
- `document_includes`: `bool`
- `document_render`: `bool`
- `document_jupyter_render`: `bool`

**Returns**:

`str`

<a name="canvasxpress.util.example.generator.generate_canvasxpress_code"></a>
#### generate\_canvasxpress\_code

```python
generate_canvasxpress_code(cx: CanvasXpress, document_includes: bool = True, document_render: bool = True, document_jupyter_render=False) -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/util/example/generator.py#L69)

Generates a string with a CanvasXPress in Python declaration.

**Arguments**:

    The `CanvasXpress` object from which to generate the example code.
    Default `True`.  Indicate if include headers should be prefixed.
    Default `True`.  Indicate if rendering should be included in the
    example code.
    Default `False`.  Indicate if Jupyter rendering should be performed;
    otherwise, popup rendering will suffixed.
- `cx`: `CanvasXpress`
- `document_includes`: `bool`
- `document_render`: `bool`
- `document_jupyter_render`: `bool`

**Returns**:

`str`

<a name="canvasxpress.util.example.generate_tutorials"></a>
# canvasxpress.util.example.generate\_tutorials

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/util/example/generate_tutorials.py#L1)

This file can be executed to render the reproducible JSON files located at
`[project]/tutorials/reproducible_json/*.json` into tutorials for general use.

<a name="canvasxpress.util.example.generate_tutorials.get_json_file_paths"></a>
#### get\_json\_file\_paths

```python
get_json_file_paths() -> List[str]
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/util/example/generate_tutorials.py#L23)

Returns a list of all reproducible JSON files tracked for tutorials.

**Returns**:

`list[str]`

<a name="canvasxpress.util.example.generate_tutorials.get_type_from_filename"></a>
#### get\_type\_from\_filename

```python
get_type_from_filename(file_name: str) -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/util/example/generate_tutorials.py#L36)

Returns the type of chart from a reproducible JSON filename.

**Arguments**:

    The name of the file without parent path.
- `file_name`: `str`

**Returns**:

`str`

<a name="canvasxpress.util.example.generate_tutorials.get_index_from_filename"></a>
#### get\_index\_from\_filename

```python
get_index_from_filename(file_name: str) -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/util/example/generate_tutorials.py#L57)

Returns the index of chart from a reproducible JSON filename.

**Arguments**:

    The name of the file without parent path.
- `file_name`: `str`

**Returns**:

`str`

<a name="canvasxpress.util.example.generate_tutorials.create_jupyer_template_text"></a>
#### create\_jupyer\_template\_text

```python
create_jupyer_template_text(chart_type: str, chart_index: str, chart_code: str) -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/util/example/generate_tutorials.py#L76)

Generates the text for a Jupyter Notebook example given a chart's type,
index, and code.
:param: chart_type: `str`
    The type text (e.g., bar) for the chart.

**Arguments**:

    The index text (e.g., 1) for the chart.
    The chart source code.
- `chart_index`: `str`
- `chart_code`: `str`

**Returns**:

`str`

<a name="canvasxpress.util.template"></a>
# canvasxpress.util.template

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/util/template.py#L1)

<a name="canvasxpress.util.template.render_from_template"></a>
#### render\_from\_template

```python
render_from_template(template: str, data: dict) -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/util/template.py#L1)

Updates the template text with the provided data.

**Arguments**:

:returns The adjusted template text
- `template`: `str` The name of the template file
- `data`: The `dict` of str values with which to update the template text

<a name="canvasxpress.config"></a>
# canvasxpress.config

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/__init__.py#L1)

The config package provides functionality for managing or assigning
configuration values associated with CanvasXpress objects.

<a name="canvasxpress.config.type"></a>
# canvasxpress.config.type

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L1)

<a name="canvasxpress.config.type.CXConfig"></a>
## CXConfig Objects

```python
@total_ordering
class CXConfig(ABC)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L12)

CXConfig provides the means by which CanvasXpress objects can be configured for
customized rendering and interaction.

<a name="canvasxpress.config.type.CXConfig.label"></a>
#### label

```python
 | @property
 | label() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L24)

Provides the label for the configuration.

**Returns**:

`str`

<a name="canvasxpress.config.type.CXConfig.value"></a>
#### value

```python
 | @property
 | @abstractmethod
 | value() -> Any
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L33)

Provides the value for the configuration.  Must be implemented by
concrete classes.

**Returns**:

`Any`

<a name="canvasxpress.config.type.CXConfig.value"></a>
#### value

```python
 | @value.setter
 | @abstractmethod
 | value(value: Any) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L44)

Sets the value of the configuration.  Must be implemented by concrete
classes.

**Arguments**:

    The value to be accepted.  Will be more specific with concrete
    implementations, such as `str` for string configurations.
- `value`: `Any`

<a name="canvasxpress.config.type.CXConfig.render"></a>
#### render

```python
 | render() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L54)

Renders the value in a form suitable for use in preparing Javascript.
Typically, this will be the native `value`.

**Returns**:

`dict`

<a name="canvasxpress.config.type.CXConfig.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(label: str, value: Any)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L65)

Initializes a new CXConfig object with a label and value.

**Arguments**:

    The label for the configuration.
    The value for the configuration.  See the `value` property for the
    concrete implementation for allowed types.
- `label`: `str`
- `value`: `Any`

<a name="canvasxpress.config.type.CXConfig.__copy__"></a>
#### \_\_copy\_\_

```python
 | __copy__() -> "CXConfig"
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L78)

*copy constructor* that provides a new CXConfig of the same type with
the data referenced.

**Returns**:

`CXConfig` of the proper type

<a name="canvasxpress.config.type.CXConfig.__deepcopy__"></a>
#### \_\_deepcopy\_\_

```python
 | __deepcopy__(memo)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L89)

*deepcopy constructor* that provides a new CXConfig of the same type with
the a deepcopy of the data.

**Returns**:

`CXConfig` of the proper type

<a name="canvasxpress.config.type.CXConfig.__hash__"></a>
#### \_\_hash\_\_

```python
 | __hash__() -> int
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L102)

Provides a hash proxy for the object as converted into its `repr` form.

**Returns**:

`int`

<a name="canvasxpress.config.type.CXConfig.__lt__"></a>
#### \_\_lt\_\_

```python
 | __lt__(other: "CXConfig") -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L109)

*less than* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

    `CXConfig` The object to compare.
- `other`: 

**Returns**:

`bool`

<a name="canvasxpress.config.type.CXConfig.__eq__"></a>
#### \_\_eq\_\_

```python
 | __eq__(other: "CXConfig") -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L138)

*equals* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

    `CXConfig` The object to compare.
- `other`: 

**Returns**:

`bool`

<a name="canvasxpress.config.type.CXConfig.__str__"></a>
#### \_\_str\_\_

```python
 | __str__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L159)

*str* function.  Converts the object into a JSON string.

<a name="canvasxpress.config.type.CXConfig.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L170)

*repr* function.  Converts the CXConfig object into a pickle string
that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.config.type.CXString"></a>
## CXString Objects

```python
class CXString(CXConfig)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L184)

A `CXConfig` object that manages `str` values.

<a name="canvasxpress.config.type.CXString.value"></a>
#### value

```python
 | @property
 | value() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L195)

Provides the value for the configuration.

**Returns**:

`str`

<a name="canvasxpress.config.type.CXString.value"></a>
#### value

```python
 | @value.setter
 | value(value: Union[object, str]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L203)

Sets the value of the configuration.

**Arguments**:

    If `None` then an empty `str` will be used.
- `value`: `str`

<a name="canvasxpress.config.type.CXString.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(label: str, value: str)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L214)

Initializes the configuration with a `str` value.

<a name="canvasxpress.config.type.CXBool"></a>
## CXBool Objects

```python
class CXBool(CXConfig)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L222)

A `CXConfig` object that manages `bool` values.

<a name="canvasxpress.config.type.CXBool.value"></a>
#### value

```python
 | @property
 | value() -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L233)

Provides the value for the configuration.

**Returns**:

`bool`

<a name="canvasxpress.config.type.CXBool.value"></a>
#### value

```python
 | @value.setter
 | value(value: Union[object, bool]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L241)

Sets the value of the configuration.

**Arguments**:

    If `None` then `False` will be used.
- `value`: `bool`

<a name="canvasxpress.config.type.CXBool.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(label: str, value: bool)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L252)

Initializes the configuration with a `bool` value.

<a name="canvasxpress.config.type.CXBool.__str__"></a>
#### \_\_str\_\_

```python
 | __str__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L259)

*str* function.  Converts the object into a Javascript statement.

<a name="canvasxpress.config.type.CXBool.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L270)

*repr* function.  Converts the CXBool object into a pickle string
that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.config.type.CXFloat"></a>
## CXFloat Objects

```python
class CXFloat(CXConfig)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L284)

A `CXConfig` object that manages `float` values.

<a name="canvasxpress.config.type.CXFloat.value"></a>
#### value

```python
 | @property
 | value() -> float
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L295)

Provides the value for the configuration.

**Returns**:

`float`

<a name="canvasxpress.config.type.CXFloat.value"></a>
#### value

```python
 | @value.setter
 | value(value: Union[object, float]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L303)

Sets the value of the configuration.

**Arguments**:

    If `None` then `float(0.0)` will be used.
- `value`: `float`

<a name="canvasxpress.config.type.CXFloat.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(label: str, value: float)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L314)

Initializes the configuration with a `float` value.

<a name="canvasxpress.config.type.CXInt"></a>
## CXInt Objects

```python
class CXInt(CXConfig)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L324)

A `CXConfig` object that manages `int` values.

<a name="canvasxpress.config.type.CXInt.value"></a>
#### value

```python
 | @property
 | value() -> int
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L335)

Provides the value for the configuration.

**Returns**:

`int`

<a name="canvasxpress.config.type.CXInt.value"></a>
#### value

```python
 | @value.setter
 | value(value: Union[object, int]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L343)

Sets the value of the configuration.

**Arguments**:

    If `None` then `int(0)` will be used.
- `value`: `int`

<a name="canvasxpress.config.type.CXInt.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(label: str, value: int)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L354)

Initializes the configuration with an `int` value.

<a name="canvasxpress.config.type.CXDict"></a>
## CXDict Objects

```python
class CXDict(CXConfig)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L364)

A `CXConfig` object that manages `dict` values.

<a name="canvasxpress.config.type.CXDict.value"></a>
#### value

```python
 | @property
 | value() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L375)

Provides the value for the configuration.

**Returns**:

`dict`

<a name="canvasxpress.config.type.CXDict.value"></a>
#### value

```python
 | @value.setter
 | value(value: Union[dict, str, None]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L383)

Sets the value of the configuration.

**Arguments**:

    If `None` then `dict()` will be used.
- `value`: `dict`

<a name="canvasxpress.config.type.CXDict.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(label: str, value: Union[dict, str, None]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L402)

Initializes the CXData object with data.  Only dict or compatible data
types are accepted.

<a name="canvasxpress.config.type.CXDict.__lt__"></a>
#### \_\_lt\_\_

```python
 | __lt__(other: "CXDict") -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L410)

*less than* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

    `CXDict` The object to compare.
- `other`: 

**Returns**:

`bool`

<a name="canvasxpress.config.type.CXDict.__eq__"></a>
#### \_\_eq\_\_

```python
 | __eq__(other: "CXDict") -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L455)

*equals* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

    `CXDict` The object to compare.
- `other`: 

**Returns**:

`bool`

<a name="canvasxpress.config.type.CXDict.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L498)

*repr* function.  Converts the CXDict object into a pickle string
that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.config.type.CXList"></a>
## CXList Objects

```python
class CXList(CXConfig)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L507)

A `CXConfig` object that manages `list` values.

<a name="canvasxpress.config.type.CXList.value"></a>
#### value

```python
 | @property
 | value() -> list
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L518)

Provides the value for the configuration.

**Returns**:

`list`

<a name="canvasxpress.config.type.CXList.value"></a>
#### value

```python
 | @value.setter
 | value(value: Union[object, list]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L526)

Sets the value of the configuration.

**Arguments**:

    If `None` then `list()` will be used.
- `value`: `list`

<a name="canvasxpress.config.type.CXList.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(label: str, value: list)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L537)

Initializes the configuration with a `list` value.

<a name="canvasxpress.config.type.CXRGBAColor"></a>
## CXRGBAColor Objects

```python
class CXRGBAColor(CXDict)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L547)

A `CXConfig` object that manages `str` Javascript rgba() values.

<a name="canvasxpress.config.type.CXRGBAColor.is_color_str"></a>
#### is\_color\_str

```python
 | @staticmethod
 | is_color_str(value: str)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L553)

A static method that evaluates a given string to see if it represents a
Javascript rgba() statement.

**Arguments**:

    A string to evaluate.  A valid Javascript value has the form
    `rgba(r, g, b, a)` where RGB values are `int` from 0-255 and A is a
    `float` from 0.0 to 1.0.
- `value`: `str`

**Returns**:

`bool`

<a name="canvasxpress.config.type.CXRGBAColor.is_color_list"></a>
#### is\_color\_list

```python
 | @staticmethod
 | is_color_list(value: list)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L594)

A static method that evaluates a given list to see if it represents a
Javascript rgba() statement.

**Arguments**:

    A list to evaluate.  A valid Javascript value has the form
    `rgba(r, g, b, a)` where RGB values are `int` from 0-255 and A is a
    `float` from 0.0 to 1.0.
- `value`: `list`

**Returns**:

`bool`

<a name="canvasxpress.config.type.CXRGBAColor.is_color_dict"></a>
#### is\_color\_dict

```python
 | @staticmethod
 | is_color_dict(value: dict)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L632)

A static method that evaluates a given dict to see if it represents a
Javascript rgba() statement.

**Arguments**:

    A dict to evaluate.  A valid Javascript value has the form
    `rgba(r, g, b, a)` where RGB values are `int` from 0-255 and A is a
    `float` from 0.0 to 1.0.  For the dict to be valid its keys must be
    lower case r, g, b, and a characters.
- `value`: `dict`

**Returns**:

`bool`

<a name="canvasxpress.config.type.CXRGBAColor.value"></a>
#### value

```python
 | @CXDict.value.setter
 | value(value: Union["CXRGBAColor", dict, list, str]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L677)

Sets the RGBA value from an existing `CXRGBAColor` object, or a `dict`,
`list`, or `string` following the Javascript `rgba()` format.

**Arguments**:

    The value to be accepted.  See the `is_color_*()` methods for
    acceptable formats.
- `value`: `Union['CXRGBAColor', dict, list, str]`

<a name="canvasxpress.config.type.CXRGBAColor.render"></a>
#### render

```python
 | render() -> Any
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L751)

Renders the value in a form suitable for use in preparing Javascript.
Typically, this will be the native `value`.

**Returns**:

`Any`

<a name="canvasxpress.config.type.CXRGBAColor.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(label: str, value: Union["CXRGBAColor", dict, list, str])
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L766)

Initializes a new CXRGBAColor object using the RGBA value from an
existing `CXRGBAColor` object, or a `dict`, `list`, or `string`
following the Javascript `rgba()` format.

**Arguments**:

    The value to be accepted.  See the `is_color_*()` methods for
    acceptable formats.
- `value`: `Union['CXRGBAColor', dict, list, str]`

<a name="canvasxpress.config.type.CXRGBAColor.__str__"></a>
#### \_\_str\_\_

```python
 | __str__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L778)

*str* function.  Converts the object into a JSON string.

<a name="canvasxpress.config.type.CXRGBAColor.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L784)

*repr* function.  Converts the CXRGBAColor object into a pickle string
that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.config.type.CXRGBColor"></a>
## CXRGBColor Objects

```python
class CXRGBColor(CXDict)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L802)

A `CXConfig` object that manages `str` Javascript rgb() values.

<a name="canvasxpress.config.type.CXRGBColor.is_color_str"></a>
#### is\_color\_str

```python
 | @staticmethod
 | is_color_str(value: str)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L808)

A static method that evaluates a given string to see if it represents a
Javascript rgb() statement.

**Arguments**:

    A string to evaluate.  A valid Javascript value has the form
    `rgb(r, g, b)` where RGB values are `int` from 0-255.
- `value`: `str`

**Returns**:

`bool`

<a name="canvasxpress.config.type.CXRGBColor.is_color_list"></a>
#### is\_color\_list

```python
 | @staticmethod
 | is_color_list(value: list)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L844)

A static method that evaluates a given list to see if it represents a
Javascript rgb() statement.

**Arguments**:

    A list to evaluate.  A valid Javascript value has the form
    `rgb(r, g, b)` where RGB values are `int` from 0-255.
- `value`: `list`

**Returns**:

`bool`

<a name="canvasxpress.config.type.CXRGBColor.is_color_dict"></a>
#### is\_color\_dict

```python
 | @staticmethod
 | is_color_dict(value: dict)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L870)

A static method that evaluates a given dict to see if it represents a
Javascript rgb() statement.

**Arguments**:

    A dict to evaluate.  A valid Javascript value has the form
    `rgba(r, g, b)` where RGB values are `int` from 0-255.  For the dict
     to be valid its keys must be lower case r, g, and b characters.
- `value`: `dict`

**Returns**:

`bool`

<a name="canvasxpress.config.type.CXRGBColor.value"></a>
#### value

```python
 | @CXDict.value.setter
 | value(value: Union["CXRGBColor", dict, list, str]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L915)

Sets the RGB value from an existing `CXRGBColor` object, or a `dict`,
`list`, or `string` following the Javascript `rgb()` format.

**Arguments**:

    The value to be accepted.  See the `is_color_*()` methods for
    acceptable formats.
- `value`: `Union['CXRGBColor', dict, list, str]`

<a name="canvasxpress.config.type.CXRGBColor.render"></a>
#### render

```python
 | render() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L983)

Renders the value in a form suitable for use in preparing Javascript.
Typically, this will be the native `value`.

**Returns**:

`Any`

<a name="canvasxpress.config.type.CXRGBColor.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(label: str, value: Union["CXRGBColor", dict, list, str])
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L997)

Initializes a new CXRGBColor object using the RGB value from an
existing `CXRGBColor` object, or a `dict`, `list`, or `string`
following the Javascript `rgb()` format.

**Arguments**:

    The value to be accepted.  See the `is_color_*()` methods for
    acceptable formats.
- `value`: `Union['CXRGBColor', dict, list, str]`

<a name="canvasxpress.config.type.CXRGBColor.__str__"></a>
#### \_\_str\_\_

```python
 | __str__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L1009)

*str* function.  Converts the object into a JSON string.

<a name="canvasxpress.config.type.CXRGBColor.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L1015)

*repr* function.  Converts the CXRGBColor object into a pickle string
that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.config.type.CXGraphTypeOptions"></a>
## CXGraphTypeOptions Objects

```python
class CXGraphTypeOptions(Enum)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L1032)

A set of known chart types permitted for use with CanvasXpress objects.  If
a chart not yet identified in this list is required then use a `CXString`
object with the label `graphType` and the value set to the name of the
chart to be used.

<a name="canvasxpress.config.type.CXGraphType"></a>
## CXGraphType Objects

```python
class CXGraphType(CXString)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L1092)

A CXString that is aware of CanvasXpress types of graphs, such as 'Bar'.

<a name="canvasxpress.config.type.CXGraphType.value"></a>
#### value

```python
 | @CXString.value.setter
 | value(value: Union[CXGraphTypeOptions, str]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L1100)

Sets the value using a known CanvasXpress option.

<a name="canvasxpress.config.type.CXGraphType.set_custom_value"></a>
#### set\_custom\_value

```python
 | set_custom_value(value: str)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L1116)

Permits a js value to be set, such as if a new option is recently
made available that the Python framework is yet to be aware of.

**Arguments**:

    The string value to set.
- `value`: `str`

<a name="canvasxpress.config.type.CXGraphType.render"></a>
#### render

```python
 | render() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L1125)

Renders the value in a form suitable for use in preparing Javascript.
Typically, this will be the native `value`.

**Returns**:

`dict`

<a name="canvasxpress.config.type.CXGraphType.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(type: Union[CXGraphTypeOptions, str] = CXGraphTypeOptions.Bar)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/type.py#L1136)

Initializes a new CXGraphType object with a value corresponding to one
of the values provided by `CXGraphTypeOptions`.

<a name="canvasxpress.config.collection"></a>
# canvasxpress.config.collection

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/collection.py#L1)

<a name="canvasxpress.config.collection.CXConfigs"></a>
## CXConfigs Objects

```python
@total_ordering
class CXConfigs(CXDictConvertable,  CXListConvertable)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/collection.py#L21)

CXConfigs provides support for addressing a collection of `CXConfig` values.

<a name="canvasxpress.config.collection.CXConfigs.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(*configs: Union[CXConfig, tuple, dict, list])
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/collection.py#L31)

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

**Arguments**:

    A list of zero or more `CXConfig` objects to associate.
- `configs`: `Union[CXConfig, tuple, dict], ...`

<a name="canvasxpress.config.collection.CXConfigs.remove"></a>
#### remove

```python
 | remove(label: str) -> Union[CXConfig, None]
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/collection.py#L52)

Removes the CXConfig if found, and if found the removed config is
provided.

**Arguments**:

    The label of the CXConfig to remove.
- `label`: 'str`

**Returns**:

`Union[CXConfig, None]`

<a name="canvasxpress.config.collection.CXConfigs.add"></a>
#### add

```python
 | add(config: Union[CXConfig, tuple, dict, list]) -> "CXConfigs"
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/collection.py#L70)

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

**Arguments**:

    The `CXConfig` to associate.  Cannot be `None`.  `tuple` an d`list`
    config values are expected to be two elements in length, with the
    first representing the label and the second representing the value.
    The label portion will be converted to a string using `str`.
- `config`: `Union[CXConfig, tuple, dict, list]`

<a name="canvasxpress.config.collection.CXConfigs.get_param"></a>
#### get\_param

```python
 | get_param(label: str) -> Union[CXConfig, None]
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/collection.py#L122)

Provides the CXConfig with the indicated label.

**Arguments**:

    The name of the congig to find.
- `label`: `str`

**Returns**:

`Union[CXConfig, None]`

<a name="canvasxpress.config.collection.CXConfigs.set_param"></a>
#### set\_param

```python
 | set_param(label: str, value: Any) -> "CXConfigs"
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/collection.py#L138)

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

**Arguments**:

    The parameter to infer and associate.  Cannot be `None`.  Defaults
    to `str` if the type cannot otherwise be deduced.
- `value`: `Any`

<a name="canvasxpress.config.collection.CXConfigs.configs"></a>
#### configs

```python
 | @property
 | configs() -> List[CXConfig]
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/collection.py#L215)

Provides access to the list of associated `CXConfig` objects.

**Returns**:

`List[CXConfig]`

<a name="canvasxpress.config.collection.CXConfigs.render_to_dict"></a>
#### render\_to\_dict

```python
 | render_to_dict() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/collection.py#L222)

Provides a `dict` representation of the configuration values.

**Returns**:

`dict`

<a name="canvasxpress.config.collection.CXConfigs.render_to_list"></a>
#### render\_to\_list

```python
 | render_to_list(**kwargs) -> list
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/collection.py#L249)

Provides a `list` representation of the configuration values.

**Returns**:

`list`

<a name="canvasxpress.config.collection.CXConfigs.merge_configs"></a>
#### merge\_configs

```python
 | @classmethod
 | merge_configs(cls, configs: List[CXConfig]) -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/collection.py#L281)

Given a list of CXConfig objects, a dictionary of unique attributes is
generated and provided.

**Returns**:

`dict`

<a name="canvasxpress.config.collection.CXConfigs.__copy__"></a>
#### \_\_copy\_\_

```python
 | __copy__() -> "CXConfigs"
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/collection.py#L300)

*copy* constructor.  Returns the `CXConfig` objects within a new
`CXConfigs` object.

<a name="canvasxpress.config.collection.CXConfigs.__deepcopy__"></a>
#### \_\_deepcopy\_\_

```python
 | __deepcopy__(memo) -> "CXConfigs"
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/collection.py#L307)

*deepcopy* constructor.  Returns a deepcopy of the `CXConfig` objects
 within a new `CXConfigs` object.

<a name="canvasxpress.config.collection.CXConfigs.__lt__"></a>
#### \_\_lt\_\_

```python
 | __lt__(other: "CXConfigs") -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/collection.py#L314)

*less than* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

    `CXConfigs` The object to compare.
- `other`: 

**Returns**:

`bool`

<a name="canvasxpress.config.collection.CXConfigs.__eq__"></a>
#### \_\_eq\_\_

```python
 | __eq__(other: "CXConfigs") -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/collection.py#L347)

*equals* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

    `CXConfigs` The object to compare.
- `other`: 

**Returns**:

`bool`

<a name="canvasxpress.config.collection.CXConfigs.__str__"></a>
#### \_\_str\_\_

```python
 | __str__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/collection.py#L380)

*str* function.  Converts the `CXConfigs` object into a JSON
representation.
:returns" `str`
    JSON form of the collection.

<a name="canvasxpress.config.collection.CXConfigs.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/config/collection.py#L389)

*repr* function.  Converts the `CXConfigs` object into a pickle string
that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.js"></a>
# canvasxpress.js

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/js/__init__.py#L1)

The js package provides functionality for integrating custom Javascript with
CanvasXpress charts.

<a name="canvasxpress.js.collection"></a>
# canvasxpress.js.collection

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/js/collection.py#L1)

<a name="canvasxpress.js.collection.CXEvents"></a>
## CXEvents Objects

```python
@total_ordering
class CXEvents(CXJavascriptConvertable)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/js/collection.py#L11)

CXEvents represents a Javascript script that can be associated with a
CanvasXpress object.

For example, when defining a CanvasXpress object Javascript could be
added for reactive feedback via:

```python
chart_events = CXEvents(
    CXEvent(
        "click",
        '''
        var s = 'click on var ' + o.y.vars[0] + ' and smp ' + o.y.smps[0];
        t.showInfoSpan(e, s);
        '''
    )
)
chart = CanvasXpress(
    events=chart_events
)
```

Also see the [CanvasXpress documentation](https://www.canvasxpress.org/docs.html#events)
or `CXEvent` for additional information.

<a name="canvasxpress.js.collection.CXEvents.events"></a>
#### events

```python
 | @property
 | events() -> List[CXEvent]
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/js/collection.py#L44)

Provides a non-associated list of the associated CXEvents.

**Returns**:

`List[CXEvent]` A list of zero or more CXEvent objects.

<a name="canvasxpress.js.collection.CXEvents.has"></a>
#### has

```python
 | has(event: CXEvent) -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/js/collection.py#L51)

Indicates if the `CXEvent` is a member.

**Arguments**:

- `event`: The `CXEvent` to consider.

**Returns**:

`bool` True if `event` is a member.

<a name="canvasxpress.js.collection.CXEvents.add"></a>
#### add

```python
 | add(event: CXEvent, unique: bool = True) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/js/collection.py#L59)

Adds the specified CXEvent.  If the CXEvent must be unique then an Error
is raised if an react is already presenbt with the same ID.

**Arguments**:

    `CXEvent` The event to add to the collection.  Cannot be `None`.
    `bool` True if `event` must not already be a part of the collection.
- `event`: 
- `unique`: 

<a name="canvasxpress.js.collection.CXEvents.remove"></a>
#### remove

```python
 | remove(event: CXEvent) -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/js/collection.py#L82)

Removes the specified object from the list.

**Arguments**:

    already included.
- `event`: The CXEvent object to remove from the list if it is

**Returns**:

True if the CXEvent was removed.  False indicates that the

<a name="canvasxpress.js.collection.CXEvents.render_to_dict"></a>
#### render\_to\_dict

```python
 | render_to_dict() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/js/collection.py#L99)

Provides a dict with each js properly formatted as JS within.

**Returns**:

`dict`

<a name="canvasxpress.js.collection.CXEvents.render_to_js"></a>
#### render\_to\_js

```python
 | render_to_js() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/js/collection.py#L125)

Converts the object into HTML5 complant script.

**Returns**:

'str'

<a name="canvasxpress.js.collection.CXEvents.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(*events)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/js/collection.py#L154)

Initializes a new CXEvents object.

**Arguments**:

    A multiple value parameter by which zero or more `CXEvent` objects
    may be provided.  Also see `add()` for how individual objects are
    processed.

    For example:
```python
event1 = CXEvent("f1", "x = 0")
event2 = CXEvent("f2", "x = 1")
events = CXEvents(event1, event2)
```
- `events`: 

<a name="canvasxpress.js.collection.CXEvents.__copy__"></a>
#### \_\_copy\_\_

```python
 | __copy__()
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/js/collection.py#L176)

*copy* constructor.  Returns the `CXEvent` objects within a new `CXEvents`
object.

<a name="canvasxpress.js.collection.CXEvents.__deepcopy__"></a>
#### \_\_deepcopy\_\_

```python
 | __deepcopy__(memo)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/js/collection.py#L183)

*deepcopy* constructor.  Returns a deep copy of `CXEvent` objects within
a new `CXEvents` object.

<a name="canvasxpress.js.collection.CXEvents.__lt__"></a>
#### \_\_lt\_\_

```python
 | __lt__(other: "CXEvents")
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/js/collection.py#L190)

*less than* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

    `CXEvent` The object to compare.
- `other`: 

**Returns**:

`bool`

<a name="canvasxpress.js.collection.CXEvents.__eq__"></a>
#### \_\_eq\_\_

```python
 | __eq__(other: "CXEvents")
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/js/collection.py#L223)

*equals* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

    `CXEvent` The object to compare.
- `other`: 

**Returns**:

`bool`

<a name="canvasxpress.js.collection.CXEvents.__str__"></a>
#### \_\_str\_\_

```python
 | __str__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/js/collection.py#L253)

*str* function.  Converts the CXEvents object into a JSON list of
`CXEvent` objects also converted into JSON representations.
:returns" `str` JSON form of the collection.

<a name="canvasxpress.js.collection.CXEvents.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/js/collection.py#L261)

*repr* function.  Converts the CXEvents object into a pickle string
that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.js.function"></a>
# canvasxpress.js.function

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/js/function.py#L1)

<a name="canvasxpress.js.function.CXEvent"></a>
## CXEvent Objects

```python
@total_ordering
class CXEvent(CXJavascriptConvertable)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/js/function.py#L15)

CXEvent is a `CXJavascriptConvertable` that represents Javascript source to
be associated with a CanvasXpress object.

CanvasXpress provides hook functions for various events that are called as
those events occur for the `div` element containing the rendered chart.
The format is:

```javascript
"event-name": function(o, e, t) {
    event code
}
```

With the following as an example:

```javascript
"mousemove": function(o, e, t) {
    t.showInfoSpan(e, '<pre>' + t.prettyJSON(o) + '</pre>');
}
```

CXEvent handles the function template, so the developer only needs to supply
the event name and the source.  Given the above example, the following
creates the equivalent CXEvent:

```python
event = CXEvent(
    id="mousemove",
    script="t.showInfoSpan(e, '<pre>' + t.prettyJSON(o) + '</pre>');"
)
```

No validations is performed for `id` or `script`.

Read the [CanvasXpress documentation](https://www.canvasxpress.org/docs.html#events)
for additional information.  Also see `CXEvents`.

<a name="canvasxpress.js.function.CXEvent.id"></a>
#### id

```python
 | @property
 | id() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/js/function.py#L71)

Provides access to the react ID.

**Returns**:

The ID as a string.

<a name="canvasxpress.js.function.CXEvent.id"></a>
#### id

```python
 | @id.setter
 | id(value: str) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/js/function.py#L79)

Sets the react ID, which is a keyword recognized by CanvasXpress.

**Arguments**:

    The ID, which must be a string compliant object.  Cannot be `None`.
- `value`: `str`

<a name="canvasxpress.js.function.CXEvent.script"></a>
#### script

```python
 | @property
 | script() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/js/function.py#L91)

Provides access to the react script.

**Returns**:

`str` The Javascript source.

<a name="canvasxpress.js.function.CXEvent.script"></a>
#### script

```python
 | @script.setter
 | script(value: str) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/js/function.py#L99)

Sets the react script, which is logic that goes inside of the react
function.  Functions take the form:

```javascript
function(o, e, t) {
    // script logic goes here
};
```

The script can be assumed to have access to all DOM elements as proper,
and it will be provided the parameters o, e, and t.  Read the
[CanvasXpress documentation](https://www.canvasxpress.org/docs.html#events)
for additional information.

**Arguments**:

    The ID, which must be a UTF-8 string compliant object.
- `value`: `str`

<a name="canvasxpress.js.function.CXEvent.render_to_js"></a>
#### render\_to\_js

```python
 | render_to_js() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/js/function.py#L123)

Converts the object into HTML5 complant script.

**Returns**:

'str'

<a name="canvasxpress.js.function.CXEvent.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(id: str = "", script: str = "")
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/js/function.py#L146)

Initializes a new CXEvent object.

**Arguments**:

    The ID of the react, such as mousemove.  Also see property `id`.
    The script logic for the react.  Also see property `script`.
- `id`: `str`
- `script`: `str`

<a name="canvasxpress.js.function.CXEvent.__copy__"></a>
#### \_\_copy\_\_

```python
 | __copy__()
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/js/function.py#L159)

*copy* constructor.  Returns a new `CXEvent` object.

<a name="canvasxpress.js.function.CXEvent.__deepcopy__"></a>
#### \_\_deepcopy\_\_

```python
 | __deepcopy__(memo)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/js/function.py#L165)

*deepcopy* constructor.  Returns a new `CXEvent` object.

<a name="canvasxpress.js.function.CXEvent.__lt__"></a>
#### \_\_lt\_\_

```python
 | __lt__(other: "CXEvent") -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/js/function.py#L171)

*less than* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

    `CXEvent` The object to compare.
- `other`: 

**Returns**:

`bool`

<a name="canvasxpress.js.function.CXEvent.__eq__"></a>
#### \_\_eq\_\_

```python
 | __eq__(other: "CXEvent") -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/js/function.py#L198)

*equal* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

    `CXEvent` The object to compare.
- `other`: 

**Returns**:

`bool`

<a name="canvasxpress.js.function.CXEvent.__str__"></a>
#### \_\_str\_\_

```python
 | __str__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/js/function.py#L220)

*str* function.  Converts the object into a Javascript statement.

<a name="canvasxpress.js.function.CXEvent.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/js/function.py#L241)

*repr* function.  Converts the CXEvent object into a pickle string
that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.render"></a>
# canvasxpress.render

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/render/__init__.py#L1)

The render package provides functionality for rendering CanvasXpress objects in
containers or environments

<a name="canvasxpress.render.popup"></a>
# canvasxpress.render.popup

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/render/popup.py#L1)

<a name="canvasxpress.render.popup.CXBrowserPopup"></a>
## CXBrowserPopup Objects

```python
class CXBrowserPopup(CXRenderable)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/render/popup.py#L50)

CXBrowserPopup is a `CXRenderable` that renders `CanvasXpress` objects into
a Web page that is displayed in a pop-up browser window.

<a name="canvasxpress.render.popup.CXBrowserPopup.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(*cx: Union[List[CanvasXpress], CanvasXpress, None])
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/render/popup.py#L56)

Initializes a new `CXBrowserPopup` object.
:praram cx: `Union[List[CanvasXpress], CanvasXpress, None], ...`
    The `CanvasXpress` object(s) to be tracked.  See the `canvas`
    property, except that on initialization cx can be `None`.
    Multiple CanvasXpress objects are supported provided that
    they have distinct `render_to` targets.

<a name="canvasxpress.render.popup.CXBrowserPopup.render"></a>
#### render

```python
 | render(**kwargs: Any)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/render/popup.py#L67)

Renders the associated CanvasXpress object appropriate for display in
a pop-up browser window.  Charts cannot have the same name,
so render_to will be updated with a uuid for each conflicting chart.

**Arguments**:

    Supports `columns` for any positive `int` of `1` or greater, with a
    default value of `1`.  Values less that `1` are ignored.  `columns`
    indicates how many charts should be rendered horizontally in the
    browser if more than one chart is being tracked.
- `kwargs`: `Any`

<a name="canvasxpress.render.dash"></a>
# canvasxpress.render.dash

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/render/dash.py#L1)

This module provides an integration solution for the CanvasXpress class and the base dash component for a feature-
rich integration with Plotly's Dash framework.

<a name="canvasxpress.render.dash.CXElementFactory"></a>
## CXElementFactory Objects

```python
class CXElementFactory(CXRenderFactory)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/render/dash.py#L13)

CXDashElementFactory converts CanvasXpress objects into PlotlyDash elements that will
render CanvasXpress charts into the Dash UI.

<a name="canvasxpress.render.dash.CXElementFactory.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(*cx: Union[List[CanvasXpress], CanvasXpress, None])
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/render/dash.py#L19)

Initializes a new `CXDashRenderFactory` object.

**Arguments**:

    The `CanvasXpress` object(s) to be tracked.  See the `canvas`
    property, except that on initialization cx can be `None`.
    Multiple CanvasXpress objects are supported provided that
    they have distinct `render_to` targets.
- `cx`: `Union[List[CanvasXpress], CanvasXpress, None], ...`

<a name="canvasxpress.render.dash.CXElementFactory.render"></a>
#### render

```python
 | @classmethod
 | render(cls, cx: CanvasXpress) -> CXDashElement
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/render/dash.py#L31)

Converts the provided CanvasXpress object into a CXDashElement object that is
primed by the configuration represented by the CanvasXpress object.

**Arguments**:

    raised if cx is `None`.
- `cx`: `CanvasXpress` The CanvasXpress object to render.  An exception is

**Returns**:

`CXDashElement` A CXDashElement with the configuration as represented

<a name="canvasxpress.render.dash.CXElementFactory.render_all"></a>
#### render\_all

```python
 | render_all(**kwargs: Any) -> List[CXDashElement]
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/render/dash.py#L56)

Provides a list of objects that can be used by the target domain or container
to create CanvasXpress illustrations or instantiations.
Not implemented.

**Arguments**:

    Parameters specific to implementations are supported.  The essential
    create_element call should work with no extra parameters, and with
    parameters that do not apply to the implementation.
- `kwargs`: `Any`

<a name="canvasxpress.render.base"></a>
# canvasxpress.render.base

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/render/base.py#L1)

<a name="canvasxpress.render.base.CXRenderAssociation"></a>
## CXRenderAssociation Objects

```python
class CXRenderAssociation(ABC)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/render/base.py#L8)

CXRenderAssociation tracks A set of CanvasXpress objects that will be used to produce
a domain- or container-specific rendering (e.g., for display in a Jupyter notebook).

<a name="canvasxpress.render.base.CXRenderAssociation.canvas"></a>
#### canvas

```python
 | @property
 | canvas() -> Union[List[CanvasXpress], CanvasXpress, None]
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/render/base.py#L20)

Provides the tracked CanvasXpress object.

**Returns**:

`value: Union[List[CanvasXpress], CanvasXpress, None]`

<a name="canvasxpress.render.base.CXRenderAssociation.canvas"></a>
#### canvas

```python
 | @canvas.setter
 | canvas(value: Union[List[CanvasXpress], CanvasXpress, None])
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/render/base.py#L37)

Sets the CanvasXpress object to be tracked.
:praram value: `value: Union[List[CanvasXpress], CanvasXpress, None]`
    A `list` of `CanvasXpress` objects if multiple are tracked,
    or one `CanvasXpress object, or `None` if no objects are to be
    tracked.

<a name="canvasxpress.render.base.CXRenderAssociation.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(*cx: Union[List[CanvasXpress], CanvasXpress, None])
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/render/base.py#L61)

Initializes a new `CXRenderable` object.
:praram cx: `Union[List[CanvasXpress], CanvasXpress, None], ...`
    The `CanvasXpress` object(s) to be tracked.  See the `canvas`
    property, except that on initialization cx can be `None`.
    Multiple CanvasXpress objects are supported provided that
    they have distinct `render_to` targets.

<a name="canvasxpress.render.base.CXRenderable"></a>
## CXRenderable Objects

```python
class CXRenderable(CXRenderAssociation)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/render/base.py#L91)

CXRenderable is capable of rendering a CanvasXpress object to some kind of
output or display device.

<a name="canvasxpress.render.base.CXRenderable.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(*cx: Union[List[CanvasXpress], CanvasXpress, None])
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/render/base.py#L97)

Initializes a new `CXRenderable` object.
:praram cx: `Union[List[CanvasXpress], CanvasXpress, None], ...`
    The `CanvasXpress` object(s) to be tracked.  See the `canvas`
    property, except that on initialization cx can be `None`.
    Multiple CanvasXpress objects are supported provided that
    they have distinct `render_to` targets.

<a name="canvasxpress.render.base.CXRenderable.render"></a>
#### render

```python
 | @abstractmethod
 | render(**kwargs: Any)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/render/base.py#L109)

Renders the associated CanvasXpress object appropriate to the render_to.
Not implemented.

**Arguments**:

    Parameters specific to implementations are supported.  The essential
    render call should work with no extra parameters, and with
    parameters that do not apply to the implementation.
- `kwargs`: `Any`

<a name="canvasxpress.render.base.CXRenderFactory"></a>
## CXRenderFactory Objects

```python
class CXRenderFactory(CXRenderAssociation)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/render/base.py#L121)

CXRenderFactory produces objects for use in a container or framework that understand how
to cooperate with the framework to produce CanvasXpress illustrations.

<a name="canvasxpress.render.base.CXRenderFactory.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(*cx: Union[List[CanvasXpress], CanvasXpress, None])
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/render/base.py#L127)

Initializes a new `CXRenderFactory` object.
:praram cx: `Union[List[CanvasXpress], CanvasXpress, None], ...`
    The `CanvasXpress` object(s) to be tracked.  See the `canvas`
    property, except that on initialization cx can be `None`.
    Multiple CanvasXpress objects are supported provided that
    they have distinct `render_to` targets.

<a name="canvasxpress.render.base.CXRenderFactory.render_all"></a>
#### render\_all

```python
 | @abstractmethod
 | render_all(**kwargs: Any) -> List[object]
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/render/base.py#L139)

Provides a list of objects that can be used by the target domain or container
to create CanvasXpress illustrations or instantiations.
Not implemented.

**Arguments**:

    Parameters specific to implementations are supported.  The essential
    render call should work with no extra parameters, and with
    parameters that do not apply to the implementation.
- `kwargs`: `Any`

<a name="canvasxpress.render.jupyter"></a>
# canvasxpress.render.jupyter

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/render/jupyter.py#L1)

<a name="canvasxpress.render.jupyter.CXNoteBook"></a>
## CXNoteBook Objects

```python
class CXNoteBook(CXRenderable)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/render/jupyter.py#L52)

CXNoteBook is a `CXRenderable` that renders `CanvasXpress` objects into
`IPython` containers (Jupyter Notebooks).

<a name="canvasxpress.render.jupyter.CXNoteBook.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(*cx: Union[List[CanvasXpress], CanvasXpress, None])
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/render/jupyter.py#L58)

Initializes a new `CXNoteBook` object.
:praram cx: `Union[List[CanvasXpress], CanvasXpress, None], ...`
    The `CanvasXpress` object(s) to be tracked.  See the `canvas`
    property, except that on initialization cx can be `None`.
    Multiple CanvasXpress objects are supported provided that
    they have distinct `render_to` targets.

<a name="canvasxpress.render.jupyter.CXNoteBook.render"></a>
#### render

```python
 | render(**kwargs: Any)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/render/jupyter.py#L69)

Renders the associated CanvasXpress object appropriate for display in
an IPython (e.g., Jupyter NoteBook/Lab) environment.  Charts cannot
have the same name, so render_to will be updated with a uuid for each
conflicting chart.

**Arguments**:

    * Supports `columns` for any positive `int` of `1` or greater, with a
      default value of `1`.  Values less that `1` are ignored.  `columns`
      indicates how many charts should be rendered horizontally in the
      Jupyter Notebook if more than one chart is being tracked.
    * Supports `output_file` as a string for a path at which the output
      should be saved.  If a file exists at the specified path then
      it will be overwritten.  This permits Jupyter sessions to render
      output that is saved and accessible in later sessions.
- `kwargs`: `Any`

<a name="canvasxpress.data"></a>
# canvasxpress.data

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/__init__.py#L1)

The data package provides functionality for integrating different kinds of data
structures and sources into a CanvasXpress object.  A balance is provided
between convenience functionality and reasonable external preparation, such as
what can be performed via `pandas`.

<a name="canvasxpress.data.matrix"></a>
# canvasxpress.data.matrix

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/matrix.py#L1)

<a name="canvasxpress.data.matrix.CXDataframeData"></a>
## CXDataframeData Objects

```python
@total_ordering
class CXDataframeData(CXMatrixData)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/matrix.py#L15)

A CXData class dedicated to processing Python DataFrame, matrix-structured
 data.

<a name="canvasxpress.data.matrix.CXDataframeData.dataframe"></a>
#### dataframe

```python
 | @property
 | dataframe() -> DataFrame
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/matrix.py#L27)

Provides the data managed by the object.

**Returns**:

`DataFrame` The managed data.

<a name="canvasxpress.data.matrix.CXDataframeData.dataframe"></a>
#### dataframe

```python
 | @dataframe.setter
 | dataframe(value: Union[DataFrame, None] = None) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/matrix.py#L35)

Sets the dataframe managed by the object.

**Arguments**:

    `None` results in an empty `DataFrame`.  A deepcopy will be made of
    `DataFrame` values.
- `value`: `Union[DataFrame, None]`

<a name="canvasxpress.data.matrix.CXDataframeData.data"></a>
#### data

```python
 | @property
 | data() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/matrix.py#L45)

Provides the data managed by the object.

**Returns**:

`DataFrame` The managed data.

<a name="canvasxpress.data.matrix.CXDataframeData.data"></a>
#### data

```python
 | @data.setter
 | data(value: Union["CXDataframeData", DataFrame, dict, str, None] = None) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/matrix.py#L53)

Sets the dataframe managed by the object.

**Arguments**:

    `None` results in an empty `DataFrame`.  A deepcopy will be made of
    `DataFrame` or equivalent values.
- `value`: `Union['CXDataframeData', DataFrame, dict, str, None]`

<a name="canvasxpress.data.matrix.CXDataframeData.get_raw_dict_form"></a>
#### get\_raw\_dict\_form

```python
 | get_raw_dict_form() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/matrix.py#L96)

"
Provides a simple dict perspective of the data with no metadata or other
contextual transformations performed.  For example, if the data is
natively in `dict` form then it would be passed-through with no
modification or enhancement.

This implementation provides matrix data formatted in a `dict` object
with `DataFrame.to_dict('split')` behaviour.

**Returns**:

`dict`

<a name="canvasxpress.data.matrix.CXDataframeData.render_to_dict"></a>
#### render\_to\_dict

```python
 | render_to_dict(**kwargs) -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/matrix.py#L112)

Provides a dict representation of the data.

**Returns**:

`dict`

<a name="canvasxpress.data.matrix.CXDataframeData.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(data: Union["CXDataframeData", DataFrame, dict, str, None] = None, profile: Union[CXDataProfile, None] = None) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/matrix.py#L126)

Initializes the CXData object with data.  Only `DataFrame` or compatible
data types are accepted.

**Arguments**:

    `None` to initialize with an empty `DataFrame`, or a `DataFrame`
    like object to assign mapped data.
    Specify the desired profile object to facilitate transformation of
    data into a CanvasXpress JSON data object.  `None` will default to
    the CXStandardProfile.
- `data`: `Union['CXDataframeData', DataFrame, dict, str, None]`
- `profile`: `Union[CXDataProfile, None]`

<a name="canvasxpress.data.matrix.CXDataframeData.__copy__"></a>
#### \_\_copy\_\_

```python
 | __copy__() -> "CXDataframeData"
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/matrix.py#L145)

*copy constructor* that returns a copy of the CXDataframeData object.

**Returns**:

`CXDataframeData`

<a name="canvasxpress.data.matrix.CXDataframeData.__deepcopy__"></a>
#### \_\_deepcopy\_\_

```python
 | __deepcopy__(memo) -> "CXDataframeData"
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/matrix.py#L153)

*deepcopy constructor* that returns a copy of the CXDataframeData object.

**Returns**:

`CXDataframeData` A copy of the wrapping object and deepcopy of

<a name="canvasxpress.data.matrix.CXDataframeData.__lt__"></a>
#### \_\_lt\_\_

```python
 | __lt__(other: "CXDataframeData") -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/matrix.py#L161)

*less than* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

    `CXDataframeData` The object to compare.
- `other`: 

**Returns**:

`bool`

<a name="canvasxpress.data.matrix.CXDataframeData.__eq__"></a>
#### \_\_eq\_\_

```python
 | __eq__(other: "CXDataframeData") -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/matrix.py#L198)

*equals* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

    `CXDataframeData` The object to compare.
- `other`: 

**Returns**:

`bool`

<a name="canvasxpress.data.matrix.CXDataframeData.__str__"></a>
#### \_\_str\_\_

```python
 | __str__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/matrix.py#L230)

*str* function.  Converts the CXDataframeData object into a JSON
representation.
:returns" `str` JSON form of the `CXDataframeData`.

<a name="canvasxpress.data.matrix.CXDataframeData.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/matrix.py#L238)

*repr* function.  Converts the CXDataframeData object into a pickle
string that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.data.matrix.CXCSVData"></a>
## CXCSVData Objects

```python
class CXCSVData(CXDataframeData)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/matrix.py#L256)

A CXData class dedicated to processing Python CSV-based, matrix-structured
 data.

<a name="canvasxpress.data.matrix.CXCSVData.csv"></a>
#### csv

```python
 | @property
 | csv() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/matrix.py#L263)

Provides the data managed by the object.

**Returns**:

`str` The managed data.

<a name="canvasxpress.data.matrix.CXCSVData.csv"></a>
#### csv

```python
 | @csv.setter
 | csv(value: str = None) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/matrix.py#L273)

Sets the CSV data managed by the object.

**Arguments**:

    `None` results in an empty CSV.  A deepcopy will be made of
    valid CSV `str` values.
- `value`: `str`

<a name="canvasxpress.data.matrix.CXCSVData.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(data: Union["CXCSVData", DataFrame, dict, str, None] = None, profile: Union[CXDataProfile, None] = None) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/matrix.py#L282)

Initializes the CXData object with data.  Only CSV `str` or compatible
data types are accepted.

**Arguments**:

    `None` to initialize with an empty CSV, or a CSV `str`
    like object to assign mapped data.
    Specify the desired profile object to facilitate transformation of
    data into a CanvasXpress JSON data object.  `None` to avoid use of
    a profile.
- `data`: `Union['CXCSVData', DataFrame, dict, str, None]`
- `profile`: `Union[CXDataProfile, None]`

<a name="canvasxpress.data.matrix.CXCSVData.__str__"></a>
#### \_\_str\_\_

```python
 | __str__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/matrix.py#L300)

*str* function.  Converts the CXCSVData object into a JSON
representation.
:returns" `str` JSON form of the `CXCSVData`.

<a name="canvasxpress.data.matrix.CXCSVData.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/matrix.py#L308)

*repr* function.  Converts the CXCSVData object into a pickle
string that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.data.convert"></a>
# canvasxpress.data.convert

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/convert.py#L1)

<a name="canvasxpress.data.convert.CXHtmlConvertable"></a>
## CXHtmlConvertable Objects

```python
class CXHtmlConvertable(ABC)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/convert.py#L4)

CXHtmlConvertable represents an object that can be converted into HTML.

<a name="canvasxpress.data.convert.CXHtmlConvertable.render_to_html_parts"></a>
#### render\_to\_html\_parts

```python
 | @abstractmethod
 | render_to_html_parts() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/convert.py#L10)

Converts the object into HTML5 compliant script.

**Returns**:

`dict`

<a name="canvasxpress.data.convert.CXDictConvertable"></a>
## CXDictConvertable Objects

```python
class CXDictConvertable(ABC)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/convert.py#L21)

CXDictConvertable represents an object that can be converted into a dict.

<a name="canvasxpress.data.convert.CXDictConvertable.render_to_dict"></a>
#### render\_to\_dict

```python
 | @abstractmethod
 | render_to_dict(**kwargs) -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/convert.py#L27)

Converts the object into a dict representation.

**Arguments**:

    Keyword arguments that can be supplied to facilitate rendering
    decisions.
- `kwargs`: 

**Returns**:

`dict`

<a name="canvasxpress.data.convert.CXListConvertable"></a>
## CXListConvertable Objects

```python
class CXListConvertable(ABC)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/convert.py#L40)

CXListConvertable represents an object that can be converted into a list.

<a name="canvasxpress.data.convert.CXListConvertable.render_to_list"></a>
#### render\_to\_list

```python
 | @abstractmethod
 | render_to_list(**kwargs) -> list
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/convert.py#L46)

Converts the object into a list representation.

**Arguments**:

    Keyword arguments that can be supplied to facilitate rendering
    decisions.
- `kwargs`: 

**Returns**:

`list`

<a name="canvasxpress.data.convert.CXJavascriptConvertable"></a>
## CXJavascriptConvertable Objects

```python
class CXJavascriptConvertable(ABC)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/convert.py#L59)

CXJavascriptConvertable represents an object that can be converted into JS.

<a name="canvasxpress.data.convert.CXJavascriptConvertable.render_to_js"></a>
#### render\_to\_js

```python
 | @abstractmethod
 | render_to_js() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/convert.py#L65)

Converts the object into HTML5 complant script.

**Returns**:

`str`

<a name="canvasxpress.data.profile"></a>
# canvasxpress.data.profile

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/profile.py#L1)

<a name="canvasxpress.data.profile.CXStandardProfile"></a>
## CXStandardProfile Objects

```python
class CXStandardProfile(CXDataProfile)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/profile.py#L25)

`CXStandardProfile` provides standard chart data profile functionality,
by which the topics of `y`, `x`, and `z` are handled in conversions.

<a name="canvasxpress.data.profile.CXStandardProfile.vars"></a>
#### vars

```python
 | @property
 | vars() -> list
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/profile.py#L93)

Provides the `y["vars"]` CanvasXPress JSON data topic.  `vars` are used
to describe the rows of data.  For example:
```python
"y": {
    "vars": [ "Variable1", Variable2 ],
    "smps": [ "Sample1", "Sample2", "Sample3" ],
    "data": [
        [ 10, 20, 30 ],  # <- This sub-list is what Variable1 references
        [ 40, 50, 60 ]  # <- This sub-list is what Variable2 references
    ]
},
```
Also see [CanvasXpress documentation](https://www.canvasxpress.org/docs.html#data).

**Returns**:

`list`

<a name="canvasxpress.data.profile.CXStandardProfile.vars"></a>
#### vars

```python
 | @vars.setter
 | vars(variables: Union[list, None]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/profile.py#L115)

Sets the variable labels to be used for rows of data.

**Arguments**:

    The list of var values.  Each must be convertable to `str`, and
    the number of var elements must match the row count.  `None` will
    reset the var list.
- `variables`: `Union[list, None]`

<a name="canvasxpress.data.profile.CXStandardProfile.smps"></a>
#### smps

```python
 | @property
 | smps() -> list
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/profile.py#L133)

Provides the `y["smps"]` CanvasXPress JSON data topic.  `smps` are used
to describe the columns of data.  For example:
```python
"y": {
    "vars": [ "Variable1", Variable2 ],
    "smps": [ "Sample1", "Sample2", "Sample3" ],
    "data": [
        [ 10, 20, 30 ],
        [ 40, 50, 60 ]
        #  ^-- This is Sample1
        #      ^-- This is Sample2
        #          ^-- This is Sample3
    ]
},
```
Also see [CanvasXpress documentation](https://www.canvasxpress.org/docs.html#data).

**Returns**:

`list`

<a name="canvasxpress.data.profile.CXStandardProfile.smps"></a>
#### smps

```python
 | @smps.setter
 | smps(samples: Union[list, None]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/profile.py#L158)

Sets the sample labels to be used for columns of data.

**Arguments**:

    The list of smps values.  Each must be convertable to `str`, and
    the number of var elements must match the column count.  `None` will
    reset the smps list.
- `samples`: `Union[list, None]`

<a name="canvasxpress.data.profile.CXStandardProfile.y"></a>
#### y

```python
 | @y.setter
 | y(value: Union[dict, None]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/profile.py#L180)

Sets the `y` attribute for the data, which is the primary data for the
chart.  At a minimum `vars` and `smps` should be present, and if those
are not provided then defaults will be provided.
A deepcopy of the provided dict is made.

**Arguments**:

    A dict value of list attributes, for which `vars` and `smps` values
    will be provided if none are specified.  Provide `None` to set
    default values.
- `value`: `Union[dict, None]`

<a name="canvasxpress.data.profile.CXStandardProfile.x"></a>
#### x

```python
 | @x.setter
 | x(value: Union[DataFrame, dict, None]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/profile.py#L226)

Sets the `x` attribute for the data, which corresponds to the
annotations for each `smps` element.  Quantities should match.
A deepcopy of the provided dict is made.

**Arguments**:

    A dict value of list attributes that should each contain one
    element per list for each `smps` element.  Provide `None` to
    reset the `x` attributes.
- `value`: `Union[DataFrame, dict, None]`

<a name="canvasxpress.data.profile.CXStandardProfile.z"></a>
#### z

```python
 | @z.setter
 | z(value: Union[DataFrame, dict, None]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/profile.py#L267)

Sets the `z` attribute for the data, which corresponds to the
annotations for each `vars` element.  Quantities should match.
A deepcopy of the provided dict is made.

**Arguments**:

    A dict value of list attributes that should each contain one
    element per list for each `vars` element.  Provide `None` to
    reset the `z` attributes.
- `value`: `Union[DataFrame, dict, None]`

<a name="canvasxpress.data.profile.CXStandardProfile.match_vars_to_rows"></a>
#### match\_vars\_to\_rows

```python
 | @property
 | match_vars_to_rows() -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/profile.py#L309)

Indicates whether vars will be match to rows when formatting data.

**Returns**:

`bool`

<a name="canvasxpress.data.profile.CXStandardProfile.match_vars_to_rows"></a>
#### match\_vars\_to\_rows

```python
 | @match_vars_to_rows.setter
 | match_vars_to_rows(value: bool) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/profile.py#L319)

Sets whether vars will be match to rows when formatting data.

**Arguments**:

    True if an error shall be raised if the number of `vars` does not
    match the number of `data` rows.
- `value`: `bool`

<a name="canvasxpress.data.profile.CXStandardProfile.match_smps_to_cols"></a>
#### match\_smps\_to\_cols

```python
 | @property
 | match_smps_to_cols() -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/profile.py#L338)

Indicates whether smps will be match to columns when formatting data.

**Returns**:

`bool`

<a name="canvasxpress.data.profile.CXStandardProfile.match_smps_to_cols"></a>
#### match\_smps\_to\_cols

```python
 | @match_smps_to_cols.setter
 | match_smps_to_cols(value: bool) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/profile.py#L348)

Sets whether smps will be match to rows when formatting data.

**Arguments**:

    True if an error shall be raised if the number of `smps` does not
    match the number of `data` columns.
- `value`: `bool`

<a name="canvasxpress.data.profile.CXStandardProfile.match_x_to_smps"></a>
#### match\_x\_to\_smps

```python
 | @property
 | match_x_to_smps() -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/profile.py#L368)

Indicates whether x member attribute elements will be matched to smps
when formatting data.

**Returns**:

`bool`

<a name="canvasxpress.data.profile.CXStandardProfile.match_x_to_smps"></a>
#### match\_x\_to\_smps

```python
 | @match_x_to_smps.setter
 | match_x_to_smps(value: bool) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/profile.py#L379)

Sets whether x member attribute elements will be matched to smps
when formatting data.

**Arguments**:

    True if an error shall be raised if the number of `x` member
    attribute elements does not match the number of `smps` elements.
- `value`: `bool`

<a name="canvasxpress.data.profile.CXStandardProfile.match_z_to_vars"></a>
#### match\_z\_to\_vars

```python
 | @property
 | match_z_to_vars() -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/profile.py#L400)

Indicates whether z member attribute elements will be matched to vars
when formatting data.

**Returns**:

`bool`

<a name="canvasxpress.data.profile.CXStandardProfile.match_z_to_vars"></a>
#### match\_z\_to\_vars

```python
 | @match_z_to_vars.setter
 | match_z_to_vars(value: bool) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/profile.py#L411)

Sets whether z member attribute elements will be matched to vars
when formatting data.

**Arguments**:

    True if an error shall be raised if the number of `z` member
    attribute elements does not match the number of `vars` elements.
- `value`: `bool`

<a name="canvasxpress.data.profile.CXStandardProfile.add_data_section"></a>
#### add\_data\_section

```python
 | add_data_section(section: str, source: dict, target: dict) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/profile.py#L425)

Adds a source data section, such as X, to the target if such a section
does not yet exist.

**Arguments**:

    The name of the section, such as X.
    The dict of lists to add.
    The dict to which source should be added.
- `section`: `str`
- `source`: `dict`
- `target`: `dict`

<a name="canvasxpress.data.profile.CXStandardProfile.render_to_profiled_dict"></a>
#### render\_to\_profiled\_dict

```python
 | render_to_profiled_dict(data: CXData, **kwargs, ,) -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/profile.py#L459)

Converts a given `CXData` instance into a dict suitable for use by
`CanvasXpress` when creating data instructions for the JS object.

*For matrix data:*<br>
If `vars` are not set then `data` will be inspected:
- The index will be used.
If `smps` are not set then `data` will be inspected:
- The column headers will be used.

*For key-pair data:*<br>
If `vars` are not set then `data` will be inspected:
- If `y` is not provided then an attribute will be established.
- If y[vars] is not provided then vars will be assigned numerically
for each row in data.

If `smps` are not set then `data` will be inspected:
- If `y` is not provided then an attribute will be established.
- If y[smps] is not provided then smps will be assigned numerically
for each row in data.

`x` and `z` values are passed-through to the rendered JSON data.

**Arguments**:

    The data object to introspect to create an enveloping profile.

    Indicates whether the number `y[vars]` must equal the number of
    rows specified in `y[data]`.  If `True` then an exception will be
    raised should the number of vars and rows of data not match.

    Indicates whether the number `y[smps]` must equal the number of
    columns specified in `y[data]`.  If `True` then an exception will be
    raised should the number of smps and columns of data not match.

    Indicates whether for each attribute of `x` the number of list
    elements should match the number of `smps` elements.  If `True`
    then an exception will be raised if the counts do not align.

    Indicates whether for each attribute of `z` the number of list
    elements should match the number of `vars` elements.  If `True`
    then an exception will be raised if the counts do not align.

- `data`: `CXData`
- `match_vars_to_rows`: `bool`
- `match_smps_to_cols`: `bool`
- `match_x_to_smps`: `bool`
- `match_z_to_vars`: `bool`

**Returns**:

`dict`

<a name="canvasxpress.data.profile.CXStandardProfile.__init__"></a>
#### \_\_init\_\_

```python
 | __init__()
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/profile.py#L726)

Initializes the CXStandardProfile object.

<a name="canvasxpress.data.profile.CXVennProfile"></a>
## CXVennProfile Objects

```python
class CXVennProfile(CXDataProfile)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/profile.py#L740)

`CXVennProfile` provides Venn diagram chart data profile functionality,
by which the topics of `venn` and `legend` are handled in conversions.

<a name="canvasxpress.data.profile.CXVennProfile.legend"></a>
#### legend

```python
 | @property
 | legend() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/profile.py#L752)

Returns the values to be used for the legend if such are not defined
in the data.

**Returns**:

`dict`

<a name="canvasxpress.data.profile.CXVennProfile.legend"></a>
#### legend

```python
 | @legend.setter
 | legend(value: Union[dict, None]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/profile.py#L763)

Sets the values to be used for the legend.  Overrides legend values in
the data if available.

"param value: `Union[dict, None]`
    The key-pair values to be used for the legend.  Use None to reset
    the key-pair values.

<a name="canvasxpress.data.profile.CXVennProfile.render_to_profiled_dict"></a>
#### render\_to\_profiled\_dict

```python
 | render_to_profiled_dict(data: CXData, **kwargs) -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/profile.py#L781)

Converts a given `CXData` instance into a dict suitable for use by
`CanvasXpress` when creating data instructions for the JS object.

*For matrix data:*<br>
Data must be one column with numeric values plus one index. `legend`
values will be provided as set for the profile.

```python
df = DataFrame.from_dict(
    {
        "A": 340,
        "B": 562,
        "C": 620,
        "AB": 639,
        "AC": 456,
        "BC": 915,
        "ABC": 552
    },
    orient="index"
)
```

If an index is not specified then the implicit index is used.

*For key-pair data:*<br>
Data must be a dict with the attribute `venn` with child attributes
`data` and `legend`.  Or, `venn` can be ommitted.  `legend` is
optional, and if values are set for the profile these will override
those in the JSON data.

```python
{
    "venn": {
        "data": {
            "A": 340,
            "B": 562,
            "C": 620,
            "AB": 639,
            "AC": 456,
            "BC": 915,
            "ABC": 552
        },
        "legend": {
            "A": "List1",
            "B": "List2",
            "C": "List3"
        }
    }
}
```

If a legend value needs to be calculated then `kwargs` is examined for
`config`, which is expected to be of type `CXConfigs`.  If `config` is
available then the CXConfig labelled `vennGroups` is sought.  The value
assigned to `vennGroups` is used to count out an index of legend labels.

**Arguments**:

    The data object to introspect to create an enveloping profile.
- `data`: `CXData`

<a name="canvasxpress.data.profile.CXNetworkProfile"></a>
## CXNetworkProfile Objects

```python
class CXNetworkProfile(CXDataProfile)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/profile.py#L938)

<a name="canvasxpress.data.profile.CXNetworkProfile.render_to_profiled_dict"></a>
#### render\_to\_profiled\_dict

```python
 | render_to_profiled_dict(data: CXData, **kwargs) -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/profile.py#L939)

Converts a given `CXData` instance into a dict suitable for use by
`CanvasXpress` when creating data instructions for the JS object.

*For matrix data:*<br>
Not supported.  A TypeError will be raised.

*For key-pair data:*<br>
Data must be provided in key-pair form.  Multiple data structures
typical of network diagrams are supported by the Javascript library,
so only a minimal check is performed for conformance at the Python tier.
Generally, data is shaped via nodes and edges.  Nodes describe points,
whereas edges describe links between nodes.

**Arguments**:

    The data object to introspect to create an enveloping profile.
- `data`: `CXData`

<a name="canvasxpress.data.profile.CXGenomeProfile"></a>
## CXGenomeProfile Objects

```python
class CXGenomeProfile(CXDataProfile)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/profile.py#L971)

<a name="canvasxpress.data.profile.CXGenomeProfile.render_to_profiled_dict"></a>
#### render\_to\_profiled\_dict

```python
 | render_to_profiled_dict(data: CXData, **kwargs) -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/profile.py#L972)

Converts a given `CXData` instance into a dict suitable for use by
`CanvasXpress` when creating data instructions for the JS object.

*For matrix data:*<br>
Not supported.  A TypeError will be raised.

*For key-pair data:*<br>
Data is provided as-is, but it is validated to ensure that a top-tier
`tracks` attribute of type `list` is present, and that child elements
are `dict` types with `type` attributes specified.

**Arguments**:

    The data object to introspect to create an enveloping profile.
- `data`: `CXData`

<a name="canvasxpress.data.profile.CXRawProfile"></a>
## CXRawProfile Objects

```python
class CXRawProfile(CXDataProfile)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/profile.py#L1020)

<a name="canvasxpress.data.profile.CXRawProfile.render_to_profiled_dict"></a>
#### render\_to\_profiled\_dict

```python
 | render_to_profiled_dict(data: CXData, **kwargs) -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/profile.py#L1021)

Passes the raw `dict` form of the `CXData` object with no modification.

*For matrix data:*<br>
Converted by the `CXData` object to `dict` form.

*For key-pair data:*<br>
Converted by the `CXData` object to `dict` form.

**Arguments**:

    The data object to introspect to create an enveloping profile.
- `data`: `CXData`

<a name="canvasxpress.data.url"></a>
# canvasxpress.data.url

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/url.py#L1)

<a name="canvasxpress.data.url.CXUrlData"></a>
## CXUrlData Objects

```python
class CXUrlData(CXData)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/url.py#L6)

CXUrlData provides the ability to accept a URL and pass it properly to the
CanvasXpress object.

<a name="canvasxpress.data.url.CXUrlData.url"></a>
#### url

```python
 | @property
 | url() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/url.py#L18)

Provides the URL formatted as a string.

**Returns**:

`str`

<a name="canvasxpress.data.url.CXUrlData.url"></a>
#### url

```python
 | @url.setter
 | url(url: str) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/url.py#L28)

Tracks the specified URL. `ValueError` will be raised if the URL is
malformed.

**Arguments**:

    A string form of the URL, which must be in a stanard format for
    files, http resources, ftp resources, etc.
- `url`: `str`

<a name="canvasxpress.data.url.CXUrlData.data"></a>
#### data

```python
 | @property
 | data() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/url.py#L40)

A property accessor for the data managed by the object.  Regardless of
the input data the returned data structure will be a dict-type for use
with CanvasXpress.

**Returns**:

`dict`

<a name="canvasxpress.data.url.CXUrlData.data"></a>
#### data

```python
 | @data.setter
 | data(data: dict) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/url.py#L52)

Sets the URL using a data dict with the following attributes:
`scheme`, `netloc`, `path`, `query`, `fragment`, `username`,
`password`, `hostname`, `port`, `params`. `ValueError` will be
raised if the URL is malformed.

**Arguments**:

    The URL as broken into a dict with the above attributes set to a
    valid string for the topic or an empty string.
- `data`: `dict`

<a name="canvasxpress.data.url.CXUrlData.get_raw_dict_form"></a>
#### get\_raw\_dict\_form

```python
 | get_raw_dict_form() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/url.py#L71)

Provides a simple dict perspective of the data with no metadata or other
contextual transformations performed.  For example, if the data is
natively in `dict` form then it would be passed-through with no
modification or enhancement.

**Returns**:

`dict`

<a name="canvasxpress.data.url.CXUrlData.render_to_dict"></a>
#### render\_to\_dict

```python
 | render_to_dict(**kwargs) -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/url.py#L83)

Converts the object into a dict representation.

**Returns**:

`dict`

<a name="canvasxpress.data.url.CXUrlData.validate_url"></a>
#### validate\_url

```python
 | @classmethod
 | validate_url(cls, url: str, detail_errors: bool = True) -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/url.py#L93)

Validates that the URL conforms to a recognized standard.  URLs must
begin with a valid scheme such as `file://` or `http://`.

**Arguments**:

    The string form of the URL to be validated.
    True (default) if an exception should be raised with information
    detailing issues or errors, or `False` if the method should
    return `False` upon encountering issues.
- `url`: `str`
- `detail_errors`: `bool`

**Returns**:

`bool`

<a name="canvasxpress.data.url.CXUrlData.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(data: str) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/url.py#L123)

Initializes the CXUrlData object with a valid URL.  URLs must begin with
a valid scheme such as `file://` or `http://`.  `ValueError` will be
raised if the URL is malformed.

**Arguments**:

    A string form of the URL, which must be in a stanard format for
    files, http resources, ftp resources, etc.
- `data`: `str`

<a name="canvasxpress.data.keypair"></a>
# canvasxpress.data.keypair

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/keypair.py#L1)

<a name="canvasxpress.data.keypair.CXDictData"></a>
## CXDictData Objects

```python
@total_ordering
class CXDictData(CXKeyPairData)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/keypair.py#L13)

A CXData class dedicated to processing Python dict-structured data.

<a name="canvasxpress.data.keypair.CXDictData.data"></a>
#### data

```python
 | @property
 | data() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/keypair.py#L24)

Provides a reference to the dict tracked by the object.

**Returns**:

`dict`

<a name="canvasxpress.data.keypair.CXDictData.data"></a>
#### data

```python
 | @data.setter
 | data(value: dict) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/keypair.py#L33)

Sets the data associated with the object.

**Arguments**:

    The dictionary to be tracked by the object.  `None` will result in
    an empty dict.  A deep copy will be made of a valid `CXDict` or
    `dict` provided.
- `value`: `dict`

<a name="canvasxpress.data.keypair.CXDictData.get_raw_dict_form"></a>
#### get\_raw\_dict\_form

```python
 | get_raw_dict_form() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/keypair.py#L53)

Provides a simple dict perspective of the data with no metadata or other
contextual transformations performed.  For example, if the data is
natively in `dict` form then it would be passed-through with no
modification or enhancement.

This implementation provides matrix data formatted in a `dict` object
with `DataFrame.to_dict('split')` behaviour.

**Returns**:

`dict`

<a name="canvasxpress.data.keypair.CXDictData.render_to_dict"></a>
#### render\_to\_dict

```python
 | render_to_dict(**kwargs) -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/keypair.py#L69)

Provides a dict representation of the data.

**Returns**:

`dict`

<a name="canvasxpress.data.keypair.CXDictData.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(data: Union[dict, None] = None, profile: Union[CXDataProfile, None] = None) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/keypair.py#L83)

Initializes the CXData object with data.  Only dict or compatible data
types are accepted.

**Arguments**:

    `None` to initialize with an empty dictionary, or a `dict`-like
    object to assign mapped data.
    Specify the desired profile object to facilitate transformation of
    data into a CanvasXpress JSON data object.  `None` to avoid use of
    a profile.
- `data`: `Union[dict, None]`
- `profile`: `Union[CXDataProfile, None]`

<a name="canvasxpress.data.keypair.CXDictData.__copy__"></a>
#### \_\_copy\_\_

```python
 | __copy__() -> "CXDictData"
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/keypair.py#L100)

*copy constructor* that returns a copy of the CXDictData object.

**Returns**:

`CXDictData` A copy of the wrapping object.

<a name="canvasxpress.data.keypair.CXDictData.__deepcopy__"></a>
#### \_\_deepcopy\_\_

```python
 | __deepcopy__(memo) -> "CXDictData"
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/keypair.py#L107)

*deepcopy constructor* that returns a copy of the CXDictData object.

**Returns**:

`CXDictData` A copy of the wrapping object and deepcopy of

<a name="canvasxpress.data.keypair.CXDictData.__lt__"></a>
#### \_\_lt\_\_

```python
 | __lt__(other: "CXDictData") -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/keypair.py#L115)

*less than* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

    `CXDictData` The object to compare.
- `other`: 

**Returns**:

`bool`

<a name="canvasxpress.data.keypair.CXDictData.__eq__"></a>
#### \_\_eq\_\_

```python
 | __eq__(other: "CXDictData") -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/keypair.py#L155)

*equals* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

    `CXDictData` The object to compare.
- `other`: 

**Returns**:

`bool`

<a name="canvasxpress.data.keypair.CXDictData.__str__"></a>
#### \_\_str\_\_

```python
 | __str__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/keypair.py#L193)

*str* function.  Converts the CXDictData object into a JSON
representation.
:returns" `str` JSON form of the `CXDictData`.

<a name="canvasxpress.data.keypair.CXDictData.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/keypair.py#L201)

*repr* function.  Converts the CXDictData object into a pickle string
that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.data.keypair.CXJSONData"></a>
## CXJSONData Objects

```python
class CXJSONData(CXDictData)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/keypair.py#L210)

A CXData class dedicated to processing JSON data.

<a name="canvasxpress.data.keypair.CXJSONData.json"></a>
#### json

```python
 | @property
 | json() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/keypair.py#L216)

Provides a copy of the JSON tracked by the object.

**Returns**:

`str`

<a name="canvasxpress.data.keypair.CXJSONData.json"></a>
#### json

```python
 | @json.setter
 | json(value: Union[dict, str]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/keypair.py#L225)

Sets the data associated with the object.

**Arguments**:

    The JSON to be tracked by the object.  `None` will result in
    an empty JSON.  If `value` is URL beginning with *http/s*
    then `json` will attempt to download the data.
- `value`: `str`

<a name="canvasxpress.data.keypair.CXJSONData.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(data: Union[dict, str, None] = None, profile: Union[CXDataProfile, None] = None) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/keypair.py#L258)

Initializes the CXData object with data.  Only dict or compatible data
types are accepted.

**Arguments**:

    `None` to initialize with an empty JSON, or a JSON/`dict`-like
    object to assign mapped data.
    Specify the desired profile object to facilitate transformation of
    data into a CanvasXpress JSON data object.  `None` to avoid use of
    a profile.
- `data`: `Union[dict, str, None]`
- `profile`: `Union[CXDataProfile, None]`

<a name="canvasxpress.data.keypair.CXJSONData.__copy__"></a>
#### \_\_copy\_\_

```python
 | __copy__() -> "CXJSONData"
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/keypair.py#L276)

*copy constructor* that returns a copy of the CXDictData objct.

**Returns**:

`CXDictData` A copy of the wrapping object.

<a name="canvasxpress.data.keypair.CXJSONData.__deepcopy__"></a>
#### \_\_deepcopy\_\_

```python
 | __deepcopy__(memo) -> "CXJSONData"
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/keypair.py#L283)

*deepcopy constructor* that returns a copy of the CXJSONData object.

**Returns**:

`CXJSONData` A copy of the wrapping object and deepcopy of

<a name="canvasxpress.data.keypair.CXJSONData.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/keypair.py#L291)

*repr* function.  Converts the CXJSONData object into a pickle string
that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.data.text"></a>
# canvasxpress.data.text

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/text.py#L1)

<a name="canvasxpress.data.text.CXTextData"></a>
## CXTextData Objects

```python
class CXTextData(CXData)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/text.py#L7)

`CXTextData` is a `CXData` class that provides plain-text data directly to
the CanvasXpress for Javascript object.  In this manner, the Python tier
makes no assumptions about the data content and permits the Javascript tier
to address any required adjustments in order to properly display the data
within a chart.  If the data is erroneously formatted then the only
feedback will be at the Javascript tier.

<a name="canvasxpress.data.text.CXTextData.text"></a>
#### text

```python
 | @property
 | text() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/text.py#L24)

Returns the raw text form of the data.

**Returns**:

`str`

<a name="canvasxpress.data.text.CXTextData.text"></a>
#### text

```python
 | @text.setter
 | text(value: str) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/text.py#L33)

Sets the text to be provided to CanvasXpress.

**Arguments**:

    The text to provide as-is to CanvasXpress.  `None` will be
    converted to an empty `str`.  Values of type other than `str`
    will be converted using `str()`.
- `value`: `str`

<a name="canvasxpress.data.text.CXTextData.data"></a>
#### data

```python
 | @property
 | data() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/text.py#L51)

A property accessor for the data managed by the object.  Regardless of
the input data the returned data structure will be a dict-type for use
with CanvasXpress.

**Returns**:

`dict`

<a name="canvasxpress.data.text.CXTextData.get_raw_dict_form"></a>
#### get\_raw\_dict\_form

```python
 | get_raw_dict_form() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/text.py#L61)

Provides a simple dict perspective of the data with no metadata or other
contextual transformations performed.  For example, if the data is
natively in `dict` form then it would be passed-through with no
modification or enhancement.

**Returns**:

`dict`

<a name="canvasxpress.data.text.CXTextData.render_to_dict"></a>
#### render\_to\_dict

```python
 | render_to_dict(**kwargs) -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/text.py#L87)

Converts the object into a dict representation.

**Returns**:

`dict`

<a name="canvasxpress.data.text.CXTextData.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(data: Union[object, None] = None) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/text.py#L96)

Initializes the CXData object with data.

**Arguments**:

    Given an object or no data prepares a new CXData instance ready for
    use by a `CanvasXpress` object.
- `data`: `Union[object, None]`

<a name="canvasxpress.data.base"></a>
# canvasxpress.data.base

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/base.py#L1)

<a name="canvasxpress.data.base.CXData"></a>
## CXData Objects

```python
class CXData(CXDictConvertable)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/base.py#L19)

CXData defines an essential data class for managing data acquisiton,
transformation, and introspection as required by the `CanvasXPress` class.

<a name="canvasxpress.data.base.CXData.data"></a>
#### data

```python
 | @property
 | @abstractmethod
 | data() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/base.py#L27)

A property accessor for the data managed by the object.  Regardless of
the input data the returned data structure will be a dict-type for use
with CanvasXpress.

**Returns**:

`dict`

<a name="canvasxpress.data.base.CXData.get_raw_dict_form"></a>
#### get\_raw\_dict\_form

```python
 | @abstractmethod
 | get_raw_dict_form() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/base.py#L38)

Provides a simple dict perspective of the data with no metadata or other
contextual transformations performed.  For example, if the data is
natively in `dict` form then it would be passed-through with no
modification or enhancement.

**Returns**:

`dict`

<a name="canvasxpress.data.base.CXData.__init__"></a>
#### \_\_init\_\_

```python
 | @abstractmethod
 | __init__(data: Union[object, None]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/base.py#L51)

Initializes the CXData object with data.

**Arguments**:

    Given an object or no data prepares a new CXData instance ready for
    use by a `CanvasXpress` object.
- `data`: `Union[object, None]`

<a name="canvasxpress.data.base.CXDataProfileException"></a>
## CXDataProfileException Objects

```python
class CXDataProfileException(ValueError)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/base.py#L61)

CXDataProfileException is used by CXDataProfile to describe validation
errors when considering CXData objects in the context of CXDataProfile
objects.

<a name="canvasxpress.data.base.CXDataProfile"></a>
## CXDataProfile Objects

```python
class CXDataProfile(ABC)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/base.py#L71)

CXDataProfile assists with CXData translations into CanvasXpress JSON data
formats, such as documented at
[CanvasXpress.org](https://www.canvasxpress.org/docs.html#data).

<a name="canvasxpress.data.base.CXDataProfile.render_to_profiled_dict"></a>
#### render\_to\_profiled\_dict

```python
 | @abstractmethod
 | render_to_profiled_dict(data: CXData, **kwargs) -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/base.py#L79)

Converts a given `CXData` instance into a dict suitable for use by
`CanvasXpress` when creating data instructions for the JS object.

<a name="canvasxpress.data.base.CXProfiledData"></a>
## CXProfiledData Objects

```python
class CXProfiledData(CXData)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/base.py#L87)

CXData defines an essential data class for managing data acquisiton,
transformation, and introspection as required by the `CanvasXPress` class.

<a name="canvasxpress.data.base.CXProfiledData.profile"></a>
#### profile

```python
 | @property
 | profile() -> Union[None, CXDataProfile]
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/base.py#L100)

Provides the `CXDataProfile` associated with the `CXData` instance.

**Returns**:

`Union[None, CXDataProfile]`

<a name="canvasxpress.data.base.CXProfiledData.profile"></a>
#### profile

```python
 | @profile.setter
 | profile(profile: Union[None, CXDataProfile]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/base.py#L109)

Sets the `CXDataProfile` associated with the `CXData` instance.  The
default associated profile is `CXStandardProfile`, which supports the
most typical CanvasXpress JSON data format for plotting.  To avoid the
use of a profile and pass only a basic raw JSON edition of the instance
to CanvasXpress set the profile to `None`.

**Arguments**:

    The profile to use when transforming the `CXData` instance into a
    CanvasXpress JSON data object.  Use `None` to avoid any
    transformation beyond the essential conversion of the instance into
    a JSON-like form.  For example, with `None` if the data tracked is
    a dict then the renderer would simply pass the data through.
- `profile`: `Union[None, CXDataProfile]`

<a name="canvasxpress.data.base.CXProfiledData.data"></a>
#### data

```python
 | @property
 | @abstractmethod
 | data() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/base.py#L128)

A property accessor for the data managed by the object.  Regardless of
the input data the returned data structure will be a dict-type for use
with CanvasXpress.

**Returns**:

`dict`

<a name="canvasxpress.data.base.CXProfiledData.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(data: Union[object, None], profile: Union[CXDataProfile, None] = None) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/base.py#L138)

Initializes the CXData object with data.

**Arguments**:

    Given an object or no data prepares a new CXData instance ready for
    use by a `CanvasXpress` object.
    Specify the desired profile object to facilitate transformation of
    data into a CanvasXpress JSON data object.  `None` to avoid use of
    a profile.
- `data`: `Union[object, None]`
- `profile`: `Union[CXDataProfile, None]`

<a name="canvasxpress.data.base.CXKeyPairData"></a>
## CXKeyPairData Objects

```python
class CXKeyPairData(CXProfiledData)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/base.py#L154)

CXKeyPairData is a marker class to indicate that the data managed will be
generally of the structure key-pair.  A `dict` is an example of key-pair
data.

<a name="canvasxpress.data.base.CXMatrixData"></a>
## CXMatrixData Objects

```python
class CXMatrixData(CXProfiledData)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/data/base.py#L164)

CXMatrixData is a marker class to indicate that the data management will be
generally of the structure matrix or tabular.  A spreadsheet is an example
of matrix data.

<a name="canvasxpress.canvas"></a>
# canvasxpress.canvas

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/canvas.py#L1)

<a name="canvasxpress.canvas.CanvasXpress"></a>
## CanvasXpress Objects

```python
class CanvasXpress(CXHtmlConvertable)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/canvas.py#L53)

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

<a name="canvasxpress.canvas.CanvasXpress.anonymous"></a>
#### anonymous

```python
 | @property
 | anonymous() -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/canvas.py#L95)

Indicates whether the object is anonymous.  If `True`, then `render_to()` will result in a one-time random
ID string being returned for use in contexts such as rapidly changing React environments.  If `False`, then
the ID string returned is the one set for the object by the developer.

**Returns**:

`bool` `True` if the object is anonymous; otherwise `False`.

<a name="canvasxpress.canvas.CanvasXpress.render_to"></a>
#### render\_to

```python
 | @property
 | render_to() -> Union[str, None]
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/canvas.py#L105)

The ID of the CanvasXpress object's associated HTML components, such as
the create_element canvas element.  Sets the `id` attribute of the `<canvas>`
element.

**Returns**:

`str` The ID, if configured; `None` if anonymous.

<a name="canvasxpress.canvas.CanvasXpress.render_to"></a>
#### render\_to

```python
 | @render_to.setter
 | render_to(value: Union[str, None]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/canvas.py#L117)

Sets the render_to of the CanvasXpress instance.  Sets the `id`
attribute of the `<canvas>` element.

**Arguments**:

    `str` The ID to be associated.  Cannot be `None`, and
    must be alphanumeric.  Non-alphanumeric characters will
    be removed, except for `_`, and if the remaining string
    is empty then a UUID4 will be substituted.  This is to preserve JS
    compatibility during rendering. `None` can also be provided to
    indicate that this object should be anonymous, such as for use
    in rapidly changing React interfaces.
- `value`: 

<a name="canvasxpress.canvas.CanvasXpress.license_available"></a>
#### license\_available

```python
 | @property
 | license_available() -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/canvas.py#L152)

Indicates if a license is associated with the CanvasXpress object.

**Returns**:

`True` if a license file URL has been set.

<a name="canvasxpress.canvas.CanvasXpress.license_url"></a>
#### license\_url

```python
 | @property
 | license_url() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/canvas.py#L160)

Returns the location of the license file associated with the
CanvasXpress object.

**Returns**:

`str` URL of the file or `None` if no file is associated.

<a name="canvasxpress.canvas.CanvasXpress.license_url"></a>
#### license\_url

```python
 | @license_url.setter
 | license_url(value: str) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/canvas.py#L169)

Sets the location of the license file to be associated with the
CanvasXpress object.

**Arguments**:

    `str` The path to the license file or `None` if a previously set URL
    is no longer valid.
- `value`: 

<a name="canvasxpress.canvas.CanvasXpress.CHART_WIDTH_DEFAULT"></a>
#### CHART\_WIDTH\_DEFAULT

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/canvas.py#L191)

Default width of the chart when rendered, such as into HTML.

<a name="canvasxpress.canvas.CanvasXpress.width"></a>
#### width

```python
 | @property
 | width() -> int
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/canvas.py#L202)

Indicates the preferred <canvas> Web element width when rendered.  This
property is used to facilitate integration with Web containers such
as Jupyter notebooks. Added to the `<canvas>` element, and also
influences create_element containers for contexts such as Jupyter Notebooks.

**Returns**:

`int` The width

<a name="canvasxpress.canvas.CanvasXpress.width"></a>
#### width

```python
 | @width.setter
 | width(value: int)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/canvas.py#L213)

Sets the preferred Web element width when rendered. Added to the
`<canvas>` element, and also influences create_element containers for contexts
such as Jupyter Notebooks.

**Arguments**:

    The pixel count.  Cannot be `None` or less than `1`.
- `value`: `int`

<a name="canvasxpress.canvas.CanvasXpress.CHART_HEIGHT_DEFAULT"></a>
#### CHART\_HEIGHT\_DEFAULT

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/canvas.py#L233)

Default height of the chart in pixels when rendered, such as into HTML.

<a name="canvasxpress.canvas.CanvasXpress.height"></a>
#### height

```python
 | @property
 | height() -> int
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/canvas.py#L244)

Indicates the preferred Web element height when rendered.  This
property is used to facilitate integration with Web containers such
as Jupyter notebooks.  Added to the `<canvas>` element, and also
influences create_element containers for contexts such as Jupyter Notebooks.

**Returns**:

`int` The pixel count

<a name="canvasxpress.canvas.CanvasXpress.height"></a>
#### height

```python
 | @height.setter
 | height(value: int)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/canvas.py#L255)

Sets the preferred Web element height when rendered.  Added to the
`<canvas>` element, and also influences create_element containers for contexts
such as Jupyter Notebooks.

**Arguments**:

- `value`: `int`

<a name="canvasxpress.canvas.CanvasXpress.data"></a>
#### data

```python
 | @property
 | data() -> CXData
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/canvas.py#L282)

Provides access to the CXData associated with this CanvasXpress chart.

**Returns**:

`CXData` The data to be associated with the chart.

<a name="canvasxpress.canvas.CanvasXpress.data"></a>
#### data

```python
 | @data.setter
 | data(value: Union[CXData, dict, DataFrame, str, None]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/canvas.py#L290)

Sets the CXData associated with this CanvasXpress chart.

**Arguments**:

    An object translatable into a CXData type. If the object is an
    instance of CXData then it will be tracked by the CanvasXpress
    object; otherwise, a new CXData object will be created to manage
    the content.
- `value`: `Union[CXData, dict, DataFrame, str, None]`

<a name="canvasxpress.canvas.CanvasXpress.events"></a>
#### events

```python
 | @property
 | events() -> CXEvents
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/canvas.py#L336)

Provides access to the CXEvents associated with this CanvasXpress chart.

**Returns**:

`CXEvents` The events to be associated with the chart.

<a name="canvasxpress.canvas.CanvasXpress.events"></a>
#### events

```python
 | @events.setter
 | events(events: Union[CXEvents, List[CXEvent], None]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/canvas.py#L344)

Sets the CXEvents associated with this CanvasXpress chart.

**Arguments**:

    `CXEvents, List[CXEvent], None` An object translatable into a
    CXEvents type.  If the object is an instance of CXEvents then it
    will be tracked by the CanvasXpress object; otherwise, a new
    CXEvents object will be created to manage the content.
- `events`: 

<a name="canvasxpress.canvas.CanvasXpress.config"></a>
#### config

```python
 | @property
 | config() -> CXConfigs
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/canvas.py#L371)

Provides access to the CXConfigs associated with this CanvasXpress chart.

**Returns**:

`CXConfigs` The config to be associated with the chart.

<a name="canvasxpress.canvas.CanvasXpress.config"></a>
#### config

```python
 | @config.setter
 | config(value: Union[List[CXConfig], List[tuple], List[list], dict, CXConfigs])
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/canvas.py#L379)

Sets the CXConfigs associated with this CanvasXpress chart.

**Arguments**:

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
- `value`: `Union[

<a name="canvasxpress.canvas.CanvasXpress.after_render"></a>
#### after\_render

```python
 | @property
 | after_render() -> CXConfigs
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/canvas.py#L421)

Provides access to the CXConfigs associated with this CanvasXpress
chart's afterRender property.

**Returns**:

`CXConfigs`

<a name="canvasxpress.canvas.CanvasXpress.after_render"></a>
#### after\_render

```python
 | @after_render.setter
 | after_render(value: Union[List[CXConfig], List[tuple], List[list], dict, CXConfigs])
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/canvas.py#L431)

Sets the CXConfigs associated with this CanvasXpress chart's afterRender
property.

**Arguments**:

    CXConfigs]`
    An object translatable into a CXConfigs
    type.  If the object is an instance of CXConfigs then it will be
    tracked by the CanvasXpress object; otherwise, a new CXConfigs
    object will be created to manage the content.
- `value`: `Union[List[CXConfig], List[tuple], dict, CXConfigs,

<a name="canvasxpress.canvas.CanvasXpress.other_init_params"></a>
#### other\_init\_params

```python
 | @property
 | other_init_params() -> CXConfigs
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/canvas.py#L468)

Provides access to additional parameters that will be used with the
`CanvasXpress` for Javascript constructor, such as `afterRencderInit`.

**Returns**:

`CXConfigs`

<a name="canvasxpress.canvas.CanvasXpress.other_init_params"></a>
#### other\_init\_params

```python
 | @other_init_params.setter
 | other_init_params(value: Union[List[CXConfig], List[tuple], List[list], dict, CXConfigs])
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/canvas.py#L480)

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

**Arguments**:

    CXConfigs]`
    An object translatable into a CXConfigs type.  If the object is an
    instance of CXConfigs then it will be tracked by the CanvasXpress
    object; otherwise, a new CXConfigs object will be created to manage
    the content.
- `value`: `Union[List[CXConfig], List[tuple], List[list], dict,

<a name="canvasxpress.canvas.CanvasXpress.from_reproducible_json"></a>
#### from\_reproducible\_json

```python
 | @classmethod
 | from_reproducible_json(cls, cx_json: str, include_factory: bool = False, include_system: bool = False) -> "CanvasXpress"
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/canvas.py#L536)

Initializes a new `CanvasXpress` object using a reproducable research
JSON saved from a CanvasXpress chart rendered in a Web browser.

**Arguments**:

    A valid reproducable research JSON typical of those created by
    CanvasXpress when running a Web browser.

    Default `False`.  If `False` remove the `factory` attribute.

    Default `False`.  If `False` remove the `system` attribute.

- `cx_json`: `str`
- `include_factory`: `bool`
- `include_system`: `bool`

**Returns**:

`CanvasXpress`

<a name="canvasxpress.canvas.CanvasXpress.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(render_to: str = None, data: Union[CXData, dict, DataFrame, str, None] = None, events: Union[List[CXEvent], CXEvents] = None, config: Union[List[CXConfig], List[tuple], dict, CXConfigs] = None, after_render: Union[List[CXConfig], List[tuple], dict, CXConfigs] = None, other_init_params: Union[List[CXConfig], List[tuple], dict, CXConfigs] = None, canvas: Union[List[CXConfig], List[tuple], dict, CXConfigs] = None, width: int = CHART_WIDTH_DEFAULT, height: int = CHART_HEIGHT_DEFAULT) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/canvas.py#L624)

Initializes a new CanvasXpress object.  Default values are provided for
all parameters if values are not specified; otherwise the arguments are
treated as if an appropriate setter were used.

**Arguments**:

    initialization the object will be assigned an UUID4 value.
- `render_to`: See `render_to` property, except that on default
- `data`: See the `data` property
- `events`: See the `events` property
- `config`: See the `config` property
- `after_render`: See the `after_render` property
- `other_init_params`: See the 'other_init_params` property
- `canvas`: DEPRECATED, use `other_init_params`
- `width`: See the `width` property
- `height`: See the `height` property

<a name="canvasxpress.canvas.CanvasXpress.update_data_profile"></a>
#### update\_data\_profile

```python
 | update_data_profile(data: CXData, fix_missing_profile: bool, match_profile_to_graphtype: bool)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/canvas.py#L663)

Inspects the `CXData` object to see if it is a `CXProfiledData` object.
If so, then `fix_missing_profile` and `match_profile_to_graphtype` are
evaluated to determine if profile adjustments are to be made, and then
applied if/as appropriate.

**Arguments**:

    The data to inspect.  Only `CXProfiledData` objects will be
    modified.

    Defaults to `True`.  If `True` then CXData used for the chart will
    be provided with a data profile appropriate to the `graphType`
    (or CXStandardProfile if no graphType is provided).  If `False`
    then no profile will be applied to those data objects without
    profiles.

    Defaults to `True`.  If `True` then the `graphType` will be
    inspected and an appropriate data profile will be applied to
    the data object.  If a profile of an appropriate type is already
    associated then nothing is changed.  If a CXRawProfile is associated
    then no change is made regardless of the paranmeter value.
    Missing profiles are ignored unless fix_missing_profile is also
    `True`.  If `False` then no change to the data profile will be made
    if a profile is already associated with the data object.
- `data`: `CXData`
- `fix_missing_profile`: `bool`
- `match_profile_to_graphtype`: `bool`

<a name="canvasxpress.canvas.CanvasXpress.prepare_html_element_parts"></a>
#### prepare\_html\_element\_parts

```python
 | prepare_html_element_parts(fix_missing_profile: bool = True, match_profile_to_graphtype: bool = True) -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/canvas.py#L721)

Converts the CanvasXpress object into CanvasXpress element components in
anticipation of further use in renderable objects or conversion into HTML.

If the associated `CXData` is a type of `CXProfiledData` and a profile
has yet to be assigned then a profile can be assigned according to the
`CXConfig` labelled `graphType`.  If a profile is assigned but is not
`CXRawProfile` then the `graphType` can be reassessed, and if
appropriate a new profile better aligned to the data can be provided.

**Arguments**:

    Defaults to `True`.  If `True` then CXData used for the chart will
    be provided with a data profile appropriate to the `graphType`
    (or CXStandardProfile if no graphType is provided).  If `False`
    then no profile will be applied to those data objects without
    profiles.

    Defaults to `True`.  If `True` then the `graphType` will be
    inspected and an appropriate data profile will be applied to
    the data object.  If a profile of an appropriate type is already
    associated then nothing is changed.  If a CXRawProfile is associated
    then no change is made regardless of the paranmeter value.
    Missing profiles are ignored unless fix_missing_profile is also
    `True`.  If `False` then no change to the data profile will be made
    if a profile is already associated with the data object.

- `fix_missing_profile`: `bool`
- `match_profile_to_graphtype`: `bool`

**Returns**:

`dict` A map of values in anticipation of further conversion

<a name="canvasxpress.canvas.CanvasXpress.render_to_html_parts"></a>
#### render\_to\_html\_parts

```python
 | render_to_html_parts(fix_missing_profile: bool = True, match_profile_to_graphtype: bool = True) -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/canvas.py#L781)

Converts the CanvasXpress object into HTML5 complant script.

If the associated `CXData` is a type of `CXProfiledData` and a profile
has yet to be assigned then a profile can be assigned according to the
`CXConfig` labelled `graphType`.  If a profile is assigned but is not
`CXRawProfile` then the `graphType` can be reassessed, and if
appropriate a new profile better aligned to the data can be provided.

**Returns**:

`dict` A map of values appropriate for use in HTML, such as

**Arguments**:

    Defaults to `True`.  If `True` then CXData used for the chart will
    be provided with a data profile appropriate to the `graphType`
    (or CXStandardProfile if no graphType is provided).  If `False`
    then no profile will be applied to those data objects without
    profiles.

    Defaults to `True`.  If `True` then the `graphType` will be
    inspected and an appropriate data profile will be applied to
    the data object.  If a profile of an appropriate type is already
    associated then nothing is changed.  If a CXRawProfile is associated
    then no change is made regardless of the paranmeter value.
    Missing profiles are ignored unless fix_missing_profile is also
    `True`.  If `False` then no change to the data profile will be made
    if a profile is already associated with the data object.
- `fix_missing_profile`: `bool`
- `match_profile_to_graphtype`: `bool`

<a name="canvasxpress.canvas.CanvasXpress.__str__"></a>
#### \_\_str\_\_

```python
 | __str__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/canvas.py#L934)

*str* function.  Converts the `CanvasXpress` object into a JSON
representation.
:returns" `str`
    JSON form of the `CanvasXpress` object.

<a name="canvasxpress.canvas.CanvasXpress.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/7a244b6bd4950d4978955ed93c8afbf2cc874897/canvasxpress/canvas.py#L954)

*repr* function.  Converts the `CanvasXpress` object into a pickle
string that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

