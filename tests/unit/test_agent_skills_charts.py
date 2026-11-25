class TestGetSkillContent:
    def test_known_skill_with_extension(self):
        from canvasxpress.agent_skills.canvasxpress_charts import get_skill_content

        content = get_skill_content("bar_skill.md")
        assert content is not None
        assert len(content) > 100

    def test_known_skill_content_matches_file(self):
        try:
            from importlib.resources import files  # novermin
        except ImportError:
            from importlib_resources import files

        from canvasxpress.agent_skills import canvasxpress_charts
        from canvasxpress.agent_skills.canvasxpress_charts import get_skill_content

        expected = (
            files(canvasxpress_charts.__name__).joinpath("bar_skill.md").read_text(encoding="utf-8")
        )
        assert get_skill_content("bar_skill.md") == expected

    def test_unknown_skill_returns_none(self):
        from canvasxpress.agent_skills.canvasxpress_charts import get_skill_content

        assert get_skill_content("nonexistent_skill.md") is None

    def test_bare_name_without_extension_returns_none(self):
        from canvasxpress.agent_skills.canvasxpress_charts import get_skill_content

        assert get_skill_content("bar_skill") is None

    def test_null_byte_name_returns_none(self):
        """A name that makes files() raise (e.g. NUL byte) must not propagate."""
        from canvasxpress.agent_skills.canvasxpress_charts import get_skill_content

        assert get_skill_content("bad\0name.md") is None


class TestGetAvailableSkills:
    def test_returns_sorted_chart_skills(self):
        from canvasxpress.agent_skills.canvasxpress_charts import (
            CHART_SKILLS,
            get_available_skills,
        )

        assert get_available_skills() == sorted(CHART_SKILLS)

    def test_returns_list_of_strings(self):
        from canvasxpress.agent_skills.canvasxpress_charts import get_available_skills

        skills = get_available_skills()
        assert isinstance(skills, list)
        assert all(isinstance(name, str) for name in skills)
        assert len(skills) == len(set(skills))


class TestListSkills:
    def test_prints_all_skills(self, capsys):
        from canvasxpress.agent_skills.canvasxpress_charts import (
            CHART_SKILLS,
            list_skills,
        )

        list_skills()

        output = capsys.readouterr().out
        assert output.splitlines() == sorted(CHART_SKILLS)
