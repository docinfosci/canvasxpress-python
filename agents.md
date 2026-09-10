# agents.md

## Project Overview
The project overview is documented in the `README.md` file located in the root directory.

## Source Code Structure
- The source code for the project is primarily located in the following directories:
  - `./canvasxpress`: Contains the core functionality related to CanvasXpress.
  - `./plotly`: Includes integration with Plotly, specifically for Dash applications.

## Automated Tests
Automated tests are maintained in the `./tests` directory. These tests ensure that the project functions as expected and cover various scenarios.

## Python Version Compatibility
The project is developed using Python 3.13 but must be compatible with Python 3.8+ to maintain broad compatibility across different environments.

## Code Formatting
Code formatting adheres to the Black style guide, ensuring consistent and readable code throughout the project.

## Package Management
Packages are managed using pip:
- `requirements.txt`: Lists packages necessary for the published package.
- `requirements-dev.txt`: Includes packages required for local development and testing.
- `requirements-project.txt`: Contains packages needed to install and manage project development tools.

The virtual environment is managed using python:
- Use python 3.13
- Created in the project root using `python -m venv venv`

## Build Process
The `build_local.sh` script is used to prepare the package for publication. It runs tests and executes various tools such as `build_pkg_setup.py` to ensure the package is ready for distribution.

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
