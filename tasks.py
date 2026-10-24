import glob
import os
import shutil

from invoke import task


@task
def clean(c, docs=False, bytecode=False, extra="", yes=False):
    """
    Cleans the project in terms of build items and directories.
    :param c:
    :param docs: True if docs should be cleaned
    :param bytecode: True if bytecode should be cleaned
    :param extra:
    :param yes: If True, skip confirmation
    :return:
    """
    patterns = [
        "dist",
        "*.egg-info",
        ".requirements",
        "build",
        "__pycache__",
    ]
    if docs:
        patterns.append("docs/build")
    if bytecode:
        patterns.append("**/*.pyc")
    if extra:
        patterns.append(extra)

    # Use Python rather than `rm -rf` so this also works on Windows.
    for pattern in patterns:
        for path in glob.glob(f"./{pattern}", recursive=True):
            if os.path.isdir(path):
                shutil.rmtree(path, ignore_errors=True)
            else:
                os.remove(path)


@task(pre=[clean])
def init(c, dev=False, list=False):
    """
    Initializes requirements for the project and app.
    :param c:
    :param dev: True if dev requirements, such as for testing, should be installed.
    :param list: True if a list of all installed requirements should be printed
    :return:
    """
    # Bootstrap already done: uv pip install setuptools wheel invoke
    # Project deps already done: uv pip install ".[all]"
    # Dev deps already done: uv sync

    c.run("npm install canvasxpress")

    if list:
        c.run("uv pip list")


@task
def test(c):
    """
    Runs the test suite.
    :param c:
    :return:
    """
    c.run(
        "python -m pytest"
        ' --junitxml="pytest_result.xml"'
        " --cov=canvasxpress"
        " --cov-fail-under=50"
        " --cov-report xml"
        " --cov-report term"
        " --cov-report html:./coverage-results"
        " ./tests"
    )


@task
def report(c):
    """
    Report to SAAS platforms
    :param c:
    :return:
    """
    c.run("coveralls")
