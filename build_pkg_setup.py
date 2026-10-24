"""Generate canvasxpress/version.txt at build time.

The date-based version string is written to canvasxpress/version.txt, which
setuptools reads dynamically via [tool.setuptools.dynamic] in pyproject.toml.

The file has a non-Python extension on purpose: a bare version string is not
valid Python, and coverage/coveralls would try to parse any ``.py`` file in
the package and fail (see coveralls NotPython errors on canvasxpress/version.py).

Usage:
    python build_pkg_setup.py       # generate version.txt
    uv build                        # build the package (reads version.txt dynamically)

Build process (CI / build_local.sh):
    python build_pkg_setup.py && uv build
"""

import os
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

    # Remove the legacy version.py (a bare string in a .py file broke coveralls).
    legacy_py = os.path.join("canvasxpress", "version.py")
    if os.path.exists(legacy_py):
        os.remove(legacy_py)

    # Write version.txt (read by setuptools via [tool.setuptools.dynamic] file:)
    with open("canvasxpress/version.txt", "w") as fh:
        fh.write(f"{version}\n")
    print(f"Generated version.txt: '{version}'")
