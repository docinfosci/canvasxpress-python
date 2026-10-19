#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# setup_mac.sh — macOS development environment setup
#
# Checks/installs: Homebrew, Node.js, uv, R, Git
# User manages their own Python (3.8+) — uv creates the venv.
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
    print_info "R not found — rpy2 extras will be skipped."
    print_info "Install via Homebrew if needed: brew install r"
else
    print_ok "R $(R --version | head -1)"
fi

# ── Git ─────────────────────────────────────────────────────────────────────
print_header "Git"

if ! command_exists git; then
    print_info "Git not found. Installing via Homebrew..."
    brew install git
fi
print_ok "Git $(git --version)"

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

# Install project + all extras
print_info "Installing project dependencies..."
uv pip install --no-cache-dir ".[all]"

# Install dev tools
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
echo "  macOS Setup Complete!"
echo "============================================================"
echo ""
echo "Next steps:"
echo "  source venv/bin/activate"
echo "  uv build            # build distribution"
echo "  uvx ruff check .     # lint"
echo "  uvx pytest           # test"
