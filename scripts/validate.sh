#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# 1) Manifest parses.
python3 -m json.tool .cursor-plugin/plugin.json >/dev/null

# 2) Required files exist (Cursor single-plugin-at-root layout).
required_files=(
  ".cursor-plugin/plugin.json"
  "scripts/validate_planner_docs.py"
  "skills/cursorqb-planner/SKILL.md"
  "skills/cursorqb-planner/planners/first-planner.md"
  "skills/cursorqb-autopsy/SKILL.md"
  "skills/cursorqb-autopsy/autopsy-planner.md"
  "skills/cursorqb-subplanner/SKILL.md"
  "skills/cursorqb-subplanner/second-planner.md"
  "skills/cursorqb-auditor/SKILL.md"
  "skills/cursorqb-auditor/third-planner.md"
  "skills/cursorqb-implementer/SKILL.md"
  "skills/cursorqb-implementer/fourth-planner.md"
  "commands/cursorqb-plan.md"
  "commands/cursorqb-autopsy.md"
  "commands/cursorqb-audit.md"
  "commands/cursorqb-implement.md"
  "references/workflow-quality.md"
  "references/repo-aware-intake.md"
  "README.md"
  "CHANGELOG.md"
  "LICENSE"
  "docs/INSTALLATION.md"
  "docs/USAGE.md"
  "docs/MAINTAINING.md"
)

for path in "${required_files[@]}"; do
  if [[ ! -f "$path" ]]; then
    echo "missing_required_file=$path"
    exit 1
  fi
done

# 3) Manifest name is the expected kebab-case id.
python3 - <<'PY'
import json
import sys

data = json.loads(open(".cursor-plugin/plugin.json", encoding="utf-8").read())
if data.get("name") != "cursorqb":
    print(f"unexpected_plugin_name={data.get('name')!r}")
    sys.exit(1)
PY

# 4) Frontmatter name == directory/filename for every skill and command.
python3 - <<'PY'
import sys
from pathlib import Path


def frontmatter_name(text: str):
    for line in text.splitlines():
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip()
    return None


problems = []
for skill in Path("skills").rglob("SKILL.md"):
    name = frontmatter_name(skill.read_text(encoding="utf-8"))
    if name != skill.parent.name:
        problems.append(f"skill_name_mismatch={skill}::name={name}::dir={skill.parent.name}")
for command in Path("commands").glob("*.md"):
    name = frontmatter_name(command.read_text(encoding="utf-8"))
    if name != command.stem:
        problems.append(f"command_name_mismatch={command}::name={name}::stem={command.stem}")

if problems:
    for problem in problems:
        print(problem)
    sys.exit(1)
PY

# 5) No parent-directory traversal and no Codex handoff residue in component docs.
python3 - <<'PY'
import sys
from pathlib import Path

forbidden_substrings = {
    "parent_traversal": "../",
    "codex_followup_button": "Hedefi Takip Et",
    "codex_invocation": "$codexqb",
}

problems = []
for base in ("skills", "references", "commands"):
    for path in Path(base).rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for label, needle in forbidden_substrings.items():
            if needle in text:
                problems.append(f"{label}={path}")

if problems:
    for problem in problems:
        print(problem)
    sys.exit(1)
PY

# 6) Unit tests (validator behavior + skill-content invariants).
python3 -m unittest discover -s tests

echo "cursorqb_repo_validation=passed"
