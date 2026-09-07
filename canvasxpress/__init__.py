"""
CanvasXpress for Python - Interactive Data Visualization

CanvasXpress is a comprehensive visualization library supporting 30+ chart types
for scientific and general-purpose data visualization.

## AI Agent Integration

This package includes agent skills for AI coding assistants. After installation,
agent skills are automatically available at:

  - ~/.opencode/skills/chart_builder/SKILL.md
  - ~/.opencode/skills/notebook_builder/SKILL.md
  - ~/.agents/skills/chart_builder/SKILL.md
  - ~/.agents/skills/notebook_builder/SKILL.md

Programmatic access to skills:

    from canvasxpress.agent_skills.registry import discover_skills
    skills = discover_skills()

Command-line installation:

    canvasxpress --target opencode
    canvasxpress --target claude
    canvasxpress --force

For more information, see: https://www.canvasxpress.org
"""
