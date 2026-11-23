"""
This module decides where the renderers in `canvasxpress.render` write pages and
other working files, and what those files are called.

Pages are named after their charts rather than given unique names, so rendering a
chart again replaces its earlier page instead of adding another file.
"""

import getpass
import hashlib
import os
import re
import stat
import tempfile
from pathlib import Path
from typing import Optional, Sequence, Union

ANONYMOUS_NAME: str = "anonymous"
"""The name used for a chart without a `render_to` ID, whose ID changes on each
render and so cannot name a file."""

MAX_FILE_STEM: int = 100
"""The longest file name, before the extension, given to a page. Longer names are
shortened, keeping well within the Windows path length limit."""

_HASH_LENGTH: int = 8

_RESERVED_STEMS = frozenset(
    ["CON", "PRN", "AUX", "NUL"]
    + [f"COM{number}" for number in range(1, 10)]
    + [f"LPT{number}" for number in range(1, 10)]
)
"""Windows device names, which cannot be used as file names even with an
extension."""

_UNSAFE_CHARACTERS = re.compile(r"[^\w.-]")

_UNSAFE_NAME_CHARACTERS = re.compile(r"[^\w-]")


def _user_suffix() -> str:
    try:
        user = getpass.getuser()
    except Exception:
        return ""

    user = _UNSAFE_CHARACTERS.sub("", user)
    return f"-{user}" if user else ""


def _is_private_directory(path: Path) -> bool:
    """
    Indicates whether a directory belongs to the current user alone. Always True
    where ownership cannot be checked, such as on Windows, whose temporary
    directory is already private to the user.
    """
    if not hasattr(os, "getuid"):
        return True

    status = path.stat()
    return status.st_uid == os.getuid() and not (
        status.st_mode & (stat.S_IRWXG | stat.S_IRWXO)
    )


def temp_directory() -> Path:
    """
    Provides the directory for pages and other working files: a
    `canvasxpress-python-<user>` folder in the system temporary directory, outside
    the package, created if needed and readable only by the current user.

    A system temporary directory can be shared between users, such as `/tmp` on
    Linux. If the folder there belongs to someone else or can be accessed by
    others, a new private folder is created instead.

    Returns:
        The path of the directory.
    """
    directory = Path(tempfile.gettempdir()) / f"canvasxpress-python{_user_suffix()}"
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)

    if not directory.is_dir() or not _is_private_directory(directory):
        directory = Path(tempfile.mkdtemp(prefix="canvasxpress-python-"))

    return directory


def page_file_name(names: Sequence[Optional[str]]) -> str:
    """
    Provides the file name for a page of charts, from the chart names in page
    order joined by `_`, such as `scatter_heatmap.html`. A chart without a name is
    called `anonymous`, as is a page without charts.

    A name longer than `MAX_FILE_STEM` is shortened and ends with a hash of the
    full name, so that different pages keep different names. A name that Windows
    reserves for a device, such as `con`, ends with `_chart`.

    Args:
        names: The name of each chart, or None for an anonymous chart.

    Returns:
        The file name, including the `.html` extension.
    """
    stem = "_".join(
        _UNSAFE_NAME_CHARACTERS.sub("", name or "") or ANONYMOUS_NAME for name in names
    )
    stem = stem or ANONYMOUS_NAME

    if len(stem) > MAX_FILE_STEM:
        digest = hashlib.sha256(stem.encode("utf-8")).hexdigest()[:_HASH_LENGTH]
        stem = f"{stem[: MAX_FILE_STEM - _HASH_LENGTH - 1]}_{digest}"

    if stem.upper() in _RESERVED_STEMS:
        stem = f"{stem}_chart"

    return f"{stem}.html"


def write_html_file(
    html: str, path: Union[str, Path], file_name: Optional[str] = None
) -> Path:
    """
    Writes HTML to a file, replacing any existing file.

    Args:
        html: The HTML to write.
        path: The file path, or a directory in which to write `file_name`.
        file_name: The file name to use when path is a directory, such as
            `CXHtmlDocument.file_name`. Defaults to `anonymous.html`.

    Returns:
        The path of the written file.
    """
    file_path = Path(path)
    if file_path.is_dir():
        file_path = file_path / (file_name or page_file_name([]))

    file_path.write_text(html, encoding="utf-8")

    return file_path
