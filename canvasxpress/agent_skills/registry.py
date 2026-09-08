"""
Dynamic agent skill discovery for CanvasXpress.

Provides programmatic access to discover and retrieve agent skills
installed with the canvasxpress package. Uses importlib.resources and
setuptools entry points for platform-agnostic discovery.
"""

import sys
from importlib.metadata import entry_points
from pathlib import Path


def _get_entry_points():
    """Get entry points for canvasxpress.skills namespace (Python 3.8+ compatible)."""
    eps = entry_points()
    if hasattr(eps, 'get'):
        # Python < 3.10
        return eps.get('canvasxpress.skills', [])
    else:
        # Python >= 3.10
        return eps


def _read_module_file(module_path, filename):
    """Read a file from a module (Python 3.8+ compatible)."""
    import importlib.resources
    if hasattr(importlib.resources, 'files'):
        # Python 3.9+
        return importlib.resources.files(module_path).joinpath(filename).read_text(encoding='utf-8')
    else:
        # Python 3.8
        return importlib.resources.read_text(module_path, filename, encoding='utf-8')


def discover_skills():
    """
    Scan the installed environment for canvasxpress agent skills
    and extract their markdown instructions dynamically.

    Returns:
        dict: Mapping of skill names to their content with metadata.
              Example: {"chart_builder": {"name": "chart_builder", "content": "..."}, ...}
    """
    skills_map = {}
    eps = _get_entry_points()

    for ep in eps:
        module_path = ep.value
        try:
            content = _read_module_file(module_path, "SKILL.md")
            skills_map[ep.name] = {
                "name": ep.name,
                "content": content
            }
        except Exception:
            pass

    return skills_map


def install_skills(target: str = 'both', force: bool = False) -> None:
    """
    Install CanvasXpress agent skills to OpenCode and/or Claude Code directories.

    Args:
        target: Where to install skills. Options: 'opencode', 'claude', 'both'.
        force: If True, overwrite existing skill files.
    """
    import importlib.resources
    from pathlib import Path

    targets = []
    if target in ('opencode', 'both'):
        targets.append(Path.home() / '.opencode/skills')
    if target in ('claude', 'both'):
        targets.append(Path.home() / '.agents/skills')

    if not targets:
        print(f"Invalid target: {target}. Use 'opencode', 'claude', or 'both'.")
        sys.exit(1)

    eps = _get_entry_points()
    if not eps:
        print("No CanvasXpress skills found. Is the package properly installed?")
        sys.exit(1)

    for ep in eps:
        module_path = ep.value
        try:
            skill_content = _read_module_file(module_path, "SKILL.md")
            for skills_dir in targets:
                dest = skills_dir / ep.name / "SKILL.md"
                dest.parent.mkdir(parents=True, exist_ok=True)
                if dest.exists() and not force:
                    print(f"Skill file already exists at {dest}. Use --force to overwrite.")
                    continue
                dest.write_text(skill_content, encoding="utf-8")
                print(f"CanvasXpress skill '{ep.name}' installed to: {dest}")
        except Exception as e:
            print(f"Failed to install skill '{ep.name}': {e}")


def cli() -> None:
    """Command-line interface for installing CanvasXpress agent skills."""
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

    install_skills(target=target, force=force)


if __name__ == '__main__':
    cli()
