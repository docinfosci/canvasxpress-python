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
The project is developed using Python 3.13 but must be compatible with Python 3.10 to maintain broad compatibility across different environments.

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
