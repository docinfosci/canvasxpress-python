@echo off
:: ---------------------------------------------------------------------------
:: setup_windows.bat - Windows development environment setup
::
:: Checks/installs: Node.js, uv, Git (via winget or Chocolatey),
::                  Python (via uv, if the requested version is missing)
:: Checks only:     R (optional, for rpy2)
::
:: Usage (from cmd or PowerShell, in the project root):
::   .\setup_windows.bat [python-version] [venv-dir]
::
::   python-version  Defaults to 3.13 (development). Use 3.8 or 3.10 to mirror
::                   the CircleCI build-python-oldest / build-python-general
::                   profiles. Must be 3.8+.
::   venv-dir        Defaults to venv.
::
:: Examples:
::   .\setup_windows.bat
::   .\setup_windows.bat 3.8 venv38
:: ---------------------------------------------------------------------------
setlocal EnableExtensions EnableDelayedExpansion

cd /d "%~dp0"

set "PY_REQ=%~1"
if not defined PY_REQ set "PY_REQ=3.13"
set "VENV_DIR=%~2"
if not defined VENV_DIR set "VENV_DIR=venv"

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
) else (
    call :print_info "R not found - rpy2 extras will be skipped."
    call :print_info "Install if needed: winget install RProject.R"
    set "EXTRAS=dash,jupyter,streamlit,shiny,dev"
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

:: -- Virtual environment & dependencies --------------------------------------
call :print_header "Project Setup"

if not exist "!VENV_DIR!\Scripts\python.exe" (
    call :print_info "Creating virtual environment !VENV_DIR!..."
    uv venv "!VENV_DIR!" --python "!PYTHON_EXE!" || goto :fail
)

:: Refuse to reuse a venv built on a different Python version.
for /f "delims=" %%v in ('call "!VENV_DIR!\Scripts\python.exe" -c "import sys; print('.'.join(map(str, sys.version_info[:2])))"') do set "VENV_PY_VER=%%v"
if not "!VENV_PY_VER!"=="!PY_VER!" (
    echo   [ERROR] !VENV_DIR! uses Python !VENV_PY_VER!, but !PY_VER! was requested.
    echo   Delete !VENV_DIR! or pass a different venv-dir, e.g.:
    echo   .\setup_windows.bat !PY_REQ! venv!PY_VER:.=!
    exit /b 1
)

call "!VENV_DIR!\Scripts\activate.bat" || goto :fail
call :print_ok "Virtual environment !VENV_DIR! activated [Python !VENV_PY_VER!]"

call :print_info "Installing build dependencies..."
uv pip install --no-cache-dir setuptools wheel pytz gitpython || goto :fail

:: pyproject.toml reads the version from this generated, git-ignored file.
if not exist "canvasxpress\version.py" (
    call :print_info "Generating canvasxpress\version.py..."
    python build_pkg_setup.py || goto :fail
)

call :print_info "Installing project with extras [!EXTRAS!]..."
:: pywinpty (Windows-only, via jupyter-server) has releases with no wheel for
:: older Pythons and an sdist that fails to build, so only accept wheels.
uv pip install --no-cache-dir --only-binary pywinpty -e ".[!EXTRAS!]" || goto :fail

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
