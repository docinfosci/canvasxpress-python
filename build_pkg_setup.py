"""Generate canvasxpress/version.py at build time.

The date-based version string is written to both:
- canvasxpress/version.py (read by canvasxpress/__init__.py)
- pyproject.toml (used by setuptools for distribution naming)

Usage:
    python build_pkg_setup.py       # generate version.py + patch pyproject.toml
    uv build                        # build the package (reads patched pyproject.toml)

Build process (CI / build_local.sh):
    python build_pkg_setup.py && uv build
"""

import re
from datetime import datetime

import pytz
from git import Repo

buildtime = pytz.utc.localize(datetime.now())


def get_version() -> str:
    """Return a PEP 440-compliant date-based version string.

    main/master  →  2026.10.19
    other        →  2026.10.19.dev155633
    """
    repo = Repo(".")
    branch = repo.active_branch

    # main/master   →  2026.10.19
    # other branches →  2026.10.19.dev155633
    is_release = branch.name in ['main', 'master']
    if is_release:
        return f"{buildtime.year}.{buildtime.month}.{buildtime.day}"
    else:
        return (
            f"{buildtime.year}.{buildtime.month}.{buildtime.day}"
            f".dev{buildtime.strftime('%H%M%S')}"
        )


if __name__ == "__main__":
    version = get_version()

    # Write version.py
    with open("canvasxpress/version.py", "w") as fh:
        fh.write(f"__version__ = '{version}'\n")
    print(f"Generated version.py: __version__ = '{version}'")

    # Patch pyproject.toml with the version
    with open("pyproject.toml", "r") as fh:
        content = fh.read()

    # Replace dynamic = ["version"] with version = "..."
    new_content = re.sub(
        r'dynamic = \["version"\]',
        f'version = "{version}"',
        content,
    )

    with open("pyproject.toml", "w") as fh:
        fh.write(new_content)
    print(f"Patched pyproject.toml with version = '{version}'")
