from datetime import datetime
from platform import python_version

import pytz
from git import Repo

setup_instructions_template = """
from setuptools import setup, find_packages
from setuptools.command.install import install

long_description = '''@PKG_DESCRIPTION@'''

core_pkgs = @PKG_REQUIREMENTS@
dash_pkgs = @PKG_REQUIREMENTS_DASH@
jupyter_pkgs = @PKG_REQUIREMENTS_JUPYTER@
streamlit_pkgs = @PKG_REQUIREMENTS_STREAMLIT@
shiny_pkgs = @PKG_REQUIREMENTS_SHINY@
rstudio_pkgs = @PKG_REQUIREMENTS_RSTUDIO@


class PostInstallCommand(install):
    '''Post-installation for skill auto-injection.'''

    def run(self):
        install.run(self)
        try:
            from canvasxpress.agent_skills.registry import install_skills
            install_skills(target='all', force=True)
            print("CanvasXpress agent skills installed successfully.")
        except Exception as e:
            print(f"Warning: Failed to auto-install agent skills: {e}")
            print("Skills can be installed manually via: canvasxpress --target all --force")


setup(
    name='canvasxpress',
    version='@PKG_VERSION@',
    packages=find_packages(exclude=["tests*", "plotly", "streamlit", "tutorials",]),
    package_data={'': ['*.json', '*.yaml', '*.yml', '*.js', '*.css', '*.html', '*.sql', '*.txt', '*.zip', '*.md']},
    include_package_data=True,
    package_dir={'': '.'},
    install_requires=core_pkgs,
    extras_require={
        "core": core_pkgs, 
        "dash": core_pkgs + dash_pkgs,
        "streamlit": core_pkgs + streamlit_pkgs,
        "jupyter": core_pkgs + jupyter_pkgs,
        "shiny": core_pkgs + shiny_pkgs,
        "rstudio": core_pkgs + shiny_pkgs + jupyter_pkgs + rstudio_pkgs,
        "all": core_pkgs + dash_pkgs + jupyter_pkgs + shiny_pkgs + rstudio_pkgs,
    },
    cmdclass={'install': PostInstallCommand},
    entry_points={
        'console_scripts': [
            'canvasxpress = canvasxpress.agent_skills.registry:cli',
        ],
        'canvasxpress.skills': [
            'canvasxpress_charts = canvasxpress.agent_skills.canvasxpress_charts',
            'canvasxpress_events = canvasxpress.agent_skills.canvasxpress_events',
            'canvasxpress_notebooks = canvasxpress.agent_skills.canvasxpress_notebooks',
            'canvasxpress_validator = canvasxpress.agent_skills.canvasxpress_validator',
        ],
        'agent_skills.plugins': [
            'canvasxpress = canvasxpress.agent_skills.registry:discover_skills',
        ],
    },
    url='https://github.com/docinfosci/canvasxpress-python.git',
    project_urls={
        'Documentation': 'https://github.com/docinfosci/canvasxpress-python',
    },
    license='Copyright 2020 to @PRESENT_YEAR@ CanvasXpress all rights reserved',
    author=(
        ' Dr. Isaac Neuhaus for CanvasXpress JS, PHP, and R;'
        ' Dr. Constance M. Brett for R;'
        ' Dr. Todd C. Brett for Python and Dash; and'
        ' Dr. Jennifer Walker for Python.'
        'Eng. Mennahtullah Mabrouk for Python.'
        'Eng. Mohamed Ali for R and Python.'
    ),
    author_email='todd@aggregate-genius.com',
    description='CanvasXpress for Python',
    long_description=long_description,
    long_description_content_type='text/markdown; charset=UTF-8; variant=GFM',
    python_requires='>=3.10',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Environment :: Web Environment',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: @PY_VERSION_MJR@',
    ]
)
"""

buildtime = pytz.utc.localize(datetime.now())


def get_version() -> str:
    # PEP 44 sanctioned version format:
    # https://www.python.org/dev/peps/pep-0440/

    repo = Repo(".")
    branch = repo.active_branch

    return (
        f"{buildtime.year}.{buildtime.month}.{buildtime.day}"
        f".{'dev' if branch.name not in ['main', 'master'] else ''}"
        f"{buildtime.strftime('%H%M%S')}"
    )


def get_requirements() -> dict:
    packages = {
        "# core": [],
        "# dash": [],
        "# streamlit": [],
        "# jupyter": [],
        "# shiny": [],
        "# rstudio": [],
    }

    with open("requirements.txt") as reqs_file:
        topics = [str(k) for k in packages.keys()]
        topic = topics[0]
        requirements_text = reqs_file.read()
        for line in requirements_text.splitlines():
            candidate = line.strip()
            if not line:
                continue

            elif candidate in topics:
                topic = candidate

            else:
                packages[topic].append(f'"{candidate}"')

    return packages


def get_description() -> str:
    with open("README.md") as readme_file:
        return readme_file.read()


if __name__ == "__main__":
    package_version = get_version()
    packages = get_requirements()
    package_requirements_core = ",\n    ".join(packages["# core"])
    package_requirements_dash = ",\n    ".join(packages["# dash"])
    package_requirements_streamlit = ",\n    ".join(packages["# streamlit"])
    package_requirements_jupyter = ",\n    ".join(packages["# jupyter"])
    package_requirements_shiny = ",\n    ".join(packages["# shiny"])
    package_requirements_rstudio = ",\n    ".join(packages["# rstudio"])
    python_version = python_version()

    setup_instructions = setup_instructions_template.replace(
        "@PKG_VERSION@", package_version
    )

    setup_instructions = setup_instructions.replace(
        "@PKG_DESCRIPTION@", get_description()
    )

    setup_instructions = setup_instructions.replace(
        "@PY_VERSION_MJR@", python_version[:1]
    )

    setup_instructions = setup_instructions.replace(
        "@PKG_REQUIREMENTS@", f"[\n    {package_requirements_core}\n]"
    )
    setup_instructions = setup_instructions.replace(
        "@PKG_REQUIREMENTS_DASH@", f"[\n    {package_requirements_dash}\n]"
    )
    setup_instructions = setup_instructions.replace(
        "@PKG_REQUIREMENTS_JUPYTER@", f"[\n    {package_requirements_jupyter}\n]"
    )
    setup_instructions = setup_instructions.replace(
        "@PKG_REQUIREMENTS_STREAMLIT@", f"[\n    {package_requirements_streamlit}\n]"
    )
    setup_instructions = setup_instructions.replace(
        "@PKG_REQUIREMENTS_SHINY@", f"[\n    {package_requirements_shiny}\n]"
    )
    setup_instructions = setup_instructions.replace(
        "@PKG_REQUIREMENTS_RSTUDIO@", f"[\n    {package_requirements_rstudio}\n]"
    )

    setup_instructions = setup_instructions.replace(
        "@PRESENT_YEAR@", str(buildtime.year)
    )

    setup_py_file = open("setup.py", "w")
    setup_py_file.writelines(setup_instructions)
    setup_py_file.close()
