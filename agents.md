# agents.md

## Project Overview
The project overview is documented in the `README.md` file located in the root directory.

## Source Code Structure
- The source code for the project is primarily located in the following directories:
  - `./canvasxpress`: Contains the core functionality related to CanvasXpress.
  - `./canvasxpress/render`: Renderers for each target framework (Jupyter, Dash, Shiny, Streamlit, browser, images).
  - `./canvasxpress/render/resources`: JavaScript shipped with the package: `canvasxpress-react.js` (the CanvasXpress React wrapper) and `canvasxpress-dash.js` (the `CXDashElement` Dash component, defined in Python in `render/dash.py`). These are plain JavaScript using the host page's global React; there is no build step, bundler, or `npm` dependency.
- Non-Python files must be listed in `[tool.setuptools.package-data]` in `pyproject.toml` (and `MANIFEST.in`), or they are left out of the wheel.

## Automated Tests
Automated tests are maintained in the `./tests` directory. These tests ensure that the project functions as expected and cover various scenarios.

## Python Version Compatibility
The project is developed using Python 3.13 and officially supports Python 3.8 through 3.14, with Python 3.15 supported as beta (not yet fully supported by all dependencies).

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
- Also check `scikit-image` compatibility on Python 3.15 when testing upgrades.

## Commits and Pull Requests
- Do not add AI/agent attribution (e.g. `Co-Authored-By: Claude ...` trailers or "Generated with ..." footers) to commit messages or pull request descriptions. Agent contributions are already acknowledged in `README.md`.

## Code Formatting
Code formatting adheres to the Black style guide, ensuring consistent and readable code throughout the project.

## Package Management
Packages are declared in `pyproject.toml` (which replaced the former `requirements*.txt` files) and installed with `uv pip`:
- `dependencies`: packages necessary for the published package.
- `[project.optional-dependencies]`: framework extras (`dash`, `jupyter`, `streamlit`, `shiny`, `rstudio`, `all`) and `dev` for local development and testing.

The virtual environment:
- A single environment on Python 3.13. Do not create per-version venvs: 3.8 compliance is enforced by vermin, and CircleCI tests 3.8, 3.10 and 3.15 at runtime.
- Created in the project root as `venv` by the platform setup scripts (`setup_mac.sh`, `setup_linux.sh`, `setup_windows.bat`).

## Build Process
The `build_local.sh` script is used to prepare the package for publication. It runs tests and executes various tools such as `build_pkg_setup.py` to ensure the package is ready for distribution.

### Build Platforms
- **Local development (macOS)**: Uses Homebrew to install R (`brew install r`) and Node.js (`nvm install`). Run `./build_local.sh` to build.
- **Local development (Windows)**: Run `.\setup_windows.bat` from cmd or PowerShell. Installs Node.js, uv and Git via winget or Chocolatey; R is optional (rpy2 is skipped if R is not found).
- **CI/CD (Debian Bullseye)**: CircleCI builds use Debian Docker images (not Ubuntu). Three build profiles:
  - `build-python-oldest`: `python:3.8.18-bullseye`
  - `build-python-latest`: `python:3.15-trixie` (beta; Debian 13, since no bullseye image exists for 3.15)
  - `build-python-general`: `python:3.10.12-bullseye` (runs only after oldest and latest pass, so a failure in either intentionally blocks deployment; deploys the package)
- `build_local.sh` simulates the CircleCI build locally.

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
   - `build_pkg_setup.py` generates `setup.py` with proper entry points
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
