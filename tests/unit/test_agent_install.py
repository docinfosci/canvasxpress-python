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
        mock_chart.name = "canvasxpress_charts"
        mock_chart.value = "canvasxpress.agent_skills.canvasxpress_charts"

        mock_notebook = MagicMock()
        mock_notebook.name = "canvasxpress_notebooks"
        mock_notebook.value = "canvasxpress.agent_skills.canvasxpress_notebooks"

        mock_validator = MagicMock()
        mock_validator.name = "canvasxpress_validator"
        mock_validator.value = "canvasxpress.agent_skills.canvasxpress_validator"

        mock_events = MagicMock()
        mock_events.name = "canvasxpress_events"
        mock_events.value = "canvasxpress.agent_skills.canvasxpress_events"

        with patch("canvasxpress.agent_skills.registry._get_entry_points") as mock:
            mock.return_value = [mock_chart, mock_notebook, mock_validator, mock_events]
            yield

    def test_discover_skills_returns_both_skills(self, mock_entry_points):
        """Test that discover_skills returns canvasxpress_charts, canvasxpress_notebooks, canvasxpress_validator, and canvasxpress_events."""
        from canvasxpress.agent_skills.registry import discover_skills

        skills = discover_skills()
        assert "canvasxpress_charts" in skills
        assert "canvasxpress_notebooks" in skills
        assert "canvasxpress_validator" in skills
        assert "canvasxpress_events" in skills
        assert "content" in skills["canvasxpress_charts"]
        assert "name" in skills["canvasxpress_charts"]
        assert skills["canvasxpress_charts"]["name"] == "canvasxpress_charts"

    def test_discover_skills_content_not_empty(self, mock_entry_points):
        """Test that discovered skills have non-empty content."""
        from canvasxpress.agent_skills.registry import discover_skills

        skills = discover_skills()
        assert len(skills["canvasxpress_charts"]["content"]) > 100
        assert len(skills["canvasxpress_notebooks"]["content"]) > 100
        assert len(skills["canvasxpress_validator"]["content"]) > 100
        assert len(skills["canvasxpress_events"]["content"]) > 100

    def test_discover_skills_has_frontmatter(self, mock_entry_points):
        """Test that skill content has YAML frontmatter."""
        from canvasxpress.agent_skills.registry import discover_skills

        skills = discover_skills()
        assert skills["canvasxpress_charts"]["content"].startswith("---")
        assert skills["canvasxpress_notebooks"]["content"].startswith("---")
        assert skills["canvasxpress_validator"]["content"].startswith("---")
        assert skills["canvasxpress_events"]["content"].startswith("---")


class TestInstallSkills:
    @pytest.fixture
    def mock_entry_points(self):
        """Mock entry points for testing."""
        mock_ep = MagicMock()
        mock_ep.name = "canvasxpress_charts"
        mock_ep.value = "canvasxpress.agent_skills.canvasxpress_charts"

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

        expected_path = mock_home / ".config" / "opencode" / "skills" / "canvasxpress_charts" / "SKILL.md"
        assert expected_path.exists()
        assert "canvasxpress_charts" in expected_path.read_text()

    def test_install_skills_claude(self, mock_entry_points, tmp_path, monkeypatch):
        """Test installing skills to Claude directory."""
        from canvasxpress.agent_skills.registry import install_skills

        mock_home = tmp_path / "home"
        mock_home.mkdir()
        monkeypatch.setattr("pathlib.Path.home", lambda: mock_home)

        install_skills(target="claude", force=True)

        expected_path = mock_home / ".claude" / "skills" / "canvasxpress_charts" / "SKILL.md"
        assert expected_path.exists()
        assert "canvasxpress_charts" in expected_path.read_text()

    def test_install_skills_both(self, mock_entry_points, tmp_path, monkeypatch):
        """Test installing skills to both directories."""
        from canvasxpress.agent_skills.registry import install_skills

        mock_home = tmp_path / "home"
        mock_home.mkdir()
        monkeypatch.setattr("pathlib.Path.home", lambda: mock_home)

        install_skills(target="both", force=True)

        opencode_path = mock_home / ".config" / "opencode" / "skills" / "canvasxpress_charts" / "SKILL.md"
        agents_path = mock_home / ".agents" / "skills" / "canvasxpress_charts" / "SKILL.md"
        assert opencode_path.exists()
        assert agents_path.exists()

    def test_install_skills_no_force(self, mock_entry_points, tmp_path, monkeypatch):
        """Test that existing file is not overwritten without force."""
        from canvasxpress.agent_skills.registry import install_skills

        mock_home = tmp_path / "home"
        mock_home.mkdir()
        monkeypatch.setattr("pathlib.Path.home", lambda: mock_home)

        # Create existing file
        existing_path = mock_home / ".config" / "opencode" / "skills" / "canvasxpress_charts" / "SKILL.md"
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
        existing_path = mock_home / ".config" / "opencode" / "skills" / "canvasxpress_charts" / "SKILL.md"
        existing_path.parent.mkdir(parents=True, exist_ok=True)
        existing_path.write_text("Old content")

        install_skills(target="opencode", force=True)

        assert "canvasxpress_charts" in existing_path.read_text()

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
