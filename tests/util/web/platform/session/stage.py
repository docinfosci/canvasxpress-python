import logging
from os import path, environ
from pathlib import Path

import git

logger = logging.getLogger(__name__)
logger.setLevel(int(environ.get('LOG_LEVEL', 10)))

STAGE_PRD: str = "prd"
# Staging constant - production

STAGE_DEV: str = "dev"
# Staging constant - development

STAGE_LCL: str = "lcl"


# Staging constant - local customizations

def _reduce_path_to_git_config_dir(dir: str) -> str:
    candidate_dir = Path(dir)
    while not candidate_dir.joinpath(".git").exists():
        candidate_dir = Path(candidate_dir).parent

    return str(candidate_dir)


def _get_stage_from_working_branch() -> str:
    """
        Indicates whether the source is running as PRD or DEV.  If the source is
        from the master branch then PRD is used, and for other branches DEV.
        :return: One of the STAGE_* constants.
        """
    working_path = _reduce_path_to_git_config_dir(
        path.dirname(path.abspath(__file__))
    )
    logger.info(f"Working path: {working_path}")

    repo = git.Repo(working_path)
    logger.info(f"Active Git branch: {repo.active_branch}")

    if str(repo.active_branch) == "main":
        logger.info(f"Per Git branch using stage == {STAGE_PRD}")
        return STAGE_PRD

    elif str(repo.active_branch) == "develop":
        logger.info(f"Per Git branch using stage == {STAGE_DEV}")
        return STAGE_DEV

    else:
        logger.info(f"Per Git branch using stage == {STAGE_DEV}")
        return STAGE_DEV


# Override environment variable
TEST_WORKING_STAGE: str = environ.get(
    "USER_PREF_STAGE",
    _get_stage_from_working_branch()
)

# Override environment location for config files
TEST_WORKING_CONFIG_PATH: str = environ.get(
    "USER_PREF_CONFIG_PATH",
    "$HOME/canvasxpress-python/tests/config"
)


def get_stage_environment() -> str:
    """
    Indicates whether the source is running as PRD or DEV.  Accounts for the
    user preference via TEST_WORKING_STAGE.
    :return: One of the STAGE_* constants.
    """
    return TEST_WORKING_STAGE
