"""
CanvasXpress for Python - Interactive Data Visualization

CanvasXpress is a comprehensive visualization library supporting 30+ chart types
for scientific and general-purpose data visualization.
"""

from canvasxpress.agent_skills.registry import install_skills

__all__ = ['install_skills']

_skills_up_to_date: bool = install_skills(force=False)
