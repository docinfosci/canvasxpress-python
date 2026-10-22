"""Tests for platform/browser detection utilities."""

from unittest.mock import patch

import pytest

from canvasxpress.context.platform import (
    detect_os,
    parse_browser_name,
    detect_browser_installed,
    BROWSER_DETECTORS,
)


class TestDetectOs:
    """Test detect_os function."""

    @patch("canvasxpress.context.platform.platform")
    def test_detects_macos(self, mock_platform):
        mock_platform.system.return_value = "Darwin"
        mock_platform.platform.return_value = "macOS-14-arm64"
        assert detect_os() == "Mac OS"

    @patch("canvasxpress.context.platform.platform")
    def test_detects_ios(self, mock_platform):
        mock_platform.system.return_value = "Darwin"
        mock_platform.platform.return_value = "iOS-17-0"
        assert detect_os() == "iOS"

    @patch("canvasxpress.context.platform.platform")
    def test_detects_windows(self, mock_platform):
        mock_platform.system.return_value = "Windows"
        assert detect_os() == "Windows"

    @patch("canvasxpress.context.platform.platform")
    def test_detects_linux(self, mock_platform):
        mock_platform.system.return_value = "Linux"
        assert detect_os() == "Linux"

    @patch("canvasxpress.context.platform.platform")
    def test_detects_android(self, mock_platform):
        mock_platform.system.return_value = "Linux"
        with patch.dict("os.environ", {"ANDROID_ROOT": "/system"}):
            assert detect_os() == "Android"

    @patch("canvasxpress.context.platform.platform")
    def test_detects_unknown(self, mock_platform):
        mock_platform.system.return_value = "UnknownPlatform"
        result = detect_os()
        assert "Unknown" in result


class TestParseBrowserName:
    """Test parse_browser_name function."""

    def test_chrome(self):
        assert parse_browser_name("/Applications/Google Chrome.app") == "Chrome"

    def test_safari(self):
        assert parse_browser_name("/Applications/Safari.app") == "Safari"

    def test_firefox(self):
        assert parse_browser_name("/Applications/Firefox.app") == "Firefox"

    def test_edge(self):
        assert parse_browser_name("/Applications/Microsoft Edge.app") == "Microsoft Edge"

    def test_chromium(self):
        assert parse_browser_name("/Applications/Chromium.app") == "Chromium"

    def test_unknown_path(self):
        assert parse_browser_name("/Applications/UnknownApp.app") == "CanvasXpress"

    def test_empty_path_returns_unknown(self):
        assert parse_browser_name("") == "CanvasXpress"


class TestDetectBrowserInstalled:
    """Test detect_browser_installed function."""

    @patch("canvasxpress.context.platform.installed_browsers", None)
    def test_returns_unknown_when_not_installed(self):
        """When installed_browsers is not available, should return unknown browser tuple."""
        result = detect_browser_installed()
        assert result == ("CanvasXpress", "0")


class TestBrowserDetectors:
    """Test BROWSER_DETECTORS mapping."""

    def test_detectors_is_dict(self):
        assert isinstance(BROWSER_DETECTORS, dict)

    def test_detectors_has_defaults(self):
        # Should have the three platform detectors
        assert len(BROWSER_DETECTORS) >= 3
