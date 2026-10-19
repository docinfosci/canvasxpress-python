"""Generate canvasxpress/version.ini at build time.

The date-based version string is read by hatch-vcs via pyproject.toml
[tool.hatch.version] → path = "canvasxpress/version.ini".

Usage:
    python build_pkg_setup.py       # generate version.ini
    uv build                        # build the package (reads version.ini)

Build process (CI / build_local.sh):
    python build_pkg_setup.py && uv build
"""

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
    with open("canvasxpress/version.ini", "w") as fh:
        fh.write(f"__version__ = '{version}'\n")
    print(f"Generated version.ini: __version__ = '{version}'")
