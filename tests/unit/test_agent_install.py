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

    def test_discover_skills_returns_path(self, mock_entry_points):
        """Test that discover_skills returns 'path' alongside content."""
        from canvasxpress.agent_skills.registry import discover_skills

        skills = discover_skills()
        assert "path" in skills["canvasxpress_charts"]
        assert "path" in skills["canvasxpress_notebooks"]
        assert "path" in skills["canvasxpress_validator"]
        assert "path" in skills["canvasxpress_events"]
        assert isinstance(skills["canvasxpress_charts"]["path"], str)
        assert skills["canvasxpress_charts"]["path"].endswith("canvasxpress_charts")

    def test_discover_skills_path_resolves(self, mock_entry_points):
        """Test that the returned path resolves to an actual directory."""
        from canvasxpress.agent_skills.registry import discover_skills

        skills = discover_skills()
        for name, skill in skills.items():
            path = Path(skill["path"])
            assert path.exists(), f"Path {path} for skill {name} does not exist"
            assert (path / "SKILL.md").exists(), f"SKILL.md not found in {path}"


class TestInstallSkills:
    @pytest.fixture
    def mock_entry_points(self):
        """Mock entry points for testing."""
        mock_chart = MagicMock()
        mock_chart.name = "canvasxpress_charts"
        mock_chart.value = "canvasxpress.agent_skills.canvasxpress_charts"

        mock_events = MagicMock()
        mock_events.name = "canvasxpress_events"
        mock_events.value = "canvasxpress.agent_skills.canvasxpress_events"

        with patch("canvasxpress.agent_skills.registry._get_entry_points") as mock:
            mock.return_value = [mock_chart, mock_events]
            yield mock_chart, mock_events

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
        """Test that existing directory is not overwritten without force when up to date."""
        from canvasxpress.agent_skills.registry import install_skills

        mock_home = tmp_path / "home"
        mock_home.mkdir()
        monkeypatch.setattr("pathlib.Path.home", lambda: mock_home)

        # Create existing skill directory with matching version stamp
        existing_dir = mock_home / ".config" / "opencode" / "skills" / "canvasxpress_charts"
        existing_dir.mkdir(parents=True, exist_ok=True)
        (existing_dir / "SKILL.md").write_text("Old content")
        (existing_dir / ".skill-version").write_text("0.0.0", encoding="utf-8")

        with patch("canvasxpress.agent_skills.registry.get_version") as mock_get_version:
            mock_get_version.return_value = "0.0.0"
            install_skills(target="opencode", force=False)

        # Directory should not be modified
        assert (existing_dir / "SKILL.md").read_text() == "Old content"

    def test_install_skills_with_force(self, mock_entry_points, tmp_path, monkeypatch):
        """Test that existing directory is overwritten with force."""
        from canvasxpress.agent_skills.registry import install_skills

        mock_home = tmp_path / "home"
        mock_home.mkdir()
        monkeypatch.setattr("pathlib.Path.home", lambda: mock_home)

        # Create existing skill directory with custom SKILL.md
        existing_dir = mock_home / ".config" / "opencode" / "skills" / "canvasxpress_charts"
        existing_dir.mkdir(parents=True, exist_ok=True)
        (existing_dir / "SKILL.md").write_text("Old content")

        install_skills(target="opencode", force=True)

        # Directory should be overwritten with new content
        assert "canvasxpress_charts" in (existing_dir / "SKILL.md").read_text()

    def test_install_skills_invalid_target(self, capsys):
        """Test that invalid target raises exit."""
        from canvasxpress.agent_skills.registry import install_skills

        with pytest.raises(SystemExit):
            install_skills(target="invalid")

    def test_install_skills_copies_all_markdown_files(self, mock_entry_points, tmp_path, monkeypatch):
        """Test that all markdown files are copied, not just SKILL.md."""
        from canvasxpress.agent_skills.registry import install_skills

        mock_home = tmp_path / "home"
        mock_home.mkdir()
        monkeypatch.setattr("pathlib.Path.home", lambda: mock_home)

        install_skills(target="opencode", force=True)

        # Check that supporting files are present
        charts_dir = mock_home / ".config" / "opencode" / "skills" / "canvasxpress_charts"
        assert (charts_dir / "SKILL.md").exists()
        assert (charts_dir / "bar_skill.md").exists()
        assert (charts_dir / "heatmap_skill.md").exists()
        assert (charts_dir / "reference_general.md").exists()
        assert (charts_dir / "reference_conversion.md").exists()
        assert (charts_dir / "events_skill.md").exists()

        # Check that non-markdown files are excluded
        assert not (charts_dir / "__init__.py").exists()

    def test_install_skills_no_python_files_in_dest(self, mock_entry_points, tmp_path, monkeypatch):
        """Test that no .py, .pyc files or __pycache__ exist in destination."""
        from canvasxpress.agent_skills.registry import install_skills

        mock_home = tmp_path / "home"
        mock_home.mkdir()
        monkeypatch.setattr("pathlib.Path.home", lambda: mock_home)

        install_skills(target="opencode", force=True)

        # Check both skill directories
        for skill_name in ["canvasxpress_charts", "canvasxpress_events"]:
            skill_dir = mock_home / ".config" / "opencode" / "skills" / skill_name
            assert skill_dir.exists()
            for p in skill_dir.rglob("*"):
                assert not p.suffix == ".py", f"Found .py file: {p}"
                assert not p.suffix == ".pyc", f"Found .pyc file: {p}"
                assert not "__pycache__" in str(p), f"Found __pycache__: {p}"

    def test_install_skills_no_force_skips_existing(self, mock_entry_points, tmp_path, monkeypatch, capsys):
        """Test that without --force, existing skills are skipped when up to date."""
        from canvasxpress.agent_skills.registry import install_skills

        mock_home = tmp_path / "home"
        mock_home.mkdir()
        monkeypatch.setattr("pathlib.Path.home", lambda: mock_home)

        # Create existing skill directory with matching version stamp
        existing_dir = mock_home / ".config" / "opencode" / "skills" / "canvasxpress_charts"
        existing_dir.mkdir(parents=True, exist_ok=True)
        (existing_dir / "SKILL.md").write_text("Old content")
        (existing_dir / ".skill-version").write_text("0.0.0", encoding="utf-8")

        with patch("canvasxpress.agent_skills.registry.get_version") as mock_get_version:
            mock_get_version.return_value = "0.0.0"
            install_skills(target="opencode", force=False)

        output = capsys.readouterr().out
        assert "skip" in output or "up to date" in output

    def test_install_skills_provenance_stamp(self, mock_entry_points, tmp_path, monkeypatch):
        """Test that .skill-version file is written during installation."""
        from canvasxpress.agent_skills.registry import install_skills

        mock_home = tmp_path / "home"
        mock_home.mkdir()
        monkeypatch.setattr("pathlib.Path.home", lambda: mock_home)

        install_skills(target="opencode", force=True)

        # Check that provenance stamp exists
        charts_dir = mock_home / ".config" / "opencode" / "skills" / "canvasxpress_charts"
        skill_version_file = charts_dir / ".skill-version"
        assert skill_version_file.exists()
        content = skill_version_file.read_text()
        assert len(content) > 0

    def test_install_skills_file_count_reported(self, mock_entry_points, tmp_path, monkeypatch, capsys):
        """Test that file count is reported during installation."""
        from canvasxpress.agent_skills.registry import install_skills

        mock_home = tmp_path / "home"
        mock_home.mkdir()
        monkeypatch.setattr("pathlib.Path.home", lambda: mock_home)

        install_skills(target="opencode", force=True)

        output = capsys.readouterr().out
        assert "installed" in output
        assert "markdown files" in output


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
