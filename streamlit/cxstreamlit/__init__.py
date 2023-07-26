import json
import os
from typing import Optional

import streamlit.components.v1 as components

COMPONENT_ID: str = "CXStreamlit"

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = (
    True if os.environ.get("CXSTREAMLIT_TESTING") is None else False
)

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("my_component"
        # does not fit this bill, so please choose something better for your
        # own component :)
        COMPONENT_ID,
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component(
        COMPONENT_ID,
        path=build_dir,
    )


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def CXStreamlit(
        id: Optional[str] = None,
        after_render: Optional[str] = None,
        cdn_edition: Optional[str] = None,
        config: Optional[str] = None,
        data: Optional[str] = None,
        events: Optional[str] = None,
        height: Optional[str] = None,
        width: Optional[str] = None,
) -> object:
    """Create a new instance of "my_component".

    Parameters
    ----------
    id: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    None

    """
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.
    component_value = _component_func(
        id=id,
        data=data,
        config=config,
        events=events,
        after_render=after_render,
        cdn_edition=cdn_edition,
        height=height,
        width=width,
    )

    # We could modify the value returned from the component if we wanted.
    # There's no need to do this in our simple example - but it's an option.
    return component_value


# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run my_component/__init__.py`
if not _RELEASE:
    import streamlit as st

    st.subheader("CanvasXpress for Streamlit")

    # Create an instance of our component
    CXStreamlit(
        id="area1",
        data=json.dumps(
            {
                "y": {
                    "data": [[10, 100, 70, 130, 60]],
                    "vars": ["A"],
                    "smps": ["S1", "S2", "S3", "S4", "S5"],
                }
            }
        ),
        config=json.dumps(
            {
                "background": "rgb(255,255,255)",
                "colorScheme": "CanvasXpress",
                "graphOrientation": "vertical",
                "graphType": "Area",
                "objectBorderColor": False,
                "plotBox": False,
                "plotBoxColor": "rgb(204,204,204)",
                "showLegend": False,
                "showLegendBorder": True,
                "smpLabelRotate": 90,
                "smpTitle": "time",
                "xAxis": ["A"],
                "xAxisTickRightShow": False,
                "yAxisTickTopShow": False,
            }
        ),
        width="609",
        height="609",
    )
