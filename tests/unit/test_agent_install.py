import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


class TestDiscoverSkills:
    @pytest.fixture
    def mock_entry_points(self):
        """Mock entry points for testing."""
        mock_chart = MagicMock()
        mock_chart.name = "canvasxpress_skill"
        mock_chart.value = "canvasxpress.agent_skills.canvasxpress_skill"

        mock_notebook = MagicMock()
        mock_notebook.name = "notebook_builder"
        mock_notebook.value = "canvasxpress.agent_skills.notebook_builder"

        mock_validator = MagicMock()
        mock_validator.name = "code_validator"
        mock_validator.value = "canvasxpress.agent_skills.code_validator"

        with patch("canvasxpress.agent_skills.registry._get_entry_points") as mock:
            mock.return_value = [mock_chart, mock_notebook, mock_validator]
            yield

    def test_discover_skills_returns_both_skills(self, mock_entry_points):
        """Test that discover_skills returns canvasxpress_skill, notebook_builder, and code_validator."""
        from canvasxpress.agent_skills.registry import discover_skills

        skills = discover_skills()
        assert "canvasxpress_skill" in skills
        assert "notebook_builder" in skills
        assert "code_validator" in skills
        assert "content" in skills["canvasxpress_skill"]
        assert "name" in skills["canvasxpress_skill"]
        assert skills["canvasxpress_skill"]["name"] == "canvasxpress_skill"

    def test_discover_skills_content_not_empty(self, mock_entry_points):
        """Test that discovered skills have non-empty content."""
        from canvasxpress.agent_skills.registry import discover_skills

        skills = discover_skills()
        assert len(skills["canvasxpress_skill"]["content"]) > 100
        assert len(skills["notebook_builder"]["content"]) > 100
        assert len(skills["code_validator"]["content"]) > 100

    def test_discover_skills_has_frontmatter(self, mock_entry_points):
        """Test that skill content has YAML frontmatter."""
        from canvasxpress.agent_skills.registry import discover_skills

        skills = discover_skills()
        assert skills["canvasxpress_skill"]["content"].startswith("---")
        assert skills["notebook_builder"]["content"].startswith("---")
        assert skills["code_validator"]["content"].startswith("---")


class TestInstallSkills:
    @pytest.fixture
    def mock_entry_points(self):
        """Mock entry points for testing."""
        mock_ep = MagicMock()
        mock_ep.name = "canvasxpress_skill"
        mock_ep.value = "canvasxpress.agent_skills.canvasxpress_skill"

        with patch("canvasxpress.agent_skills.registry._get_entry_points") as mock:
            mock.return_value = [mock_ep]
            yield mock_ep

    def test_install_skills_opencode(self, mock_entry_points, tmp_path, monkeypatch):
        """Test installing skills to OpenCode directory."""
        from canvasxpress.agent_skills.registry import install_skills

        mock_home = tmp_path / "home"
        mock_home.mkdir()
        monkeypatch.setattr("pathlib.Path.home", lambda: mock_home)

        install_skills(target="opencode", force=True)

        expected_path = mock_home / ".opencode/skills/canvasxpress_skill/SKILL.md"
        assert expected_path.exists()
        assert "canvasxpress_skill" in expected_path.read_text()

    def test_install_skills_claude(self, mock_entry_points, tmp_path, monkeypatch):
        """Test installing skills to Claude directory."""
        from canvasxpress.agent_skills.registry import install_skills

        mock_home = tmp_path / "home"
        mock_home.mkdir()
        monkeypatch.setattr("pathlib.Path.home", lambda: mock_home)

        install_skills(target="claude", force=True)

        expected_path = mock_home / ".agents/skills/canvasxpress_skill/SKILL.md"
        assert expected_path.exists()
        assert "canvasxpress_skill" in expected_path.read_text()

    def test_install_skills_both(self, mock_entry_points, tmp_path, monkeypatch):
        """Test installing skills to both directories."""
        from canvasxpress.agent_skills.registry import install_skills

        mock_home = tmp_path / "home"
        mock_home.mkdir()
        monkeypatch.setattr("pathlib.Path.home", lambda: mock_home)

        install_skills(target="both", force=True)

        opencode_path = mock_home / ".opencode/skills/canvasxpress_skill/SKILL.md"
        claude_path = mock_home / ".agents/skills/canvasxpress_skill/SKILL.md"
        assert opencode_path.exists()
        assert claude_path.exists()

    def test_install_skills_no_force(self, mock_entry_points, tmp_path, monkeypatch):
        """Test that existing file is not overwritten without force."""
        from canvasxpress.agent_skills.registry import install_skills

        mock_home = tmp_path / "home"
        mock_home.mkdir()
        monkeypatch.setattr("pathlib.Path.home", lambda: mock_home)

        # Create existing file
        existing_path = mock_home / ".opencode/skills/canvasxpress_skill/SKILL.md"
        existing_path.parent.mkdir(parents=True, exist_ok=True)
        existing_path.write_text("Old content")

        install_skills(target="opencode", force=False)

        assert existing_path.read_text() == "Old content"

    def test_install_skills_with_force(self, mock_entry_points, tmp_path, monkeypatch):
        """Test that existing file is overwritten with force."""
        from canvasxpress.agent_skills.registry import install_skills

        mock_home = tmp_path / "home"
        mock_home.mkdir()
        monkeypatch.setattr("pathlib.Path.home", lambda: mock_home)

        # Create existing file
        existing_path = mock_home / ".opencode/skills/canvasxpress_skill/SKILL.md"
        existing_path.parent.mkdir(parents=True, exist_ok=True)
        existing_path.write_text("Old content")

        install_skills(target="opencode", force=True)

        assert "canvasxpress_skill" in existing_path.read_text()

    def test_install_skills_invalid_target(self, capsys):
        """Test that invalid target raises exit."""
        from canvasxpress.agent_skills.registry import install_skills

        with pytest.raises(SystemExit):
            install_skills(target="invalid")


class TestCLI:
    def test_cli_help(self, monkeypatch, capsys):
        """Test that --help displays help message."""
        from canvasxpress.agent_skills.registry import cli

        monkeypatch.setattr("sys.argv", ["canvasxpress", "--help"])
        with pytest.raises(SystemExit) as exc_info:
            cli()
        assert exc_info.value.code == 0

    def test_cli_short_help(self, monkeypatch, capsys):
        """Test that -h displays help message."""
        from canvasxpress.agent_skills.registry import cli

        monkeypatch.setattr("sys.argv", ["canvasxpress", "-h"])
        with pytest.raises(SystemExit) as exc_info:
            cli()
        assert exc_info.value.code == 0

    def test_cli_unknown_argument(self, monkeypatch, capsys):
        """Test CLI with unknown argument."""
        from canvasxpress.agent_skills.registry import cli

        monkeypatch.setattr("sys.argv", ["canvasxpress", "--unknown"])
        with pytest.raises(SystemExit):
            cli()

    def test_cli_target_missing_value(self, monkeypatch, capsys):
        """Test CLI with --target but no value."""
        from canvasxpress.agent_skills.registry import cli

        monkeypatch.setattr("sys.argv", ["canvasxpress", "--target"])
        with pytest.raises(SystemExit):
            cli()
