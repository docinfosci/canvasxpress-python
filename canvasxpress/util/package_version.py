"""
Provides the canvasxpress package version.

The version is created at build time: `build_pkg_setup.py` writes the bare
version string to `canvasxpress/version.txt`, which setuptools also reads via
`[tool.setuptools.dynamic]` in `pyproject.toml`. The file has a non-Python
extension on purpose: a bare version string is not valid Python, and
coverage/coveralls would try to parse any ``.py`` file in the package and fail.
The package `__version__` and
the version stamped on installed agent skills both come from this function so
that they always agree.
"""

import os

DEV_VERSION: str = "0.0.0.dev0"
"""The version of an unbuilt source tree, i.e. one without `version.txt`."""

_VERSION_FILE: str = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "version.txt"
)


def read_package_version() -> str:
    """
    Reads the version written to `canvasxpress/version.txt` at build time.

    Accepts the bare version string written by `build_pkg_setup.py`, as well as
    the older `__version__ = "..."` form.

    Returns:
        The package version, or `DEV_VERSION` if `version.txt` is missing or empty.
    """
    try:
        with open(_VERSION_FILE, encoding="utf-8") as fh:
            lines = [line.strip() for line in fh.read().splitlines() if line.strip()]

    except OSError:
        return DEV_VERSION

    if not lines:
        return DEV_VERSION

    value = lines[0]
    if value.startswith("__version__"):
        value = value.split("=", 1)[1].strip() if "=" in value else ""

    value = value.strip("'\"")

    return value if value else DEV_VERSION
