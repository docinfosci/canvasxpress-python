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

# ── Python virtual environment & dependencies ───────────────────────────────
echo ""
echo "Setting up Python virtual environment..."
if ! [[ -d ./venv ]] ; then
    python3 -m venv ./venv
fi
source ./venv/bin/activate

echo "Python version: $(python3 --version)"

# Bootstrap build tools (replaces requirements-project.txt)
echo "Installing build dependencies..."
pip install --no-cache-dir -U pip setuptools wheel

# Install project + all extras (replaces requirements.txt)
echo "Installing project dependencies..."
uv pip install --no-cache-dir ".[all]"

# Install dev tools (replaces requirements-dev.txt — handled by uv tools)
echo "Installing dev tools..."
uv sync

# Run the invoke init step
invoke init --dev --list

# ── Build Dash components ───────────────────────────────────────────────────
echo ""
echo "Building Dash components..."
cd plotly/cxdash/

if ! [[ -d ./venv ]] ; then
    python3 -m venv ./venv
fi
source ./venv/bin/activate

pip install -U pip setuptools wheel
uv pip install --no-cache-dir -r requirements.txt

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
nvm install 20
nvm use 20

npm install canvasxpress
npm install canvasxpress-react
npm run build
cp -R ./cxdash ../../

cd ../../

# ── Back to main venv ───────────────────────────────────────────────────────
deactivate
source venv/bin/activate

# ── Static analysis (replaces prospector → ruff) ────────────────────────────
echo ""
echo "Running static analysis (ruff)..."
uvx ruff check ./canvasxpress

# ── Run tests ───────────────────────────────────────────────────────────────
echo ""
echo "Running tests..."
invoke test

# ── Update version & build distribution ─────────────────────────────────────
echo ""
echo "Generating version.ini..."
python3 ./build_pkg_setup.py

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
