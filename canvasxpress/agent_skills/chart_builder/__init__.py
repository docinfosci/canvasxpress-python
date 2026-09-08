"""CanvasXpress chart builder skill for AI coding agents."""

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files
from pathlib import Path

CHART_SKILLS = [
    "area_skill.md",
    "bar_skill.md",
    "boxplot_skill.md",
    "chord_skill.md",
    "contour_skill.md",
    "correlation_skill.md",
    "density_skill.md",
    "dotplot_skill.md",
    "dumbbell_skill.md",
    "heatmap_skill.md",
    "histogram_skill.md",
    "lollipop_skill.md",
    "line_skill.md",
    "map_skill.md",
    "network_skill.md",
    "pie_skill.md",
    "radar_skill.md",
    "stacked_skill.md",
    "streamgraph_skill.md",
    "sunburst_skill.md",
    "treemap_skill.md",
    "tree_skill.md",
    "venn_skill.md",
    "violin_skill.md",
    "waterfall_skill.md",
    "bullet_skill.md",
]


def get_skill_content(skill_name: str) -> str | None:
    """
    Retrieve the content of a specific chart skill file.

    Args:
        skill_name: Name of the skill file (e.g., 'area_skill.md' or 'area_skill').

    Returns:
        The markdown content of the skill file, or None if not found.
    """
    skill_file = skill_name.replace(".md", ".md")
    try:
        skill_md = files(__package__).joinpath(skill_file)
        if skill_md.exists():
            return skill_md.read_text(encoding="utf-8")
    except Exception:
        pass
    return None


def get_available_skills() -> list[str]:
    """Return a sorted list of all available chart skill names."""
    return sorted(CHART_SKILLS)


def list_skills() -> None:
    """Print all available chart skills to stdout."""
    for skill in get_available_skills():
        print(skill)


if __name__ == "__main__":
    list_skills()
