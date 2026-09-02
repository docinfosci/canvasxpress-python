import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from canvasxpress.agent._install import (
    OPENCODE_DEST,
    CLAUDE_DEST,
    _install_skill,
    install,
)


@pytest.fixture
def mock_skill_file():
    """Create a temporary mock skill file for testing."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False
    ) as f:
        f.write("# Mock Skill File")
        skill_path = f.name
    yield skill_path
    os.unlink(skill_path)


@pytest.fixture
def mock_canvasxpress(mock_skill_file):
    """Mock the canvasxpress module to return a mock skill file path."""
    mock_module = MagicMock()
    mock_module.__file__ = "/mock/path/canvasxpress/__init__.py"

    with patch("canvasxpress.agent._install._SKILL_FILE", mock_skill_file):
        yield mock_skill_file


class TestInstallSkill:
    def test_install_skill_success(self, mock_canvasxpress, tmp_path):
        """Test successful skill installation."""
        dest = tmp_path / "test" / "SKILL.md"
        result = _install_skill(dest, force=False)
        assert result is True
        assert dest.exists()
        assert dest.read_text() == "# Mock Skill File"

    def test_install_skill_file_not_found(self, tmp_path):
        """Test when skill file does not exist."""
        with patch("canvasxpress.agent._install._SKILL_FILE", "/nonexistent/path.md"):
            dest = tmp_path / "test" / "SKILL.md"
            result = _install_skill(dest, force=False)
            assert result is False

    def test_install_skill_no_force(self, mock_canvasxpress, tmp_path):
        """Test that existing file is not overwritten without force."""
        dest = tmp_path / "test" / "SKILL.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text("Existing content")

        result = _install_skill(dest, force=False)
        assert result is False
        assert dest.read_text() == "Existing content"

    def test_install_skill_with_force(self, mock_canvasxpress, tmp_path):
        """Test that existing file is overwritten with force."""
        dest = tmp_path / "test" / "SKILL.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text("Existing content")

        result = _install_skill(dest, force=True)
        assert result is True
        assert dest.read_text() == "# Mock Skill File"


class TestInstallFunction:
    def test_install_invalid_target(self, capsys):
        """Test that invalid target raises exit."""
        with pytest.raises(SystemExit):
            install(target="invalid")

    def test_install_skill_not_found(self, capsys):
        """Test when skill file is not found."""
        with patch("canvasxpress.agent._install._SKILL_FILE", "/nonexistent/path.md"):
            with pytest.raises(SystemExit):
                install(target="opencode")


class TestCLI:
    def test_cli_help(self, monkeypatch, capsys):
        """Test that --help displays help message."""
        from canvasxpress.agent._install import cli

        monkeypatch.setattr("sys.argv", ["_install", "--help"])
        with pytest.raises(SystemExit) as exc_info:
            cli()
        assert exc_info.value.code == 0

    def test_cli_target_opencode(self, monkeypatch, mock_canvasxpress, tmp_path,
                                 capsys):
        """Test CLI with opencode target."""
        from canvasxpress.agent import _install

        mock_home = tmp_path / "home"
        mock_home.mkdir()
        monkeypatch.setattr(_install, "OPENCODE_DEST", mock_home / ".opencode/skills/canvasxpress/SKILL.md")

        monkeypatch.setattr("sys.argv", ["_install", "--target", "opencode"])
        cli = _install.cli
        cli()

        expected_path = mock_home / ".opencode/skills/canvasxpress/SKILL.md"
        assert expected_path.exists()

    def test_cli_target_claude(self, monkeypatch, mock_canvasxpress, tmp_path,
                               capsys):
        """Test CLI with claude target."""
        from canvasxpress.agent import _install

        mock_home = tmp_path / "home"
        mock_home.mkdir()
        monkeypatch.setattr(_install, "CLAUDE_DEST", mock_home / ".agents/skills/canvasxpress/SKILL.md")

        monkeypatch.setattr("sys.argv", ["_install", "--target", "claude"])
        cli = _install.cli
        cli()

        expected_path = mock_home / ".agents/skills/canvasxpress/SKILL.md"
        assert expected_path.exists()

    def test_cli_target_both(self, monkeypatch, mock_canvasxpress, tmp_path,
                             capsys):
        """Test CLI with both targets."""
        from canvasxpress.agent import _install

        mock_home = tmp_path / "home"
        mock_home.mkdir()
        monkeypatch.setattr(_install, "OPENCODE_DEST", mock_home / ".opencode/skills/canvasxpress/SKILL.md")
        monkeypatch.setattr(_install, "CLAUDE_DEST", mock_home / ".agents/skills/canvasxpress/SKILL.md")

        monkeypatch.setattr("sys.argv", ["_install", "--target", "both"])
        cli = _install.cli
        cli()

        opencode_path = mock_home / ".opencode/skills/canvasxpress/SKILL.md"
        claude_path = mock_home / ".agents/skills/canvasxpress/SKILL.md"
        assert opencode_path.exists()
        assert claude_path.exists()

    def test_cli_force(self, monkeypatch, mock_canvasxpress, tmp_path, capsys):
        """Test CLI with force flag."""
        from canvasxpress.agent import _install

        mock_home = tmp_path / "home"
        mock_home.mkdir()
        monkeypatch.setattr(_install, "OPENCODE_DEST", mock_home / ".opencode/skills/canvasxpress/SKILL.md")

        # Create existing skill file
        opencode_path = mock_home / ".opencode/skills/canvasxpress/SKILL.md"
        opencode_path.parent.mkdir(parents=True, exist_ok=True)
        opencode_path.write_text("Old content")

        monkeypatch.setattr("sys.argv", ["_install", "--target", "opencode", "--force"])
        cli = _install.cli
        cli()

        assert opencode_path.read_text() == "# Mock Skill File"

    def test_cli_short_options(self, monkeypatch, mock_canvasxpress, tmp_path,
                               capsys):
        """Test CLI with short options."""
        from canvasxpress.agent import _install

        mock_home = tmp_path / "home"
        mock_home.mkdir()
        monkeypatch.setattr(_install, "CLAUDE_DEST", mock_home / ".agents/skills/canvasxpress/SKILL.md")

        monkeypatch.setattr("sys.argv", ["_install", "-t", "claude", "-f"])
        cli = _install.cli
        cli()

        expected_path = mock_home / ".agents/skills/canvasxpress/SKILL.md"
        assert expected_path.exists()

    def test_cli_unknown_argument(self, monkeypatch, capsys):
        """Test CLI with unknown argument."""
        from canvasxpress.agent._install import cli

        monkeypatch.setattr("sys.argv", ["_install", "--unknown"])
        with pytest.raises(SystemExit):
            cli()
