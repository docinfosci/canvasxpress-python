"""Tests for platform/browser detection utilities."""

import ctypes
import plistlib
import subprocess
import sys
from types import SimpleNamespace
from unittest.mock import patch

import canvasxpress.context.platform as platform_module
from canvasxpress.context.platform import (
    BROWSER_DETECTORS,
    UNKNOWN_BROWSER,
    UNKNOWN_VERSION,
    app_version_macos,
    browser_version_linux,
    browser_version_windows,
    detect_browser,
    detect_browser_installed,
    detect_browser_linux,
    detect_browser_macos,
    detect_browser_windows,
    detect_os,
    get_exec_from_desktop,
    get_file_version,
    parse_browser_name,
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


def _write_plist(path, contents):
    """Writes a binary plist file to path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as file_handle:
        plistlib.dump(contents, file_handle)


class TestAppVersionMacOS:
    """Test app_version_macos function."""

    def test_none_path_returns_unknown(self):
        assert app_version_macos(None) == UNKNOWN_VERSION

    def test_missing_app_returns_unknown(self):
        assert app_version_macos("/nonexistent/Fake.app") == UNKNOWN_VERSION

    def test_reads_version_from_info_plist(self, tmp_path):
        _write_plist(
            tmp_path / "Fake.app" / "Contents" / "Info.plist",
            {"CFBundleShortVersionString": "1.2.3"},
        )
        assert app_version_macos(str(tmp_path / "Fake.app")) == "1.2.3"

    def test_info_plist_without_version(self, tmp_path):
        _write_plist(tmp_path / "Fake.app" / "Contents" / "Info.plist", {"Foo": "bar"})
        assert app_version_macos(str(tmp_path / "Fake.app")) == UNKNOWN_VERSION

    def test_corrupt_info_plist(self, tmp_path):
        info_plist = tmp_path / "Fake.app" / "Contents" / "Info.plist"
        info_plist.parent.mkdir(parents=True, exist_ok=True)
        info_plist.write_bytes(b"this is not a plist")
        assert app_version_macos(str(tmp_path / "Fake.app")) == UNKNOWN_VERSION


class TestDetectBrowserMacOS:
    """Test detect_browser_macos function."""

    def test_missing_launch_services_returns_unknown(self, tmp_path):
        with patch("os.path.expanduser", return_value=str(tmp_path / "missing.plist")):
            assert detect_browser_macos() == UNKNOWN_BROWSER

    def test_corrupt_launch_services_returns_unknown(self, tmp_path):
        plist_path = tmp_path / "launchservices.secure.plist"
        plist_path.write_bytes(b"this is not a plist")
        with patch("os.path.expanduser", return_value=str(plist_path)):
            assert detect_browser_macos() == UNKNOWN_BROWSER

    def test_finds_http_handler(self, tmp_path):
        plist_path = tmp_path / "launchservices.secure.plist"
        _write_plist(
            plist_path,
            {
                "LSHandlers": [
                    {"LSHandlerURLScheme": "https", "LSHandlerRoleAll": "com.apple.Safari"},
                    {"LSHandlerURLScheme": "http", "LSHandlerRoleAll": "com.google.Chrome"},
                ]
            },
        )
        with patch("os.path.expanduser", return_value=str(plist_path)):
            name, _version = detect_browser_macos()
        assert name == "Chrome"

    def test_unknown_http_handler_returns_unknown(self, tmp_path):
        plist_path = tmp_path / "launchservices.secure.plist"
        _write_plist(
            plist_path,
            {
                "LSHandlers": [
                    {"LSHandlerURLScheme": "http", "LSHandlerRoleAll": "com.example.custom"},
                ]
            },
        )
        with patch("os.path.expanduser", return_value=str(plist_path)):
            assert detect_browser_macos() == UNKNOWN_BROWSER


class _FakeWinreg:
    """A stand-in for the winreg module, backed by a dict of registry values."""

    HKEY_CURRENT_USER = "HKCU"
    HKEY_CLASSES_ROOT = "HKCR"

    def __init__(self, entries):
        self._entries = entries
        self._opened = None

    def OpenKey(self, root, path):
        if (root, path) not in self._entries:
            raise OSError("registry key not found")
        self._opened = (root, path)
        return self

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        return False

    def QueryValueEx(self, key, name):
        return (self._entries[self._opened][name], 0)


class TestDetectBrowserWindows:
    """Test detect_browser_windows function (via a fake winreg module)."""

    @staticmethod
    def _user_choice_path():
        return r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice"

    def test_user_choice_prog_id(self, monkeypatch):
        fake = _FakeWinreg(
            {
                (_FakeWinreg.HKEY_CURRENT_USER, self._user_choice_path()): {
                    "ProgId": "ChromeHTML"
                }
            }
        )
        monkeypatch.setattr(platform_module, "winreg", fake)
        with patch.object(platform_module, "browser_version_windows", return_value="1.2"):
            assert detect_browser_windows() == ("Chrome", "1.2")

    def test_fallback_to_classes_root_command(self, monkeypatch):
        fake = _FakeWinreg(
            {
                (_FakeWinreg.HKEY_CLASSES_ROOT, r"http\shell\open\command"): {
                    "": "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
                }
            }
        )
        monkeypatch.setattr(platform_module, "winreg", fake)
        with patch.object(platform_module, "browser_version_windows", return_value="1.2"):
            assert detect_browser_windows() == ("Firefox", "1.2")

    def test_no_registry_access_returns_unknown(self, monkeypatch):
        monkeypatch.setattr(platform_module, "winreg", None)
        assert detect_browser_windows() == UNKNOWN_BROWSER

    def test_unknown_prog_id_returns_unknown(self, monkeypatch):
        fake = _FakeWinreg(
            {
                (_FakeWinreg.HKEY_CURRENT_USER, self._user_choice_path()): {
                    "ProgId": "SomeCustomHandler"
                }
            }
        )
        monkeypatch.setattr(platform_module, "winreg", fake)
        assert detect_browser_windows() == UNKNOWN_BROWSER


class TestBrowserVersionWindows:
    """Test browser_version_windows function (via a fake winreg module)."""

    def test_app_path_from_registry(self, monkeypatch):
        fake = _FakeWinreg(
            {(_FakeWinreg.HKEY_CLASSES_ROOT, "ChromeHTML\\Application"): {"": "C:\\chrome.exe"}}
        )
        monkeypatch.setattr(platform_module, "winreg", fake)
        monkeypatch.setattr(platform_module, "get_file_version", lambda path: "120.0.1")
        assert browser_version_windows("ChromeHTML") == "120.0.1"

    def test_command_with_quoted_path(self, monkeypatch):
        fake = _FakeWinreg(
            {
                (
                    _FakeWinreg.HKEY_CLASSES_ROOT,
                    "MyBrowser\\shell\\open\\command",
                ): {"": '"C:\\Program Files\\mybrowser.exe" --flag'}
            }
        )
        monkeypatch.setattr(platform_module, "winreg", fake)
        seen = {}

        def fake_version(path):
            seen["path"] = path
            return "9.9"

        monkeypatch.setattr(platform_module, "get_file_version", fake_version)
        assert browser_version_windows("MyBrowser") == "9.9"
        assert seen["path"] == "C:\\Program Files\\mybrowser.exe"

    def test_command_without_quotes(self, monkeypatch):
        fake = _FakeWinreg(
            {
                (
                    _FakeWinreg.HKEY_CLASSES_ROOT,
                    "MyBrowser\\shell\\open\\command",
                ): {"": "C:\\mybrowser.exe --flag"}
            }
        )
        monkeypatch.setattr(platform_module, "winreg", fake)
        seen = {}

        def fake_version(path):
            seen["path"] = path
            return "9.9"

        monkeypatch.setattr(platform_module, "get_file_version", fake_version)
        assert browser_version_windows("MyBrowser") == "9.9"
        assert seen["path"] == "C:\\mybrowser.exe"

    def test_empty_command_returns_unknown(self, monkeypatch):
        fake = _FakeWinreg(
            {
                (
                    _FakeWinreg.HKEY_CLASSES_ROOT,
                    "MyBrowser\\shell\\open\\command",
                ): {"": ""}
            }
        )
        monkeypatch.setattr(platform_module, "winreg", fake)
        assert browser_version_windows("MyBrowser") == UNKNOWN_VERSION

    def test_no_registry_access_returns_unknown(self, monkeypatch):
        monkeypatch.setattr(platform_module, "winreg", None)
        assert browser_version_windows("ChromeHTML") == UNKNOWN_VERSION


class TestGetFileVersion:
    """Test get_file_version function (via a fake Windows DLL)."""

    @staticmethod
    def _make_fake_dll(size, version_bytes):
        version_dll = SimpleNamespace()

        def get_size(path, _unused):
            return size

        def get_info(path, _extra, _size, _buf):
            return 0

        def query_value(buf, _query, p, length):
            # p and length are byref proxies; write through to the originals.
            if version_bytes is not None:
                p._obj.value = ctypes.addressof(version_bytes)
                length._obj.value = ctypes.sizeof(version_bytes)
            return 1 if version_bytes is not None else 0

        version_dll.GetFileVersionInfoSizeW = get_size
        version_dll.GetFileVersionInfoW = get_info
        version_dll.VerQueryValueW = query_value
        return SimpleNamespace(version=version_dll)

    def test_no_version_info_returns_unknown(self, monkeypatch):
        monkeypatch.setattr(ctypes, "windll", self._make_fake_dll(0, None), raising=False)
        assert get_file_version("anything") == UNKNOWN_VERSION

    def test_failed_query_returns_unknown(self, monkeypatch):
        monkeypatch.setattr(ctypes, "windll", self._make_fake_dll(16, None), raising=False)
        assert get_file_version("anything") == UNKNOWN_VERSION

    def test_reads_version_info(self, monkeypatch):
        # VERSIONINFO fixed section: dwMajorMinor and dwBuildVersion words.
        info = (ctypes.c_uint32 * 17)()
        info[2] = (1 << 16) | 2
        info[3] = (3 << 16) | 4
        fake_dll = self._make_fake_dll(ctypes.sizeof(info), info)
        monkeypatch.setattr(ctypes, "windll", fake_dll, raising=False)
        assert get_file_version("anything") == "1.2.3.4"

    def test_unavailable_platform_returns_unknown(self):
        # Without a patched windll, non-Windows platforms hit the error path.
        if not hasattr(ctypes, "windll"):
            assert get_file_version("anything") == UNKNOWN_VERSION


class TestDetectBrowserLinux:
    """Test detect_browser_linux function."""

    def test_env_browser_recognized(self, monkeypatch):
        monkeypatch.setenv("BROWSER", "firefox")
        result = detect_browser_linux()
        assert result[0] == "Firefox"

    def test_env_browser_unrecognized_falls_through(self, monkeypatch):
        monkeypatch.setenv("BROWSER", "totally-unknown-browser")
        with patch.object(
            platform_module.subprocess, "run", side_effect=OSError("no xdg-mime")
        ):
            assert detect_browser_linux() == UNKNOWN_BROWSER

    def test_xdg_mime_without_desktop_file(self, monkeypatch):
        monkeypatch.delenv("BROWSER", raising=False)
        with patch.object(
            platform_module.subprocess,
            "run",
            return_value=SimpleNamespace(stdout="", stderr=""),
        ):
            assert detect_browser_linux() == UNKNOWN_BROWSER

    def test_xdg_mime_with_executable(self, monkeypatch):
        monkeypatch.delenv("BROWSER", raising=False)

        def fake_run(command, **kwargs):
            if command[0] == "xdg-mime":
                return SimpleNamespace(stdout="fake-firefox.desktop\n", stderr="")
            return SimpleNamespace(stdout="Mozilla Firefox 121.0\n", stderr="")

        with patch.object(platform_module.subprocess, "run", side_effect=fake_run), \
             patch.object(
                 platform_module, "get_exec_from_desktop",
                 return_value="/usr/bin/firefox",
             ):
            assert detect_browser_linux() == ("Firefox", "121.0")

    def test_xdg_mime_missing(self, monkeypatch):
        monkeypatch.delenv("BROWSER", raising=False)
        with patch.object(
            platform_module.subprocess, "run", side_effect=OSError("no xdg-mime")
        ):
            assert detect_browser_linux() == UNKNOWN_BROWSER


class TestGetExecFromDesktop:
    """Test get_exec_from_desktop function."""

    def test_found_in_user_applications(self, tmp_path):
        applications = tmp_path / ".local" / "share" / "applications"
        applications.mkdir(parents=True)
        (applications / "test-browser.desktop").write_text(
            "[Desktop Entry]\nExec=google-chrome --new-window %U\n"
        )
        with patch("os.path.expanduser", return_value=str(applications)):
            assert get_exec_from_desktop("test-browser.desktop") == "google-chrome"

    def test_not_found(self, tmp_path):
        with patch("os.path.expanduser", return_value=str(tmp_path)):
            assert get_exec_from_desktop("missing.desktop") is None

    def test_empty_exec_line(self, tmp_path):
        applications = tmp_path / "applications"
        applications.mkdir(parents=True)
        (applications / "empty.desktop").write_text("[Desktop Entry]\nExec=\n")
        with patch("os.path.expanduser", return_value=str(applications)):
            assert get_exec_from_desktop("empty.desktop") is None

    def test_unreadable_entry(self, tmp_path):
        # A directory with a .desktop name exists but cannot be opened as a file.
        blocker = tmp_path / "blocked.desktop"
        blocker.mkdir()
        with patch("os.path.expanduser", return_value=str(tmp_path)):
            assert get_exec_from_desktop("blocked.desktop") is None


class TestBrowserVersionLinux:
    """Test browser_version_linux function."""

    def test_parses_version_from_python(self):
        # The Python interpreter always answers --version with a version string.
        result = browser_version_linux(sys.executable)
        assert result.startswith("3.")

    def test_missing_command_returns_unknown(self):
        assert browser_version_linux("/nonexistent/browser") == UNKNOWN_VERSION

    def test_timeout_returns_unknown(self):
        with patch.object(
            platform_module.subprocess,
            "run",
            side_effect=subprocess.TimeoutExpired("browser", 5),
        ):
            assert browser_version_linux("anything") == UNKNOWN_VERSION

    def test_no_version_in_output(self):
        with patch.object(
            platform_module.subprocess,
            "run",
            return_value=SimpleNamespace(stdout="no digits here\n", stderr=""),
        ):
            assert browser_version_linux("anything") == UNKNOWN_VERSION


class TestDetectBrowserInstalledExpanded:
    """Test detect_browser_installed with a fake installed_browsers module."""

    def test_finds_default_browser(self):
        fake_module = SimpleNamespace(
            what_is_the_default_browser=lambda: "Firefox",
            browsers=lambda: [
                {"name": "firefox", "description": "Mozilla Firefox", "version": "121.0"},
                {"name": "chrome", "description": "Google Chrome", "version": "120.0"},
            ],
        )
        with patch.object(platform_module, "installed_browsers", fake_module):
            assert detect_browser_installed() == ("Mozilla Firefox", "121.0")

    def test_no_default_browser(self):
        fake_module = SimpleNamespace(
            what_is_the_default_browser=lambda: None,
            browsers=lambda: [],
        )
        with patch.object(platform_module, "installed_browsers", fake_module):
            assert detect_browser_installed() == UNKNOWN_BROWSER

    def test_default_not_in_browser_list(self):
        fake_module = SimpleNamespace(
            what_is_the_default_browser=lambda: "opera",
            browsers=lambda: [
                {"name": "firefox", "description": "Mozilla Firefox", "version": "121.0"},
            ],
        )
        with patch.object(platform_module, "installed_browsers", fake_module):
            assert detect_browser_installed() == UNKNOWN_BROWSER

    def test_missing_version_uses_unknown(self):
        fake_module = SimpleNamespace(
            what_is_the_default_browser=lambda: "Brave",
            browsers=lambda: [{"name": "brave-browser", "description": "Brave"}],
        )
        with patch.object(platform_module, "installed_browsers", fake_module):
            assert detect_browser_installed() == ("Brave", UNKNOWN_VERSION)

    def test_exception_returns_unknown(self):
        def broken():
            raise RuntimeError("boom")

        fake_module = SimpleNamespace(
            what_is_the_default_browser=broken,
            browsers=lambda: [],
        )
        with patch.object(platform_module, "installed_browsers", fake_module):
            assert detect_browser_installed() == UNKNOWN_BROWSER


class TestDetectBrowser:
    """Test the top-level detect_browser function.

    BROWSER_DETECTORS holds direct function references, so the detectors are
    substituted by patching the dict's entries rather than module attributes.
    """

    @staticmethod
    def _patched_detector(result=None, error=None):
        def detector():
            if error is not None:
                raise error
            return result

        return detector

    def test_uses_platform_detector(self):
        with patch.object(platform_module, "platform") as mock_platform, \
             patch.dict(
                 platform_module.BROWSER_DETECTORS,
                 {"Linux": self._patched_detector(result=("Firefox", "1.2"))},
             ), \
             patch.object(
                 platform_module, "detect_browser_installed", return_value=("CanvasXpress", "0")
             ):
            mock_platform.system.return_value = "Linux"
            assert detect_browser() == ("Firefox", "1.2")

    def test_falls_back_to_installed_browsers(self):
        with patch.object(platform_module, "platform") as mock_platform, \
             patch.dict(
                 platform_module.BROWSER_DETECTORS,
                 {"Linux": self._patched_detector(result=UNKNOWN_BROWSER)},
             ), \
             patch.object(
                 platform_module, "detect_browser_installed", return_value=("Opera", "2.0")
             ):
            mock_platform.system.return_value = "Linux"
            assert detect_browser() == ("Opera", "2.0")

    def test_detector_exception_falls_back(self):
        with patch.object(platform_module, "platform") as mock_platform, \
             patch.dict(
                 platform_module.BROWSER_DETECTORS,
                 {"Linux": self._patched_detector(error=OSError("boom"))},
             ), \
             patch.object(
                 platform_module, "detect_browser_installed", return_value=("Lynx", "3.0")
             ):
            mock_platform.system.return_value = "Linux"
            assert detect_browser() == ("Lynx", "3.0")

    def test_unknown_system_uses_installed_browsers(self):
        with patch.object(platform_module, "platform") as mock_platform, \
             patch.object(
                 platform_module, "detect_browser_installed", return_value=("w3m", "4.0")
             ):
            mock_platform.system.return_value = "Solaris"
            assert detect_browser() == ("w3m", "4.0")
