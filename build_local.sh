#!/usr/bin/env bash

set -e

echo "========================================"
echo "  CanvasXpress Python Build (Local)"
echo "========================================"
echo ""

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="darwin"
else
    echo "Unknown OS: $OSTYPE"
    exit 1
fi

echo "Detected OS: $OS"

# Install system dependencies
if [[ "$OS" == "linux" ]]; then
    echo ""
    echo "Installing system packages..."
    export DEBIAN_FRONTEND=noninteractive
    export DEBIAN_PRIORITY=critical

    # Fix expired repository issue by synchronizing clock
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
      debconf-utils \
      dialog \
      apt-utils \
      wget \
      curl \
      gcc \
      make \
      cmake \
      build-essential \
      || true

    apt-get clean
    rm -rf /var/lib/apt/lists/*
fi

# Install NVM and Node.js 18
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

# Create virtual environment
echo ""
echo "Setting up Python virtual environment..."
if ! [[ -d ./venv ]] ; then
    python3 -m venv ./venv
fi
source ./venv/bin/activate

echo "Python version: $(python3 --version)"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip config set global.root-user-action ignore 2>/dev/null || true
pip install --no-cache-dir -U pip==24.3.1 setuptools wheel
pip install --no-cache-dir -U -r ./requirements-project.txt
pip install --no-cache-dir -U -r ./requirements.txt
pip install --no-cache-dir -U -r ./requirements-dev.txt
invoke init --dev --list

# Build Dash components
echo ""
echo "Building Dash components..."
cd plotly/cxdash/

if ! [[ -d ./venv ]] ; then
    python3 -m venv ./venv
fi
source ./venv/bin/activate

pip install -U pip setuptools wheel
pip install -U -r requirements.txt

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
nvm install 20
nvm use 20

npm install canvasxpress
npm install canvasxpress-react

npm run build
cp -R ./cxdash ../../

cd ../../

# Switch back to main venv
deactivate
source venv/bin/activate

# Static analysis
echo ""
echo "Running static analysis..."
prospector \
    --zero-exit \
    --show-profile \
    --no-autodetect \
    --strictness low \
    -o text \
    ./canvasxpress

# Run tests
echo ""
echo "Running tests..."
invoke test

# Run reports (disabled for local builds - requires CI token)
# echo ""
# echo "Generating reports..."
# invoke report

# Update VERSION file and generate setup.py
echo ""
echo "Updating version and generating setup.py..."
python3 ./build_pkg_setup.py

# Run setup.py
echo ""
echo "Running setup.py..."
python3 setup.py --version

echo ""
echo "========================================"
echo "  Build Complete!"
echo "========================================"
