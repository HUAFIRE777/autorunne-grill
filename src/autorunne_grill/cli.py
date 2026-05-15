from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
SKILL_RELATIVE = Path("skills/productivity/autorunne-grill/SKILL.md")
DEFAULT_TARGET = Path.home() / ".hermes" / "skills" / "productivity" / "autorunne-grill" / "SKILL.md"


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


def install(target: Path = DEFAULT_TARGET, force: bool = True) -> Path:
    src = _source_skill()
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and not force:
        raise FileExistsError(f"Target already exists: {target}")
    shutil.copyfile(src, target)
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="autorunne-grill",
        description="Install the autorunne-grill skill into a local Hermes skills directory.",
    )
    sub = parser.add_subparsers(dest="command")

    install_parser = sub.add_parser("install", help="Install SKILL.md into ~/.hermes/skills")
    install_parser.add_argument("--target", type=Path, default=DEFAULT_TARGET, help="Target SKILL.md path")
    install_parser.add_argument("--no-force", action="store_true", help="Do not overwrite an existing skill")

    path_parser = sub.add_parser("path", help="Print the bundled source SKILL.md path")
    path_parser.add_argument("--target", action="store_true", help="Print the default install target path instead")

    args = parser.parse_args(argv)

    if args.command == "install":
        try:
            target = install(args.target.expanduser(), force=not args.no_force)
        except Exception as exc:  # pragma: no cover - user-facing path
            print(f"autorunne-grill install failed: {exc}", file=sys.stderr)
            return 1
        print(f"Installed autorunne-grill skill to {target}")
        return 0

    if args.command == "path":
        print(DEFAULT_TARGET if args.target else _source_skill())
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
