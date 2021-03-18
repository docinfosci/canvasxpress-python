from datetime import datetime
from platform import python_version

import pytz
from git import Repo

setup_instructions_template = """
from setuptools import setup, find_packages

setup(
    name='canvasxpress',
    version='@PKG_VERSION@',
    packages=find_packages(exclude=['tests*']),
    package_dir={'': '.'},
    install_requires=[
        'deepdiff>=5.2.2',
        'IPython>=7.20.0',
        'gitpython>=3.1.12',
        'pytz>=2020.5',
    ],
    url='https://github.com/Aggregate-Genius/tbio-pkg-cx-python.git',
    license='Copyright 2020 to @PRESENT_YEAR@ CanvasXpress all rights reserved',
    author='CanvasXpress (original author) and Aggregate Genius Inc. (Python edition)',
    author_email='info@aggregate-genius.com',
    description='CanvasXpress via Python',
    python_requires='>=@PY_VERSION_RQD@',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Graphing',
        'License :: Commercial',
        'Programming Language :: Python :: @PY_VERSION_MJR@',
        'Programming Language :: Python :: @PY_VERSION@',
    ]
)
"""

buildtime = pytz.utc.localize(datetime.now())


def get_version() -> str:
    # PEP 44 sanctioned version format:
    # https://www.python.org/dev/peps/pep-0440/

    repo = Repo('.')  # os.getcwd()
    branch = repo.active_branch

    return f"{buildtime.year}.{buildtime.month}.{buildtime.day}" \
        f".{'dev' if branch.name != 'master' else ''}" \
        f"{buildtime.hour}{buildtime.minute}{buildtime.second}" \
        f"{buildtime.microsecond}"


if __name__ == "__main__":
    package_version = get_version()
    python_version = python_version()

    setup_instructions = setup_instructions_template.replace(
        '@PKG_VERSION@',
        package_version
    )

    setup_instructions = setup_instructions.replace(
        '@PRESENT_YEAR@',
        str(buildtime.year)
    )

    setup_instructions = setup_instructions.replace(
        '@PY_VERSION@',
        python_version
    )

    setup_instructions = setup_instructions.replace(
        '@PY_VERSION_MJR@',
        python_version[:1]
    )

    setup_instructions = setup_instructions.replace(
        '@PY_VERSION_RQD@',
        python_version[:3]
    )

    setup_py_file = open("setup.py", "w")
    setup_py_file.writelines(setup_instructions)
    setup_py_file.close()
