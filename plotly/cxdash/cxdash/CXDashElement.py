# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
from typing import Literal  # noqa: F401

from dash.development.base_component import Component, _explicitize_args

try:
    from dash.types import NumberType  # noqa: F401
except ImportError:
    # Backwards compatibility for dash<=4.1.0
    if typing.TYPE_CHECKING:
        raise
    NumberType = typing.Union[  # noqa: F401
        typing.SupportsFloat, typing.SupportsInt, typing.SupportsComplex
    ]

ComponentSingleType = typing.Union[str, int, float, Component, None]
ComponentType = typing.Union[
    ComponentSingleType,
    typing.Sequence[ComponentSingleType],
]


class CXDashElement(Component):
    """A CXDashElement component.
CXDashElement implements a Plotly Dash integration of CanvasXpress React.
Properties are defined for use by the CanvasXpress class to update
CanvasXpress aspects such as data, config, and sizing.

Keyword arguments:

- id (string; required):
    The ID of the element for use in function calls and element
    identification.

- after_render (string; optional):
    The events functions for increased reactivity.

- config (string; optional):
    The configuration JSON dictating formatting and content
    management.

- css_url (string; optional):
    The CSS CDN URL that should be used for CanvasXpress
    functionality.

- data (string; optional):
    The data JSON, generally in the XYZ format.

- events (string; optional):
    The events functions for increased reactivity.

- height (string; optional):
    The element height.

- js_url (string; optional):
    The Javascript URL that should be used for CanvasXpress
    functionality.

- width (string; optional):
    The element width."""
    _children_props: list[str] = []
    _base_nodes = ['children']
    _namespace = 'cxdash'
    _type = 'CXDashElement'


    def __init__(
        self,
        id: str | dict | None = None,
        data: str | None = None,
        config: str | None = None,
        events: str | None = None,
        after_render: str | None = None,
        js_url: str | None = None,
        css_url: str | None = None,
        width: str | None = None,
        height: str | None = None,
        **kwargs
    ):
        self._prop_names = ['id', 'after_render', 'config', 'css_url', 'data', 'events', 'height', 'js_url', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'after_render', 'config', 'css_url', 'data', 'events', 'height', 'js_url', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super().__init__(**args)

setattr(CXDashElement, "__init__", _explicitize_args(CXDashElement.__init__))
