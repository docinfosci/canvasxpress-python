@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo   CanvasXpress Python — Windows Setup
echo ============================================================
echo.

:: ── Helpers ─────────────────────────────────────────────────────────────
:command_exists
    where %1 >nul 2>&1
    if !errorlevel! equ 0 (
        echo   [OK] %1
        exit /b 0
    ) else (
        echo   [MISSING] %1
        exit /b 1
    )
endlocal

:print_header
echo.
echo -- %1 --
exit /b

:print_ok
echo   [OK] %1
exit /b

:print_info
echo   [*] %1
exit /b

:install_with_choco
    set PKG=%1
    if not exist "%ProgramData%\chocolatey\bin\choco.exe" (
        echo   [*] Chocolatey not found. Installing...
        powershell -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
    )
    echo   [*] Installing %PKG% via Chocolatey...
    choco install %PKG% -y
    echo   [OK] %PKG%
    exit /b

:print_rscript
    echo.
    echo ============================================================
    echo   Windows Setup Complete!
    echo ============================================================
    echo.
    echo Next steps:
    echo   .\venv\Scripts\activate
    echo   uv build                   :: build distribution
    echo   uvx ruff check .           :: lint
    echo   uvx pytest                 :: test
    exit /b

:: ── Package manager check ─────────────────────────────────────────────────

echo   [*] Checking package manager...
command_exists choco || command_exists winget || (
    echo.
    echo   [ERROR] No package manager found.
    echo   Install Chocolatey: https://chocolatey.org/install
    echo   or winget: https://aka.ms/winget-client
    echo.
    echo   Then re-run this script.
    exit /b 1
)

:: ── Python 3.8+ (check only — user manages their own) ─────────────────────
print_header "Python"

command_exists python || command_exists python3 || (
    echo   [ERROR] Python 3.8+ required. Please install Python.
    echo   (choco: choco install python)
    exit /b 1
)

for /f "tokens=1-2 delims=." %%a in ('python --version 2^>^&1') do set PY_VER=%%a.%%b
for /f "delims=." %%a in ('python --version 2^>^&1') do set PY_MAJOR=%%a
for /f "tokens=1-2 delims=." %%a in ('python --version 2^>^&1') do set PY_MINOR=%%b

if !PY_MAJOR! lss 3 (
    echo   [ERROR] Python 3.8+ required.
    exit /b 1
)
if !PY_MINOR! lss 8 (
    echo   [ERROR] Python 3.8+ required (found !PY_VER!).
    exit /b 1
)
echo   [OK] Python !PY_VER!

:: ── Node.js (needed for Dash component builds) ────────────────────────────
print_header "Node.js"

command_exists node || (
    print_info "Installing Node.js..."
    if exist "%ProgramData%\chocolatey\bin\choco.exe" (
        choco install nodejs-lts
    ) else (
        winget install OpenJS.NodeJS.LTS
    )
)
for /f "delims=" %%a in ('node --version') do set NODE_VER=%%a
echo   [OK] Node.js !NODE_VER!

:: ── uv ────────────────────────────────────────────────────────────────────
print_header "uv"

command_exists uv || (
    print_info "Installing uv via pip..."
    python -m pip install --upgrade uv
)
for /f "delims=" %%a in ('uv --version') do set UV_VER=%%a
echo   [OK] uv !UV_VER!

:: ── R (for rpy2 — optional) ───────────────────────────────────────────────
print_header "R"

command_exists R || command_exists Rscript || (
    echo   [*] R not found — rpy2 extras will be skipped.
    echo   Install via Chocolatey: choco install r.project
) || (
    for /f "tokens=1-2 delims= " %%a in ('R --version 2^>^&1 ^| findstr /c:"R version"') do set R_VER=%%a %%b
    echo   [OK] R !R_VER!
)

:: ── Git ───────────────────────────────────────────────────────────────────
print_header "Git"

command_exists git || (
    print_info "Installing Git..."
    if exist "%ProgramData%\chocolatey\bin\choco.exe" (
        choco install git
    ) else (
        winget install Git.Git
    )
)
for /f "delims=" %%a in ('git --version') do set GIT_VER=%%a
echo   [OK] Git !GIT_VER!

:: ── Build tools ───────────────────────────────────────────────────────────
print_header "Build tools"

command_exists cl || (
    echo   [*] Visual Studio C++ Build Tools not found.
    echo   Required for building some Python packages (e.g. rpy2, selenium).
    echo   Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
    echo   Select 'Desktop development with C++' workload.
)

:: ── Virtual environment & dependencies ────────────────────────────────────
print_header "Project Setup"

if not exist "venv" (
    print_info "Creating virtual environment..."
    python -m venv venv
)
call venv\Scripts\activate
echo   [OK] Virtual environment activated

:: Bootstrap tools
print_info "Installing build dependencies..."
uv pip install --no-cache-dir setuptools wheel

:: Project + all extras
print_info "Installing project dependencies..."
uv pip install --no-cache-dir ".[all]"

:: Dev tools
print_info "Installing development tools..."
uv sync

:: Run invoke init
where invoke >nul 2>&1 && (
    invoke init --dev --list
) || (
    echo   [*] invoke not found — skipping init
)

print_rscript
