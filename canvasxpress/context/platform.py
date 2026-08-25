import ctypes
import os
import platform
import plistlib
import re
import subprocess
from typing import Tuple, Union

try:
    import winreg
except ImportError:
    winreg = None

try:
    import installed_browsers
except ImportError:
    installed_browsers = None

UNKNOWN_BROWSER_NAME = "CanvasXpress"
UNKNOWN_VERSION = "0"
UNKNOWN_BROWSER = (UNKNOWN_BROWSER_NAME, UNKNOWN_VERSION)

# macOS browser bundle identifiers mapped to (name, application path).
BROWSER_APPS_MACOS = {
    "com.google.Chrome": ("Chrome", "/Applications/Google Chrome.app"),
    "com.apple.Safari": ("Safari", "/Applications/Safari.app"),
    "org.mozilla.firefox": ("Firefox", "/Applications/Firefox.app"),
    "com.microsoft.edgemac": (
        "Microsoft Edge",
        "/Applications/Microsoft Edge.app",
    ),
    "com.brave.browser": ("Brave", "/Applications/Brave Browser.app"),
    "com.operasoftware.Opera": ("Opera", "/Applications/Opera.app"),
}

# Windows ProgId substrings mapped to browser names.
BROWSER_PROGIDS = {
    "chrome": "Chrome",
    "firefox": "Firefox",
    "mse": "Microsoft Edge",
    "edge": "Microsoft Edge",
    "ie": "Internet Explorer",
    "opera": "Opera",
    "brave": "Brave",
}

# Linux command/file basename substrings mapped to browser names.
BROWSER_NAMES = [
    ("chrome", "Chrome"),
    ("chromium", "Chromium"),
    ("firefox", "Firefox"),
    ("mozilla", "Firefox"),
    ("edge", "Microsoft Edge"),
    ("opera", "Opera"),
    ("brave", "Brave"),
    ("safari", "Safari"),
    ("lynx", "Lynx"),
    ("w3m", "w3m"),
]

# HTML entities used by CanvasXpress for macOS modifier keys.
MACOS_KEY_SYMBOLS = {
    "alt": "&#8997;",
    "command": "&#8984;",
    "control": "&#8963;",
    "shift": "&#8679;",
}

# Plain-text modifier key labels used on Windows and Linux.
DEFAULT_KEY_SYMBOLS = {
    "alt": "Alt",
    "command": "Win",
    "control": "Ctrl",
    "shift": "Shift",
}


def detect_os() -> str:
    """
    Detects the operating system name, matching the values used by the
    CanvasXpress JS export (Mac OS, iOS, Windows, Android, Linux).

    Returns:
        Operating system name.
    """
    system = platform.system()
    if system == "Windows":
        return "Windows"
    elif system == "Darwin":
        return "iOS" if "iOS" in platform.platform() else "Mac OS"
    elif system == "Linux":
        return (
            "Android"
            if "ANDROID_ROOT" in os.environ or "ANDROID_DATA" in os.environ
            else "Linux"
        )
    else:
        return system


def detect_browser_macos() -> Tuple[str, str]:
    """
    Detects the default web browser on macOS by reading the LaunchServices preferences.

    Reads the com.apple.launchservices.secure.plist file to find the bundle
    identifier of the default HTTP handler, maps it to a known browser name,
    and retrieves the version from the application's Info.plist.

    Returns:
        A tuple of (browser_name, browser_version).
    """
    launch_services_path = os.path.expanduser(
        "~/Library/Preferences/com.apple.LaunchServices/"
        "com.apple.launchservices.secure.plist"
    )
    if not os.path.exists(launch_services_path):
        return UNKNOWN_BROWSER

    try:
        with open(launch_services_path, "rb") as file_handle:
            launch_services_plist = plistlib.load(file_handle)
    except (OSError, plistlib.Error):
        return UNKNOWN_BROWSER

    for handler in launch_services_plist.get("LSHandlers", []):
        if handler.get("LSHandlerURLScheme") != "http":
            continue
        app_info = BROWSER_APPS_MACOS.get(handler.get("LSHandlerRoleAll"))
        if app_info is not None:
            browser_name, app_path = app_info
            return browser_name, app_version_macos(app_path)
    return UNKNOWN_BROWSER


def app_version_macos(app_path: Union[str, None]) -> str:
    """
    Retrieves the version string from a macOS application's Info.plist.

    Args:
        app_path: The path to the .app bundle directory, or None.

    Returns:
        The CFBundleShortVersionString value, or UNKNOWN_VERSION if not found.
    """
    if not app_path:
        return UNKNOWN_VERSION
    info_plist_path = os.path.join(app_path, "Contents/Info.plist")
    if not os.path.exists(info_plist_path):
        return UNKNOWN_VERSION
    try:
        with open(info_plist_path, "rb") as file_handle:
            info_plist_data = plistlib.load(file_handle)
        return info_plist_data.get("CFBundleShortVersionString", UNKNOWN_VERSION)
    except (OSError, plistlib.Error):
        return UNKNOWN_VERSION


def get_file_version(file_path: str) -> str:
    """
    Retrieves the file version string from a Windows executable using ctypes.

    Args:
        file_path: Absolute path to the executable.

    Returns:
        The file version string (e.g. '120.0.6099.109'), or UNKNOWN_VERSION if unavailable.
    """
    try:
        size = ctypes.windll.version.GetFileVersionInfoSizeW(file_path, None)
        if not size:
            return UNKNOWN_VERSION
        buf = ctypes.create_string_buffer(size)
        ctypes.windll.version.GetFileVersionInfoW(file_path, 0, size, buf)
        p = ctypes.c_void_p()
        length = ctypes.c_uint()
        success = ctypes.windll.version.VerQueryValueW(
            buf, r"\\", ctypes.byref(p), ctypes.byref(length)
        )
        if not success:
            return UNKNOWN_VERSION
        info = ctypes.cast(p, ctypes.POINTER(ctypes.c_uint32 * 17)).contents
        major = (info[2] >> 16) & 0xFFFF
        minor = info[2] & 0xFFFF
        build = (info[3] >> 16) & 0xFFFF
        revision = info[3] & 0xFFFF
        return f"{major}.{minor}.{build}.{revision}".rstrip(".0")
    except (AttributeError, OSError):
        return UNKNOWN_VERSION


def detect_browser_windows() -> Tuple[str, str]:
    """
    Detects the default web browser on Windows by reading the registry.

    Checks HKCU\\UserChoice for the ProgId of the default HTTP handler,
    then maps the ProgId to a known browser name. Falls back to
    reading the command from HKCR\\http\\shell\\open\\command.

    Returns:
        A tuple of (browser_name, browser_version).
    """
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice",
        ) as key:
            prog_id, _ = winreg.QueryValueEx(key, "ProgId")
    except (AttributeError, OSError):
        try:
            with winreg.OpenKey(
                winreg.HKEY_CLASSES_ROOT,
                r"http\shell\open\command",
            ) as key:
                command, _ = winreg.QueryValueEx(key, "")
                prog_id = command
        except (AttributeError, OSError):
            return UNKNOWN_BROWSER

    prog_id_lower = (prog_id or "").lower()
    for key, name in BROWSER_PROGIDS.items():
        if key in prog_id_lower:
            return name, browser_version_windows(prog_id)
    return UNKNOWN_BROWSER


def browser_version_windows(prog_id: str) -> str:
    """
    Retrieves the version of a Windows browser given its ProgId.

    Attempts to find the application path from the registry and then
    read the version information from the executable file.

    Args:
        prog_id: The ProgId string (e.g. 'ChromeHTML').

    Returns:
        The version string, or UNKNOWN_VERSION if not found.
    """
    app_path = None
    try:
        with winreg.OpenKey(
            winreg.HKEY_CLASSES_ROOT,
            f"{prog_id}\\Application",
        ) as key:
            app_path, _ = winreg.QueryValueEx(key, "")
    except (AttributeError, OSError):
        try:
            with winreg.OpenKey(
                winreg.HKEY_CLASSES_ROOT,
                f"{prog_id}\\shell\\open\\command",
            ) as key:
                command, _ = winreg.QueryValueEx(key, "")
                if command:
                    app_path = (
                        command.split('"')[1]
                        if '"' in command
                        else command.split()[0]
                    )
        except (AttributeError, OSError):
            return UNKNOWN_VERSION

    if app_path:
        return get_file_version(app_path)
    return UNKNOWN_VERSION


def detect_browser_linux() -> Tuple[str, str]:
    """
    Detects the default web browser on Linux.

    Checks the BROWSER environment variable first. If not set, uses
    xdg-mime to query the default handler for the http scheme and
    parses the associated .desktop file for the browser name.

    Returns:
        A tuple of (browser_name, browser_version).
    """
    env_browser = os.environ.get("BROWSER")
    if env_browser:
        browser_command = env_browser.split(":", 1)[0].strip().split()
        if browser_command:
            browser_name = parse_browser_name(browser_command[0])
            if browser_name != UNKNOWN_BROWSER_NAME:
                return browser_name, browser_version_linux(browser_command[0])

    try:
        result = subprocess.run(
            ["xdg-mime", "query", "default", "x-scheme-handler/http"],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return UNKNOWN_BROWSER

    desktop_file = result.stdout.strip()
    if desktop_file:
        exec_path = get_exec_from_desktop(desktop_file)
        if exec_path:
            browser_name = parse_browser_name(exec_path)
            if browser_name != UNKNOWN_BROWSER_NAME:
                return browser_name, browser_version_linux(exec_path)
    return UNKNOWN_BROWSER


def get_exec_from_desktop(desktop_file: str) -> Union[str, None]:
    """
    Extracts the executable command from the Exec= line of a Linux .desktop file.

    Searches standard application directories for the desktop file and returns
    the first token of the Exec value after removing common placeholders.

    Args:
        desktop_file: Filename of the .desktop entry (e.g. 'firefox.desktop').

    Returns:
        The executable path/command string, or None if not found.
    """
    search_dirs = [
        "/usr/share/applications",
        "/usr/local/share/applications",
        os.path.expanduser("~/.local/share/applications"),
    ]
    for search_dir in search_dirs:
        file_path = os.path.join(search_dir, desktop_file)
        if not os.path.exists(file_path):
            continue
        try:
            with open(file_path) as file_handle:
                for line in file_handle:
                    if line.startswith("Exec="):
                        command = line.split("=", 1)[1].strip().split()
                        return command[0] if command else None
        except OSError:
            continue
    return None


def parse_browser_name(path: str) -> str:
    """
    Extracts a human-readable browser name from a file path or command name.

    Args:
        path: A file path or command name containing a browser identifier.

    Returns:
        A human-readable browser name (e.g. 'Chrome', 'Firefox'),
        or UNKNOWN_BROWSER_NAME if no known browser is recognized.
    """
    basename = os.path.basename(path).lower()
    for key, name in BROWSER_NAMES:
        if key in basename:
            return name
    return UNKNOWN_BROWSER_NAME


def browser_version_linux(browser_command: str) -> str:
    """
    Retrieves the version of a Linux browser by running its --version command.

    Args:
        browser_command: The command or path to the browser executable.

    Returns:
        The version string (e.g. '120.0.1'), or UNKNOWN_VERSION if not found.
    """
    try:
        result = subprocess.run(
            [browser_command, "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return UNKNOWN_VERSION
    output = result.stdout.strip()
    match = re.search(r"(\d+\.\d+(?:\.\d+)*)", output)
    return match.group(1) if match else UNKNOWN_VERSION


def detect_browser_installed() -> Tuple[str, str]:
    """
    Detects the default web browser using the installed-browsers package.

    Uses the `installed-browsers` package, if available, to identify the
    default browser and read its installed version.

    Returns:
        A tuple of (browser_name, browser_version).
    """
    if installed_browsers is None:
        return UNKNOWN_BROWSER
    try:
        default_browser = installed_browsers.what_is_the_default_browser()
        if not default_browser:
            return UNKNOWN_BROWSER

        default_lower = default_browser.lower()
        for browser in installed_browsers.browsers():
            name = browser.get("name") or ""
            description = browser.get("description") or ""
            if (
                name.lower() == default_lower
                or description.lower() == default_lower
            ):
                browser_name = description or name
                browser_version = browser.get("version") or UNKNOWN_VERSION
                return browser_name, browser_version
    except Exception:
        pass

    return UNKNOWN_BROWSER


BROWSER_DETECTORS = {
    "Darwin": detect_browser_macos,
    "Windows": detect_browser_windows,
    "Linux": detect_browser_linux,
}


def detect_browser() -> Tuple[str, str]:
    """
    Detects the default web browser on the current system.

    First attempts the platform-specific raw detection, then falls back to
    the installed-browsers package if the raw detection fails.

    Returns:
        A tuple of (browser_name, browser_version).
    """
    detector = BROWSER_DETECTORS.get(platform.system())
    if detector is not None:
        try:
            browser = detector()
            if browser != UNKNOWN_BROWSER:
                return browser
        except Exception:
            pass

    return detect_browser_installed()
