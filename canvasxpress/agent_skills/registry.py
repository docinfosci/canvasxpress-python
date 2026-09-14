"""
Dynamic agent skill discovery for CanvasXpress.

Provides programmatic access to discover and retrieve agent skills
installed with the canvasxpress package. Uses importlib.resources and
setuptools entry points for platform-agnostic discovery.
"""

import shutil
import sys
from importlib.metadata import entry_points, version as get_version
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


def _skill_source(ep):
    """Directory containing the skill's SKILL.md and its supporting files."""
    import importlib.resources
    if sys.version_info >= (3, 9):
        # Python 3.9+ has importlib.resources.files()
        return Path(str(importlib.resources.files(ep.value)))
    else:
        # Python 3.8 uses pkg_resources fallback
        import pkg_resources
        return Path(pkg_resources.resource_filename(ep.value, ''))


def discover_skills():
    """
    Scan the installed environment for canvasxpress agent skills
    and extract their markdown instructions dynamically.

    Returns:
        dict: Mapping of skill names to their content with metadata.
              Each entry includes:
              - 'name': The skill name
              - 'content': The SKILL.md content
              - 'path': The directory path to supporting files
              Example: {"canvasxpress_charts": {"name": "canvasxpress_charts", "content": "...", "path": "/path/to/skill"}, ...}
    """
    skills_map = {}
    eps = _get_entry_points()

    for ep in eps:
        try:
            source_dir = _skill_source(ep)
            skill_md_path = source_dir / "SKILL.md"
            if not skill_md_path.is_file():
                print(f"skip {ep.name}: no SKILL.md in {source_dir}")
                continue
            content = skill_md_path.read_text(encoding='utf-8')
            skills_map[ep.name] = {
                "name": ep.name,
                "content": content,
                "path": str(source_dir)
            }
        except Exception as e:
            print(f"Failed to discover skill '{ep.name}': {e}")

    return skills_map


def _install_one(src: Path, dest_root: Path, name: str, force: bool) -> int:
    """Copy one skill directory. Returns the number of markdown files written."""
    if not (src / "SKILL.md").is_file():
        print(f"skip {name}: no SKILL.md in {src}")
        return 0

    target = dest_root / name
    if target.exists():
        if not force:
            stamp_file = target / ".skill-version"
            needs_update = True
            try:
                if stamp_file.is_file():
                    installed_version = stamp_file.read_text(encoding='utf-8').strip()
                    if installed_version:
                        pkg_version = get_version('canvasxpress')
                        if pkg_version == installed_version:
                            needs_update = False
            except Exception:
                pass
            if not needs_update:
                print(f"skip {name}: up to date at {target}")
                return 0
            print(f"replace {name}: out of date at {target}")
        shutil.rmtree(target)

    shutil.copytree(
        src, target,
        ignore=shutil.ignore_patterns("__pycache__", "*.py", "*.pyc")
    )

    # Write provenance stamp
    try:
        pkg_version = get_version('canvasxpress')
    except Exception:
        pkg_version = 'unknown'
    (target / ".skill-version").write_text(pkg_version, encoding='utf-8')

    count = len(list(target.rglob("*.md")))
    print(f"installed {name} -> {target} ({count} markdown files)")
    return count


def install_skills(target: str = 'all', force: bool = False) -> bool:
    """
    Install CanvasXpress agent skills to OpenCode, Claude Code, and/or agents directories.

    Args:
        target: Where to install skills. Options:
            - 'opencode': ~/.config/opencode/skills/ or ~/.opencode/skills/
            - 'claude': ~/.claude/skills/
            - 'agents': ~/.agents/skills/
            - 'all': Install to all directories (default)
            - 'both': Install to opencode and agents only
        force: If True, overwrite existing skill directories.

    Returns:
        True if all skills are installed and up to date, False otherwise.
    """
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

    total_installed = 0
    for ep in eps:
        source_dir = _skill_source(ep)
        skill_name = ep.name
        for skills_dir in targets:
            count = _install_one(source_dir, skills_dir, skill_name, force)
            total_installed += count

    if total_installed == 0 and not force:
        print("No skills were installed. All skills are already present. Use --force to replace.")
    elif total_installed == 0 and force:
        print("No skills were installed. Check that the package is properly installed.")

    return True


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
            print("  --force, -f          Overwrite existing skill directories")
            print("  --help, -h           Show this help")
            sys.exit(0)
        else:
            print(f"Unknown argument: {args[i]}")
            sys.exit(1)

    install_skills(target=target, force=force)


if __name__ == '__main__':
    cli()
