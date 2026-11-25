# Contributing Guidelines

Welcome! This project is built for seamless collaboration between human developers and AI coding agents (such as **Qwen**, **Claude**, and others). Whether you are fixing a bug, adding a feature, or improving documentation, please follow these instructions to keep the codebase clean, well-tested, and aligned with our architecture.

---

## 1. Repository Orientation & Key Files

Before making any changes, orient yourself using the repository's core documentation and configuration files:

* **`AGENTS.md`**: Contains mandatory housekeeping rules, formatting preferences, coding standards, and operational guardrails for AI agents. **All agents must read and strictly obey `AGENTS.md` before executing tasks.**
* **`ARCHITECTURE.md`**: Explains the technical design, module boundaries, data flows, and design patterns of the repository for both humans and agents. Consult this file before introducing new modules or altering core behavior.
* **`.opencode/`**: Contains project-specific skills, workflows, and helper scripts for local development and testing. Agents and developers should leverage the skills inside `.opencode/` to run test suites, lint code, and scaffold components consistently.
* **`README.md`**: Serves as the public-facing **PyPI package description**. Keep changes to `README.md` focused on end-user installation, quickstart examples, and high-level features. Avoid cluttering it with internal contributor notes or PyPI-incompatible Markdown syntax.

---

## 2. Gitflow & Branching Strategy

This repository strictly enforces **Gitflow** to separate active development from production releases:

* **`main`**: Reflects accepted, production-ready, released code only. Direct pull requests to `main` are reserved for release integration and hotfixes.
* **`develop`**: The primary working and integration branch. **All pull requests from forked repositories and feature branches must target `develop`.**

### Standard Workflow for Contributors & Agents

1. **Fork & Clone**: Fork the repository to your account and clone it locally.
2. **Sync with `develop`**: Ensure your local `develop` branch is up to date with `upstream/develop`.
3. **Create a Topic Branch**: Branch off `develop` using a descriptive prefix:
   * `feat/<short-description>` for new features
   * `fix/<short-description>` for bug fixes
   * `docs/<short-description>` for documentation updates
   * `refactor/<short-description>` for code restructuring without behavior changes
   * `test/<short-description>` for adding or updating tests
4. **Target `develop` on PR**: When opening a Pull Request from your fork, verify that the base branch is set to **`develop`**, not `main`.

---

## 3. Agentic Contribution Protocol

Because **Qwen** acts as our primary development agent alongside third-party agent contributors like **Claude**, maintaining context across sessions is critical:

1. **Context Loading**: At the start of a session, ingest `AGENTS.md`, `ARCHITECTURE.md`, and relevant skills in `.opencode/`.
2. **Skill Usage**: Use the development and testing skills provided in `.opencode/` rather than inventing ad-hoc shell commands for testing, linting, or building.
3. **Scope Discipline**: Keep changes atomic and strictly scoped to the assigned issue or feature. Do not perform unsolicited repository-wide reformatting.
4. **Documentation Sync**:
   * If you alter system design, public APIs, or module relationships, update **`ARCHITECTURE.md`**.
   * If you add user-facing features or change CLI/API usage, update **`README.md`** (ensuring PyPI rendering compatibility).
   * If you introduce new repeatable development workflows or testing procedures, add or update the corresponding skill in **`.opencode/`**.
5. **Commit Hygiene**: Write clear, imperative commit messages (e.g., `feat(parser): add support for nested config blocks`). If your contribution was co-authored by an AI agent, include an appropriate `Co-authored-by:` trailer in the commit message.

---

## 4. Development & Testing Checklist

Before submitting a Pull Request against `develop`, confirm all of the following:

* [ ] **Housekeeping**: All rules in `AGENTS.md` have been respected.
* [ ] **Architecture Alignment**: Changes adhere to the patterns described in `ARCHITECTURE.md`.
* [ ] **Tests Pass**: All existing unit and integration tests pass, and new tests cover your additions (run via the `.opencode/` testing skills or standard project test runner).
* [ ] **PyPI Readiness**: Any edits to `README.md` use standard Markdown compatible with PyPI (`twine check` passes if packaging tools are installed).
* [ ] **Target Branch**: The PR targets **`develop`** from a feature/fix branch on your fork.
* [ ] **API Documentation**: Classes, functions, and code are documented using the Google Python Standards.
* [ ] **Formatting**: Code is formatted using Ruff configured for black default settings.
* [ ] **Python 3.8+ compliance**: All logic must survive Python 3.8 through 3.15 runtime contexts. 
---

## 5. Submitting a Pull Request

When opening your PR against `develop`, please provide:

1. **Summary of Changes**: What was changed and why.
2. **Architectural Impact**: Note whether `ARCHITECTURE.md` or `.opencode/` skills were updated.
3. **Verification**: Brief confirmation of the test suites or `.opencode/` skills executed to validate the work.
