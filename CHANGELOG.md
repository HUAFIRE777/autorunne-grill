# Changelog

## 0.1.4

- Added the short default command: running `autorunne-grill` inside an Autorunne-backed repo now auto-installs repo-local rules.
- The short command writes `.agents/skills/autorunne-grill/SKILL.md`, `.claude/skills/autorunne-grill/SKILL.md`, and `.cursor/rules/autorunne-grill.mdc`.
- If the current directory is not Autorunne-backed yet, the CLI now gives a clear `autorunne open --path .` hint instead of silently doing a user-level install.
- Kept the explicit advanced command `autorunne-grill install --scope repo --repo .` for scripts and old docs.

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
