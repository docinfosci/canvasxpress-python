<a name="canvasxpress"></a>
# canvasxpress

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/__init__.py#L1)

The CanvasXpress package provides Python friendly management of the Javascript-
based [CanvasXpress](https://www.canvasxpress.org) library.  For an overview
and detailed instructions about CanvasXpress specifically please visit the site.

<a name="canvasxpress.util"></a>
# canvasxpress.util

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/util/__init__.py#L2)

<a name="canvasxpress.util.template"></a>
# canvasxpress.util.template

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/util/template.py#L1)

<a name="canvasxpress.util.template.render_from_template"></a>
#### render\_from\_template

```python
render_from_template(template: str, data: dict) -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/util/template.py#L1)

Updates the template text with the provided data.

**Arguments**:

- `template`: `str` The name of the template file
- `data`: The `dict` of str values with which to update the template text
:returns The adjusted template text

<a name="canvasxpress.config"></a>
# canvasxpress.config

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/__init__.py#L1)

The config package provides functionality for managing or assigning
configuration values associated with CanvasXpress objects.

<a name="canvasxpress.config.type"></a>
# canvasxpress.config.type

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L1)

<a name="canvasxpress.config.type.CXConfig"></a>
## CXConfig Objects

```python
@total_ordering
class CXConfig(ABC)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L12)

CXConfig provides the means by which CanvasXpress objects can be configured for
customized rendering and interaction.

<a name="canvasxpress.config.type.CXConfig.label"></a>
#### label

```python
 | @property
 | label() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L24)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L33)

Provides the value for the configuration.  Must be implemented by
concrete classes.

**Returns**:

`Any`
    The relevant type of value.

<a name="canvasxpress.config.type.CXConfig.value"></a>
#### value

```python
 | @value.setter
 | @abstractmethod
 | value(value: Any) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L44)

Sets the value of the configuration.  Must be implemented by concrete
classes.

**Arguments**:

- `value`: `Any`
    The value to be accepted.  Will be more specific with concrete
    implementations, such as `str` for string configurations.

<a name="canvasxpress.config.type.CXConfig.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(label: str, value: Any)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L54)

Initializes a new CXConfig object with a label and value.

**Arguments**:

- `label`: `str`
    The label for the configuration.
- `value`: `Any`
    The value for the configuration.  See the `value` property for the
    concrete implementation for allowed types.

<a name="canvasxpress.config.type.CXConfig.__copy__"></a>
#### \_\_copy\_\_

```python
 | __copy__() -> 'CXConfig'
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L71)

*copy constructor* that provides a new CXConfig of the same type with
the data referenced.

**Returns**:

`CXConfig` of the proper type

<a name="canvasxpress.config.type.CXConfig.__deepcopy__"></a>
#### \_\_deepcopy\_\_

```python
 | __deepcopy__(memo)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L82)

*deepcopy constructor* that provides a new CXConfig of the same type with
the a deepcopy of the data.

**Returns**:

`CXConfig` of the proper type

<a name="canvasxpress.config.type.CXConfig.__hash__"></a>
#### \_\_hash\_\_

```python
 | __hash__() -> int
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L96)

Provides a hash proxy for the object as converted into its `repr` form.

**Returns**:

`int`

<a name="canvasxpress.config.type.CXConfig.__lt__"></a>
#### \_\_lt\_\_

```python
 | __lt__(other: 'CXConfig') -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L103)

*less than* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

- `other`: 
    `CXConfig` The object to compare.

**Returns**:

`bool`
    <ul>
    <li> If `other` is `None` then `False`
    <li> If `other` is not a `CXConfig` object then `False`
    <li> If `other` is a `CXConfig` object then True if label and value
        of `other` are less than that of `self`.
    </ul>

<a name="canvasxpress.config.type.CXConfig.__eq__"></a>
#### \_\_eq\_\_

```python
 | __eq__(other: 'CXConfig') -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L135)

*equals* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

- `other`: 
    `CXConfig` The object to compare.

**Returns**:

`bool`
    <ul>
    <li> If `other` is `None` then `False`
    <li> If `other` is not a `CXConfig` object then `False`
    <li> If `other` is a `CXConfig` object then True if label and value
        of `other` are equal to that of `self`.
    </ul>

<a name="canvasxpress.config.type.CXConfig.__str__"></a>
#### \_\_str\_\_

```python
 | __str__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L159)

*str* function.  Converts the object into a JSON string.

<a name="canvasxpress.config.type.CXConfig.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L170)

*repr* function.  Converts the CXConfig object into a pickle string
that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.config.type.CXString"></a>
## CXString Objects

```python
class CXString(CXConfig)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L182)

A `CXConfig` object that manages `str` values.

<a name="canvasxpress.config.type.CXString.value"></a>
#### value

```python
 | @property
 | value() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L192)

Provides the value for the configuration.

**Returns**:

`str`

<a name="canvasxpress.config.type.CXString.value"></a>
#### value

```python
 | @value.setter
 | value(value: Union[object, str]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L200)

Sets the value of the configuration.

**Arguments**:

- `value`: `str`
    If `None` then an empty `str` will be used.

<a name="canvasxpress.config.type.CXString.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(label: str, value: str)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L211)

Initializes the configuration with a `str` value.

<a name="canvasxpress.config.type.CXBool"></a>
## CXBool Objects

```python
class CXBool(CXConfig)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L219)

A `CXConfig` object that manages `bool` values.

<a name="canvasxpress.config.type.CXBool.value"></a>
#### value

```python
 | @property
 | value() -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L229)

Provides the value for the configuration.

**Returns**:

`bool`

<a name="canvasxpress.config.type.CXBool.value"></a>
#### value

```python
 | @value.setter
 | value(value: Union[object, bool]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L237)

Sets the value of the configuration.

**Arguments**:

- `value`: `bool`
    If `None` then `False` will be used.

<a name="canvasxpress.config.type.CXBool.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(label: str, value: bool)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L248)

Initializes the configuration with a `bool` value.

<a name="canvasxpress.config.type.CXBool.__str__"></a>
#### \_\_str\_\_

```python
 | __str__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L255)

*str* function.  Converts the object into a Javascript statement.

<a name="canvasxpress.config.type.CXBool.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L266)

*repr* function.  Converts the CXBool object into a pickle string
that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.config.type.CXFloat"></a>
## CXFloat Objects

```python
class CXFloat(CXConfig)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L278)

A `CXConfig` object that manages `float` values.

<a name="canvasxpress.config.type.CXFloat.value"></a>
#### value

```python
 | @property
 | value() -> float
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L288)

Provides the value for the configuration.

**Returns**:

`float`

<a name="canvasxpress.config.type.CXFloat.value"></a>
#### value

```python
 | @value.setter
 | value(value: Union[object, float]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L296)

Sets the value of the configuration.

**Arguments**:

- `value`: `float`
    If `None` then `float(0.0)` will be used.

<a name="canvasxpress.config.type.CXFloat.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(label: str, value: float)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L307)

Initializes the configuration with a `float` value.

<a name="canvasxpress.config.type.CXInt"></a>
## CXInt Objects

```python
class CXInt(CXConfig)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L317)

A `CXConfig` object that manages `int` values.

<a name="canvasxpress.config.type.CXInt.value"></a>
#### value

```python
 | @property
 | value() -> int
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L327)

Provides the value for the configuration.

**Returns**:

`int`

<a name="canvasxpress.config.type.CXInt.value"></a>
#### value

```python
 | @value.setter
 | value(value: Union[object, int]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L335)

Sets the value of the configuration.

**Arguments**:

- `value`: `int`
    If `None` then `int(0)` will be used.

<a name="canvasxpress.config.type.CXInt.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(label: str, value: int)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L346)

Initializes the configuration with an `int` value.

<a name="canvasxpress.config.type.CXDict"></a>
## CXDict Objects

```python
class CXDict(CXConfig)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L356)

A `CXConfig` object that manages `dict` values.

<a name="canvasxpress.config.type.CXDict.value"></a>
#### value

```python
 | @property
 | value() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L366)

Provides the value for the configuration.

**Returns**:

`dict`

<a name="canvasxpress.config.type.CXDict.value"></a>
#### value

```python
 | @value.setter
 | value(value: Union[dict, str, None]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L374)

Sets the value of the configuration.

**Arguments**:

- `value`: `dict`
    If `None` then `dict()` will be used.

<a name="canvasxpress.config.type.CXDict.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(label: str, value: Union[dict, str, None]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L393)

Initializes the CXData object with data.  Only dict or compatible data
types are accepted.

<a name="canvasxpress.config.type.CXDict.__lt__"></a>
#### \_\_lt\_\_

```python
 | __lt__(other: 'CXDict') -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L401)

*less than* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

- `other`: 
    `CXDict` The object to compare.

**Returns**:

`bool`
    <ul>
    <li> If `other` is `None` then `False`
    <li> If `other` is not a `CXDict` object then `False`
    <li> If `other` is a `CXDict` object then True if the label and
        value parts are less than that of self.
    </ul>

<a name="canvasxpress.config.type.CXDict.__eq__"></a>
#### \_\_eq\_\_

```python
 | __eq__(other: 'CXDict') -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L453)

*equals* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

- `other`: 
    `CXDict` The object to compare.

**Returns**:

`bool`
    <ul>
    <li> If `other` is `None` then `False`
    <li> If `other` is not a `CXDict` object then `False`
    <li> If `other` is a `CXDict` object then True if the label and
        value parts are equal to that of self.
    </ul>

<a name="canvasxpress.config.type.CXDict.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L503)

*repr* function.  Converts the CXDict object into a pickle string
that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.config.type.CXList"></a>
## CXList Objects

```python
class CXList(CXConfig)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L512)

A `CXConfig` object that manages `list` values.

<a name="canvasxpress.config.type.CXList.value"></a>
#### value

```python
 | @property
 | value() -> list
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L522)

Provides the value for the configuration.

**Returns**:

`list`

<a name="canvasxpress.config.type.CXList.value"></a>
#### value

```python
 | @value.setter
 | value(value: Union[object, list]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L530)

Sets the value of the configuration.

**Arguments**:

- `value`: `list`
    If `None` then `list()` will be used.

<a name="canvasxpress.config.type.CXList.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(label: str, value: list)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L541)

Initializes the configuration with a `list` value.

<a name="canvasxpress.config.type.CXRGBAColor"></a>
## CXRGBAColor Objects

```python
class CXRGBAColor(CXDict)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L551)

A `CXConfig` object that manages `str` Javascript rgba() values.

<a name="canvasxpress.config.type.CXRGBAColor.is_color_str"></a>
#### is\_color\_str

```python
 | @staticmethod
 | is_color_str(value: str)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L557)

A static method that evaluates a given string to see if it represents a
Javascript rgba() statement.

**Arguments**:

- `value`: `str`
    A string to evaluate.  A valid Javascript value has the form
    `rgba(r, g, b, a)` where RGB values are `int` from 0-255 and A is a
    `float` from 0.0 to 1.0.

**Returns**:

`bool`
    True if the string represents a Javascript rgba() statement.

<a name="canvasxpress.config.type.CXRGBAColor.is_color_list"></a>
#### is\_color\_list

```python
 | @staticmethod
 | is_color_list(value: list)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L598)

A static method that evaluates a given list to see if it represents a
Javascript rgba() statement.

**Arguments**:

- `value`: `list`
    A list to evaluate.  A valid Javascript value has the form
    `rgba(r, g, b, a)` where RGB values are `int` from 0-255 and A is a
    `float` from 0.0 to 1.0.

**Returns**:

`bool`
    True if the list represents a Javascript rgba() statement.

<a name="canvasxpress.config.type.CXRGBAColor.is_color_dict"></a>
#### is\_color\_dict

```python
 | @staticmethod
 | is_color_dict(value: dict)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L636)

A static method that evaluates a given dict to see if it represents a
Javascript rgba() statement.

**Arguments**:

- `value`: `dict`
    A dict to evaluate.  A valid Javascript value has the form
    `rgba(r, g, b, a)` where RGB values are `int` from 0-255 and A is a
    `float` from 0.0 to 1.0.  For the dict to be valid its keys must be
    lower case r, g, b, and a characters.

**Returns**:

`bool`
    True if the dict represents a Javascript rgba() statement.

<a name="canvasxpress.config.type.CXRGBAColor.value"></a>
#### value

```python
 | @CXDict.value.setter
 | value(value: Union['CXRGBAColor', dict, list, str]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L680)

Sets the RGBA value from an existing `CXRGBAColor` object, or a `dict`,
`list`, or `string` following the Javascript `rgba()` format.

**Arguments**:

- `value`: `Union['CXRGBAColor', dict, list, str]`
    The value to be accepted.  See the `is_color_*()` methods for
    acceptable formats.

<a name="canvasxpress.config.type.CXRGBAColor.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(label: str, value: Union['CXRGBAColor', dict, list, str])
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L758)

Initializes a new CXRGBAColor object using the RGBA value from an
existing `CXRGBAColor` object, or a `dict`, `list`, or `string`
following the Javascript `rgba()` format.

**Arguments**:

- `value`: `Union['CXRGBAColor', dict, list, str]`
    The value to be accepted.  See the `is_color_*()` methods for
    acceptable formats.

<a name="canvasxpress.config.type.CXRGBAColor.__str__"></a>
#### \_\_str\_\_

```python
 | __str__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L774)

*str* function.  Converts the object into a JSON string.

<a name="canvasxpress.config.type.CXRGBAColor.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L789)

*repr* function.  Converts the CXRGBAColor object into a pickle string
that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.config.type.CXRGBColor"></a>
## CXRGBColor Objects

```python
class CXRGBColor(CXDict)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L805)

A `CXConfig` object that manages `str` Javascript rgb() values.

<a name="canvasxpress.config.type.CXRGBColor.is_color_str"></a>
#### is\_color\_str

```python
 | @staticmethod
 | is_color_str(value: str)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L811)

A static method that evaluates a given string to see if it represents a
Javascript rgb() statement.

**Arguments**:

- `value`: `str`
    A string to evaluate.  A valid Javascript value has the form
    `rgb(r, g, b)` where RGB values are `int` from 0-255.

**Returns**:

`bool`
    True if the string represents a Javascript rgb() statement.

<a name="canvasxpress.config.type.CXRGBColor.is_color_list"></a>
#### is\_color\_list

```python
 | @staticmethod
 | is_color_list(value: list)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L847)

A static method that evaluates a given list to see if it represents a
Javascript rgb() statement.

**Arguments**:

- `value`: `list`
    A list to evaluate.  A valid Javascript value has the form
    `rgb(r, g, b)` where RGB values are `int` from 0-255.

**Returns**:

`bool`
    True if the list represents a Javascript rgb() statement.

<a name="canvasxpress.config.type.CXRGBColor.is_color_dict"></a>
#### is\_color\_dict

```python
 | @staticmethod
 | is_color_dict(value: dict)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L875)

A static method that evaluates a given dict to see if it represents a
Javascript rgb() statement.

**Arguments**:

- `value`: `dict`
    A dict to evaluate.  A valid Javascript value has the form
    `rgba(r, g, b)` where RGB values are `int` from 0-255.  For the dict
     to be valid its keys must be lower case r, g, and b characters.

**Returns**:

`bool`
    True if the dict represents a Javascript rgb() statement.

<a name="canvasxpress.config.type.CXRGBColor.value"></a>
#### value

```python
 | @CXDict.value.setter
 | value(value: Union['CXRGBColor', dict, list, str]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L913)

Sets the RGB value from an existing `CXRGBColor` object, or a `dict`,
`list`, or `string` following the Javascript `rgb()` format.

**Arguments**:

- `value`: `Union['CXRGBColor', dict, list, str]`
    The value to be accepted.  See the `is_color_*()` methods for
    acceptable formats.

<a name="canvasxpress.config.type.CXRGBColor.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(label: str, value: Union['CXRGBColor', dict, list, str])
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L987)

Initializes a new CXRGBColor object using the RGB value from an
existing `CXRGBColor` object, or a `dict`, `list`, or `string`
following the Javascript `rgb()` format.

**Arguments**:

- `value`: `Union['CXRGBColor', dict, list, str]`
    The value to be accepted.  See the `is_color_*()` methods for
    acceptable formats.

<a name="canvasxpress.config.type.CXRGBColor.__str__"></a>
#### \_\_str\_\_

```python
 | __str__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L1003)

*str* function.  Converts the object into a JSON string.

<a name="canvasxpress.config.type.CXRGBColor.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L1017)

*repr* function.  Converts the CXRGBColor object into a pickle string
that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.config.type.CXGraphTypeOptions"></a>
## CXGraphTypeOptions Objects

```python
class CXGraphTypeOptions(Enum)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L1032)

A set of known chart types permitted for use with CanvasXpress objects.  If
a chart not yet identified in this list is required then use a `CXString`
object with the label `graphType` and the value set to the name of the
chart to be used.

<a name="canvasxpress.config.type.CXGraphType"></a>
## CXGraphType Objects

```python
class CXGraphType(CXString)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L1091)

A CXString that is aware of CanvasXpress types of graphs, such as 'Bar'.

<a name="canvasxpress.config.type.CXGraphType.value"></a>
#### value

```python
 | @CXString.value.setter
 | value(value: Union[CXGraphTypeOptions, str]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L1099)

Sets the value using a known CanvasXpress option.

<a name="canvasxpress.config.type.CXGraphType.set_custom_value"></a>
#### set\_custom\_value

```python
 | set_custom_value(value: str)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L1115)

Permits a js value to be set, such as if a new option is recently
made available that the Python framework is yet to be aware of.

**Arguments**:

- `value`: `str`
    The string value to set.

<a name="canvasxpress.config.type.CXGraphType.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(type: Union[CXGraphTypeOptions, str] = CXGraphTypeOptions.Bar)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/type.py#L1124)

Initializes a new CXGraphType object with a value corresponding to one
of the values provided by `CXGraphTypeOptions`.

<a name="canvasxpress.config.collection"></a>
# canvasxpress.config.collection

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/collection.py#L1)

<a name="canvasxpress.config.collection.CXConfigs"></a>
## CXConfigs Objects

```python
@total_ordering
class CXConfigs(CXDictConvertable)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/collection.py#L12)

CXConfigs provides support for addressing a collection of `CXConfig` values.

<a name="canvasxpress.config.collection.CXConfigs.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(*configs: CXConfig)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/collection.py#L22)

Initializes a new `CXConfigs` object with zero or more `CXConfig`
objects.

**Arguments**:

- `configs`: `CXConfig, ...`
    A list of zero or more `CXConfig` objects to associate.

<a name="canvasxpress.config.collection.CXConfigs.add"></a>
#### add

```python
 | add(config: CXConfig) -> 'CXConfigs'
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/collection.py#L33)

Adds the specified configuration to the collection.  This method
supports chaining for efficient additions of `CXConfig` objects.

Example:
```python
configs = CXConfigs()
configs \
    .add(CXString("1", "one") \
    .add(CXString("2", "two") \
    .add(CXString("3", "three")
```

**Arguments**:

- `config`: `CXConfig`
    The `CXConfig` to associate.  Cannot be `None`.

<a name="canvasxpress.config.collection.CXConfigs.set_param"></a>
#### set\_param

```python
 | set_param(label: str, value: Any) -> 'CXConfigs'
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/collection.py#L61)

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

- `value`: `Any`
    The parameter to infer and associate.  Cannot be `None`.  Defaults
    to `str` if the type cannot otherwise be deduced.

<a name="canvasxpress.config.collection.CXConfigs.configs"></a>
#### configs

```python
 | @property
 | configs() -> List[CXConfig]
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/collection.py#L181)

Provides access to the list of associated `CXConfig` objects.

**Returns**:

`List[CXConfig]`

<a name="canvasxpress.config.collection.CXConfigs.render_to_dict"></a>
#### render\_to\_dict

```python
 | render_to_dict() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/collection.py#L188)

Provides a `dict` representation of the configuration values.

**Returns**:

`dict`
    A `dict` representing the configuration values arranged as a map
    of keys and values.

    Given:
    ```python
    configs = CXConfigs()
    configs \
        .set_param("1", "rgb(3, 172, 198)") \
        .set_param("2", 2) \
        .set_param("3", True)
    ```

    Then `render_to_dict()` results in:
    ```python
    {
        "1": "rgb(3, 172, 198)",
        "2": 2,
        "3": True,
    }
    ```

<a name="canvasxpress.config.collection.CXConfigs.merge_configs"></a>
#### merge\_configs

```python
 | @classmethod
 | merge_configs(cls, configs: List[CXConfig]) -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/collection.py#L218)

Given a list of CXConfig objects, a dictionary of unique attributes is
generated and provided.

**Returns**:

`dict`
    A dict of zero or more keys representing the CXConfigs.

<a name="canvasxpress.config.collection.CXConfigs.__copy__"></a>
#### \_\_copy\_\_

```python
 | __copy__() -> 'CXConfigs'
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/collection.py#L239)

*copy* constructor.  Returns the `CXConfig` objects within a new
`CXConfigs` object.

<a name="canvasxpress.config.collection.CXConfigs.__deepcopy__"></a>
#### \_\_deepcopy\_\_

```python
 | __deepcopy__(memo) -> 'CXConfigs'
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/collection.py#L248)

*deepcopy* constructor.  Returns a deepcopy of the `CXConfig` objects
 within a new `CXConfigs` object.

<a name="canvasxpress.config.collection.CXConfigs.__lt__"></a>
#### \_\_lt\_\_

```python
 | __lt__(other: 'CXConfigs') -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/collection.py#L260)

*less than* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

- `other`: 
    `CXConfigs` The object to compare.

**Returns**:

`bool`
    <ul>
    <li> If `other` is `None` then `False`
    <li> If `other` is not a `CXConfigs` object then False
    <li> If `other` is a `CXConfigs` object then True of all `CXConfig`
        objects are also less than the events tracked by `self`.
    </ul>

<a name="canvasxpress.config.collection.CXConfigs.__eq__"></a>
#### \_\_eq\_\_

```python
 | __eq__(other: 'CXConfigs') -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/collection.py#L296)

*equals* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

- `other`: 
    `CXConfigs` The object to compare.

**Returns**:

`bool`
    <ul>
    <li> If `other` is `None` then `False`
    <li> If `other` is not a `CXConfigs` object then False
    <li> If `other` is a `CXConfigs` object then True of all `CXConfig`
        objects are also equal to the events tracked by `self`.
    </ul>

<a name="canvasxpress.config.collection.CXConfigs.__str__"></a>
#### \_\_str\_\_

```python
 | __str__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/collection.py#L329)

*str* function.  Converts the `CXConfigs` object into a JSON
representation.
:returns" `str`
    JSON form of the collection.

<a name="canvasxpress.config.collection.CXConfigs.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/config/collection.py#L340)

*repr* function.  Converts the `CXConfigs` object into a pickle string
that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.js"></a>
# canvasxpress.js

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/js/__init__.py#L1)

The js package provides functionality for integrating custom Javascript with
CanvasXpress charts.

<a name="canvasxpress.js.collection"></a>
# canvasxpress.js.collection

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/js/collection.py#L1)

<a name="canvasxpress.js.collection.CXEvents"></a>
## CXEvents Objects

```python
@total_ordering
class CXEvents(CXJavascriptConvertable)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/js/collection.py#L11)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/js/collection.py#L44)

Provides a non-associated list of the associated CXEvents.

**Returns**:

`List[CXEvent]` A list of zero or more CXEvent objects.

<a name="canvasxpress.js.collection.CXEvents.has"></a>
#### has

```python
 | has(event: CXEvent) -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/js/collection.py#L51)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/js/collection.py#L62)

Adds the specified CXEvent.  If the CXEvent must be unique then an Error
is raised if an react is already presenbt with the same ID.

**Arguments**:

- `event`: 
    `CXEvent` The event to add to the collection.  Cannot be `None`.
- `unique`: 
    `bool` True if `event` must not already be a part of the collection.

<a name="canvasxpress.js.collection.CXEvents.remove"></a>
#### remove

```python
 | remove(event: CXEvent) -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/js/collection.py#L89)

Removes the specified object from the list.

**Arguments**:

- `event`: The CXEvent object to remove from the list if it is
    already included.

**Returns**:

True if the CXEvent was removed.  False indicates that the
    object was not a member.

<a name="canvasxpress.js.collection.CXEvents.render_to_dict"></a>
#### render\_to\_dict

```python
 | render_to_dict() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/js/collection.py#L109)

Provides a dict with each js properly formatted as JS within.

**Returns**:

`dict`
Given:
```python
event1 = CXEvent("f1", "x = 0")
event2 = CXEvent("f2", "x = 1")
events = CXEvents(event1, event2)
functions = events.render_to_dict()
```
Then the value of `functions` would be:
```python
{
    "f1": function(o, e, t){x = 0},
    "f2": function(o, e, t){x = 1}
}
```

<a name="canvasxpress.js.collection.CXEvents.render_to_js"></a>
#### render\_to\_js

```python
 | render_to_js() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/js/collection.py#L135)

Converts the object into HTML5 complant script.

**Returns**:

'str'
Given:
```python
event1 = CXEvent("f1", "x = 0")
event2 = CXEvent("f2", "x = 1")
events = CXEvents(event1, event2)
functions = events.render_to_js()
```
Then the value of `functions` would be:
```text
{
    'f1': 'function(o, e, t){x = 0}',
    'f2': 'function(o, e, t){x = 1}',
}
```

<a name="canvasxpress.js.collection.CXEvents.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(*events)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/js/collection.py#L170)

Initializes a new CXEvents object.

**Arguments**:

- `events`: 
    A multiple value parameter by which zero or more `CXEvent` objects
    may be provided.  Also see `add()` for how individual objects are
    processed.

    For example:
```python
event1 = CXEvent("f1", "x = 0")
event2 = CXEvent("f2", "x = 1")
events = CXEvents(event1, event2)
```

<a name="canvasxpress.js.collection.CXEvents.__copy__"></a>
#### \_\_copy\_\_

```python
 | __copy__()
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/js/collection.py#L192)

*copy* constructor.  Returns the `CXEvent` objects within a new `CXEvents`
object.

<a name="canvasxpress.js.collection.CXEvents.__deepcopy__"></a>
#### \_\_deepcopy\_\_

```python
 | __deepcopy__(memo)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/js/collection.py#L201)

*deepcopy* constructor.  Returns a deep copy of `CXEvent` objects within
a new `CXEvents` object.

<a name="canvasxpress.js.collection.CXEvents.__lt__"></a>
#### \_\_lt\_\_

```python
 | __lt__(other: 'CXEvents')
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/js/collection.py#L213)

*less than* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

- `other`: 
    `CXEvent` The object to compare.

**Returns**:

`bool`
    <ul>
    <li> If `other` is `None` then `False`
    <li> If `other` is not a `CXEvents` object then False
    <li> If `other` is a `CXEvents` object then True of all `CXEvent`
        objects are also less than the events tracked by `self`.
    </ul>

<a name="canvasxpress.js.collection.CXEvents.__eq__"></a>
#### \_\_eq\_\_

```python
 | __eq__(other: 'CXEvents')
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/js/collection.py#L249)

*equals* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

- `other`: 
    `CXEvent` The object to compare.

**Returns**:

`bool`
    <ul>
    <li> If `other` is `None` then `False`
    <li> If `other` is not a `CXEvents` object then False
    <li> If `other` is a `CXEvents` object then True of all `CXEvent`
        objects are also equal to the events tracked by `self`.
    </ul>

<a name="canvasxpress.js.collection.CXEvents.__str__"></a>
#### \_\_str\_\_

```python
 | __str__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/js/collection.py#L282)

*str* function.  Converts the CXEvents object into a JSON list of
`CXEvent` objects also converted into JSON representations.
:returns" `str` JSON form of the collection.

<a name="canvasxpress.js.collection.CXEvents.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/js/collection.py#L292)

*repr* function.  Converts the CXEvents object into a pickle string
that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.js.function"></a>
# canvasxpress.js.function

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/js/function.py#L1)

<a name="canvasxpress.js.function.CXEvent"></a>
## CXEvent Objects

```python
@total_ordering
class CXEvent(CXJavascriptConvertable)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/js/function.py#L15)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/js/function.py#L71)

Provides access to the react ID.

**Returns**:

The ID as a string.

<a name="canvasxpress.js.function.CXEvent.id"></a>
#### id

```python
 | @id.setter
 | id(value: str) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/js/function.py#L79)

Sets the react ID, which is a keyword recognized by CanvasXpress.

**Arguments**:

- `value`: `str`
    The ID, which must be a string compliant object.  Cannot be `None`.

<a name="canvasxpress.js.function.CXEvent.script"></a>
#### script

```python
 | @property
 | script() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/js/function.py#L94)

Provides access to the react script.

**Returns**:

`str` The Javascript source.

<a name="canvasxpress.js.function.CXEvent.script"></a>
#### script

```python
 | @script.setter
 | script(value: str) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/js/function.py#L102)

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

- `value`: `str`
    The ID, which must be a UTF-8 string compliant object.

<a name="canvasxpress.js.function.CXEvent.render_to_js"></a>
#### render\_to\_js

```python
 | render_to_js() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/js/function.py#L129)

Converts the object into HTML5 complant script.

**Returns**:

'str'
Given:
```python
event1 = CXEvent("f1", "x = 0")
function = event1.render_to_js()
```
Then the value of `function` would be:
```text
'f1': 'function(o, e, t){x = 0}
```

<a name="canvasxpress.js.function.CXEvent.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(id: str = "", script: str = "")
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/js/function.py#L152)

Initializes a new CXEvent object.

**Arguments**:

- `id`: `str`
    The ID of the react, such as mousemove.  Also see property `id`.
- `script`: `str`
    The script logic for the react.  Also see property `script`.

<a name="canvasxpress.js.function.CXEvent.__copy__"></a>
#### \_\_copy\_\_

```python
 | __copy__()
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/js/function.py#L169)

*copy* constructor.  Returns a new `CXEvent` object.

<a name="canvasxpress.js.function.CXEvent.__deepcopy__"></a>
#### \_\_deepcopy\_\_

```python
 | __deepcopy__(memo)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/js/function.py#L178)

*deepcopy* constructor.  Returns a new `CXEvent` object.

<a name="canvasxpress.js.function.CXEvent.__lt__"></a>
#### \_\_lt\_\_

```python
 | __lt__(other: 'CXEvent') -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/js/function.py#L190)

*less than* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

- `other`: 
    `CXEvent` The object to compare.

**Returns**:

`bool`
    <ul>
    <li> If `other` is `None` then `False`
    <li> If `other` is not a `CXEvent` object then `False`
    <li> If `other` is a `CXEvent` object then True if id and string of
        `other` are less than that of `self`.
    </ul>

<a name="canvasxpress.js.function.CXEvent.__eq__"></a>
#### \_\_eq\_\_

```python
 | __eq__(other: 'CXEvent') -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/js/function.py#L220)

*equal* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

- `other`: 
    `CXEvent` The object to compare.

**Returns**:

`bool`
    <ul>
    <li> If `other` is `None` then `False`
    <li> If `other` is not a `CXEvent` object then `False`
    <li> If `other` is a `CXEvent` object then True if id and string of
        `other` are equal to that of `self`.
    </ul>

<a name="canvasxpress.js.function.CXEvent.__str__"></a>
#### \_\_str\_\_

```python
 | __str__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/js/function.py#L245)

*str* function.  Converts the object into a Javascript statement.

<a name="canvasxpress.js.function.CXEvent.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/js/function.py#L270)

*repr* function.  Converts the CXEvent object into a pickle string
that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.render"></a>
# canvasxpress.render

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/render/__init__.py#L1)

The render package provides functionality for rendering CanvasXpress objects in
containers or environments

<a name="canvasxpress.render.base"></a>
# canvasxpress.render.base

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/render/base.py#L1)

<a name="canvasxpress.render.base.CXRenderable"></a>
## CXRenderable Objects

```python
class CXRenderable(ABC)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/render/base.py#L6)

CXRenderable is capable of rendering a CanvasXpress object to some kind of
output or display device.

<a name="canvasxpress.render.base.CXRenderable.canvas"></a>
#### canvas

```python
 | @property
 | canvas() -> CanvasXpress
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/render/base.py#L18)

Provides the tracked CanvasXpress object.

**Returns**:

The `CanvasXpress` object if tracked, or `None` if not object
    is yet associated with the CXRenderable.

<a name="canvasxpress.render.base.CXRenderable.canvas"></a>
#### canvas

```python
 | @canvas.setter
 | canvas(value: CanvasXpress)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/render/base.py#L27)

Sets the CanvasXpress object to be tracked.
:praram value:
    The `CanvasXpress` object to be tracked.  Cannot be `None`.

<a name="canvasxpress.render.base.CXRenderable.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(cx: CanvasXpress)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/render/base.py#L42)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/render/base.py#L57)

Renders the associated CanvasXpress object appropriate to the target.
Not implemented.

<a name="canvasxpress.render.jupyter"></a>
# canvasxpress.render.jupyter

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/render/jupyter.py#L1)

<a name="canvasxpress.render.jupyter.CXNoteBook"></a>
## CXNoteBook Objects

```python
class CXNoteBook(CXRenderable)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/render/jupyter.py#L43)

CXNoteBook is a `CXRenderable` that renders `CanvasXpress` objects into
`IPython` containers (Jupyter Notebooks).

<a name="canvasxpress.render.jupyter.CXNoteBook.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(cx: CanvasXpress)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/render/jupyter.py#L49)

Initializes a new CXNoteBook object.
:praram cx:
    The `CanvasXpress` object to be tracked.  See the `canvas`
    property, except that on initialization cx can be `None`.

<a name="canvasxpress.render.jupyter.CXNoteBook.render"></a>
#### render

```python
 | render()
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/render/jupyter.py#L61)

Renders the associated CanvasXpress object appropriate for display in
an IPython (e.g., Jupyter NoteBook/Lab) environment.

<a name="canvasxpress.data"></a>
# canvasxpress.data

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/__init__.py#L1)

The data package provides functionality for integrating different kinds of data
structures and sources into a CanvasXpress object.  A balance is provided
between convenience functionality and reasonable external preparation, such as
what can be performed via `pandas`.

<a name="canvasxpress.data.matrix"></a>
# canvasxpress.data.matrix

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/matrix.py#L1)

<a name="canvasxpress.data.matrix.CXDataframeData"></a>
## CXDataframeData Objects

```python
@total_ordering
class CXDataframeData(CXData)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/matrix.py#L14)

A CXData class dedicated to processing Python DataFrame, matrix-structured
 data.

<a name="canvasxpress.data.matrix.CXDataframeData.dataframe"></a>
#### dataframe

```python
 | @property
 | dataframe() -> DataFrame
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/matrix.py#L26)

Provides the data managed by the object.

**Returns**:

`DataFrame` The managed data.

<a name="canvasxpress.data.matrix.CXDataframeData.dataframe"></a>
#### dataframe

```python
 | @dataframe.setter
 | dataframe(value: Union[DataFrame, None] = None) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/matrix.py#L34)

Sets the dataframe managed by the object.

**Arguments**:

- `value`: `Union[DataFrame, None]`
    `None` results in an empty `DataFrame`.  A deepcopy will be made of
    `DataFrame` values.

<a name="canvasxpress.data.matrix.CXDataframeData.data"></a>
#### data

```python
 | @property
 | data() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/matrix.py#L47)

Provides the data managed by the object.

**Returns**:

`DataFrame` The managed data.

<a name="canvasxpress.data.matrix.CXDataframeData.data"></a>
#### data

```python
 | @data.setter
 | data(value: Union['CXDataframeData', DataFrame, dict, str, None] = None) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/matrix.py#L55)

Sets the dataframe managed by the object.

**Arguments**:

- `value`: `Union['CXDataframeData', DataFrame, dict, str, None]`
    `None` results in an empty `DataFrame`.  A deepcopy will be made of
    `DataFrame` or equivalent values.

<a name="canvasxpress.data.matrix.CXDataframeData.render_to_dict"></a>
#### render\_to\_dict

```python
 | render_to_dict() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/matrix.py#L102)

Provides a dict representation of the data.

**Returns**:

`dict`
    The data in `dict` form.

<a name="canvasxpress.data.matrix.CXDataframeData.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(data: Union['CXDataframeData', DataFrame, dict, str, None] = None) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/matrix.py#L110)

Initializes the CXData object with data.  Only `DataFrame` or compatible
data types are accepted.

**Arguments**:

- `data`: `Union['CXDataframeData', DataFrame, dict, str, None]`
    `None` to initialize with an empty `DataFrame`, or a `DataFrame`
    like object to assign mapped data.

<a name="canvasxpress.data.matrix.CXDataframeData.__copy__"></a>
#### \_\_copy\_\_

```python
 | __copy__() -> 'CXDataframeData'
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/matrix.py#L124)

*copy constructor* that returns a copy of the CXDataframeData object.

**Returns**:

`CXDataframeData`
    A copy of the wrapping object.

<a name="canvasxpress.data.matrix.CXDataframeData.__deepcopy__"></a>
#### \_\_deepcopy\_\_

```python
 | __deepcopy__(memo) -> 'CXDataframeData'
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/matrix.py#L132)

*deepcopy constructor* that returns a copy of the CXDataframeData object.

**Returns**:

`CXDataframeData` A copy of the wrapping object and deepcopy of
    the tracked data.

<a name="canvasxpress.data.matrix.CXDataframeData.__lt__"></a>
#### \_\_lt\_\_

```python
 | __lt__(other: 'CXDataframeData') -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/matrix.py#L143)

*less than* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

- `other`: 
    `CXDataframeData` The object to compare.

**Returns**:

`bool`
    <ul>
    <li> If `other` is `None` then `False`
    <li> If `other` is not a `CXDataframeData` object then False
    <li> If `other` is a `CXDataframeData` object then True of all
        `CXDataframeData` aspects are also less than the data tracked by
        `self`.
    </ul>

<a name="canvasxpress.data.matrix.CXDataframeData.__eq__"></a>
#### \_\_eq\_\_

```python
 | __eq__(other: 'CXDataframeData') -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/matrix.py#L185)

*equals* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

- `other`: 
    `CXDataframeData` The object to compare.

**Returns**:

`bool`
    <ul>
    <li> If `other` is `None` then `False`
    <li> If `other` is not a `CXDataframeData` object then False
    <li> If `other` is a `CXDataframeData` object then True of all
        `CXDataframeData` aspects are also less than the data tracked by
        `self`.
    </ul>

<a name="canvasxpress.data.matrix.CXDataframeData.__str__"></a>
#### \_\_str\_\_

```python
 | __str__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/matrix.py#L222)

*str* function.  Converts the CXDataframeData object into a JSON
representation.
:returns" `str` JSON form of the `CXDataframeData`.

<a name="canvasxpress.data.matrix.CXDataframeData.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/matrix.py#L230)

*repr* function.  Converts the CXDataframeData object into a pickle
string that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.data.matrix.CXCSVData"></a>
## CXCSVData Objects

```python
class CXCSVData(CXDataframeData)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/matrix.py#L245)

A CXData class dedicated to processing Python CSV-based, matrix-structured
 data.

<a name="canvasxpress.data.matrix.CXCSVData.csv"></a>
#### csv

```python
 | @property
 | csv() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/matrix.py#L252)

Provides the data managed by the object.

**Returns**:

`str` The managed data.

<a name="canvasxpress.data.matrix.CXCSVData.csv"></a>
#### csv

```python
 | @csv.setter
 | csv(value: str = None) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/matrix.py#L265)

Sets the CSV data managed by the object.

**Arguments**:

- `value`: `str`
    `None` results in an empty CSV.  A deepcopy will be made of
    valid CSV `str` values.

<a name="canvasxpress.data.matrix.CXCSVData.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(data: Union['CXCSVData', DataFrame, dict, str, None] = None) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/matrix.py#L277)

Initializes the CXData object with data.  Only CSV `str` or compatible
data types are accepted.

**Arguments**:

- `data`: `Union['CXCSVData', DataFrame, dict, str, None]`
    `None` to initialize with an empty CSV, or a CSV `str`
    like object to assign mapped data.

<a name="canvasxpress.data.matrix.CXCSVData.__str__"></a>
#### \_\_str\_\_

```python
 | __str__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/matrix.py#L290)

*str* function.  Converts the CXCSVData object into a JSON
representation.
:returns" `str` JSON form of the `CXCSVData`.

<a name="canvasxpress.data.matrix.CXCSVData.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/matrix.py#L298)

*repr* function.  Converts the CXCSVData object into a pickle
string that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.data.convert"></a>
# canvasxpress.data.convert

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/convert.py#L1)

<a name="canvasxpress.data.convert.CXHtmlConvertable"></a>
## CXHtmlConvertable Objects

```python
class CXHtmlConvertable(ABC)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/convert.py#L4)

CXHtmlConvertable represents an object that can be converted into HTML.

<a name="canvasxpress.data.convert.CXHtmlConvertable.render_to_html_parts"></a>
#### render\_to\_html\_parts

```python
 | @abstractmethod
 | render_to_html_parts() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/convert.py#L10)

Converts the object into HTML5 compliant script.

**Returns**:

`dict`
    A `dict` representation of the object with each component of the
    necessary HTML indicated by a key.  For example, there might be
    a `div` element and a `script` import.

<a name="canvasxpress.data.convert.CXDictConvertable"></a>
## CXDictConvertable Objects

```python
class CXDictConvertable(ABC)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/convert.py#L21)

CXDictConvertable represents an object that can be converted into a dict.

<a name="canvasxpress.data.convert.CXDictConvertable.render_to_dict"></a>
#### render\_to\_dict

```python
 | @abstractmethod
 | render_to_dict() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/convert.py#L27)

Converts the object into a dict representation.

**Returns**:

`dict`
    A dictionary representation of the object, such as what might be
    needed for a JSON export.

<a name="canvasxpress.data.convert.CXJavascriptConvertable"></a>
## CXJavascriptConvertable Objects

```python
class CXJavascriptConvertable(ABC)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/convert.py#L37)

CXJavascriptConvertable represents an object that can be converted into JS.

<a name="canvasxpress.data.convert.CXJavascriptConvertable.render_to_js"></a>
#### render\_to\_js

```python
 | @abstractmethod
 | render_to_js() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/convert.py#L43)

Converts the object into HTML5 complant script.

**Returns**:

`str`
    A string representation of the object in a form that can be used
    within HTML or Javascript.

<a name="canvasxpress.data.keypair"></a>
# canvasxpress.data.keypair

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/keypair.py#L1)

<a name="canvasxpress.data.keypair.CXDictData"></a>
## CXDictData Objects

```python
@total_ordering
class CXDictData(CXData)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/keypair.py#L12)

A CXData class dedicated to processing Python dict-structured data.

<a name="canvasxpress.data.keypair.CXDictData.data"></a>
#### data

```python
 | @property
 | data() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/keypair.py#L23)

Provides a reference to the dict tracked by the object.

**Returns**:

`dict`
    The associated dictionary, with zero or more keys as appropriate.

<a name="canvasxpress.data.keypair.CXDictData.data"></a>
#### data

```python
 | @data.setter
 | data(value: dict) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/keypair.py#L32)

Sets the data associated with the object.

**Arguments**:

- `value`: `dict`
    The dictionary to be tracked by the object.  `None` will result in
    an empty dict.  A deep copy will be made of a valid `CXDict` or
    `dict` provided.

<a name="canvasxpress.data.keypair.CXDictData.render_to_dict"></a>
#### render\_to\_dict

```python
 | render_to_dict() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/keypair.py#L52)

Provides a dict representation of the data.

**Returns**:

`dict`
    The data in `dict` form.

<a name="canvasxpress.data.keypair.CXDictData.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(data: Union[dict, None] = None) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/keypair.py#L60)

Initializes the CXData object with data.  Only dict or compatible data
types are accepted.

**Arguments**:

- `data`: `Union[dict, None]`
    `None` to initialize with an empty dictionary, or a `dict`-like
    object to assign mapped data.

<a name="canvasxpress.data.keypair.CXDictData.__copy__"></a>
#### \_\_copy\_\_

```python
 | __copy__() -> 'CXDictData'
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/keypair.py#L71)

*copy constructor* that returns a copy of the CXDictData object.

**Returns**:

`CXDictData` A copy of the wrapping object.

<a name="canvasxpress.data.keypair.CXDictData.__deepcopy__"></a>
#### \_\_deepcopy\_\_

```python
 | __deepcopy__(memo) -> 'CXDictData'
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/keypair.py#L78)

*deepcopy constructor* that returns a copy of the CXDictData object.

**Returns**:

`CXDictData` A copy of the wrapping object and deepcopy of
    the tracked data.

<a name="canvasxpress.data.keypair.CXDictData.__lt__"></a>
#### \_\_lt\_\_

```python
 | __lt__(other: 'CXDictData') -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/keypair.py#L91)

*less than* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

- `other`: 
    `CXDictData` The object to compare.

**Returns**:

`bool`
    <ul>
    <li> If `other` is `None` then `False`
    <li> If `other` is not a `CXDictData` object then False
    <li> If `other` is a `CXDictData` object then True of all
        `CXDictData` objects are also less than the data tracked by
        `self`.
    </ul>

<a name="canvasxpress.data.keypair.CXDictData.__eq__"></a>
#### \_\_eq\_\_

```python
 | __eq__(other: 'CXDictData') -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/keypair.py#L138)

*equals* comparison.  Also see `@total_ordering` in `functools`.

**Arguments**:

- `other`: 
    `CXDictData` The object to compare.

**Returns**:

`bool`
    <ul>
    <li> If `other` is `None` then `False`
    <li> If `other` is not a `CXDictData` object then False
    <li> If `other` is a `CXDictData` object then True of all
        `CXDictData` objects are also equal to the data tracked by
        `self`.
    </ul>

<a name="canvasxpress.data.keypair.CXDictData.__str__"></a>
#### \_\_str\_\_

```python
 | __str__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/keypair.py#L183)

*str* function.  Converts the CXDictData object into a JSON
representation.
:returns" `str` JSON form of the `CXDictData`.

<a name="canvasxpress.data.keypair.CXDictData.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/keypair.py#L191)

*repr* function.  Converts the CXDictData object into a pickle string
that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.data.keypair.CXJSONData"></a>
## CXJSONData Objects

```python
class CXJSONData(CXDictData)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/keypair.py#L200)

A CXData class dedicated to processing JSON data.

<a name="canvasxpress.data.keypair.CXJSONData.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(data: Union[dict, str, None] = None) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/keypair.py#L225)

Initializes the CXData object with data.  Only dict or compatible data
types are accepted.

**Arguments**:

- `data`: `Union[dict, str, None]`
    `None` to initialize with an empty JSON, or a JSON/`dict`-like
    object to assign mapped data.

<a name="canvasxpress.data.keypair.CXJSONData.__copy__"></a>
#### \_\_copy\_\_

```python
 | __copy__() -> 'CXJSONData'
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/keypair.py#L236)

*copy constructor* that returns a copy of the CXDictData objct.

**Returns**:

`CXDictData` A copy of the wrapping object.

<a name="canvasxpress.data.keypair.CXJSONData.__deepcopy__"></a>
#### \_\_deepcopy\_\_

```python
 | __deepcopy__(memo) -> 'CXJSONData'
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/keypair.py#L243)

*deepcopy constructor* that returns a copy of the CXJSONData object.

**Returns**:

`CXJSONData` A copy of the wrapping object and deepcopy of
    the tracked data.

<a name="canvasxpress.data.keypair.CXJSONData.__repr__"></a>
#### \_\_repr\_\_

```python
 | __repr__() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/keypair.py#L254)

*repr* function.  Converts the CXJSONData object into a pickle string
that can be used with `eval` to establish a copy of the object.

**Returns**:

`str` An evaluatable representation of the object.

<a name="canvasxpress.data.base"></a>
# canvasxpress.data.base

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/base.py#L1)

<a name="canvasxpress.data.base.CXData"></a>
## CXData Objects

```python
class CXData(CXDictConvertable)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/base.py#L7)

CXData defines an essential data class for managing data acquisiton,
transformation, and introspection as required by the CXPress class.

<a name="canvasxpress.data.base.CXData.data"></a>
#### data

```python
 | @property
 | @abstractmethod
 | data() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/base.py#L15)

A property accessor for the data managed by the object.  Regardless of
the input data the returned data structure will be a dict-type for use
with CanvasXpress.

**Returns**:

`dict`
    A dictionary representing a data map suitable for use with a chart.

<a name="canvasxpress.data.base.CXData.__init__"></a>
#### \_\_init\_\_

```python
 | @abstractmethod
 | __init__(data: Union[object, None]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/data/base.py#L26)

Initializes the CXData object with data.

**Arguments**:

- `data`: `Union[object, None]`
    Given an object or no data prepares a new CXData instance ready for
    use by a `CanvasXpress` object.

<a name="canvasxpress.canvas"></a>
# canvasxpress.canvas

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/canvas.py#L1)

<a name="canvasxpress.canvas.CanvasXpress"></a>
## CanvasXpress Objects

```python
class CanvasXpress(CXHtmlConvertable)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/canvas.py#L36)

CanvasXpress acts as a proxy to the Javascript CanvasXpress object, and in
general use remains similar to its Javascript counterpart.

Assuming a flask function that returns a rendered page using the data from
a CanvasXpress object:

```python
@app.route('/pythonexample')
def get_simple_chart() -> str:
    chart: CanvasXpress = CanvasXpress(
        target_id="example_chart",
        data=CXDictData(
            {
                "y": {
                "vars": ["Gene1"],
                "smps": ["Smp1", "Smp2", "Smp3"],
                "data": [[10, 35, 88]],
            }
        ),
        configs=CXConfigs(
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

<a name="canvasxpress.canvas.CanvasXpress.target_id"></a>
#### target\_id

```python
 | @property
 | target_id() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/canvas.py#L78)

The ID of the CanvasXpress object's associated HTML components, such as
the render canvas element.

**Returns**:

`str` The ID

<a name="canvasxpress.canvas.CanvasXpress.target_id"></a>
#### target\_id

```python
 | @target_id.setter
 | target_id(value: str) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/canvas.py#L87)

Sets the target_id of the CanvasXpress instance.

**Arguments**:

- `value`: 
    `str` The ID to be associated.  Cannot be `None`, and
    must be alphanumeric.

<a name="canvasxpress.canvas.CanvasXpress.license_available"></a>
#### license\_available

```python
 | @property
 | license_available() -> bool
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/canvas.py#L112)

Indicates if a license is associated with the CanvasXpress object.

**Returns**:

`True` if a license file URL has been set.

<a name="canvasxpress.canvas.CanvasXpress.license_url"></a>
#### license\_url

```python
 | @property
 | license_url() -> str
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/canvas.py#L120)

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

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/canvas.py#L129)

Sets the location of the license file to be associated with the
CanvasXpress object.

**Arguments**:

- `value`: 
    `str` The path to the license file or `None` if a previously set URL
    is no longer valid.

<a name="canvasxpress.canvas.CanvasXpress.CHART_WIDTH_DEFAULT"></a>
#### CHART\_WIDTH\_DEFAULT

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/canvas.py#L148)

Default width in pixels of the chart when rendered, such as into HTML.

<a name="canvasxpress.canvas.CanvasXpress.chart_width"></a>
#### chart\_width

```python
 | @property
 | chart_width() -> int
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/canvas.py#L159)

Indicates the preferred canvas width when rendered.

**Returns**:

`int` The pixel count

<a name="canvasxpress.canvas.CanvasXpress.chart_width"></a>
#### chart\_width

```python
 | @chart_width.setter
 | chart_width(value: int)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/canvas.py#L167)

Sets the preferred canvas width when rendered.

**Arguments**:

- `value`: 
    `int` The pixel count.  Cannot be `None` or less than `1`.

<a name="canvasxpress.canvas.CanvasXpress.CHART_HEIGHT_DEFAULT"></a>
#### CHART\_HEIGHT\_DEFAULT

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/canvas.py#L185)

Default height in pixels of the chart when rendered, such as into HTML.

<a name="canvasxpress.canvas.CanvasXpress.chart_height"></a>
#### chart\_height

```python
 | @property
 | chart_height() -> int
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/canvas.py#L196)

Indicates the preferred canvas height when rendered.

**Returns**:

`int` The pixel count

<a name="canvasxpress.canvas.CanvasXpress.chart_height"></a>
#### chart\_height

```python
 | @chart_height.setter
 | chart_height(value: int)
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/canvas.py#L204)

Sets the preferred canvas height when rendered.

**Arguments**:

- `value`: 
    `int` The pixel count.  Cannot be `None` or less than `1`.

<a name="canvasxpress.canvas.CanvasXpress.data"></a>
#### data

```python
 | @property
 | data() -> CXData
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/canvas.py#L230)

Provides access to the CXData associated with this CanvasXpress chart.

**Returns**:

`CXData` The data to be associated with the chart.

<a name="canvasxpress.canvas.CanvasXpress.data"></a>
#### data

```python
 | @data.setter
 | data(value: Union[CXData, dict, None]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/canvas.py#L238)

Sets the CXData associated with this CanvasXpress chart.

**Arguments**:

- `value`: 
    `CXData, dict, None` An object translatable into a CXData type.
    If the object is an instance of CXData then it will be tracked
    by the CanvasXpress object; otherwise, a new CXData object will
    be created to manage the content.

<a name="canvasxpress.canvas.CanvasXpress.events"></a>
#### events

```python
 | @property
 | events() -> CXEvents
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/canvas.py#L265)

Provides access to the CXEvents associated with this CanvasXpress chart.

**Returns**:

`CXEvents` The events to be associated with the chart.

<a name="canvasxpress.canvas.CanvasXpress.events"></a>
#### events

```python
 | @events.setter
 | events(events: Union[CXEvents, List[CXEvent], None]) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/canvas.py#L273)

Sets the CXEvents associated with this CanvasXpress chart.

**Arguments**:

- `value`: 
    `CXEvents, List[CXEvent], None` An object translatable into a
    CXEvents type.  If the object is an instance of CXEvents then it
    will be tracked by the CanvasXpress object; otherwise, a new
    CXEvents object will be created to manage the content.

<a name="canvasxpress.canvas.CanvasXpress.configs"></a>
#### configs

```python
 | @property
 | configs() -> CXConfigs
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/canvas.py#L300)

Provides access to the CXConfigs associated with this CanvasXpress chart.

**Returns**:

`CXConfigs` The configs to be associated with the chart.

<a name="canvasxpress.canvas.CanvasXpress.configs"></a>
#### configs

```python
 | @configs.setter
 | configs(value: Union[List[CXConfig], CXConfigs])
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/canvas.py#L308)

Sets the CXConfigs associated with this CanvasXpress chart.

**Arguments**:

- `value`: 
    `List[CXConfig], CXConfigs` An object translatable into a CXConfigs
    type.  If the object is an instance of CXConfigs then it will be
    tracked by the CanvasXpress object; otherwise, a new CXConfigs
    object will be created to manage the content.

<a name="canvasxpress.canvas.CanvasXpress.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(target_id: str = None, data: Union[CXData, dict] = None, events: Union[List[CXEvent], CXEvents] = None, configs: Union[List[CXConfig], CXConfigs] = None) -> None
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/canvas.py#L329)

Initializes a new CanvasXpress object.  Default values are provided for
all parameters if values are not specified; otherwise the arguments are
treated as if an appropriate setter were used.

**Arguments**:

- `target_id`: See `target_id` property, except that on default
    initialization the object will be assigned an UUID4 value.
- `data`: See `data` property
- `events`: See `events` property
- `configs`: See `configs` property

<a name="canvasxpress.canvas.CanvasXpress.render_to_html_parts"></a>
#### render\_to\_html\_parts

```python
 | render_to_html_parts() -> dict
```

[[view_source]](https://github.com/docinfosci/canvasxpress-python/blob/05ad94eb5c66662bf333297fb46ed9340072d6d5/canvasxpress/canvas.py#L357)

Converts the CanvasXpress object into HTML5 complant script.

**Returns**:

`dict` A map of values appropriate for use in HTML, such as
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
        target_id="example_chart",
        data=CXDictData(
            {
                "y": {
                "vars": ["Gene1"],
                "smps": ["Smp1", "Smp2", "Smp3"],
                "data": [[10, 35, 88]],
            }
        ),
        configs=CXConfigs(
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
