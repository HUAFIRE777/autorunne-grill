from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "productivity" / "autorunne-grill" / "SKILL.md"


def test_skill_frontmatter_is_valid():
    content = SKILL.read_text(encoding="utf-8")
    assert content.startswith("---\n")
    match = re.search(r"\n---\n", content[4:])
    assert match, "frontmatter must close with ---"
    fm = yaml.safe_load(content[4 : 4 + match.start()])
    assert fm["name"] == "autorunne-grill"
    assert "description" in fm
    assert len(fm["description"]) <= 1024
    assert fm["version"] == "0.1.2"
    assert len(content) <= 100_000
    assert content[4 + match.end() :].strip()


def test_skill_requires_autorunne_state_before_questions():
    content = SKILL.read_text(encoding="utf-8")
    required = [
        ".autorunne/views/STATUS.md",
        ".autorunne/views/START_HERE.md",
        ".autorunne/views/PROJECT_CONTEXT.md",
        ".autorunne/TASKS.md",
        ".autorunne/DECISIONS.md",
        ".autorunne/state/current.json",
        "Ask at most one question at a time.",
        "If a question can be answered by reading `.autorunne/`",
        "autorunne ingest --source <agent>",
        "autorunne finish --summary",
    ]
    for text in required:
        assert text in content


def test_beginner_real_project_examples_are_present():
    content = SKILL.read_text(encoding="utf-8")
    assert "帮我加一个登录功能" in content
    assert "课程线索收集 Demo" in content
    assert "管理员登录" in content
    assert "python -m pytest -q" in content
    assert "不会改" in content


def test_cli_installs_skill_to_custom_target(tmp_path):
    target = tmp_path / "skills" / "productivity" / "autorunne-grill" / "SKILL.md"
    result = subprocess.run(
        [sys.executable, "-m", "autorunne_grill", "install", "--target", str(target)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert target.exists()
    installed = target.read_text(encoding="utf-8")
    assert "name: autorunne-grill" in installed
    assert "Required Read Order" in installed


def test_cli_installs_repo_local_agent_skills(tmp_path):
    repo = tmp_path / "demo"
    (repo / ".autorunne").mkdir(parents=True)

    result = subprocess.run(
        [sys.executable, "-m", "autorunne_grill", "install", "--scope", "repo", "--repo", str(repo)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    agent_skill = repo / ".agents" / "skills" / "autorunne-grill" / "SKILL.md"
    claude_skill = repo / ".claude" / "skills" / "autorunne-grill" / "SKILL.md"
    assert agent_skill.exists()
    assert claude_skill.exists()
    assert "name: autorunne-grill" in agent_skill.read_text(encoding="utf-8")
    assert "Installed autorunne-grill skill to" in result.stdout


def test_cli_refuses_repo_scope_without_autorunne_state(tmp_path):
    result = subprocess.run(
        [sys.executable, "-m", "autorunne_grill", "install", "--scope", "repo", "--repo", str(tmp_path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "missing .autorunne" in result.stderr
