import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


class TestDiscoverSkills:
    def test_discover_skills_returns_both_skills(self):
        """Test that discover_skills returns chart_builder, notebook_builder, and code_validator."""
        from canvasxpress.agent_skills.registry import discover_skills

        skills = discover_skills()
        assert "chart_builder" in skills
        assert "notebook_builder" in skills
        assert "code_validator" in skills
        assert "content" in skills["chart_builder"]
        assert "name" in skills["chart_builder"]
        assert skills["chart_builder"]["name"] == "chart_builder"

    def test_discover_skills_content_not_empty(self):
        """Test that discovered skills have non-empty content."""
        from canvasxpress.agent_skills.registry import discover_skills

        skills = discover_skills()
        assert len(skills["chart_builder"]["content"]) > 100
        assert len(skills["notebook_builder"]["content"]) > 100
        assert len(skills["code_validator"]["content"]) > 100

    def test_discover_skills_has_frontmatter(self):
        """Test that skill content has YAML frontmatter."""
        from canvasxpress.agent_skills.registry import discover_skills

        skills = discover_skills()
        assert skills["chart_builder"]["content"].startswith("---")
        assert skills["notebook_builder"]["content"].startswith("---")
        assert skills["code_validator"]["content"].startswith("---")


class TestInstallSkills:
    @pytest.fixture
    def mock_entry_points(self):
        """Mock entry points for testing."""
        mock_ep = MagicMock()
        mock_ep.name = "chart_builder"
        mock_ep.value = "canvasxpress.agent_skills.chart_builder"

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

        expected_path = mock_home / ".opencode/skills/chart_builder/SKILL.md"
        assert expected_path.exists()
        assert "chart_builder" in expected_path.read_text()

    def test_install_skills_claude(self, mock_entry_points, tmp_path, monkeypatch):
        """Test installing skills to Claude directory."""
        from canvasxpress.agent_skills.registry import install_skills

        mock_home = tmp_path / "home"
        mock_home.mkdir()
        monkeypatch.setattr("pathlib.Path.home", lambda: mock_home)

        install_skills(target="claude", force=True)

        expected_path = mock_home / ".agents/skills/chart_builder/SKILL.md"
        assert expected_path.exists()
        assert "chart_builder" in expected_path.read_text()

    def test_install_skills_both(self, mock_entry_points, tmp_path, monkeypatch):
        """Test installing skills to both directories."""
        from canvasxpress.agent_skills.registry import install_skills

        mock_home = tmp_path / "home"
        mock_home.mkdir()
        monkeypatch.setattr("pathlib.Path.home", lambda: mock_home)

        install_skills(target="both", force=True)

        opencode_path = mock_home / ".opencode/skills/chart_builder/SKILL.md"
        claude_path = mock_home / ".agents/skills/chart_builder/SKILL.md"
        assert opencode_path.exists()
        assert claude_path.exists()

    def test_install_skills_no_force(self, mock_entry_points, tmp_path, monkeypatch):
        """Test that existing file is not overwritten without force."""
        from canvasxpress.agent_skills.registry import install_skills

        mock_home = tmp_path / "home"
        mock_home.mkdir()
        monkeypatch.setattr("pathlib.Path.home", lambda: mock_home)

        # Create existing file
        existing_path = mock_home / ".opencode/skills/chart_builder/SKILL.md"
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
        existing_path = mock_home / ".opencode/skills/chart_builder/SKILL.md"
        existing_path.parent.mkdir(parents=True, exist_ok=True)
        existing_path.write_text("Old content")

        install_skills(target="opencode", force=True)

        assert "chart_builder" in existing_path.read_text()

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
