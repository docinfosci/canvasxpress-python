"""Generate canvasxpress/version.py at build time.

The date-based version string is written to both:
- canvasxpress/version.py (read by canvasxpress/__init__.py)
- pyproject.toml (used by setuptools/uv for distribution naming)

Usage:
    python build_pkg_setup.py       # generate version.py + patch pyproject.toml
    uv build                        # build the package (reads patched pyproject.toml)

Build process (CI / build_local.sh):
    python build_pkg_setup.py && uv build
"""

from datetime import datetime
import re

import pytz

buildtime = pytz.utc.localize(datetime.now())


def get_version() -> str:
    """Return a PEP 440-compliant date-based version string.

    All branches  →  2026.10.21.dev181512345  (always includes time)
    """
    ms = buildtime.strftime('%f')[:3]  # milliseconds (3 digits)
    return (
        f"{buildtime.year}.{buildtime.month}.{buildtime.day}"
        f".dev{buildtime.strftime('%H%M%S')}{ms}"
    )


if __name__ == "__main__":
    version = get_version()

    # Write version.py (used by canvasxpress/__init__.py)
    with open("canvasxpress/version.py", "w") as fh:
        fh.write(f"__version__ = '{version}'\n")
    print(f"Generated version.py: __version__ = '{version}'")

    # Patch pyproject.toml with the new version.
    # The version line may be:
    #   version = "..."  (static)
    #   version = '...'  (alternative quotes)
    #   dynamic = ["version"]  (legacy - replaced with static)
    # A single regex handles all cases to guarantee the patch takes effect.
    with open("pyproject.toml", "r") as fh:
        content = fh.read()

    patched = re.sub(
        r'(dynamic\s*=\s*\["version"\]|version\s*=\s*["\x27].*?["\x27])',
        f'version = "{version}"',
        content,
        count=1,
    )

    with open("pyproject.toml", "w") as fh:
        fh.write(patched)
    print(f"Patched pyproject.toml with version = '{version}'")
