from os import path

import git
from invoke import task


def git_project_working_version():
    working_path = path.dirname(path.abspath(__file__))
    repo = git.Repo(working_path)
    active_branch = repo.active_branch
    commit_hash = repo.head.commit
    commit_dirty = repo.is_dirty()
    return f"{active_branch if active_branch != 'master' else ''}" \
           f"{'.' if active_branch != 'master' else ''}" \
           f"{'dirty.' if commit_dirty else ''}{commit_hash}"


@task
def project_version(c):
    """
    States the version of the project.
    :param c:
    :return:
    """
    print(git_project_working_version())


@task
def clean(c, docs=False, bytecode=False, extra=''):
    """
    Cleans the project in terms of build items and directories.
    :param c:
    :param docs: True if docs should be cleaned
    :param bytecode: True if bytecode should be cleaned
    :param extra:
    :return:
    """
    c.run("pip freeze | xargs pip uninstall -y")

    patterns = [
        'dist',
        '*.egg-info',
        '.requirements',
    ]
    if docs:
        patterns.append('docs/build')
    if bytecode:
        patterns.append('**/*.pyc')
    if extra:
        patterns.append(extra)

    for pattern in patterns:
        c.run(f"rm -rf ./{pattern}")


@task(pre=[clean])
def init(c, dev=False, list=False):
    """
    Initializes requirements for the project and app.
    :param c:
    :param dev: True if dev requirements, such as for testing, should be installed.
    :param list: True if a list of all installed requirements should be printed
    :return:
    """
    c.run("pip install -U -r ./requirements-project.txt")
    c.run("pip install -U -r ./requirements.txt")

    if dev:
        c.run("pip install -U -r ./requirements-dev.txt")

    if list:
        c.run("pip list")


@task
def test(c):
    """
    Runs the test suite.
    :param c:
    :return:
    """
    c.run(
        "python -m pytest"
        " --cov=canvasxpress"
        " --cov-report term"
        " --cov-report html:./coverage-results"
        " --alluredir=./allure-results"
        " ./tests"
    )
