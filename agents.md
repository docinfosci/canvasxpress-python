# agents.md

## Project Overview
The project overview is documented in the `README.md` file located in the root directory.

## Source Code Structure
- The source code for the project is primarily located in the following directories:
  - `./canvasxpress`: Contains the core functionality related to CanvasXpress.
  - `./canvasxpress/render`: Renderers for each target framework (Jupyter, Dash, Shiny, Streamlit, browser, images).
  - `./canvasxpress/render/context`: The HTML/CSS/JS layer shared by the renderers. `CXLibraryAssets` (library, stylesheet and license URLs, as tags or an on-demand loader), `CXChartAssets` (a chart's `<canvas>` and init JS, rendered on a copy with unique IDs) and `CXHtmlDocument` (arranges charts in a grid, optionally with `fill_to_width`/`fill_to_height` so they follow their container's width and/or height, and provides a full `page()`, a `fragment()` with library mode `LIBRARY_NONE`/`LIBRARY_TAGS`/`LIBRARY_LOADER`, or the separate `layout_html()`/`loader_js()` parts). `files.py` decides where pages and working files go and what they are called: `temp_directory()` (a per-user `canvasxpress-python-<user>` folder in the system temp directory; never write into the package) and `page_file_name()`/`CXHtmlDocument.file_name` (named after the charts' `render_to` IDs, `anonymous` for anonymous charts, so re-rendering replaces a page instead of adding files). Renderers should build their HTML through this layer rather than keep their own templates.
  - `./canvasxpress/render/resources`: JavaScript shipped with the package: `canvasxpress-loader.js` (`window.canvasxpress.loadLibrary()`, the shared on-demand CanvasXpress loader, embedded by the Jupyter and Streamlit renderers and served first by Dash), `canvasxpress-fill.js` (`window.canvasxpress.fillContainer()`, the `fill_to_width` and `fill_to_height` options of `graph()` and the renderers: redraws a chart at its container's width and/or height via `setDimensions` on a debounced `ResizeObserver`/window resize, keeping an unfilled dimension at its configured size; height is measured net of the content beyond the chart so a content-sized container cannot ratchet the chart taller; this is package behaviour, not a CanvasXpress library feature, and is distinct from the CanvasXpress `resizable` config), `canvasxpress-react.js` (the CanvasXpress React wrapper, which uses the loader) and `canvasxpress-dash.js` (the `CXDashElement` Dash component, defined in Python in `render/dash.py`). These are plain JavaScript using the host page's global React; there is no build step, bundler, or `npm` dependency.
- Non-Python files must be listed in `[tool.setuptools.package-data]` in `pyproject.toml` (and `MANIFEST.in`), or they are left out of the wheel.

## Architecture Documentation
`ARCHITECTURE.md` (repository root) is the authoritative description of the package's architecture, written for both human and agent contributors: the package map, the HTML/JS/CSS pipeline (`render/context`, `render/resources`), the library modes and escaping and ID rules, import direction, per-platform rendering, and extension recipes. It must be kept in sync with the code: any change that adds, removes, or renames a module, renderer, or shipped resource; changes the HTML/JS/CSS pipeline, loader, or escaping/ID rules; changes import direction or adds a core→render seam; or adds or changes an IPython display representation must update `ARCHITECTURE.md` in the same change. Process-level detail (environment, build, CI, testing) stays in this file and the project skills; `ARCHITECTURE.md` is the source for structure.

## Automated Tests
Automated tests are maintained in the `./tests` directory. These tests ensure that the project functions as expected and cover various scenarios. `invoke test` (used by CircleCI) runs everything under `./tests` except the platform visual tests below; `invoke test --platform` (used by `build_local.sh`) runs them too.

- `./tests/unit`: unit tests, including `test_render_context.py` for the shared HTML/CSS/JS layer. Run with `.venv/bin/python -m pytest tests/unit` (Windows: `.venv\Scripts\python.exe`), or `uv run python -m pytest tests/unit`.
- Known issue: image export (`canvasxpress/render/image.py`) cannot find `npm` on Windows (it is `npm.cmd`) and uses POSIX-only `shlex.quote`, so `test_CXImage.py::test_cx_converst_to_image_base64` and `test_plot.py::test_convert_to_image_returns_none_when_no_nodejs` fail on Windows.
- `./tests/functional/platform/{streamlit,dash,shiny,jupyter,rstudio}`: platform visual tests, run locally (`build_local.sh`, or `python -m pytest tests/functional/platform`) and not in CircleCI, which would need Chromium's system libraries on its Debian images. Each renders a minimal live app (or executed notebook / saved page) in headless Chromium via Playwright at a 1920x1080 window (device pixel ratio 1), captures the window and each chart's on-page box, and compares them to canon: chart boxes within 4 px, and the drawn-on 32 px cells overlapping canon's by >= 0.85 (whole-window SSIM is not used: a blank page scores ~0.95). Streamlit, Dash, Shiny and Jupyter each have a stacked layout (`app.py`: a fixed-size control chart above a `fill_to_width` chart) and a columns layout (`app_columns.py`: two `fill_to_width` charts in the framework's own columns), each captured `initial` and `resized`; RStudio's page is already two filling charts side by side. One canon per case (`expected/<case>.png` and `.json`) is shared by all platforms; Windows and Linux captures match it. A case without canon is skipped and its capture kept in `tests/functional/platform/captures/` (git-ignored) for a person to review; approve with `python -m tests.functional.platform.approve <framework>/<case>`. Never approve a capture on the user's behalf. The tests skip where Playwright or scikit-image is not installed (Python 3.15) and fail with install instructions where Playwright is installed without its Chromium (`python -m playwright install chromium`; on Linux add `--with-deps`). They load CanvasXpress from its CDN, so they need network access. See `tests/functional/platform/README.md`.

## Python Version Compatibility
The project is developed using Python 3.13 (the local dev interpreter is pinned by the tracked `.python-version` file, which uv reads) and officially supports Python 3.8 through 3.14, with Python 3.15 supported as beta (not yet fully supported by all dependencies).

- **Python 3.8 is the minimum** and is required by a client. All package logic under `./canvasxpress` must be pure Python 3.8 — any 3.9+ syntax or stdlib API breaks the package on 3.8 systems. Do not use e.g. `list[int]`/`dict[str, int]`/`X | Y` annotations (use `typing.List`, `Dict`, `Optional`, `Union`), `str.removeprefix()`, parenthesized multi-item `with`, `match`, or `importlib.resources.files()` without a guarded fallback.
  - Enforced by ruff `target-version = "py38"` (syntax) and **vermin** (`vermin.ini`; syntax, stdlib APIs and annotations). Run `uvx vermin canvasxpress` before committing; it runs in `build_local.sh` and the CircleCI deploy job.
  - Version-guarded code (`sys.version_info` checks, `try/except ImportError` fallbacks) must mark the newer-API line with `# novermin`.
- **Agent skills content may target the latest Python.** Example code in the skill Markdown files (`canvasxpress/agent_skills/**/*.md`) is for client projects and can use any version (e.g. a 3.15 client). The skills' `.py` modules (`registry.py`, `__init__.py`) are package logic and must stay 3.8.
- Tests (`./tests`) are not package logic, but they run on 3.8 in CI, so they must still execute on 3.8.
- Dependencies in `pyproject.toml` are intentionally floating (mostly unpinned) so third-party versions can drift to whatever suits the hosting platform and Python version. Only add ceilings when a known incompatibility requires it.
- CircleCI covers the range: `build-python-oldest` (3.8), `build-python-latest` (3.15 beta), and `build-python-general` (3.10, which deploys the package).

### Python 3.15 To-Do
- `deepdiff<9.0.0` is temporarily pinned in `pyproject.toml` because deepdiff 9.x depends on `cachebox` which uses PyO3 that doesn't support Python 3.15 yet.
- **TODO**: Periodically check if deepdiff 9.x has released a version that supports Python 3.15. When it does, remove the `<9.0.0` ceiling and regenerate `uv.lock`.
- `playwright` and `scikit-image` (dev extra, for the platform visual tests) are limited to `python_full_version < '3.15'`, as Playwright's `greenlet` dependency and scikit-image are not yet confirmed on 3.15; the platform tests skip there.
- **TODO**: When both install on Python 3.15, remove those markers so the platform tests also run in local builds on 3.15.

## Commits and Pull Requests
- Do not add AI/agent attribution (e.g. `Co-Authored-By: Claude ...` trailers or "Generated with ..." footers) to commit messages or pull request descriptions. Agent contributions are already acknowledged in `README.md`.

## Code Formatting
Code formatting adheres to the Black style guide, ensuring consistent and readable code throughout the project.

## Package Management
Dependencies are declared in `pyproject.toml` (which replaced the former `requirements*.txt` files) and managed with `uv`:
- `dependencies`: packages necessary for the published package.
- `[project.optional-dependencies]`: framework extras (`dash`, `jupyter`, `streamlit`, `shiny`, `rstudio`, `all`) and `dev` for local development and testing.

### Local development environment (uv-managed `.venv`)
- The local environment is uv's default `.venv`, pinned to Python 3.13 by the tracked `.python-version` file (uv downloads the interpreter if it is missing). The project is installed editable, so source edits take effect immediately.
- `uv.lock` is committed and is the source of truth for local resolutions; keep it in step with `pyproject.toml` (commit both together).
- Sync the environment after `git pull` or any dependency change:
  - `uv sync --extra all --extra dev` (R available), or `uv sync --extra dash --extra jupyter --extra streamlit --extra shiny --extra dev` (no R, skips rpy2).
  - The setup scripts (`setup_mac.sh`, `setup_linux.sh`, `setup_windows.bat`) do this on fresh machines.
- `canvasxpress/version.txt` (generated, git-ignored) must exist before `uv sync`/`uv build` can build the project; the setup scripts and `build_local.sh` generate it first with `uv run --no-project --with pytz --with gitpython python build_pkg_setup.py`.
- Prefer `uv run <command>` over activating the venv: it uses the synced `.venv` without shell state.
- Do not create per-version venvs for day-to-day work: 3.8 compliance is enforced by vermin, and CircleCI tests 3.8, 3.10 and 3.15 at runtime. To verify 3.8 *runtime* behaviour (e.g. a stdlib-version fallback), create a throwaway venv outside the project: `uv venv /tmp/cx38 --python 3.8 && uv pip install --python /tmp/cx38/bin/python -e ".[all,dev]"`, then run the tests with that interpreter.

### Adding a dependency
Record it with `uv add` so that `pyproject.toml` and `uv.lock` update together, e.g. `uv add --optional dev "<package>"` for a dev tool, then `uv sync --extra all --extra dev` to refresh the full development environment. Never only `pip install` / `uv pip install` it into the environment.

### CircleCI (separate `./venv`, `uv pip`)
CI does not use `uv sync`: each job creates `./venv` with `uv venv` and installs `.[all]` and `.[dev]` with `uv pip install` against the job's fixed Python image (fresh resolution; `uv.lock` is not consulted). `build_local.sh` simulates the CircleCI build locally on the shared `.venv` and additionally runs the platform visual tests (`invoke test --platform`).

## Build Process
The `build_local.sh` script is used to prepare the package for publication. It generates `canvasxpress/version.txt` (via `build_pkg_setup.py`), syncs the uv-managed `.venv`, runs ruff and vermin, runs the test suite including the platform visual tests, and builds the distribution.

### Build Platforms
- **Local development (macOS)**: Run `./setup_mac.sh` to create the uv-managed `.venv` (Python 3.13 per `.python-version`; uv downloads the interpreter if missing). Uses Homebrew to install R (`brew install r`) and Node.js (`nvm install`). Run `./build_local.sh` to build.
- **Local development (Linux, Debian/Ubuntu)**: Run `./setup_linux.sh` to create `.venv`; it installs build tools and Chromium's system libraries with apt.
- **Local development (Windows)**: Run `.\setup_windows.bat` from cmd or PowerShell. Installs Node.js, uv and Git via winget or Chocolatey; R is optional (rpy2 is skipped if R is not found). An editor's Ruff server running from `.venv\Scripts\ruff.exe` locks the environment; close it before deleting or rebuilding `.venv`.
- All three setup scripts skip rpy2 (they install the individual framework extras instead of `all`) when R is not found, and install Playwright's Chromium for the platform visual tests.
- **CI/CD (Debian Bullseye)**: CircleCI builds use Debian Docker images (not Ubuntu). Three build profiles:
  - `build-python-oldest`: `python:3.8.18-bullseye`
  - `build-python-latest`: `python:3.15-trixie` (beta; Debian 13, since no bullseye image exists for 3.15)
  - `build-python-general`: `python:3.10.12-bullseye` (runs only after oldest and latest pass, so a failure in either intentionally blocks deployment; deploys the package)
- Each job installs `.[all]` and `.[dev]` into `./venv` with `uv pip` and runs `invoke test`, which leaves out the platform visual tests; no browser is installed.
- `build_local.sh` simulates the CircleCI build locally (on the shared `.venv`), and additionally installs Playwright's Chromium (`--with-deps` on Linux) and runs the platform visual tests (`invoke test --platform`).

**Important:** CircleCI uses Debian Bullseye, NOT Ubuntu. When installing packages:
- Use `https://cloud.r-project.org/bin/linux/debian bullseye-cran40/` for R (NOT jammy-cran40)
- Use `apt-get` with Debian packages, NOT Ubuntu packages
- The deploy image is `python:3.10.12-bullseye` (Debian 11)

### R Dependency
The `rpy2` package requires R to be installed:
- **macOS**: `brew install r` (via Homebrew)
- **CI/Debian Bullseye**: Added via CRAN Debian repository (`bullseye-cran40`), NOT Ubuntu Jammy

**R in CI:** Each `run:` step in CircleCI runs in a separate shell. To persist R_HOME across steps:
1. R installation step: saves R_HOME to `$HOME/.r_home`
2. Steps needing R (Python deps, tests): reads `$HOME/.r_home` and exports R_HOME

### Skill Installation Validation
During local builds, the skill installation is validated to ensure all expected skills are present:

1. **Skills are distributed to three agent directories:**
   - `~/.agents/skills/` (Standard Agents open standard)
   - `~/.config/opencode/skills/` (OpenCode native)
   - `~/.claude/skills/` (Claude-compatible)

2. **Expected skills:**
   - `canvasxpress_charts` — Core API, chart types, configuration patterns
   - `canvasxpress_events` — Event handling (click, dblclick, mousemove, mouseout)
   - `canvasxpress_notebooks` — Jupyter notebook creation and structure
   - `canvasxpress_validator` — Code syntax validation

3. **Validation process:**
   - `build_pkg_setup.py` generates `canvasxpress/version.txt` (git-ignored; `pyproject.toml` reads the version from it) and removes any legacy `canvasxpress/version.py`; entry points are declared in `pyproject.toml`
   - `build_local.sh` runs tests and validates package structure
   - The `canvasxpress` CLI can be used to reinstall skills: `canvasxpress --force`

4. **Manual skill installation:**
    ```terminal
    canvasxpress --target all --force
    ```
    Available targets: `opencode`, `claude`, `agents`, `all` (default), or `both` (opencode + agents).

5. **Skill verification:**
    After installation, verify skills are present:
    ```terminal
    ls ~/.agents/skills/
    ls ~/.config/opencode/skills/
    ls ~/.claude/skills/
    ```
    Each directory should contain: `canvasxpress_charts`, `canvasxpress_events`, `canvasxpress_notebooks`, `canvasxpress_validator`.

### Internal project skills
This repository carries two skills for working *on* the project itself. They are not part of the shipped skill bundle above: they are tracked in git, live in the project's own OpenCode config (`.opencode/skills/`), and are never installed into user skill directories.
- `.opencode/skills/project_development/SKILL.md` — local environment setup, dependency management, Python 3.8 compatibility rules, and packaging/versioning workflow.
- `.opencode/skills/project_testing/SKILL.md` — test suites, the coverage gate, platform visual tests and canon approval, CircleCI job mapping, and 3.8 runtime verification.
