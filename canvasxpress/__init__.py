"""
CanvasXpress for Python - Interactive Data Visualization

CanvasXpress is a comprehensive visualization library supporting 30+ chart types
for scientific and general-purpose data visualization.
"""

import os

from canvasxpress.agent_skills.registry import install_skills


def _read_version() -> str:
    version_file = os.path.join(os.path.dirname(__file__), 'version.ini')
    try:
        with open(version_file, 'r') as f:
            content = f.read().strip()
            if content:
                for line in content.splitlines():
                    if line.startswith('__version__'):
                        value = line.split('=', 1)[1].strip().strip("'\"")
                        if value:
                            return value
    except FileNotFoundError:
        pass
    return '0.0.0.dev0'


__version__: str = _read_version()

__all__ = ['install_skills', '__version__']

try:
    _force_skills = __version__ == '0.0.0.dev0'
    _skills_up_to_date: bool = install_skills(force=_force_skills, verbose=False)
except SystemExit:
    _skills_up_to_date = False
