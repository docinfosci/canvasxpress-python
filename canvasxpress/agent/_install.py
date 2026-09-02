"""
Internal installation logic for CanvasXpress agent skill injection.

This module provides the core functionality to inject the CanvasXpress
agent skill into OpenCode and Claude Code skill directories.
"""

import os
import shutil
import sys
from pathlib import Path

try:
    import canvasxpress
    _SKILL_FILE = os.path.join(os.path.dirname(canvasxpress.__file__), 'agent', 'canvasxpress.md')
except ImportError:
    # When running as a module, canvasxpress may not be installed yet
    _SKILL_FILE = None

OPENCODE_DEST = Path.home() / '.opencode/skills/canvasxpress/SKILL.md'
CLAUDE_DEST = Path.home() / '.agents/skills/canvasxpress/SKILL.md'


def _install_skill(target_path: Path, force: bool = False) -> bool:
    """Install the CanvasXpress skill file to the specified path.

    Args:
        target_path: The path where the SKILL.md file should be installed.
        force: If True, overwrite an existing skill file.

    Returns:
        True if the skill was installed successfully, False otherwise.
    """
    if not os.path.exists(_SKILL_FILE):
        print(f"Warning: CanvasXpress skill file not found at {_SKILL_FILE}")
        return False

    target_path.parent.mkdir(parents=True, exist_ok=True)

    if target_path.exists() and not force:
        print(f"Skill file already exists at {target_path}. Use --force to overwrite.")
        return False

    shutil.copy2(_SKILL_FILE, target_path)
    return True


def install(target: str = 'both', force: bool = False) -> None:
    """Install the CanvasXpress agent skill to OpenCode and/or Claude Code.

    Args:
        target: Where to install the skill. Options: 'opencode', 'claude', 'both'.
        force: If True, overwrite existing skill files.

    Returns:
        None. Prints status messages to stdout/stderr.
    """
    targets = []
    if target in ('opencode', 'both'):
        targets.append(OPENCODE_DEST)
    if target in ('claude', 'both'):
        targets.append(CLAUDE_DEST)

    if not targets:
        print(f"Invalid target: {target}. Use 'opencode', 'claude', or 'both'.")
        sys.exit(1)

    if not os.path.exists(_SKILL_FILE):
        print(f"Error: CanvasXpress skill file not found at {_SKILL_FILE}")
        print("The canvasxpress package may not be properly installed.")
        print("You can try: pip install canvasxpress")
        sys.exit(1)

    for dest in targets:
        try:
            success = _install_skill(dest, force)
            if success:
                print(f"CanvasXpress skill installed to: {dest}")
        except Exception as e:
            print(f"Failed to install skill to {dest}: {e}")


def cli() -> None:
    """Command-line interface for installing the CanvasXpress agent skill.

    Parses command-line arguments and calls install() to perform the
    actual installation.

    Usage:
        python -m canvasxpress.agent._install [--target TARGET] [--force]

    Args:
        --target: Where to install the skill. Options: 'opencode', 'claude', 'both'.
            Default: 'both'.
        --force: Overwrite existing skill files.

    Returns:
        None. Exits with status code 0 on success, 1 on error.
    """
    target = 'both'
    force = False

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] in ('--target', '-t'):
            if i + 1 < len(args):
                target = args[i + 1]
                i += 2
            else:
                print("Error: --target requires a value")
                sys.exit(1)
        elif args[i] in ('--force', '-f'):
            force = True
            i += 1
        elif args[i] in ('--help', '-h'):
            print("Usage: canvasxpress [--target TARGET] [--force]")
            print("")
            print("Options:")
            print("  --target, -t TARGET  Where to install: 'opencode', 'claude', 'both' (default: 'both')")
            print("  --force, -f          Overwrite existing skill files")
            print("  --help, -h           Show this help message")
            sys.exit(0)
        else:
            print(f"Unknown argument: {args[i]}")
            sys.exit(1)

    install(target=target, force=force)


if __name__ == '__main__':
    cli()
