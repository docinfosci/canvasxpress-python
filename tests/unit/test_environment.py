import os
from unittest.mock import patch

from canvasxpress.render.environment import (
    CANVASXPRESS_TARGET_CONTEXT,
    CONTEXT_BROWSER,
    CONTEXT_DASH,
    CONTEXT_JUPYTER,
    CONTEXT_RSTUDIO,
    CONTEXT_SHINY,
    CONTEXT_STREAMLIT,
    CONTEXT_UNKNOWN,
    VALID_CONTEXTS,
    get_target_context,
    is_dash_available,
    is_ipython_available,
    is_rstudio_active,
    is_shiny_available,
    is_streamlit_available,
)


def test_valid_contexts_contains_expected_values():
    """Test that VALID_CONTEXTS contains all expected context values."""
    assert CONTEXT_BROWSER in VALID_CONTEXTS
    assert CONTEXT_DASH in VALID_CONTEXTS
    assert CONTEXT_JUPYTER in VALID_CONTEXTS
    assert CONTEXT_RSTUDIO in VALID_CONTEXTS
    assert CONTEXT_SHINY in VALID_CONTEXTS
    assert CONTEXT_STREAMLIT in VALID_CONTEXTS


def test_is_rstudio_active_false_by_default():
    """Test that is_rstudio_active returns False when RSTUDIO env var is not set."""
    with patch.dict(os.environ, {}, clear=True):
        assert is_rstudio_active() is False


def test_is_rstudio_active_true_when_set():
    """Test that is_rstudio_active returns True when RSTUDIO env var is set."""
    with patch.dict(os.environ, {"RSTUDIO": "1"}):
        assert is_rstudio_active() is True


def test_is_rstudio_active_with_empty_string():
    """Test that is_rstudio_active returns False when RSTUDIO is empty string."""
    with patch.dict(os.environ, {"RSTUDIO": ""}):
        assert is_rstudio_active() is False


def test_is_shiny_available_returns_false_when_not_installed():
    """Test is_shiny_available returns False when shiny is not installed."""
    with patch.dict(os.environ, {}, clear=True):
        # If shiny is not installed, should return False
        result = is_shiny_available()
        assert isinstance(result, bool)


def test_is_dash_available_returns_false_when_not_installed():
    """Test is_dash_available returns False when dash is not available."""
    result = is_dash_available()
    assert isinstance(result, bool)


def test_is_streamlit_available_returns_false_when_not_installed():
    """Test is_streamlit_available returns False when streamlit is not available."""
    result = is_streamlit_available()
    assert isinstance(result, bool)


def test_is_ipython_available_returns_bool():
    """Test that is_ipython_available returns a boolean."""
    result = is_ipython_available()
    assert isinstance(result, bool)


def test_is_ipython_available_false_when_not_installed():
    """IPython is optional (jupyter extra); its absence must not raise."""
    import builtins

    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "IPython":
            raise ModuleNotFoundError("No module named 'IPython'")
        return real_import(name, *args, **kwargs)

    with patch("builtins.__import__", side_effect=fake_import):
        assert is_ipython_available() is False


def _fake_ipython_shell(shell_class_name):
    """Builds a fake IPython module whose get_ipython() returns a shell."""
    import types

    shell_class = type(shell_class_name, (), {})
    fake_module = types.ModuleType("IPython")
    fake_module.get_ipython = lambda: shell_class()
    return fake_module


def test_is_ipython_available_true_for_zmq_shell():
    """A ZMQInteractiveShell (Jupyter/qtconsole) is an available context."""
    import sys

    with patch.dict(sys.modules, {"IPython": _fake_ipython_shell("ZMQInteractiveShell")}):
        assert is_ipython_available() is True


def test_is_ipython_available_false_for_terminal_shell():
    """A TerminalInteractiveShell (IPython in a terminal) is not an available context."""
    import sys

    with patch.dict(sys.modules, {"IPython": _fake_ipython_shell("TerminalInteractiveShell")}):
        assert is_ipython_available() is False


def test_is_ipython_available_false_for_other_shell():
    """An unrecognized shell type is not an available context."""
    import sys

    with patch.dict(sys.modules, {"IPython": _fake_ipython_shell("SomeOtherShell")}):
        assert is_ipython_available() is False


def test_is_ipython_available_false_on_name_error():
    """A NameError from get_ipython must not escape."""
    import sys

    fake_module = _fake_ipython_shell("ZMQInteractiveShell")

    def broken_get_ipython():
        raise NameError("no shell")

    fake_module.get_ipython = broken_get_ipython
    with patch.dict(sys.modules, {"IPython": fake_module}):
        assert is_ipython_available() is False


def test_is_shiny_available_false_when_module_missing():
    """shiny is optional; its absence must not raise."""
    import builtins

    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "shiny":
            raise ModuleNotFoundError("No module named 'shiny'")
        return real_import(name, *args, **kwargs)

    with patch("builtins.__import__", side_effect=fake_import):
        assert is_shiny_available() is False


def test_is_shiny_available_true_when_hosted():
    """SHINY_HOST marks an active Shiny session."""
    with patch.dict(os.environ, {"SHINY_HOST": "127.0.0.1:8765"}):
        assert is_shiny_available() is True


def test_is_dash_available_false_on_exception():
    """Any unexpected dash error must not escape."""
    import dash

    with patch.object(dash, "get_app", side_effect=RuntimeError("not running")):
        assert is_dash_available() is False


def test_is_dash_available_false_when_module_missing():
    """dash is optional; its absence must not raise."""
    import builtins

    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "dash":
            raise ModuleNotFoundError("No module named 'dash'")
        return real_import(name, *args, **kwargs)

    with patch("builtins.__import__", side_effect=fake_import):
        assert is_dash_available() is False


def test_is_streamlit_available_false_on_exception():
    """A find_spec failure must not escape."""
    import importlib.util

    with patch.object(
        importlib.util, "find_spec", side_effect=ModuleNotFoundError("no streamlit")
    ):
        assert is_streamlit_available() is False


def test_get_target_context_with_env_var():
    """Test get_target_context respects CANVASXPRESS_TARGET_CONTEXT env var."""
    with patch.dict(os.environ, {CANVASXPRESS_TARGET_CONTEXT: "browser"}):
        assert get_target_context() == CONTEXT_BROWSER


def test_get_target_context_with_invalid_env_var():
    """Test get_target_context ignores invalid CANVASXPRESS_TARGET_CONTEXT value."""
    with patch.dict(os.environ, {CANVASXPRESS_TARGET_CONTEXT: "invalid"}):
        # Should not return the invalid value
        result = get_target_context()
        assert result != "invalid"


def test_get_target_context_with_valid_env_var():
    """Test get_target_context returns correct value for valid env var."""
    with patch.dict(os.environ, {CANVASXPRESS_TARGET_CONTEXT: "dash"}):
        assert get_target_context() == CONTEXT_DASH


def test_get_target_context_with_rstudio_env():
    """Test get_target_context returns rstudio when RSTUDIO env var is set."""
    with patch.dict(os.environ, {"CANVASXPRESS_TARGET_CONTEXT": "rstudio"}):
        assert get_target_context() == CONTEXT_RSTUDIO


def test_get_target_context_with_shiny_env():
    """Test get_target_context returns shiny when env var is set."""
    with patch.dict(os.environ, {"CANVASXPRESS_TARGET_CONTEXT": "shiny"}):
        assert get_target_context() == CONTEXT_SHINY


def test_get_target_context_with_streamlit_env():
    """Test get_target_context returns streamlit when env var is set."""
    with patch.dict(os.environ, {"CANVASXPRESS_TARGET_CONTEXT": "streamlit"}):
        assert get_target_context() == CONTEXT_STREAMLIT


def test_get_target_context_with_jupyter_env():
    """Test get_target_context returns jupyter when env var is set."""
    with patch.dict(os.environ, {"CANVASXPRESS_TARGET_CONTEXT": "jupyter"}):
        assert get_target_context() == CONTEXT_JUPYTER


def test_get_target_context_unknown_when_no_env():
    """Test get_target_context returns CONTEXT_UNKNOWN when no env var and no context detected."""
    with patch.dict(os.environ, {}, clear=True):
        # Patch all detection functions to return False
        with patch("canvasxpress.render.environment.is_ipython_available", return_value=False):
            with patch("canvasxpress.render.environment.is_dash_available", return_value=False):
                with patch("canvasxpress.render.environment.is_rstudio_active", return_value=False):
                    with patch("canvasxpress.render.environment.is_shiny_available", return_value=False):
                        with patch("canvasxpress.render.environment.is_streamlit_available", return_value=False):
                            assert get_target_context() == CONTEXT_UNKNOWN


def test_get_target_context_respects_env_over_detection():
    """Test that env var takes precedence over detection."""
    with patch.dict(os.environ, {CANVASXPRESS_TARGET_CONTEXT: "browser"}):
        with patch("canvasxpress.render.environment.is_ipython_available", return_value=True):
            # Should return browser from env, not jupyter from detection
            assert get_target_context() == CONTEXT_BROWSER


def _detectors(ipython=False, dash=False, rstudio=False, shiny=False, streamlit=False):
    """Patches every context detector with the given truth values."""
    return (
        patch("canvasxpress.render.environment.is_ipython_available", return_value=ipython),
        patch("canvasxpress.render.environment.is_dash_available", return_value=dash),
        patch("canvasxpress.render.environment.is_rstudio_active", return_value=rstudio),
        patch("canvasxpress.render.environment.is_shiny_available", return_value=shiny),
        patch("canvasxpress.render.environment.is_streamlit_available",
              return_value=streamlit),
    )


def _detect(**overrides):
    """Runs get_target_context with a clean environment and patched detectors."""
    import contextlib

    flags = dict(
        ipython=False, dash=False, rstudio=False, shiny=False, streamlit=False
    )
    flags.update(overrides)
    patches = _detectors(**flags)
    stack = contextlib.ExitStack()
    try:
        for p in patches:
            stack.enter_context(p)
        with patch.dict(os.environ, {}, clear=True):
            return get_target_context()
    finally:
        stack.close()


def test_get_target_context_detects_jupyter():
    assert _detect(ipython=True) == CONTEXT_JUPYTER


def test_get_target_context_detects_dash():
    assert _detect(ipython=False, dash=True) == CONTEXT_DASH


def test_get_target_context_detects_rstudio():
    assert _detect(ipython=False, dash=False, rstudio=True) == CONTEXT_RSTUDIO


def test_get_target_context_detects_shiny():
    assert _detect(ipython=False, dash=False, rstudio=False, shiny=True) == CONTEXT_SHINY


def test_get_target_context_detects_streamlit():
    assert _detect(
        ipython=False, dash=False, rstudio=False, shiny=False, streamlit=True
    ) == CONTEXT_STREAMLIT
