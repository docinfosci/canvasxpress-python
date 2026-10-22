"""Generate canvasxpress/version.py at build time.

The date-based version string is written to canvasxpress/version.py, which
setuptools reads dynamically via [tool.setuptools.dynamic] in pyproject.toml.

Usage:
    python build_pkg_setup.py       # generate version.py
    uv build                        # build the package (reads version.py dynamically)

Build process (CI / build_local.sh):
    python build_pkg_setup.py && uv build
"""

from datetime import datetime

import pytz
from git import Repo

buildtime = pytz.utc.localize(datetime.now())


def get_version() -> str:
    """Return a PEP 440-compliant date-based version string.

    main/master  →  2026.10.21.200702292       (date + time, no .dev)
    other        →  2026.10.21.dev200702292    (date + .dev + time)
    """
    repo = Repo(".")
    branch = repo.active_branch

    time_suffix = buildtime.strftime('%H%M%S') + buildtime.strftime('%f')[:3]

    if branch.name in ('main', 'master'):
        return f"{buildtime.year}.{buildtime.month}.{buildtime.day}.{time_suffix}"
    else:
        return f"{buildtime.year}.{buildtime.month}.{buildtime.day}.dev{time_suffix}"


if __name__ == "__main__":
    version = get_version()

    # Write version.py (read by setuptools via [tool.setuptools.dynamic] file:)
    with open("canvasxpress/version.py", "w") as fh:
        fh.write(f"{version}\n")
    print(f"Generated version.py: __version__ = '{version}'")
