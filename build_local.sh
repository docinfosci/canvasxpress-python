#!/usr/bin/env bash

set -e

echo "========================================"
echo "  CanvasXpress Python Build (Local)"
echo "========================================"
echo ""

# ── OS detection and system dependencies ────────────────────────────────────
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="darwin"
else
    echo "Unknown OS: $OSTYPE"
    exit 1
fi

echo "Detected OS: $OS"

if [[ "$OS" == "linux" ]]; then
    echo "Installing system packages..."
    export DEBIAN_FRONTEND=noninteractive
    export DEBIAN_PRIORITY=critical

    if command -v ntpdate &> /dev/null; then
      ntpdate -s time.nist.gov 2>/dev/null || true
    elif command -v chronyc &> /dev/null; then
      chronyc makestep 2>/dev/null || true
    else
      apt-get install -y -o Acquire::Retries=3 ntpdate 2>/dev/null || true
      ntpdate -s time.nist.gov 2>/dev/null || true
    fi

    rm -rf /var/lib/apt/lists/*
    apt-get clean
    apt-get update -y -o Acquire::Retries=3 || true

    apt-get install -y -o Acquire::Retries=3 \
      debconf-utils dialog apt-utils wget curl gcc make cmake build-essential \
      || true

    apt-get clean
    rm -rf /var/lib/apt/lists/*

elif [[ "$OS" == "darwin" ]]; then
    echo "Installing system packages via Homebrew..."

    if ! command -v R &> /dev/null; then
      brew install r || true
    else
      echo "R is already installed: $(R --version | head -1)"
    fi

    mkdir -p "$HOME/.nvm"
fi

# ── Node.js (needed for Dash component builds) ──────────────────────────────
echo ""
echo "Installing Node.js 18..."
export NVM_DIR="$HOME/.nvm"
mkdir -p "$NVM_DIR"
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash 2>/dev/null || true

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

nvm install 18
nvm use 18
nvm alias default 18

echo "Node.js version: $(node --version)"
echo "NPM version: $(npm --version)"

# ── Project environment & dependencies (uv-managed .venv) ───────────────────
echo ""
echo "Syncing project environment (uv-managed .venv)..."

# Generate version.txt once, before installing the project, so that the installed,
# tested and skill-stamped package has the same version as the built distribution.
echo "Generating version.txt..."
uv run --no-project --with pytz --with gitpython python ./build_pkg_setup.py

# `uv sync` creates/updates .venv (interpreter pinned by .python-version) and
# installs the project plus the chosen extras from pyproject.toml, keeping
# uv.lock in step. CircleCI uses a separate ./venv built with `uv pip install`.
EXTRA_ARGS=(--extra dash --extra jupyter --extra streamlit --extra shiny --extra dev)
if command -v R &> /dev/null; then
    EXTRA_ARGS=(--extra all --extra dev)
fi
echo "Installing project with extras ${EXTRA_ARGS[*]}"
uv sync "${EXTRA_ARGS[@]}"
source ./.venv/bin/activate

echo "Python version: $(python --version)"

# Headless Chromium for the platform visual tests (tests/functional/platform),
# which run here but not in CircleCI. On Linux, also the system libraries it needs.
if python -c "import playwright" 2>/dev/null; then
    if [[ "$OS" == "linux" ]]; then
        python -m playwright install --with-deps chromium
    else
        python -m playwright install chromium
    fi
fi

# Run the invoke init step
invoke init --dev --list


# ── Static analysis (replaces prospector → ruff) ────────────────────────────
echo ""
echo "Running static analysis (ruff)..."
uvx ruff check ./canvasxpress

echo ""
echo "Checking Python 3.8 compatibility (vermin)..."
uvx vermin ./canvasxpress

# ── Run tests ───────────────────────────────────────────────────────────────
echo ""
echo "Running tests, including the platform visual tests..."
invoke test --platform

# ── Build distribution ──────────────────────────────────────────────────────
# Uses the version.txt generated above, so the distribution matches what was tested.
echo ""
echo "Building distribution version $(cat canvasxpress/version.txt)..."

# Clear uv build cache and stale metadata to ensure fresh build
uv cache clean 2>/dev/null || true
rm -rf canvasxpress.egg-info build

echo ""
echo "Building distribution..."
uv build

echo ""
echo "========================================"
echo "  Build Complete!"
echo "========================================"
echo ""
echo "Distributions in ./dist/:"
ls -la dist/ 2>/dev/null || true
