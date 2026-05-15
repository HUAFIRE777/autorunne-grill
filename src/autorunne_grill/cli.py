from __future__ import annotations

import argparse
import shutil
import sys
from importlib import metadata
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
SKILL_RELATIVE = Path("skills/productivity/autorunne-grill/SKILL.md")
DEFAULT_TARGET = Path.home() / ".hermes" / "skills" / "productivity" / "autorunne-grill" / "SKILL.md"
REPO_AGENT_TARGETS = (
    Path(".agents") / "skills" / "autorunne-grill" / "SKILL.md",
    Path(".claude") / "skills" / "autorunne-grill" / "SKILL.md",
)
CURSOR_RULE_TARGET = Path(".cursor") / "rules" / "autorunne-grill.mdc"


def _package_version() -> str:
    try:
        return metadata.version("autorunne-grill")
    except metadata.PackageNotFoundError:
        ns: dict[str, str] = {}
        init_path = Path(__file__).resolve().parent / "__init__.py"
        exec(init_path.read_text(encoding="utf-8"), ns)
        return ns.get("__version__", "0.0.0")


def _cursor_rule_content() -> str:
    version = _package_version()
    return f"""---
description: Use autorunne-grill before changing features in this Autorunne-backed repo
alwaysApply: false
---

# autorunne-grill

Use this rule when the user asks to add, change, remove, redesign, or "just tweak" a product feature in this repo.

This repo is expected to use Autorunne project state. Before writing code, read the project memory first:

1. `.autorunne/views/STATUS.md`
2. `.autorunne/views/START_HERE.md`
3. `.autorunne/views/PROJECT_CONTEXT.md`
4. `.autorunne/views/NEXT_ACTION.md`
5. `.autorunne/views/COMMANDS.md`
6. `.autorunne/TASKS.md`
7. `.autorunne/DECISIONS.md`
8. `.autorunne/state/current.json`

Then inspect only the relevant source files for the requested change. Do not ask the user questions that the repo state, README, tests, routes, schemas, or existing code can answer.

Before implementation, write a compact safety summary in plain language:

```text
我先看了 Autorunne 状态：<current state in one sentence>
这次改动属于：<tiny safe / normal feature / risky architecture / unclear / blocked>
安全边界：<what will change>
不会改：<what is explicitly out of scope>
可能影响：<files/modules/user flows>
验证方式：<exact command>
需要确认：<0 or 1 question, with your recommended answer>
```

Rules:

- Prefer the smallest safe slice.
- Ask at most one question at a time.
- If no question is needed, say so and proceed.
- Preserve existing working flows.
- Add or update tests when behavior changes.
- Run the relevant validation command before finishing.
- If this is a fresh task and no matching active task exists, record it with `autorunne ingest --source cursor --task "<user task>" --next "<small safe next action>"`.
- After validation, finish with `autorunne finish --summary "<what changed>" --validate "<command>" --next "<next safe action>"`.

Installed by autorunne-grill {version}.
"""


def _source_skill() -> Path:
    # Editable/source checkout path.
    checkout_path = PACKAGE_ROOT / SKILL_RELATIVE
    if checkout_path.exists():
        return checkout_path

    # Installed wheel path. Hatch includes the skill as an artifact at package root.
    wheel_path = Path(__file__).resolve().parent / "SKILL.md"
    if wheel_path.exists():
        return wheel_path

    # Fallback for wheels that place artifacts relative to site-packages root.
    for parent in Path(__file__).resolve().parents:
        candidate = parent / SKILL_RELATIVE
        if candidate.exists():
            return candidate

    raise FileNotFoundError("Could not locate autorunne-grill SKILL.md inside the package.")


def _copy_skill(target: Path, force: bool = True) -> Path:
    src = _source_skill()
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and not force:
        raise FileExistsError(f"Target already exists: {target}")
    shutil.copyfile(src, target)
    return target


def _write_cursor_rule(target: Path, force: bool = True) -> Path:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and not force:
        raise FileExistsError(f"Target already exists: {target}")
    target.write_text(_cursor_rule_content(), encoding="utf-8")
    return target


def install(target: Path = DEFAULT_TARGET, force: bool = True) -> Path:
    return _copy_skill(target, force=force)


def install_repo(repo: Path = Path("."), force: bool = True, include_cursor: bool = True) -> list[Path]:
    repo = repo.expanduser().resolve()
    if not repo.exists():
        raise FileNotFoundError(f"Repo path does not exist: {repo}")
    if not (repo / ".autorunne").exists():
        raise FileNotFoundError(f"Repo does not look Autorunne-backed yet: {repo} (missing .autorunne)")
    installed = [_copy_skill(repo / relative, force=force) for relative in REPO_AGENT_TARGETS]
    if include_cursor:
        installed.append(_write_cursor_rule(repo / CURSOR_RULE_TARGET, force=force))
    return installed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="autorunne-grill",
        description="Install the autorunne-grill skill for user-level Hermes or repo-local agent handoff.",
    )
    sub = parser.add_subparsers(dest="command")

    install_parser = sub.add_parser("install", help="Install SKILL.md into ~/.hermes/skills or repo-local agent skill folders")
    install_parser.add_argument("--scope", choices=["user", "repo", "both"], default="user", help="Install for the current user, the current repo, or both")
    install_parser.add_argument("--repo", type=Path, default=Path("."), help="Repo path for --scope repo/both; must contain .autorunne")
    install_parser.add_argument("--target", type=Path, default=None, help="Custom single SKILL.md path; implies --scope user-style single-target install")
    install_parser.add_argument("--no-force", action="store_true", help="Do not overwrite an existing skill")
    install_parser.add_argument("--no-cursor", action="store_true", help="Skip writing .cursor/rules/autorunne-grill.mdc during repo install")

    path_parser = sub.add_parser("path", help="Print the bundled source SKILL.md path")
    path_parser.add_argument("--target", action="store_true", help="Print the default install target path instead")
    path_parser.add_argument("--repo-local", action="store_true", help="Print repo-local install paths including Cursor rule")

    sub.add_parser("version", help="Print the installed autorunne-grill version")

    args = parser.parse_args(argv)

    if args.command == "install":
        try:
            installed: list[Path] = []
            if args.target is not None:
                installed.append(install(args.target.expanduser(), force=not args.no_force))
            else:
                if args.scope in {"user", "both"}:
                    installed.append(install(DEFAULT_TARGET, force=not args.no_force))
                if args.scope in {"repo", "both"}:
                    installed.extend(install_repo(args.repo, force=not args.no_force, include_cursor=not args.no_cursor))
        except Exception as exc:  # pragma: no cover - user-facing path
            print(f"autorunne-grill install failed: {exc}", file=sys.stderr)
            return 1
        for target in installed:
            print(f"Installed autorunne-grill to {target}")
        return 0

    if args.command == "path":
        if args.repo_local:
            for relative in (*REPO_AGENT_TARGETS, CURSOR_RULE_TARGET):
                print(relative)
        else:
            print(DEFAULT_TARGET if args.target else _source_skill())
        return 0

    if args.command == "version":
        print(_package_version())
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
