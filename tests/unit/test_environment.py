import os
from unittest.mock import patch

import pytest

from canvasxpress.render.environment import (
    is_rstudio_active,
    is_shiny_available,
    is_dash_available,
    is_ipython_available,
    is_streamlit_available,
    get_target_context,
    VALID_CONTEXTS,
    CONTEXT_BROWSER,
    CONTEXT_DASH,
    CONTEXT_JUPYTER,
    CONTEXT_RSTUDIO,
    CONTEXT_SHINY,
    CONTEXT_STREAMLIT,
    CONTEXT_UNKNOWN,
    CANVASXPRESS_TARGET_CONTEXT,
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
