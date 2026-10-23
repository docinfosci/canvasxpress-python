"""
CanvasXpress for Python - Interactive Data Visualization

CanvasXpress is a comprehensive visualization library supporting 30+ chart types
for scientific and general-purpose data visualization.
"""

from canvasxpress.agent_skills.registry import install_skills
from canvasxpress.util.package_version import DEV_VERSION, read_package_version

__version__: str = read_package_version()

__all__ = ['install_skills', '__version__']

try:
    # An unbuilt source tree has no version to compare stamps against, so
    # always refresh its skills.
    _force_skills = __version__ == DEV_VERSION
    _skills_up_to_date: bool = install_skills(force=_force_skills, verbose=False)
except SystemExit:
    _skills_up_to_date = False
