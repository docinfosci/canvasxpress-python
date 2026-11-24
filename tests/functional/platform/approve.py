"""
Makes reviewed captures canon.

After a platform test run, each case's capture is in
tests/functional/platform/captures/<framework>/<case>.png, with the layout of
its charts in <case>.json. Once a person has checked that a capture looks right,
this copies both to tests/functional/platform/<framework>/expected/, where later
runs compare against them.

Usage:
    python -m tests.functional.platform.approve            # list captures
    python -m tests.functional.platform.approve streamlit/initial dash/resized
    python -m tests.functional.platform.approve --all      # every capture
"""

import shutil
import sys
from typing import List

from tests.functional.platform.visual import (
    CANON_SUFFIXES,
    CAPTURE_DIR,
    canon_path,
    capture_path,
)


def _captured_cases() -> List[str]:
    return sorted(
        f"{path.parent.name}/{path.stem}"
        for path in CAPTURE_DIR.glob("*/*.png")
        if not path.stem.endswith(".diff")
    )


def main(argv: List[str]) -> int:
    cases = _captured_cases()

    if not argv:
        if not cases:
            print(f"No captures in {CAPTURE_DIR}. Run the platform tests first.")
            return 0
        for case in cases:
            framework, name = case.split("/")
            status = "canon" if canon_path(framework, name).exists() else "new"
            print(f"{case:40} {status:6} {capture_path(framework, name)}")
        return 0

    selected = cases if argv == ["--all"] else argv
    for case in selected:
        if case.count("/") != 1:
            print(f"Expected <framework>/<case>, got {case!r}")
            return 1

        framework, name = case.split("/")
        for suffix in CANON_SUFFIXES:
            source = capture_path(framework, name, suffix)
            if not source.exists():
                print(f"No capture for {case} at {source}")
                return 1

        for suffix in CANON_SUFFIXES:
            target = canon_path(framework, name, suffix)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(capture_path(framework, name, suffix)), str(target))
        print(f"Approved {case}: {canon_path(framework, name)}")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
