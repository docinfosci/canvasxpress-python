#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# setup_mac.sh — macOS development environment setup
#
# Checks/installs: Homebrew, Node.js, uv, R, Git
# The dev interpreter is uv-managed (pinned by .python-version).
#
# Usage:
#   chmod +x setup_mac.sh && ./setup_mac.sh
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

echo "============================================================"
echo "  CanvasXpress Python — macOS Setup"
echo "============================================================"
echo ""

# ── Helpers ─────────────────────────────────────────────────────────────────
command_exists() { command -v "$1" &>/dev/null; }

print_header() { echo ""; echo "── $1 ──"; }

print_ok()   { echo "  ✓ $1"; }
print_info() { echo "  • $1"; }

# ── Homebrew ────────────────────────────────────────────────────────────────
print_header "Homebrew"

if ! command_exists brew; then
    echo "  ✗ Homebrew required. Install from https://brew.sh"
    echo ""
    echo "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    echo ""
    echo "  Re-run this script after installing Homebrew."
    exit 1
fi
print_ok "Homebrew $(brew --version | head -1)"

# ── Python 3.8+ (check only — the dev interpreter is uv-managed) ────────────
print_header "Python"

PYTHON_CMD=""
if command_exists python3; then
    PYTHON_CMD="python3"
elif command_exists python; then
    PYTHON_CMD="python"
fi

if [ -z "$PYTHON_CMD" ]; then
    echo "  ✗ Python 3.8+ required. Please install Python."
    echo "  (Homebrew: brew install python)"
    exit 1
fi

PY_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PY_MAJOR=$($PYTHON_CMD -c "import sys; print(sys.version_info.major)")
PY_MINOR=$($PYTHON_CMD -c "import sys; print(sys.version_info.minor)")

if [ "$PY_MAJOR" -lt 3 ] || ([ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 8 ]); then
    echo "  ✗ Python 3.8+ required (found $PY_VERSION)."
    exit 1
fi
print_ok "Python $PY_VERSION"

# ── Node.js (needed for Dash component builds) ─────────────────────────────
print_header "Node.js"

if ! command_exists node; then
    if command_exists nvm; then
        print_info "Installing via nvm..."
        nvm install 20
        nvm use 20
        nvm alias default 20
    else
        print_info "Installing via Homebrew..."
        brew install node
    fi
fi

NODE_VERSION=$(node --version)
print_ok "Node.js $NODE_VERSION"

# ── uv ──────────────────────────────────────────────────────────────────────
print_header "uv"

if ! command_exists uv; then
    print_info "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bash_profile"
    PATH="$HOME/.local/bin:$PATH"
fi
print_ok "uv $(uv --version)"

# ── R (for rpy2 — optional, skip if not needed) ────────────────────────────
print_header "R"

if ! command_exists R; then
    print_info "R not found — rpy2 extra will be skipped."
    print_info "Install via Homebrew if needed: brew install r"
    EXTRA_ARGS=(--extra dash --extra jupyter --extra streamlit --extra shiny --extra dev)
else
    print_ok "R $(R --version | head -1)"
    EXTRA_ARGS=(--extra all --extra dev)
fi

# ── Git ─────────────────────────────────────────────────────────────────────
print_header "Git"

if ! command_exists git; then
    print_info "Git not found. Installing via Homebrew..."
    brew install git
fi
print_ok "Git $(git --version)"

# ── Project environment & dependencies (uv-managed .venv) ───────────────────
print_header "Project Setup"

# pyproject.toml reads the version from this generated, git-ignored file, so
# generate it before `uv sync` (which builds the project).
if [ ! -f "canvasxpress/version.txt" ]; then
    print_info "Generating canvasxpress/version.txt..."
    uv run --no-project --with pytz --with gitpython python build_pkg_setup.py
fi

# The local development environment is uv-managed: `uv sync` creates/updates
# .venv (interpreter pinned by .python-version; uv downloads it if missing),
# installs the project plus the chosen extras from pyproject.toml, and
# refreshes uv.lock (committed). CircleCI uses a separate ./venv built with
# `uv pip install` — see AGENTS.md.
print_info "Syncing project environment with extras ${EXTRA_ARGS[*]}"
uv sync "${EXTRA_ARGS[@]}"
source ./.venv/bin/activate
print_ok "Virtual environment activated (.venv)"

# Headless Chromium for the platform visual tests (tests/functional/platform)
if python -c "import playwright" 2>/dev/null; then
    print_info "Installing headless Chromium for Playwright..."
    python -m playwright install chromium
fi

# Run invoke init
if command_exists invoke; then
    invoke init --dev --list
else
    print_info "invoke not found — skipping init"
fi

echo ""
echo "============================================================"
echo "  macOS Setup Complete!"
echo "============================================================"
echo ""
echo "Next steps:"
echo "  source .venv/bin/activate"
echo "  uv build            # build distribution"
echo "  uvx ruff check .     # lint"
echo "  invoke test          # test"
