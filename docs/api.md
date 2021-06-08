<a name="canvasxpress"></a>
# canvasxpress

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/__init__.py#L1)

The CanvasXpress package provides Python friendly management of the Javascript-
based [CanvasXpress](https://www.canvasxpress.org) library.  For an overview
and detailed instructions about CanvasXpress specifically please visit the site.

<a name="canvasxpress.util"></a>
# canvasxpress.util

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/util/__init__.py#L2)

<a name="canvasxpress.util.template"></a>
# canvasxpress.util.template

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/util/template.py#L1)

<a name="canvasxpress.util.template.render_from_template"></a>
#### render\_from\_template

```python
render_from_template(template: str, data: dict) -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/util/template.py#L1)

Updates the template text with the provided data.

**Arguments**:

:returns The adjusted template text
- `template`: `str` The name of the template file
- `data`: The `dict` of str values with which to update the template text

<a name="canvasxpress.config"></a>
# canvasxpress.config

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/__init__.py#L1)

The config package provides functionality for managing or assigning
configuration values associated with CanvasXpress objects.

<a name="canvasxpress.config.type"></a>
# canvasxpress.config.type

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L1)

<a name="canvasxpress.config.type.CXConfig"></a>
## CXConfig Objects

```python
@total_ordering
class CXConfig(ABC)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L12)

CXConfig provides the means by which CanvasXpress objects can be configured for
customized rendering and interaction.

<a name="canvasxpress.config.type.CXConfig.label"></a>
#### label

```python
 | @property
 | label() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L24)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L33)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L44)

Sets the value of the configuration.  Must be implemented by concrete
classes.

**Arguments**:

    The value to be accepted.  Will be more specific with concrete
    implementations, such as `str` for string configurations.
- `value`: `Any`

<a name="canvasxpress.config.type.CXConfig.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(label: str, value: Any)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L54)

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
 | __copy__() -> 'CXConfig'
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L71)

*copy constructor* that provides a new CXConfig of the same type with
the data referenced.

**Returns**:

`CXConfig` of the proper type

<a name="canvasxpress.config.type.CXConfig.__deepcopy__"></a>
#### \_\_deepcopy\_\_

```python
 | __deepcopy__(memo)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L82)

*deepcopy constructor* that provides a new CXConfig of the same type with
the a deepcopy of the data.

**Returns**:

`CXConfig` of the proper type

<a name="canvasxpress.config.type.CXConfig.__hash__"></a>
#### \_\_hash\_\_

```python
 | __hash__() -> int
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L96)

Provides a hash proxy for the object as converted into its `repr` form.

**Returns**:

`int`

<a name="canvasxpress.config.type.CXConfig.__lt__"></a>
#### \_\_lt\_\_

```python
 | __lt__(other: 'CXConfig') -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L103)

*less than* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

    `CXConfig` The object to compare.
- `other`: 

**Returns**:

`bool`

<a name="canvasxpress.config.type.CXConfig.__eq__"></a>
#### \_\_eq\_\_

```python
 | __eq__(other: 'CXConfig') -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L135)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L159)

*str* function.  Converts the object into a JSON string.

<a name="canvasxpress.config.type.CXConfig.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L170)

*repr* function.  Converts the CXConfig object into a pickle string
that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.config.type.CXString"></a>
## CXString Objects

```python
class CXString(CXConfig)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L182)

A `CXConfig` object that manages `str` values.

<a name="canvasxpress.config.type.CXString.value"></a>
#### value

```python
 | @property
 | value() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L192)

Provides the value for the configuration.

**Returns**:

`str`

<a name="canvasxpress.config.type.CXString.value"></a>
#### value

```python
 | @value.setter
 | value(value: Union[object, str]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L200)

Sets the value of the configuration.

**Arguments**:

    If `None` then an empty `str` will be used.
- `value`: `str`

<a name="canvasxpress.config.type.CXString.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(label: str, value: str)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L211)

Initializes the configuration with a `str` value.

<a name="canvasxpress.config.type.CXBool"></a>
## CXBool Objects

```python
class CXBool(CXConfig)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L219)

A `CXConfig` object that manages `bool` values.

<a name="canvasxpress.config.type.CXBool.value"></a>
#### value

```python
 | @property
 | value() -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L229)

Provides the value for the configuration.

**Returns**:

`bool`

<a name="canvasxpress.config.type.CXBool.value"></a>
#### value

```python
 | @value.setter
 | value(value: Union[object, bool]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L237)

Sets the value of the configuration.

**Arguments**:

    If `None` then `False` will be used.
- `value`: `bool`

<a name="canvasxpress.config.type.CXBool.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(label: str, value: bool)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L248)

Initializes the configuration with a `bool` value.

<a name="canvasxpress.config.type.CXBool.__str__"></a>
#### \_\_str\_\_

```python
 | __str__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L255)

*str* function.  Converts the object into a Javascript statement.

<a name="canvasxpress.config.type.CXBool.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L266)

*repr* function.  Converts the CXBool object into a pickle string
that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.config.type.CXFloat"></a>
## CXFloat Objects

```python
class CXFloat(CXConfig)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L278)

A `CXConfig` object that manages `float` values.

<a name="canvasxpress.config.type.CXFloat.value"></a>
#### value

```python
 | @property
 | value() -> float
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L288)

Provides the value for the configuration.

**Returns**:

`float`

<a name="canvasxpress.config.type.CXFloat.value"></a>
#### value

```python
 | @value.setter
 | value(value: Union[object, float]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L296)

Sets the value of the configuration.

**Arguments**:

    If `None` then `float(0.0)` will be used.
- `value`: `float`

<a name="canvasxpress.config.type.CXFloat.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(label: str, value: float)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L307)

Initializes the configuration with a `float` value.

<a name="canvasxpress.config.type.CXInt"></a>
## CXInt Objects

```python
class CXInt(CXConfig)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L317)

A `CXConfig` object that manages `int` values.

<a name="canvasxpress.config.type.CXInt.value"></a>
#### value

```python
 | @property
 | value() -> int
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L327)

Provides the value for the configuration.

**Returns**:

`int`

<a name="canvasxpress.config.type.CXInt.value"></a>
#### value

```python
 | @value.setter
 | value(value: Union[object, int]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L335)

Sets the value of the configuration.

**Arguments**:

    If `None` then `int(0)` will be used.
- `value`: `int`

<a name="canvasxpress.config.type.CXInt.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(label: str, value: int)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L346)

Initializes the configuration with an `int` value.

<a name="canvasxpress.config.type.CXDict"></a>
## CXDict Objects

```python
class CXDict(CXConfig)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L356)

A `CXConfig` object that manages `dict` values.

<a name="canvasxpress.config.type.CXDict.value"></a>
#### value

```python
 | @property
 | value() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L366)

Provides the value for the configuration.

**Returns**:

`dict`

<a name="canvasxpress.config.type.CXDict.value"></a>
#### value

```python
 | @value.setter
 | value(value: Union[dict, str, None]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L374)

Sets the value of the configuration.

**Arguments**:

    If `None` then `dict()` will be used.
- `value`: `dict`

<a name="canvasxpress.config.type.CXDict.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(label: str, value: Union[dict, str, None]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L393)

Initializes the CXData object with data.  Only dict or compatible data
types are accepted.

<a name="canvasxpress.config.type.CXDict.__lt__"></a>
#### \_\_lt\_\_

```python
 | __lt__(other: 'CXDict') -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L401)

*less than* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

    `CXDict` The object to compare.
- `other`: 

**Returns**:

`bool`

<a name="canvasxpress.config.type.CXDict.__eq__"></a>
#### \_\_eq\_\_

```python
 | __eq__(other: 'CXDict') -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L453)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L503)

*repr* function.  Converts the CXDict object into a pickle string
that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.config.type.CXList"></a>
## CXList Objects

```python
class CXList(CXConfig)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L512)

A `CXConfig` object that manages `list` values.

<a name="canvasxpress.config.type.CXList.value"></a>
#### value

```python
 | @property
 | value() -> list
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L522)

Provides the value for the configuration.

**Returns**:

`list`

<a name="canvasxpress.config.type.CXList.value"></a>
#### value

```python
 | @value.setter
 | value(value: Union[object, list]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L530)

Sets the value of the configuration.

**Arguments**:

    If `None` then `list()` will be used.
- `value`: `list`

<a name="canvasxpress.config.type.CXList.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(label: str, value: list)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L541)

Initializes the configuration with a `list` value.

<a name="canvasxpress.config.type.CXRGBAColor"></a>
## CXRGBAColor Objects

```python
class CXRGBAColor(CXDict)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L551)

A `CXConfig` object that manages `str` Javascript rgba() values.

<a name="canvasxpress.config.type.CXRGBAColor.is_color_str"></a>
#### is\_color\_str

```python
 | @staticmethod
 | is_color_str(value: str)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L557)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L598)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L636)

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
 | value(value: Union['CXRGBAColor', dict, list, str]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L680)

Sets the RGBA value from an existing `CXRGBAColor` object, or a `dict`,
`list`, or `string` following the Javascript `rgba()` format.

**Arguments**:

    The value to be accepted.  See the `is_color_*()` methods for
    acceptable formats.
- `value`: `Union['CXRGBAColor', dict, list, str]`

<a name="canvasxpress.config.type.CXRGBAColor.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(label: str, value: Union['CXRGBAColor', dict, list, str])
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L758)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L774)

*str* function.  Converts the object into a JSON string.

<a name="canvasxpress.config.type.CXRGBAColor.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L789)

*repr* function.  Converts the CXRGBAColor object into a pickle string
that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.config.type.CXRGBColor"></a>
## CXRGBColor Objects

```python
class CXRGBColor(CXDict)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L805)

A `CXConfig` object that manages `str` Javascript rgb() values.

<a name="canvasxpress.config.type.CXRGBColor.is_color_str"></a>
#### is\_color\_str

```python
 | @staticmethod
 | is_color_str(value: str)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L811)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L847)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L875)

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
 | value(value: Union['CXRGBColor', dict, list, str]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L913)

Sets the RGB value from an existing `CXRGBColor` object, or a `dict`,
`list`, or `string` following the Javascript `rgb()` format.

**Arguments**:

    The value to be accepted.  See the `is_color_*()` methods for
    acceptable formats.
- `value`: `Union['CXRGBColor', dict, list, str]`

<a name="canvasxpress.config.type.CXRGBColor.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(label: str, value: Union['CXRGBColor', dict, list, str])
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L987)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L1003)

*str* function.  Converts the object into a JSON string.

<a name="canvasxpress.config.type.CXRGBColor.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L1017)

*repr* function.  Converts the CXRGBColor object into a pickle string
that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.config.type.CXGraphTypeOptions"></a>
## CXGraphTypeOptions Objects

```python
class CXGraphTypeOptions(Enum)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L1032)

A set of known chart types permitted for use with CanvasXpress objects.  If
a chart not yet identified in this list is required then use a `CXString`
object with the label `graphType` and the value set to the name of the
chart to be used.

<a name="canvasxpress.config.type.CXGraphType"></a>
## CXGraphType Objects

```python
class CXGraphType(CXString)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L1091)

A CXString that is aware of CanvasXpress types of graphs, such as 'Bar'.

<a name="canvasxpress.config.type.CXGraphType.value"></a>
#### value

```python
 | @CXString.value.setter
 | value(value: Union[CXGraphTypeOptions, str]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L1099)

Sets the value using a known CanvasXpress option.

<a name="canvasxpress.config.type.CXGraphType.set_custom_value"></a>
#### set\_custom\_value

```python
 | set_custom_value(value: str)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L1115)

Permits a js value to be set, such as if a new option is recently
made available that the Python framework is yet to be aware of.

**Arguments**:

    The string value to set.
- `value`: `str`

<a name="canvasxpress.config.type.CXGraphType.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(type: Union[CXGraphTypeOptions, str] = CXGraphTypeOptions.Bar)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/type.py#L1124)

Initializes a new CXGraphType object with a value corresponding to one
of the values provided by `CXGraphTypeOptions`.

<a name="canvasxpress.config.collection"></a>
# canvasxpress.config.collection

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/collection.py#L1)

<a name="canvasxpress.config.collection.CXConfigs"></a>
## CXConfigs Objects

```python
@total_ordering
class CXConfigs(CXDictConvertable)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/collection.py#L12)

CXConfigs provides support for addressing a collection of `CXConfig` values.

<a name="canvasxpress.config.collection.CXConfigs.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(*configs: Union[CXConfig, tuple, dict])
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/collection.py#L22)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/collection.py#L43)

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
 | add(config: Union[CXConfig, tuple, dict]) -> 'CXConfigs'
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/collection.py#L61)

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

    The `CXConfig` to associate.  Cannot be `None`.
- `config`: `Union[CXConfig, tuple, dict]`

<a name="canvasxpress.config.collection.CXConfigs.get_param"></a>
#### get\_param

```python
 | get_param(label: str) -> Union[CXConfig, None]
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/collection.py#L106)

Provides the CXConfig with the indicated label.

**Arguments**:

    The name of the congig to find.
- `label`: `str`

**Returns**:

`Union[CXConfig, None]`

<a name="canvasxpress.config.collection.CXConfigs.set_param"></a>
#### set\_param

```python
 | set_param(label: str, value: Any) -> 'CXConfigs'
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/collection.py#L125)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/collection.py#L245)

Provides access to the list of associated `CXConfig` objects.

**Returns**:

`List[CXConfig]`

<a name="canvasxpress.config.collection.CXConfigs.render_to_dict"></a>
#### render\_to\_dict

```python
 | render_to_dict() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/collection.py#L252)

Provides a `dict` representation of the configuration values.

**Returns**:

`dict`

<a name="canvasxpress.config.collection.CXConfigs.merge_configs"></a>
#### merge\_configs

```python
 | @classmethod
 | merge_configs(cls, configs: List[CXConfig]) -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/collection.py#L282)

Given a list of CXConfig objects, a dictionary of unique attributes is
generated and provided.

**Returns**:

`dict`

<a name="canvasxpress.config.collection.CXConfigs.__copy__"></a>
#### \_\_copy\_\_

```python
 | __copy__() -> 'CXConfigs'
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/collection.py#L304)

*copy* constructor.  Returns the `CXConfig` objects within a new
`CXConfigs` object.

<a name="canvasxpress.config.collection.CXConfigs.__deepcopy__"></a>
#### \_\_deepcopy\_\_

```python
 | __deepcopy__(memo) -> 'CXConfigs'
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/collection.py#L313)

*deepcopy* constructor.  Returns a deepcopy of the `CXConfig` objects
 within a new `CXConfigs` object.

<a name="canvasxpress.config.collection.CXConfigs.__lt__"></a>
#### \_\_lt\_\_

```python
 | __lt__(other: 'CXConfigs') -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/collection.py#L325)

*less than* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

    `CXConfigs` The object to compare.
- `other`: 

**Returns**:

`bool`

<a name="canvasxpress.config.collection.CXConfigs.__eq__"></a>
#### \_\_eq\_\_

```python
 | __eq__(other: 'CXConfigs') -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/collection.py#L361)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/collection.py#L394)

*str* function.  Converts the `CXConfigs` object into a JSON
representation.
:returns" `str`
    JSON form of the collection.

<a name="canvasxpress.config.collection.CXConfigs.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/config/collection.py#L405)

*repr* function.  Converts the `CXConfigs` object into a pickle string
that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.js"></a>
# canvasxpress.js

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/js/__init__.py#L1)

The js package provides functionality for integrating custom Javascript with
CanvasXpress charts.

<a name="canvasxpress.js.collection"></a>
# canvasxpress.js.collection

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/js/collection.py#L1)

<a name="canvasxpress.js.collection.CXEvents"></a>
## CXEvents Objects

```python
@total_ordering
class CXEvents(CXJavascriptConvertable)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/js/collection.py#L11)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/js/collection.py#L44)

Provides a non-associated list of the associated CXEvents.

**Returns**:

`List[CXEvent]` A list of zero or more CXEvent objects.

<a name="canvasxpress.js.collection.CXEvents.has"></a>
#### has

```python
 | has(event: CXEvent) -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/js/collection.py#L51)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/js/collection.py#L62)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/js/collection.py#L89)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/js/collection.py#L109)

Provides a dict with each js properly formatted as JS within.

**Returns**:

`dict`

<a name="canvasxpress.js.collection.CXEvents.render_to_js"></a>
#### render\_to\_js

```python
 | render_to_js() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/js/collection.py#L135)

Converts the object into HTML5 complant script.

**Returns**:

'str'

<a name="canvasxpress.js.collection.CXEvents.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(*events)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/js/collection.py#L170)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/js/collection.py#L192)

*copy* constructor.  Returns the `CXEvent` objects within a new `CXEvents`
object.

<a name="canvasxpress.js.collection.CXEvents.__deepcopy__"></a>
#### \_\_deepcopy\_\_

```python
 | __deepcopy__(memo)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/js/collection.py#L201)

*deepcopy* constructor.  Returns a deep copy of `CXEvent` objects within
a new `CXEvents` object.

<a name="canvasxpress.js.collection.CXEvents.__lt__"></a>
#### \_\_lt\_\_

```python
 | __lt__(other: 'CXEvents')
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/js/collection.py#L213)

*less than* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

    `CXEvent` The object to compare.
- `other`: 

**Returns**:

`bool`

<a name="canvasxpress.js.collection.CXEvents.__eq__"></a>
#### \_\_eq\_\_

```python
 | __eq__(other: 'CXEvents')
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/js/collection.py#L249)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/js/collection.py#L282)

*str* function.  Converts the CXEvents object into a JSON list of
`CXEvent` objects also converted into JSON representations.
:returns" `str` JSON form of the collection.

<a name="canvasxpress.js.collection.CXEvents.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/js/collection.py#L292)

*repr* function.  Converts the CXEvents object into a pickle string
that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.js.function"></a>
# canvasxpress.js.function

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/js/function.py#L1)

<a name="canvasxpress.js.function.CXEvent"></a>
## CXEvent Objects

```python
@total_ordering
class CXEvent(CXJavascriptConvertable)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/js/function.py#L15)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/js/function.py#L71)

Provides access to the react ID.

**Returns**:

The ID as a string.

<a name="canvasxpress.js.function.CXEvent.id"></a>
#### id

```python
 | @id.setter
 | id(value: str) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/js/function.py#L79)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/js/function.py#L94)

Provides access to the react script.

**Returns**:

`str` The Javascript source.

<a name="canvasxpress.js.function.CXEvent.script"></a>
#### script

```python
 | @script.setter
 | script(value: str) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/js/function.py#L102)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/js/function.py#L129)

Converts the object into HTML5 complant script.

**Returns**:

'str'

<a name="canvasxpress.js.function.CXEvent.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(id: str = "", script: str = "")
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/js/function.py#L152)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/js/function.py#L169)

*copy* constructor.  Returns a new `CXEvent` object.

<a name="canvasxpress.js.function.CXEvent.__deepcopy__"></a>
#### \_\_deepcopy\_\_

```python
 | __deepcopy__(memo)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/js/function.py#L178)

*deepcopy* constructor.  Returns a new `CXEvent` object.

<a name="canvasxpress.js.function.CXEvent.__lt__"></a>
#### \_\_lt\_\_

```python
 | __lt__(other: 'CXEvent') -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/js/function.py#L190)

*less than* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

    `CXEvent` The object to compare.
- `other`: 

**Returns**:

`bool`

<a name="canvasxpress.js.function.CXEvent.__eq__"></a>
#### \_\_eq\_\_

```python
 | __eq__(other: 'CXEvent') -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/js/function.py#L220)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/js/function.py#L245)

*str* function.  Converts the object into a Javascript statement.

<a name="canvasxpress.js.function.CXEvent.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/js/function.py#L270)

*repr* function.  Converts the CXEvent object into a pickle string
that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.render"></a>
# canvasxpress.render

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/render/__init__.py#L1)

The render package provides functionality for rendering CanvasXpress objects in
containers or environments

<a name="canvasxpress.render.base"></a>
# canvasxpress.render.base

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/render/base.py#L1)

<a name="canvasxpress.render.base.CXRenderable"></a>
## CXRenderable Objects

```python
class CXRenderable(ABC)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/render/base.py#L6)

CXRenderable is capable of rendering a CanvasXpress object to some kind of
output or display device.

<a name="canvasxpress.render.base.CXRenderable.canvas"></a>
#### canvas

```python
 | @property
 | canvas() -> CanvasXpress
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/render/base.py#L18)

Provides the tracked CanvasXpress object.

**Returns**:

The `CanvasXpress` object if tracked, or `None` if not object

<a name="canvasxpress.render.base.CXRenderable.canvas"></a>
#### canvas

```python
 | @canvas.setter
 | canvas(value: CanvasXpress)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/render/base.py#L27)

Sets the CanvasXpress object to be tracked.
:praram value:
    The `CanvasXpress` object to be tracked.  Cannot be `None`.

<a name="canvasxpress.render.base.CXRenderable.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(cx: CanvasXpress)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/render/base.py#L42)

Initializes a new CXRenderable object.
:praram cx:
    The `CanvasXpress` object to be tracked.  See the `canvas`
    property, except that on initialization cx can be `None`.

<a name="canvasxpress.render.base.CXRenderable.render"></a>
#### render

```python
 | @abstractmethod
 | render()
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/render/base.py#L57)

Renders the associated CanvasXpress object appropriate to the render_to.
Not implemented.

<a name="canvasxpress.render.jupyter"></a>
# canvasxpress.render.jupyter

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/render/jupyter.py#L1)

<a name="canvasxpress.render.jupyter.CXNoteBook"></a>
## CXNoteBook Objects

```python
class CXNoteBook(CXRenderable)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/render/jupyter.py#L43)

CXNoteBook is a `CXRenderable` that renders `CanvasXpress` objects into
`IPython` containers (Jupyter Notebooks).

<a name="canvasxpress.render.jupyter.CXNoteBook.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(cx: CanvasXpress)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/render/jupyter.py#L49)

Initializes a new CXNoteBook object.
:praram cx:
    The `CanvasXpress` object to be tracked.  See the `canvas`
    property, except that on initialization cx can be `None`.

<a name="canvasxpress.render.jupyter.CXNoteBook.render"></a>
#### render

```python
 | render()
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/render/jupyter.py#L61)

Renders the associated CanvasXpress object appropriate for display in
an IPython (e.g., Jupyter NoteBook/Lab) environment.

<a name="canvasxpress.data"></a>
# canvasxpress.data

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/__init__.py#L1)

The data package provides functionality for integrating different kinds of data
structures and sources into a CanvasXpress object.  A balance is provided
between convenience functionality and reasonable external preparation, such as
what can be performed via `pandas`.

<a name="canvasxpress.data.matrix"></a>
# canvasxpress.data.matrix

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/matrix.py#L1)

<a name="canvasxpress.data.matrix.CXDataframeData"></a>
## CXDataframeData Objects

```python
@total_ordering
class CXDataframeData(CXMatrixData)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/matrix.py#L15)

A CXData class dedicated to processing Python DataFrame, matrix-structured
 data.

<a name="canvasxpress.data.matrix.CXDataframeData.dataframe"></a>
#### dataframe

```python
 | @property
 | dataframe() -> DataFrame
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/matrix.py#L27)

Provides the data managed by the object.

**Returns**:

`DataFrame` The managed data.

<a name="canvasxpress.data.matrix.CXDataframeData.dataframe"></a>
#### dataframe

```python
 | @dataframe.setter
 | dataframe(value: Union[DataFrame, None] = None) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/matrix.py#L35)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/matrix.py#L48)

Provides the data managed by the object.

**Returns**:

`DataFrame` The managed data.

<a name="canvasxpress.data.matrix.CXDataframeData.data"></a>
#### data

```python
 | @data.setter
 | data(value: Union['CXDataframeData', DataFrame, dict, str, None] = None) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/matrix.py#L56)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/matrix.py#L107)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/matrix.py#L123)

Provides a dict representation of the data.

**Returns**:

`dict`

<a name="canvasxpress.data.matrix.CXDataframeData.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(data: Union['CXDataframeData', DataFrame, dict, str, None] = None, profile: Union[CXDataProfile, None] = None) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/matrix.py#L140)

Initializes the CXData object with data.  Only `DataFrame` or compatible
data types are accepted.

**Arguments**:

    `None` to initialize with an empty `DataFrame`, or a `DataFrame`
    like object to assign mapped data.
    Omit to initialize with CXStandardProfile, or specify the desired
    profile object to facilitate transformation of data into a
    CanvasXpress JSON data object.  `None` to avoid use of a profile.
- `data`: `Union['CXDataframeData', DataFrame, dict, str, None]`
- `profile`: `Union[CXDataProfile, None]`

<a name="canvasxpress.data.matrix.CXDataframeData.__copy__"></a>
#### \_\_copy\_\_

```python
 | __copy__() -> 'CXDataframeData'
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/matrix.py#L159)

*copy constructor* that returns a copy of the CXDataframeData object.

**Returns**:

`CXDataframeData`

<a name="canvasxpress.data.matrix.CXDataframeData.__deepcopy__"></a>
#### \_\_deepcopy\_\_

```python
 | __deepcopy__(memo) -> 'CXDataframeData'
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/matrix.py#L167)

*deepcopy constructor* that returns a copy of the CXDataframeData object.

**Returns**:

`CXDataframeData` A copy of the wrapping object and deepcopy of

<a name="canvasxpress.data.matrix.CXDataframeData.__lt__"></a>
#### \_\_lt\_\_

```python
 | __lt__(other: 'CXDataframeData') -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/matrix.py#L178)

*less than* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

    `CXDataframeData` The object to compare.
- `other`: 

**Returns**:

`bool`

<a name="canvasxpress.data.matrix.CXDataframeData.__eq__"></a>
#### \_\_eq\_\_

```python
 | __eq__(other: 'CXDataframeData') -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/matrix.py#L220)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/matrix.py#L257)

*str* function.  Converts the CXDataframeData object into a JSON
representation.
:returns" `str` JSON form of the `CXDataframeData`.

<a name="canvasxpress.data.matrix.CXDataframeData.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/matrix.py#L265)

*repr* function.  Converts the CXDataframeData object into a pickle
string that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.data.matrix.CXCSVData"></a>
## CXCSVData Objects

```python
class CXCSVData(CXDataframeData)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/matrix.py#L281)

A CXData class dedicated to processing Python CSV-based, matrix-structured
 data.

<a name="canvasxpress.data.matrix.CXCSVData.csv"></a>
#### csv

```python
 | @property
 | csv() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/matrix.py#L288)

Provides the data managed by the object.

**Returns**:

`str` The managed data.

<a name="canvasxpress.data.matrix.CXCSVData.csv"></a>
#### csv

```python
 | @csv.setter
 | csv(value: str = None) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/matrix.py#L301)

Sets the CSV data managed by the object.

**Arguments**:

    `None` results in an empty CSV.  A deepcopy will be made of
    valid CSV `str` values.
- `value`: `str`

<a name="canvasxpress.data.matrix.CXCSVData.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(data: Union['CXCSVData', DataFrame, dict, str, None] = None, profile: Union[CXDataProfile, None] = None) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/matrix.py#L313)

Initializes the CXData object with data.  Only CSV `str` or compatible
data types are accepted.

**Arguments**:

    `None` to initialize with an empty CSV, or a CSV `str`
    like object to assign mapped data.
    Omit to initialize with CXStandardProfile, or specify the desired
    profile object to facilitate transformation of data into a
    CanvasXpress JSON data object.  `None` to avoid use of a profile.
- `data`: `Union['CXCSVData', DataFrame, dict, str, None]`
- `profile`: `Union[CXDataProfile, None]`

<a name="canvasxpress.data.matrix.CXCSVData.__str__"></a>
#### \_\_str\_\_

```python
 | __str__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/matrix.py#L331)

*str* function.  Converts the CXCSVData object into a JSON
representation.
:returns" `str` JSON form of the `CXCSVData`.

<a name="canvasxpress.data.matrix.CXCSVData.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/matrix.py#L339)

*repr* function.  Converts the CXCSVData object into a pickle
string that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.data.convert"></a>
# canvasxpress.data.convert

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/convert.py#L1)

<a name="canvasxpress.data.convert.CXHtmlConvertable"></a>
## CXHtmlConvertable Objects

```python
class CXHtmlConvertable(ABC)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/convert.py#L4)

CXHtmlConvertable represents an object that can be converted into HTML.

<a name="canvasxpress.data.convert.CXHtmlConvertable.render_to_html_parts"></a>
#### render\_to\_html\_parts

```python
 | @abstractmethod
 | render_to_html_parts() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/convert.py#L10)

Converts the object into HTML5 compliant script.

**Returns**:

`dict`

<a name="canvasxpress.data.convert.CXDictConvertable"></a>
## CXDictConvertable Objects

```python
class CXDictConvertable(ABC)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/convert.py#L21)

CXDictConvertable represents an object that can be converted into a dict.

<a name="canvasxpress.data.convert.CXDictConvertable.render_to_dict"></a>
#### render\_to\_dict

```python
 | @abstractmethod
 | render_to_dict(**kwargs) -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/convert.py#L27)

Converts the object into a dict representation.

**Arguments**:

    Keyword arguments that can be supplied to facilitate rendering
    decisions.
- `kwargs`: 

**Returns**:

`dict`

<a name="canvasxpress.data.convert.CXJavascriptConvertable"></a>
## CXJavascriptConvertable Objects

```python
class CXJavascriptConvertable(ABC)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/convert.py#L43)

CXJavascriptConvertable represents an object that can be converted into JS.

<a name="canvasxpress.data.convert.CXJavascriptConvertable.render_to_js"></a>
#### render\_to\_js

```python
 | @abstractmethod
 | render_to_js() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/convert.py#L49)

Converts the object into HTML5 complant script.

**Returns**:

`str`

<a name="canvasxpress.data.profile"></a>
# canvasxpress.data.profile

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/profile.py#L1)

<a name="canvasxpress.data.profile.CXStandardProfile"></a>
## CXStandardProfile Objects

```python
class CXStandardProfile(CXDataProfile)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/profile.py#L9)

`CXStandardProfile` provides standard chart data profile functionality,
by which the topics of `y`, `x`, and `z` are handled in conversions.

<a name="canvasxpress.data.profile.CXStandardProfile.vars"></a>
#### vars

```python
 | @property
 | vars() -> list
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/profile.py#L80)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/profile.py#L102)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/profile.py#L120)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/profile.py#L145)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/profile.py#L167)

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
 | x(value: Union[dict, None]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/profile.py#L213)

Sets the `x` attribute for the data, which corresponds to the
annotations for each `smps` element.  Quantities should match.
A deepcopy of the provided dict is made.

**Arguments**:

    A dict value of list attributes that should each contain one
    element per list for each `smps` element.  Provide `None` to
    reset the `x` attributes.
- `value`: `Union[dict, None]`

<a name="canvasxpress.data.profile.CXStandardProfile.z"></a>
#### z

```python
 | @z.setter
 | z(value: Union[dict, None]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/profile.py#L251)

Sets the `z` attribute for the data, which corresponds to the
annotations for each `vars` element.  Quantities should match.
A deepcopy of the provided dict is made.

**Arguments**:

    A dict value of list attributes that should each contain one
    element per list for each `vars` element.  Provide `None` to
    reset the `z` attributes.
- `value`: `Union[dict, None]`

<a name="canvasxpress.data.profile.CXStandardProfile.add_data_section"></a>
#### add\_data\_section

```python
 | add_data_section(section: str, source: dict, target: dict) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/profile.py#L284)

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
 | render_to_profiled_dict(data: CXData, match_vars_to_rows: bool = True, match_smps_to_cols: bool = True, match_x_to_smps: bool = True, match_z_to_vars: bool = True, **kwargs, ,) -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/profile.py#L319)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/profile.py#L614)

Initializes the CXStandardProfile object.

<a name="canvasxpress.data.profile.CXVennProfile"></a>
## CXVennProfile Objects

```python
class CXVennProfile(CXDataProfile)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/profile.py#L624)

`CXVennProfile` provides Venn diagram chart data profile functionality,
by which the topics of `venn` and `legend` are handled in conversions.

<a name="canvasxpress.data.profile.CXVennProfile.legend"></a>
#### legend

```python
 | @property
 | legend() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/profile.py#L636)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/profile.py#L647)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/profile.py#L668)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/profile.py#L835)

<a name="canvasxpress.data.profile.CXNetworkProfile.render_to_profiled_dict"></a>
#### render\_to\_profiled\_dict

```python
 | render_to_profiled_dict(data: CXData, **kwargs) -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/profile.py#L836)

Converts a given `CXData` instance into a dict suitable for use by
`CanvasXpress` when creating data instructions for the JS object.

*For matrix data:*<br>
TBD

*For key-pair data:*<br>
TBD

**Arguments**:

    The data object to introspect to create an enveloping profile.
- `data`: `CXData`

<a name="canvasxpress.data.profile.CXGenomeProfile"></a>
## CXGenomeProfile Objects

```python
class CXGenomeProfile(CXDataProfile)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/profile.py#L857)

<a name="canvasxpress.data.profile.CXGenomeProfile.render_to_profiled_dict"></a>
#### render\_to\_profiled\_dict

```python
 | render_to_profiled_dict(data: CXData, **kwargs) -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/profile.py#L858)

Converts a given `CXData` instance into a dict suitable for use by
`CanvasXpress` when creating data instructions for the JS object.

*For matrix data:*<br>
TBD

*For key-pair data:*<br>
TBD

**Arguments**:

    The data object to introspect to create an enveloping profile.
- `data`: `CXData`

<a name="canvasxpress.data.url"></a>
# canvasxpress.data.url

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/url.py#L1)

<a name="canvasxpress.data.url.CXUrlData"></a>
## CXUrlData Objects

```python
class CXUrlData(CXData)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/url.py#L6)

CXUrlData provides the ability to accept a URL and pass it properly to the
CanvasXpress object.

<a name="canvasxpress.data.url.CXUrlData.url"></a>
#### url

```python
 | @property
 | url() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/url.py#L18)

Provides the URL formatted as a string.

**Returns**:

`str`

<a name="canvasxpress.data.url.CXUrlData.url"></a>
#### url

```python
 | @url.setter
 | url(url: str) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/url.py#L28)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/url.py#L40)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/url.py#L52)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/url.py#L74)

"
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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/url.py#L88)

Converts the object into a dict representation.

**Returns**:

`dict`

<a name="canvasxpress.data.url.CXUrlData.validate_url"></a>
#### validate\_url

```python
 | @classmethod
 | validate_url(cls, url: str, detail_errors: bool = True) -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/url.py#L101)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/url.py#L135)

Initializes the CXUrlData object with a valid URL.  URLs must begin with
a valid scheme such as `file://` or `http://`.  `ValueError` will be
raised if the URL is malformed.

**Arguments**:

    A string form of the URL, which must be in a stanard format for
    files, http resources, ftp resources, etc.
- `data`: `str`

<a name="canvasxpress.data.keypair"></a>
# canvasxpress.data.keypair

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/keypair.py#L1)

<a name="canvasxpress.data.keypair.CXDictData"></a>
## CXDictData Objects

```python
@total_ordering
class CXDictData(CXKeyPairData)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/keypair.py#L14)

A CXData class dedicated to processing Python dict-structured data.

<a name="canvasxpress.data.keypair.CXDictData.data"></a>
#### data

```python
 | @property
 | data() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/keypair.py#L25)

Provides a reference to the dict tracked by the object.

**Returns**:

`dict`

<a name="canvasxpress.data.keypair.CXDictData.data"></a>
#### data

```python
 | @data.setter
 | data(value: dict) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/keypair.py#L34)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/keypair.py#L54)

"
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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/keypair.py#L70)

Provides a dict representation of the data.

**Returns**:

`dict`

<a name="canvasxpress.data.keypair.CXDictData.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(data: Union[dict, None] = None, profile: Union[CXDataProfile, None] = None) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/keypair.py#L87)

Initializes the CXData object with data.  Only dict or compatible data
types are accepted.

**Arguments**:

    `None` to initialize with an empty dictionary, or a `dict`-like
    object to assign mapped data.
    Omit to initialize with CXStandardProfile, or specify the desired
    profile object to facilitate transformation of data into a
    CanvasXpress JSON data object.  `None` to avoid use of a profile.
- `data`: `Union[dict, None]`
- `profile`: `Union[CXDataProfile, None]`

<a name="canvasxpress.data.keypair.CXDictData.__copy__"></a>
#### \_\_copy\_\_

```python
 | __copy__() -> 'CXDictData'
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/keypair.py#L106)

*copy constructor* that returns a copy of the CXDictData object.

**Returns**:

`CXDictData` A copy of the wrapping object.

<a name="canvasxpress.data.keypair.CXDictData.__deepcopy__"></a>
#### \_\_deepcopy\_\_

```python
 | __deepcopy__(memo) -> 'CXDictData'
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/keypair.py#L113)

*deepcopy constructor* that returns a copy of the CXDictData object.

**Returns**:

`CXDictData` A copy of the wrapping object and deepcopy of

<a name="canvasxpress.data.keypair.CXDictData.__lt__"></a>
#### \_\_lt\_\_

```python
 | __lt__(other: 'CXDictData') -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/keypair.py#L126)

*less than* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

    `CXDictData` The object to compare.
- `other`: 

**Returns**:

`bool`

<a name="canvasxpress.data.keypair.CXDictData.__eq__"></a>
#### \_\_eq\_\_

```python
 | __eq__(other: 'CXDictData') -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/keypair.py#L173)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/keypair.py#L218)

*str* function.  Converts the CXDictData object into a JSON
representation.
:returns" `str` JSON form of the `CXDictData`.

<a name="canvasxpress.data.keypair.CXDictData.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/keypair.py#L226)

*repr* function.  Converts the CXDictData object into a pickle string
that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.data.keypair.CXJSONData"></a>
## CXJSONData Objects

```python
class CXJSONData(CXDictData)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/keypair.py#L235)

A CXData class dedicated to processing JSON data.

<a name="canvasxpress.data.keypair.CXJSONData.json"></a>
#### json

```python
 | @property
 | json() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/keypair.py#L241)

Provides a copy of the JSON tracked by the object.

**Returns**:

`str`

<a name="canvasxpress.data.keypair.CXJSONData.json"></a>
#### json

```python
 | @json.setter
 | json(value: Union[dict, str]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/keypair.py#L250)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/keypair.py#L286)

Initializes the CXData object with data.  Only dict or compatible data
types are accepted.

**Arguments**:

    `None` to initialize with an empty JSON, or a JSON/`dict`-like
    object to assign mapped data.
    Omit to initialize with CXStandardProfile, or specify the desired
    profile object to facilitate transformation of data into a
    CanvasXpress JSON data object.  `None` to avoid use of a profile.
- `data`: `Union[dict, str, None]`
- `profile`: `Union[CXDataProfile, None]`

<a name="canvasxpress.data.keypair.CXJSONData.__copy__"></a>
#### \_\_copy\_\_

```python
 | __copy__() -> 'CXJSONData'
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/keypair.py#L304)

*copy constructor* that returns a copy of the CXDictData objct.

**Returns**:

`CXDictData` A copy of the wrapping object.

<a name="canvasxpress.data.keypair.CXJSONData.__deepcopy__"></a>
#### \_\_deepcopy\_\_

```python
 | __deepcopy__(memo) -> 'CXJSONData'
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/keypair.py#L311)

*deepcopy constructor* that returns a copy of the CXJSONData object.

**Returns**:

`CXJSONData` A copy of the wrapping object and deepcopy of

<a name="canvasxpress.data.keypair.CXJSONData.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/keypair.py#L322)

*repr* function.  Converts the CXJSONData object into a pickle string
that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.data.base"></a>
# canvasxpress.data.base

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/base.py#L1)

<a name="canvasxpress.data.base.CXData"></a>
## CXData Objects

```python
class CXData(CXDictConvertable)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/base.py#L18)

CXData defines an essential data class for managing data acquisiton,
transformation, and introspection as required by the `CanvasXPress` class.

<a name="canvasxpress.data.base.CXData.data"></a>
#### data

```python
 | @property
 | @abstractmethod
 | data() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/base.py#L26)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/base.py#L37)

"
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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/base.py#L50)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/base.py#L60)

CXDataProfileException is used by CXDataProfile to describe validation
errors when considering CXData objects in the context of CXDataProfile
objects.

<a name="canvasxpress.data.base.CXDataProfile"></a>
## CXDataProfile Objects

```python
class CXDataProfile(ABC)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/base.py#L69)

CXDataProfile assists with CXData translations into CanvasXpress JSON data
formats, such as documented at
[CanvasXpress.org](https://www.canvasxpress.org/docs.html#data).

<a name="canvasxpress.data.base.CXDataProfile.render_to_profiled_dict"></a>
#### render\_to\_profiled\_dict

```python
 | @abstractmethod
 | render_to_profiled_dict(data: CXData, **kwargs) -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/base.py#L77)

Converts a given `CXData` instance into a dict suitable for use by
`CanvasXpress` when creating data instructions for the JS object.

<a name="canvasxpress.data.base.CXProfiledData"></a>
## CXProfiledData Objects

```python
class CXProfiledData(CXData)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/base.py#L89)

CXData defines an essential data class for managing data acquisiton,
transformation, and introspection as required by the `CanvasXPress` class.

<a name="canvasxpress.data.base.CXProfiledData.profile"></a>
#### profile

```python
 | @property
 | profile() -> Union[None, CXDataProfile]
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/base.py#L102)

Provides the `CXDataProfile` associated with the `CXData` instance.

**Returns**:

`Union[None, CXDataProfile]`

<a name="canvasxpress.data.base.CXProfiledData.profile"></a>
#### profile

```python
 | @profile.setter
 | profile(profile: Union[None, CXDataProfile]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/base.py#L111)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/base.py#L133)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/base.py#L143)

Initializes the CXData object with data.

**Arguments**:

    Given an object or no data prepares a new CXData instance ready for
    use by a `CanvasXpress` object.
    `None` to initialize with CXStandardProfile, or specify the desired
    profile object to facilitate transformation of data into a
    CanvasXpress JSON data object.
- `data`: `Union[object, None]`
- `profile`: `Union[CXDataProfile, None]`

<a name="canvasxpress.data.base.CXKeyPairData"></a>
## CXKeyPairData Objects

```python
class CXKeyPairData(CXProfiledData)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/base.py#L161)

CXKeyPairData is a marker class to indicate that the data managed will be
generally of the structure key-pair.  A `dict` is an example of key-pair
data.

<a name="canvasxpress.data.base.CXMatrixData"></a>
## CXMatrixData Objects

```python
class CXMatrixData(CXProfiledData)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/data/base.py#L170)

CXMatrixData is a marker class to indicate that the data management will be
generally of the structure matrix or tabular.  A spreadsheet is an example
of matrix data.

<a name="canvasxpress.canvas"></a>
# canvasxpress.canvas

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/canvas.py#L1)

<a name="canvasxpress.canvas.CanvasXpress"></a>
## CanvasXpress Objects

```python
class CanvasXpress(CXHtmlConvertable)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/canvas.py#L32)

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

<a name="canvasxpress.canvas.CanvasXpress.render_to"></a>
#### render\_to

```python
 | @property
 | render_to() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/canvas.py#L74)

The ID of the CanvasXpress object's associated HTML components, such as
the render canvas element.  Sets the `id` attribute of the `<canvas>`
element.

**Returns**:

`str` The ID

<a name="canvasxpress.canvas.CanvasXpress.render_to"></a>
#### render\_to

```python
 | @render_to.setter
 | render_to(value: str) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/canvas.py#L84)

Sets the render_to of the CanvasXpress instance.  Sets the `id`
attribute of the `<canvas>` element.

**Arguments**:

    `str` The ID to be associated.  Cannot be `None`, and
    must be alphanumeric.
- `value`: 

<a name="canvasxpress.canvas.CanvasXpress.license_available"></a>
#### license\_available

```python
 | @property
 | license_available() -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/canvas.py#L110)

Indicates if a license is associated with the CanvasXpress object.

**Returns**:

`True` if a license file URL has been set.

<a name="canvasxpress.canvas.CanvasXpress.license_url"></a>
#### license\_url

```python
 | @property
 | license_url() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/canvas.py#L118)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/canvas.py#L127)

Sets the location of the license file to be associated with the
CanvasXpress object.

**Arguments**:

    `str` The path to the license file or `None` if a previously set URL
    is no longer valid.
- `value`: 

<a name="canvasxpress.canvas.CanvasXpress.CHART_WIDTH_DEFAULT"></a>
#### CHART\_WIDTH\_DEFAULT

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/canvas.py#L147)

Default width of the chart when rendered, such as into HTML.

<a name="canvasxpress.canvas.CanvasXpress.element_width"></a>
#### element\_width

```python
 | @property
 | @deprecated(
 |         reason="As part of improved alignment with CanvasXpress for JS, use the"
 |                " width property instead."
 |     )
 | element_width() -> int
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/canvas.py#L162)

DEPRECATED - USE  `width`

<a name="canvasxpress.canvas.CanvasXpress.element_width"></a>
#### element\_width

```python
 | @element_width.setter
 | @deprecated(
 |         reason="As part of improved alignment with CanvasXpress for JS, use the"
 |                " width property instead."
 |     )
 | element_width(value: int)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/canvas.py#L173)

DEPRECATED - USE  `width`

<a name="canvasxpress.canvas.CanvasXpress.width"></a>
#### width

```python
 | @property
 | width() -> int
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/canvas.py#L180)

Indicates the preferred <canvas> Web element width when rendered.  This
property is used to facilitate integration with Web containers such
as Jupyter notebooks. Added to the `<canvas>` element, and also
influences render containers for contexts such as Jupyter Notebooks.

**Returns**:

`int` The width

<a name="canvasxpress.canvas.CanvasXpress.width"></a>
#### width

```python
 | @width.setter
 | width(value: int)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/canvas.py#L191)

Sets the preferred Web element width when rendered. Added to the
`<canvas>` element, and also influences render containers for contexts
such as Jupyter Notebooks.

**Arguments**:

    The pixel count.  Cannot be `None` or less than `1`.
- `value`: `int`

<a name="canvasxpress.canvas.CanvasXpress.CHART_HEIGHT_DEFAULT"></a>
#### CHART\_HEIGHT\_DEFAULT

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/canvas.py#L211)

Default height of the chart in pixels when rendered, such as into HTML.

<a name="canvasxpress.canvas.CanvasXpress.element_height"></a>
#### element\_height

```python
 | @property
 | @deprecated(
 |         reason="As part of improved alignment with CanvasXpress for JS, use the"
 |                " height property instead."
 |     )
 | element_height() -> int
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/canvas.py#L226)

DEPRECATED - USE `height`

<a name="canvasxpress.canvas.CanvasXpress.element_height"></a>
#### element\_height

```python
 | @element_height.setter
 | @deprecated(
 |         reason="As part of improved alignment with CanvasXpress for JS, use the"
 |                " height property instead."
 |     )
 | element_height(value: int)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/canvas.py#L237)

DEPRECATED - USE `height`

<a name="canvasxpress.canvas.CanvasXpress.height"></a>
#### height

```python
 | @property
 | height() -> int
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/canvas.py#L244)

Indicates the preferred Web element height when rendered.  This
property is used to facilitate integration with Web containers such
as Jupyter notebooks.  Added to the `<canvas>` element, and also
influences render containers for contexts such as Jupyter Notebooks.

**Returns**:

`int` The pixel count

<a name="canvasxpress.canvas.CanvasXpress.height"></a>
#### height

```python
 | @height.setter
 | height(value: int)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/canvas.py#L255)

Sets the preferred Web element height when rendered.  Added to the
`<canvas>` element, and also influences render containers for contexts
such as Jupyter Notebooks.

**Arguments**:

- `value`: `int`

<a name="canvasxpress.canvas.CanvasXpress.data"></a>
#### data

```python
 | @property
 | data() -> CXData
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/canvas.py#L282)

Provides access to the CXData associated with this CanvasXpress chart.

**Returns**:

`CXData` The data to be associated with the chart.

<a name="canvasxpress.canvas.CanvasXpress.data"></a>
#### data

```python
 | @data.setter
 | data(value: Union[CXData, dict, None]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/canvas.py#L290)

Sets the CXData associated with this CanvasXpress chart.

**Arguments**:

    `CXData, dict, None` An object translatable into a CXData type.
    If the object is an instance of CXData then it will be tracked
    by the CanvasXpress object; otherwise, a new CXData object will
    be created to manage the content.
- `value`: 

<a name="canvasxpress.canvas.CanvasXpress.events"></a>
#### events

```python
 | @property
 | events() -> CXEvents
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/canvas.py#L317)

Provides access to the CXEvents associated with this CanvasXpress chart.

**Returns**:

`CXEvents` The events to be associated with the chart.

<a name="canvasxpress.canvas.CanvasXpress.events"></a>
#### events

```python
 | @events.setter
 | events(events: Union[CXEvents, List[CXEvent], None]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/canvas.py#L325)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/canvas.py#L352)

Provides access to the CXConfigs associated with this CanvasXpress chart.

**Returns**:

`CXConfigs` The config to be associated with the chart.

<a name="canvasxpress.canvas.CanvasXpress.config"></a>
#### config

```python
 | @config.setter
 | config(value: Union[
 |                 List[CXConfig], List[tuple], dict, CXConfigs, CXConfigs
 |             ])
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/canvas.py#L360)

Sets the CXConfigs associated with this CanvasXpress chart.

**Arguments**:

    An object translatable into a CXConfigs
    type.  If the object is an instance of CXConfigs then it will be
    tracked by the CanvasXpress object; otherwise, a new CXConfigs
    object will be created to manage the content.
- `value`: `Union[List[CXConfig], List[tuple], dict, CXConfigs, CXConfigs]`

<a name="canvasxpress.canvas.CanvasXpress.canvas"></a>
#### canvas

```python
 | @property
 | canvas() -> CXConfigs
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/canvas.py#L398)

Provides access to the attributes to be used with the `<canvas>`
element generated by this object.  Each element is tracked as a CXConfig
object.  Note that `id`, `width`, and `height` are uniquely set using
the respective `id`, `width`, and `height` properties of this
`CanvasXpress` object due to their mandatory nature.

**Returns**:

`CXConfigs`

<a name="canvasxpress.canvas.CanvasXpress.canvas"></a>
#### canvas

```python
 | @canvas.setter
 | canvas(value: Union[
 |                 List[CXConfig], List[tuple], dict, CXConfigs, CXConfigs
 |             ])
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/canvas.py#L412)

Sets the attributes to be incorporated into the `<canvas>` element
generated by this object.  Each element is tracked as a CXConfig
object. <br><br>
Note that `id`, `width`, and `height` are uniquely set using
the respective `id`, `width`, and `height` properties of this
`CanvasXpress` object due to their mandatory nature, and values for such
will not be kept in the `canvas` configs.

**Arguments**:

    An object translatable into a CXConfigs
    type.  If the object is an instance of CXConfigs then it will be
    tracked by the CanvasXpress object; otherwise, a new CXConfigs
    object will be created to manage the content.
- `value`: `Union[List[CXConfig], List[tuple], dict, CXConfigs, CXConfigs]`

<a name="canvasxpress.canvas.CanvasXpress.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(render_to: str = None, data: Union[CXData, dict] = None, events: Union[List[CXEvent], CXEvents] = None, config: Union[List[CXConfig], List[tuple], dict, CXConfigs] = None, canvas: Union[List[CXConfig], List[tuple], dict, CXConfigs] = None, width: int = CHART_WIDTH_DEFAULT, height: int = CHART_HEIGHT_DEFAULT) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/canvas.py#L456)

Initializes a new CanvasXpress object.  Default values are provided for
all parameters if values are not specified; otherwise the arguments are
treated as if an appropriate setter were used.

**Arguments**:

    initialization the object will be assigned an UUID4 value.
- `render_to`: See `render_to` property, except that on default
- `data`: See the `data` property
- `events`: See the `events` property
- `config`: See the `config` property
- `canvas`: See the 'canvas` property
- `width`: See the `width` property
- `height`: See the `height` property

<a name="canvasxpress.canvas.CanvasXpress.render_to_html_parts"></a>
#### render\_to\_html\_parts

```python
 | render_to_html_parts() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/2c6009ef51d5ee562b1ab9c1d20b4e33aed0785d/canvasxpress/canvas.py#L495)

Converts the CanvasXpress object into HTML5 complant script.

If the associated `CXData` is a type of `CXProfiledData` and a profile
has yet to be assigned then a profile is assigned according to the
`CXConfig` labelled `graphType`.

**Returns**:

`dict` A map of values appropriate for use in HTML, such as

