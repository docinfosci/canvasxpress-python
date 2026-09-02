"""
User-facing CLI entry point for CanvasXpress agent skill installation.

Usage:
    python -m canvasxpress.agent.install [--target TARGET] [--force]
"""

import sys

from canvasxpress.agent._install import install, cli

__all__ = ['install', 'cli']


def main() -> None:
    """Entry point for the agent skill installation CLI.

    This function serves as the programmatic entry point for the CLI.
    It delegates to the cli() function from the internal _install module.

    Returns:
        None. Exits with status code 0 on success, 1 on error.
    """
    cli()


if __name__ == '__main__':
    main()
