from invoke import task


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
    c.run("pip install --no-cache-dir -U -r ./requirements-project.txt")
    c.run("pip install --no-cache-dir -U -r ./requirements.txt")

    c.run("npm install canvasxpress")
    c.run("npm install canvasxpress-react")

    if dev:
        c.run("pip install --no-cache-dir -U -r ./requirements-dev.txt")

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
        " --junitxml=\"pytest_result.xml\""
        " --cov=canvasxpress"
        " --cov-fail-under=80"
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
    c.run(
        "coveralls"
    )
