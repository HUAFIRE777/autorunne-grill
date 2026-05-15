# Changelog

## 0.1.3

- Added one-command Cursor support for repo-local installs via `.cursor/rules/autorunne-grill.mdc`.
- Repo installs now write Codex-style, Claude Code, and Cursor handoff files together.
- Added `autorunne-grill path --repo-local` and `autorunne-grill version`.
- Tightened the skill rules: read Autorunne first, state the safe boundary before editing, ask at most one needed question, validate, then record back to Autorunne.

## 0.1.2

- Added repo-local install mode for `.agents/skills` and `.claude/skills`.
- Improved real-development examples and Autorunne-backed safe-change workflow.

## 0.1.1

- Made PyPI/pipx the primary install path.

## 0.1.0

- Initial autorunne-grill skill and installer.
