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
    """Get entry points for canvasxpress.skills namespace (Python 3.8+)."""
    eps = entry_points()
    if hasattr(eps, 'select'):
        # Python 3.10+ has select() method
        return eps.select(group='canvasxpress.skills')
    else:
        # Python 3.8-3.9 requires get() method
        return eps.get('canvasxpress.skills', [])


def _read_module_file(module_path, filename):
    """Read a file from a module (Python 3.8+ compatible)."""
    import importlib.resources
    if sys.version_info >= (3, 9):
        # Python 3.9+ has importlib.resources.files()
        return importlib.resources.files(module_path).joinpath(filename).read_text(encoding='utf-8')
    else:
        # Python 3.8 uses read_text()
        return importlib.resources.read_text(module_path, filename, encoding='utf-8')


def discover_skills():
    """
    Scan the installed environment for canvasxpress agent skills
    and extract their markdown instructions dynamically.

    Returns:
        dict: Mapping of skill names to their content with metadata.
              Example: {"canvasxpress_charts": {"name": "canvasxpress_charts", "content": "..."}, ...}
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


def install_skills(target: str = 'all', force: bool = False) -> None:
    """
    Install CanvasXpress agent skills to OpenCode, Claude Code, oMLX, and/or Ollama directories.

    Args:
        target: Where to install skills. Options:
            - 'opencode': ~/.config/opencode/skills/ or ~/.opencode/skills/
            - 'claude': ~/.claude/skills/
            - 'agents': ~/.agents/skills/
            - 'all': Install to all directories (default)
            - 'both': Install to opencode and agents only
        force: If True, overwrite existing skill files.
    """
    import importlib.resources
    from pathlib import Path

    home = Path.home()
    target_map = {
        'opencode': home / '.config' / 'opencode' / 'skills',
        'claude': home / '.claude' / 'skills',
        'agents': home / '.agents' / 'skills',
    }

    targets = []
    if target == 'all':
        targets = list(target_map.values())
    elif target == 'both':
        targets = [target_map['opencode'], target_map['agents']]
    elif target in target_map:
        targets.append(target_map[target])
    else:
        print(f"Invalid target: {target}. Use 'opencode', 'claude', 'agents', 'all', or 'both'.")
        sys.exit(1)

    eps = _get_entry_points()
    if not eps:
        print("No CanvasXpress skills found. Is the package properly installed?")
        sys.exit(1)

    for ep in eps:
        module_path = ep.value
        try:
            skill_content = _read_module_file(module_path, "SKILL.md")
            # Handle sub-skills: if name contains '.', install as subdirectory
            skill_name = ep.name
            parts = skill_name.split('.')
            if len(parts) > 1:
                # Sub-skill: use full path (e.g., canvasxpress_charts.events -> canvasxpress_charts/events)
                relative_path = '/'.join(parts)
            else:
                relative_path = skill_name

            for skills_dir in targets:
                try:
                    dest = skills_dir / relative_path / "SKILL.md"
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    if dest.exists() and not force:
                        print(f"Skill file already exists at {dest}. Use --force to overwrite.")
                        continue
                    dest.write_text(skill_content, encoding="utf-8")
                    print(f"CanvasXpress skill '{skill_name}' installed to: {dest}")
                except PermissionError:
                    print(f"Permission denied: Cannot write to {skills_dir}. Skipping.")
                except OSError as e:
                    print(f"OS error writing to {skills_dir}: {e}. Skipping.")
        except Exception as e:
            print(f"Failed to install skill '{skill_name}': {e}")


def cli() -> None:
    """Command-line interface for installing CanvasXpress agent skills."""
    target = 'all'
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
            print("  --target, -t TARGET  Where to install:")
            print("                       'opencode', 'claude', 'agents'")
            print("                       'all' (all frameworks), 'both' (opencode + agents)")
            print("  --force, -f          Overwrite existing skill files")
            print("  --help, -h           Show this help")
            sys.exit(0)
        else:
            print(f"Unknown argument: {args[i]}")
            sys.exit(1)

    install_skills(target=target, force=force)


if __name__ == '__main__':
    cli()
