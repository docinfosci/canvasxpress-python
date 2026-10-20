#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# setup_linux.sh — Ubuntu / Debian development environment setup
#
# Checks/installs: Node.js, uv, R, Git, build tools
# User manages their own Python (3.8+) — uv creates the venv.
#
# Package manager: apt (Debian/Ubuntu)
# R installation:   official CRAN repository
#
# Usage:
#   chmod +x setup_linux.sh && ./setup_linux.sh
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

echo "============================================================"
echo "  CanvasXpress Python — Linux Setup (Ubuntu/Debian)"
echo "============================================================"
echo ""

# ── Helpers ─────────────────────────────────────────────────────────────────
command_exists() { command -v "$1" &>/dev/null; }

print_header() { echo ""; echo "── $1 ──"; }
print_ok()     { echo "  ✓ $1"; }
print_info()   { echo "  • $1"; }

apt_install() {
    sudo apt-get update -y
    sudo apt-get install -y "$@"
}

# ── Python 3.8+ (check only — user manages their own) ──────────────────────
print_header "Python"

PYTHON_CMD=""
if command_exists python3; then
    PYTHON_CMD="python3"
elif command_exists python; then
    PYTHON_CMD="python"
fi

if [ -z "$PYTHON_CMD" ]; then
    echo "  ✗ Python 3.8+ required. Please install Python."
    echo "  (apt: sudo apt install python3 python3-venv python3-dev)"
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
    # Use NodeSource for latest Node.js on Debian/Ubuntu
    if command_exists curl; then
        print_info "Installing via NodeSource..."
        curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
        apt_install nodejs
    else
        print_info "Installing via apt..."
        apt_install nodejs npm
    fi
fi

NODE_VERSION=$(node --version)
print_ok "Node.js $NODE_VERSION"

# ── uv ──────────────────────────────────────────────────────────────────────
print_header "uv"

if ! command_exists uv; then
    print_info "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.profile"
    PATH="$HOME/.local/bin:$PATH"
fi
print_ok "uv $(uv --version)"

# ── R (for rpy2 — optional) ────────────────────────────────────────────────
print_header "R"

if ! command_exists R; then
    print_info "R not found — rpy2 extras will be skipped."
    print_info "Install via CRAN: sudo apt install r-base r-base-dev"
else
    print_ok "R $(R --version | head -1)"
fi

# ── Git ─────────────────────────────────────────────────────────────────────
print_header "Git"

if ! command_exists git; then
    print_info "Git not found. Installing via apt..."
    apt_install git
fi
print_ok "Git $(git --version)"

# ── Build tools ─────────────────────────────────────────────────────────────
print_header "Build tools"

print_info "Installing build dependencies..."
apt_install build-essential gcc g++ make cmake pkg-config

# ── Virtual environment & dependencies ──────────────────────────────────────
print_header "Project Setup"

if [ ! -d "venv" ]; then
    print_info "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
fi
source ./venv/bin/activate
print_ok "Virtual environment activated"

# Bootstrap tools
print_info "Installing build dependencies..."
uv pip install --no-cache-dir setuptools wheel

# Project + all extras
print_info "Installing project dependencies..."
uv pip install --no-cache-dir ".[all]"

# Dev tools
print_info "Installing development tools..."
uv sync

# Run invoke init
if command_exists invoke; then
    invoke init --dev --list
else
    print_info "invoke not found — skipping init"
fi

echo ""
echo "============================================================"
echo "  Linux Setup Complete!"
echo "============================================================"
echo ""
echo "Next steps:"
echo "  source venv/bin/activate"
echo "  uv build            # build distribution"
echo "  uvx ruff check .     # lint"
echo "  uvx pytest           # test"
