"""
This module provides functionality for detecting the platform context that is active, such as RStudio.
"""
import os
from os import environ

CANVASXPRESS_TARGET_CONTEXT: str = "CANVASXPRESS_TARGET_CONTEXT"
"""
The ENV variable that can be set to indicate which context should be targetted regardless of what is detected.
Valid options are:

- shiny
- jupyter
- dash
- streamlit
- browser
"""

CONTEXT_BROWSER: str = "browser"
CONTEXT_DASH: str = "dash"
CONTEXT_JUPYTER: str = "jupyter"
CONTEXT_RSTUDIO: str = "rstudio"
CONTEXT_SHINY: str = "shiny"
CONTEXT_STREAMLIT: str = "streamlit"
CONTEXT_UNKNOWN: str = "UNKNOWN"

VALID_CONTEXTS: list = [
    CONTEXT_BROWSER,
    CONTEXT_DASH,
    CONTEXT_JUPYTER,
    CONTEXT_RSTUDIO,
    CONTEXT_SHINY,
    CONTEXT_STREAMLIT,
]


def is_rstudio_active() -> bool:
    """
    Indicates if RStudio is active at the time of function call.
    :returns" `bool` `True` if the RStudio IDE is running.
    """
    try:
        import shiny

        return bool(environ.get("RSTUDIO", False))

    except ModuleNotFoundError:
        return False


def is_shiny_available() -> bool:
    """
    Indicates if shiny is available at the time of function call.
    :returns" `bool` `True` if shiny is available.
    """
    try:
        import shiny

        return os.environ.get("SHINY_HOST") is not None

    except ModuleNotFoundError:
        return False


def is_dash_available() -> bool:
    """
    Indicates if dash is available at the time of function call.
    :returns" `bool` `True` if dash is available.
    """
    try:
        import dash

        return dash.get_app() is not None

    except ModuleNotFoundError:
        return False

    except Exception:
        return False


def is_ipython_available() -> bool:
    """
    Indicates if IPython is available at the time of function call.
    :returns" `bool` `True` if IPython is available.
    """
    try:
        from IPython import get_ipython

        return get_ipython().__class__.__name__ != "NoneType"

    except ModuleNotFoundError:
        return False

    except NameError:
        return False


def is_streamlit_available() -> bool:
    """
    Indicates if streamlit is available at the time of function call.
    :returns" `bool` `True` if streamlit is available.
    """
    try:
        import streamlit

        return True

    except ModuleNotFoundError:
        return False


def get_target_context() -> str:
    """
    Indicates the runtime context that should be targetted for illustrating charts.
    :returns" `str` One of the options for VALID_CONTEXTS.
    """
    target = environ.get(CANVASXPRESS_TARGET_CONTEXT)

    if target is not None:
        if target in VALID_CONTEXTS:
            return target

    else:
        if is_ipython_available():
            return CONTEXT_JUPYTER
        if is_dash_available():
            return CONTEXT_DASH
        if is_rstudio_active():
            return CONTEXT_RSTUDIO
        if is_shiny_available():
            return CONTEXT_SHINY
        if is_streamlit_available():
            return CONTEXT_STREAMLIT

        return CONTEXT_UNKNOWN
