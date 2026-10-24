from unittest.mock import patch

import pytest

import canvasxpress
from canvasxpress.util import package_version
from canvasxpress.util.package_version import DEV_VERSION, read_package_version


@pytest.fixture
def version_file(tmp_path):
    path = tmp_path / "version.txt"
    with patch.object(package_version, "_VERSION_FILE", str(path)):
        yield path


def test_bare_version_string(version_file):
    """build_pkg_setup.py writes the bare version string."""
    version_file.write_text("2026.10.23.dev101102021\n", encoding="utf-8")
    assert read_package_version() == "2026.10.23.dev101102021"


def test_legacy_assignment(version_file):
    version_file.write_text("__version__ = '2026.10.22.52258430'\n", encoding="utf-8")
    assert read_package_version() == "2026.10.22.52258430"


def test_legacy_assignment_double_quotes(version_file):
    version_file.write_text('__version__ = "2026.1.2.3"\n', encoding="utf-8")
    assert read_package_version() == "2026.1.2.3"


def test_missing_file_is_dev_version(version_file):
    assert read_package_version() == DEV_VERSION


def test_empty_file_is_dev_version(version_file):
    version_file.write_text("\n\n", encoding="utf-8")
    assert read_package_version() == DEV_VERSION


def test_package_version_matches_reader():
    """__version__ and the skill stamp use the same source."""
    assert canvasxpress.__version__ == read_package_version()


def test_skill_stamp_uses_package_version(tmp_path):
    from canvasxpress.agent_skills.registry import _install_one

    source = tmp_path / "src" / "demo_skill"
    source.mkdir(parents=True)
    (source / "SKILL.md").write_text("# Demo", encoding="utf-8")

    with patch(
        "canvasxpress.agent_skills.registry.read_package_version",
        return_value="2026.10.23.123",
    ):
        _install_one(source, tmp_path / "dest", "demo_skill", force=False, verbose=False)
        stamp = tmp_path / "dest" / "demo_skill" / ".skill-version"
        assert stamp.read_text(encoding="utf-8") == "2026.10.23.123"

        # Same version: left alone.
        assert (
            _install_one(source, tmp_path / "dest", "demo_skill", force=False, verbose=False)
            == 0
        )

    with patch(
        "canvasxpress.agent_skills.registry.read_package_version",
        return_value="2026.10.24.456",
    ):
        # New version: replaced and restamped.
        assert (
            _install_one(source, tmp_path / "dest", "demo_skill", force=False, verbose=False)
            == 1
        )
        assert stamp.read_text(encoding="utf-8") == "2026.10.24.456"
