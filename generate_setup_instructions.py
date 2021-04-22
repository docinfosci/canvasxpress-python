from datetime import datetime
from platform import python_version

import pytz
import requirements
from git import Repo

setup_instructions_template = """
from setuptools import setup, find_packages

long_description = '''@PKG_DESCRIPTION@'''

setup(
    name='canvasxpress',
    version='@PKG_VERSION@',
    packages=find_packages(exclude=['tests*']),
    package_dir={'': '.'},
    install_requires=@PKG_REQUIREMENTS@,
    url='https://github.com/docinfosci/canvasxpress-python.git',
    project_urls={
        'Documentation': 'https://canvasxpress-python.readthedocs.io',
    },
    license='Copyright 2020 to @PRESENT_YEAR@ CanvasXpress all rights reserved',
    author='CanvasXpress (original author) and Dr. Todd C. Brett (Python edition)',
    author_email='todd@aggregate-genius.com',
    description='CanvasXpress for Python',
    long_description=long_description,
    long_description_content_type='text/markdown; charset=UTF-8; variant=GFM',
    python_requires='>=3.6',
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

    repo = Repo('.')
    branch = repo.active_branch

    return f"{buildtime.year}.{buildtime.month}.{buildtime.day}" \
           f".{'dev' if branch.name not in ['main', 'master'] else ''}" \
           f"{buildtime.strftime('%H%M%S')}"


def get_requirements() -> list:
    with open('requirements.txt') as reqs_file:
        return [
            f"'{req.name}" \
            f"{','.join([f'{spec[0]}{spec[1]}' for spec in req.specs])}'"
            for req in requirements.parse(reqs_file)
        ]


def get_description() -> str:
    with open('README.md') as readme_file:
        return readme_file.read()


if __name__ == "__main__":
    package_version = get_version()
    package_requirements = ',\n        '.join(get_requirements())
    python_version = python_version()

    setup_instructions = setup_instructions_template.replace(
        '@PKG_VERSION@',
        package_version
    )

    setup_instructions = setup_instructions.replace(
        '@PKG_REQUIREMENTS@',
        f"[\n        {package_requirements}\n    ]"
    )

    setup_instructions = setup_instructions.replace(
        '@PRESENT_YEAR@',
        str(buildtime.year)
    )

    setup_instructions = setup_instructions.replace(
        '@PKG_DESCRIPTION@',
        get_description()
    )

    setup_instructions = setup_instructions.replace(
        '@PY_VERSION_MJR@',
        python_version[:1]
    )

    setup_py_file = open("setup.py", "w")
    setup_py_file.writelines(setup_instructions)
    setup_py_file.close()
