# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


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

- cdn_edition (string; optional):
    The Javascript and CSS CDN edition that should be used for
    CanvasXpress functionality.

- config (string; optional):
    The configuration JSON dictating formatting and content
    management.

- data (string; optional):
    The data JSON, generally in the XYZ format.

- events (string; optional):
    The events functions for increased reactivity.

- height (string; optional):
    The element height.

- width (string; optional):
    The element width."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'cxdash'
    _type = 'CXDashElement'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, data=Component.UNDEFINED, config=Component.UNDEFINED, events=Component.UNDEFINED, after_render=Component.UNDEFINED, cdn_edition=Component.UNDEFINED, width=Component.UNDEFINED, height=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'after_render', 'cdn_edition', 'config', 'data', 'events', 'height', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'after_render', 'cdn_edition', 'config', 'data', 'events', 'height', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(CXDashElement, self).__init__(**args)
