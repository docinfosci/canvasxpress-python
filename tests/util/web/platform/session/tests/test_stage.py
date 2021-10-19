from os import path

import allure
import git

from tests.util.web.platform.session.stage import (
    _get_stage_from_working_branch,
    _reduce_path_to_git_config_dir,
)


@allure.feature("Test Framework Self-Check")
def test_get_stage_from_working_branch():
    stage = _get_stage_from_working_branch()

    working_path = _reduce_path_to_git_config_dir(path.dirname(path.abspath(__file__)))

    repo = git.Repo(working_path)
    active_branch = str(repo.active_branch)

    if active_branch == "main":
        assert stage == "prd"

    else:
        assert stage == "dev"
