@echo off
:: ---------------------------------------------------------------------------
:: setup_windows.bat - Windows development environment setup
::
:: Checks/installs: Node.js, uv, Git (via winget or Chocolatey),
::                  Python (via uv, if the requested version is missing)
:: Checks only:     R (optional, for rpy2)
::
:: Creates a single uv-managed development environment (.venv) on Python 3.13
:: (pinned by .python-version; uv downloads it if missing). Python 3.8
:: compliance of the package logic is enforced by vermin (see vermin.ini),
:: and CircleCI tests 3.8 / 3.10 / 3.15 at runtime.
::
:: Usage (from cmd or PowerShell, in the project root):
::   .\setup_windows.bat
:: ---------------------------------------------------------------------------
setlocal EnableExtensions EnableDelayedExpansion

cd /d "%~dp0"

set "PY_REQ=3.13"
set "VENV_DIR=.venv"

echo ============================================================
echo   CanvasXpress Python - Windows Setup
echo ============================================================

:: -- Package manager --------------------------------------------------------
call :print_header "Package manager"

set "PKG_MGR="
where winget >nul 2>&1 && set "PKG_MGR=winget"
if not defined PKG_MGR where choco >nul 2>&1 && set "PKG_MGR=choco"
if not defined PKG_MGR (
    echo   [ERROR] No package manager found.
    echo   Install winget: https://aka.ms/winget-client
    echo   or Chocolatey:  https://chocolatey.org/install
    echo   Then re-run this script.
    exit /b 1
)
call :print_ok "!PKG_MGR!"

:: -- Node.js (needed for Dash component builds) -----------------------------
call :print_header "Node.js"

where node >nul 2>&1 || (
    call :print_info "Installing Node.js LTS..."
    call :pkg_install OpenJS.NodeJS.LTS nodejs-lts
    set "PATH=%ProgramFiles%\nodejs;!PATH!"
)
where node >nul 2>&1 || (
    echo   [ERROR] Node.js not found after install. Open a new terminal and re-run.
    exit /b 1
)
for /f "delims=" %%v in ('node --version') do set "NODE_VER=%%v"
call :print_ok "Node.js !NODE_VER!"

:: -- uv ----------------------------------------------------------------------
call :print_header "uv"

where uv >nul 2>&1 || (
    call :print_info "Installing uv..."
    powershell -NoProfile -ExecutionPolicy ByPass -Command "irm https://astral.sh/uv/install.ps1 | iex"
    set "PATH=%USERPROFILE%\.local\bin;!PATH!"
)
where uv >nul 2>&1 || (
    echo   [ERROR] uv not found after install. Open a new terminal and re-run.
    exit /b 1
)
for /f "delims=" %%v in ('uv --version') do set "UV_VER=%%v"
call :print_ok "!UV_VER!"

:: -- Python (uses an installed interpreter, else uv downloads one) -----------
call :print_header "Python !PY_REQ!"

set "PYTHON_EXE="
for /f "delims=" %%p in ('uv python find !PY_REQ! 2^>nul') do set "PYTHON_EXE=%%p"
if not defined PYTHON_EXE (
    call :print_info "Python !PY_REQ! not found. Installing via uv..."
    uv python install !PY_REQ! || goto :fail
    for /f "delims=" %%p in ('uv python find !PY_REQ! 2^>nul') do set "PYTHON_EXE=%%p"
)
if not defined PYTHON_EXE (
    echo   [ERROR] Could not find or install Python !PY_REQ!.
    exit /b 1
)

for /f "delims=" %%v in ('call "!PYTHON_EXE!" -c "import sys; print('.'.join(map(str, sys.version_info[:2])))"') do set "PY_VER=%%v"
"!PYTHON_EXE!" -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)"
if errorlevel 1 (
    echo   [ERROR] Python 3.8+ required, found !PY_VER!.
    exit /b 1
)
call :print_ok "Python !PY_VER! [!PYTHON_EXE!]"

:: -- R (for rpy2 - optional) -------------------------------------------------
call :print_header "R"

:: The R installer does not add R to PATH, so also look in Program Files.
set "R_FOUND="
where R >nul 2>&1 && set "R_FOUND=1"
if not defined R_FOUND (
    for /d %%d in ("%ProgramFiles%\R\R-*") do (
        if exist "%%d\bin\R.exe" (
            set "R_HOME=%%d"
            set "R_FOUND=1"
        )
    )
    if defined R_FOUND set "PATH=!R_HOME!\bin;!PATH!"
)
if defined R_FOUND (
    for /f "tokens=3" %%v in ('R --version 2^>^&1 ^| findstr /b /c:"R version"') do set "R_VER=%%v"
    call :print_ok "R !R_VER!"
    set "EXTRAS=all,dev"
    set "EXTRA_ARGS=--extra all --extra dev"
) else (
    call :print_info "R not found - rpy2 extra will be skipped."
    call :print_info "Install if needed: winget install RProject.R"
    set "EXTRAS=dash,jupyter,streamlit,shiny,dev"
    set "EXTRA_ARGS=--extra dash --extra jupyter --extra streamlit --extra shiny --extra dev"
)

:: -- Git ---------------------------------------------------------------------
call :print_header "Git"

where git >nul 2>&1 || (
    call :print_info "Installing Git..."
    call :pkg_install Git.Git git
    set "PATH=%ProgramFiles%\Git\cmd;!PATH!"
)
where git >nul 2>&1 || (
    echo   [ERROR] Git not found after install. Open a new terminal and re-run.
    exit /b 1
)
for /f "delims=" %%v in ('git --version') do set "GIT_VER=%%v"
call :print_ok "!GIT_VER!"

:: -- Build tools (check only) ------------------------------------------------
call :print_header "Build tools"

where cl >nul 2>&1 && (
    call :print_ok "MSVC C++ compiler"
) || (
    call :print_info "Visual Studio C++ Build Tools not on PATH."
    call :print_info "Only needed if a dependency has no prebuilt wheel."
    call :print_info "https://visualstudio.microsoft.com/visual-cpp-build-tools/"
)

:: -- Project environment & dependencies (uv-managed .venv) -------------------
call :print_header "Project Setup"

:: pyproject.toml reads the version from this generated, git-ignored file, so
:: generate it before `uv sync` (which builds the project).
if not exist "canvasxpress\version.txt" (
    call :print_info "Generating canvasxpress\version.txt..."
    uv run --no-project --with pytz --with gitpython python build_pkg_setup.py || goto :fail
)

:: The local development environment is uv-managed: `uv sync` creates/updates
:: .venv (interpreter pinned by .python-version), installs the project plus
:: the chosen extras from pyproject.toml, and refreshes uv.lock (committed).
:: CircleCI uses a separate .\venv built with `uv pip install` - see AGENTS.md.
:: (pywinpty's sdist needs MSVC; [tool.uv] no-build in pyproject.toml keeps
:: resolution and sync on wheels only.)
call :print_info "Syncing project environment with extras [!EXTRAS!]..."
uv sync !EXTRA_ARGS! || goto :fail
call "!VENV_DIR!\Scripts\activate.bat" || goto :fail
call :print_ok "Virtual environment !VENV_DIR! activated"

:: Headless Chromium for the platform visual tests (tests\functional\platform)
python -c "import playwright" >nul 2>&1 && (
    call :print_info "Installing headless Chromium for Playwright..."
    python -m playwright install chromium || goto :fail
)

where invoke >nul 2>&1 && (
    invoke init --dev --list || goto :fail
) || (
    call :print_info "invoke not found - skipping init"
)

echo.
echo ============================================================
echo   Windows Setup Complete!
echo ============================================================
echo.
echo Next steps:
echo   .\!VENV_DIR!\Scripts\activate        (PowerShell: .\!VENV_DIR!\Scripts\Activate.ps1)
echo   uv build                       build distribution
echo   uvx ruff check .               lint
echo   invoke test                    test
endlocal
exit /b 0

:: ===========================================================================
:: Subroutines
:: ===========================================================================
:fail
echo.
echo   [ERROR] Setup failed - see the output above.
exit /b 1

:print_header
echo.
echo -- %~1 --
exit /b 0

:print_ok
echo   [OK] %~1
exit /b 0

:print_info
echo   [*] %~1
exit /b 0

:: pkg_install <winget-id> <choco-package>
:pkg_install
if /i "%PKG_MGR%"=="winget" (
    winget install --id %~1 -e --accept-source-agreements --accept-package-agreements
) else (
    choco install %~2 -y
)
exit /b %errorlevel%
