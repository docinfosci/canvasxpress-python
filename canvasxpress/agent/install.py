"""
User-facing CLI entry point for CanvasXpress agent skill installation.

Usage:
    python -m canvasxpress.agent.install [--target TARGET] [--force]
"""

import sys

from canvasxpress.agent._install import install, cli

__all__ = ['install', 'cli']


def main() -> None:
    """Entry point for the agent skill installation CLI."""
    cli()


if __name__ == '__main__':
    main()
