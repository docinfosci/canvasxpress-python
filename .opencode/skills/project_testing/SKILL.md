---
name: Project Testing
description: How to test canvasxpress-python — unit and functional suites, the 50% coverage gate, platform visual tests with canon images, CircleCI job mapping, and Python 3.8 runtime verification. Use when running, writing, or debugging tests in this repo.
---

# Testing canvasxpress-python

Commands assume the synced uv-managed `.venv` (see the `project_development`
skill for environment setup). Prefer `uv run <command>` over activating the
venv.

## Quick commands

```terminal
uv run python -m pytest tests/unit -q        # unit tests only
uv run invoke test                           # full suite == what CircleCI runs
uv run invoke test --platform                # full suite + platform visual tests (local only)
```

- `invoke test` covers everything under `./tests` **except** the platform
  visual tests, and enforces a **50% coverage gate**
  (`--cov-fail-under=50`). Coverage currently lands around 87–88%.
- `invoke test --platform` is used by `build_local.sh` and is not run in
  CircleCI (its Debian images lack Chromium's system libraries).

## Platform visual tests (`tests/functional/platform`)

- Platforms: `streamlit`, `dash`, `shiny`, `jupyter`, `rstudio`. Each renders a
  minimal live app (or executed notebook / saved page) in headless Chromium
  via Playwright at a 1920x1080 window (device pixel ratio 1), captures the
  window and each chart's on-page box, and compares to canon: chart boxes
  within 4 px, and drawn-on 32 px cells overlapping canon's by >= 0.85
  (whole-window SSIM is deliberately not used — a blank page scores ~0.95).
- One canon per case (`expected/<case>.png` and `.json`) is shared by all
  platforms; Windows and Linux captures match it.
- A case **without** canon is skipped, and its capture is kept in
  `tests/functional/platform/captures/` (git-ignored) for a person to review.
  Approve with `python -m tests.functional.platform.approve <framework>/<case>`.
  **Never approve a capture on the user's behalf** — present it and wait.
- Skip/fail conditions: the tests skip where Playwright or scikit-image is not
  installed (Python 3.15 today), and fail with install instructions where
  Playwright is installed without its Chromium
  (`python -m playwright install chromium`; add `--with-deps` on Linux).
  They load CanvasXpress from its CDN, so they need network access.
- Details: `tests/functional/platform/README.md`.

## CircleCI mapping

CircleCI builds on Debian (Bullseye, not Ubuntu) and runs `invoke test`
(no `--platform`) in three jobs:

- `build-python-oldest`: `python:3.8.18-bullseye`
- `build-python-latest`: `python:3.15-trixie` (beta)
- `build-python-general`: `python:3.10.12-bullseye` — runs only after oldest
  and latest pass (a failure in either intentionally blocks deployment);
  performs the static analysis (`uvx ruff check ./canvasxpress`,
  `uvx vermin canvasxpress`) and deploys the package.

Each job creates `./venv` with `uv venv` and installs `.[all]` and `.[dev]`
with `uv pip install` (fresh resolution; the committed `uv.lock` is not
consulted). Tests must execute on 3.8 even though they are not package logic.

## Verifying Python 3.8 runtime behaviour

vermin and CI prove compatibility, but for a quick local runtime check
(e.g. a stdlib-version fallback path) create a throwaway venv **outside** the
project:

```terminal
uv venv /tmp/cx38 --python 3.8
uv pip install --python /tmp/cx38/bin/python -e ".[all,dev]"
/tmp/cx38/bin/python -m pytest tests/unit -q
```

Delete it afterwards. Never create per-version venvs inside the tree.

## Known issues

- Image export (`canvasxpress/render/image.py`) cannot find `npm` on Windows
  (it is `npm.cmd`) and uses POSIX-only `shlex.quote`, so
  `test_CXImage.py::test_cx_converst_to_image_base64` and
  `test_plot.py::test_convert_to_image_returns_none_when_no_nodejs` fail on
  Windows.
