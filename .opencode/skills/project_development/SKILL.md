---
name: Project Development
description: How to develop in the canvasxpress-python repository — the uv-managed local environment, Python 3.8 compatibility rules, static analysis, dependency management, and packaging/versioning. Use when making code changes in this repo, adding or changing dependencies, or preparing a local build.
---

# Developing canvasxpress-python

Full documentation lives in `AGENTS.md` (project root); this skill is a working
reference. For running tests, use the `project_testing` skill.

## Local environment (uv-managed `.venv`)

- The development environment is uv's default `.venv`, pinned to Python 3.13
  by the tracked `.python-version` file (uv downloads the interpreter if it is
  missing). The project is installed **editable** — source edits take effect
  immediately.
- `uv.lock` is **committed** and is the source of truth for local
  resolutions. Keep it in step with `pyproject.toml` — commit both together.
- After `git pull` or any dependency change, sync the environment:
  - `uv sync --extra all --extra dev` (R available), or
  - `uv sync --extra dash --extra jupyter --extra streamlit --extra shiny --extra dev`
    (no R — skips rpy2).
- Prefer `uv run <command>` over activating the venv; it uses the synced
  `.venv` without shell state.
- `canvasxpress/version.txt` (generated, git-ignored) must exist before
  `uv sync`/`uv build` can build the project. Generate it with:
  `uv run --no-project --with pytz --with gitpython python build_pkg_setup.py`
- CircleCI is different on purpose: it does **not** use `uv sync` — each job
  creates `./venv` with `uv venv` and runs `uv pip install ".[all]"` /
  `".[dev]"` against its fixed Python image (fresh resolution). Do not mix the
  two workflows or create per-version venvs in the tree; 3.8 compliance is
  enforced by vermin and tested at runtime in CI. To check 3.8 *runtime*
  behaviour, use a throwaway venv outside the project (see `project_testing`).

## Python 3.8 compatibility (hard rule)

All package logic under `./canvasxpress` must be pure Python 3.8:

- No 3.9+ syntax or stdlib: not `list[int]`/`dict[str, int]`/`X | Y`
  annotations (use `typing.List`, `Dict`, `Optional`, `Union`), not
  `str.removeprefix()`, not parenthesized multi-item `with`, not `match`, not
  `importlib.resources.files()` without a guarded fallback.
- Version-guarded code (`sys.version_info` checks, `try/except ImportError`
  backports) must mark the newer-API line with `# novermin` — vermin honors the
  marker **per line**, so on multi-line expressions the marker must sit on the
  line containing the newer API (this exact mistake broke the general CI build
  in `canvasxpress/agent_skills/registry.py`).
- Reference pattern: the `importlib_resources` backport conditional import in
  `canvasxpress/agent_skills/canvasxpress_charts/__init__.py` and
  `canvasxpress/agent_skills/registry.py`.
- Agent-skill *content* (the `.md` files under `canvasxpress/agent_skills/`)
  may target the latest Python — only the package logic (including the skills'
  `.py` modules) must stay 3.8.
- Enforced by ruff (`target-version = "py38"`) and vermin (`vermin.ini`,
  `targets = 3.8-`).

## Static analysis (run before committing)

```terminal
uvx ruff check ./canvasxpress
uvx vermin canvasxpress
```

Both run in the CircleCI general job and in `build_local.sh`.

## Adding a dependency

Record it with `uv add` so `pyproject.toml` and `uv.lock` update together,
then refresh the full development environment:

```terminal
uv add --optional dev "<package>"      # e.g. a dev tool
uv sync --extra all --extra dev        # refresh .venv (or the no-R variant)
```

- Never only `pip install` / `uv pip install` into the environment.
- Dependencies are intentionally floating (mostly unpinned) so hosting
  platforms can drift versions; add a ceiling only when a known
  incompatibility requires one.
- Non-Python files must be listed in `[tool.setuptools.package-data]` in
  `pyproject.toml` (and `MANIFEST.in`), or they are left out of the wheel.

## Versioning and packaging

- `build_pkg_setup.py` generates `canvasxpress/version.txt` (a date-based PEP
  440 string: `YYYY.MM.DD.HHMMSSmmm` on main/master,
  `YYYY.MM.DD.devHHMMSSmmm` otherwise). `pyproject.toml` reads the version
  from it dynamically; the file is git-ignored and non-`.py` so coverage never
  parses it.
- `build_local.sh` simulates the CircleCI build locally on the shared `.venv`
  and additionally runs the platform visual tests. Run it before publishing.

## Commits and pull requests

- No AI/agent attribution — no `Co-Authored-By:` trailers, no
  "Generated with ..." footers. Agent contributions are acknowledged in
  `README.md`.
- Keep Black formatting.
