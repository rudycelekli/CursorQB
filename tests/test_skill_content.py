from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS = REPO_ROOT / "skills"
COMMANDS = REPO_ROOT / "commands"
REFERENCES = REPO_ROOT / "references"

AUTOPSY_HEADINGS = [
    "# Project Autopsy",
    "## 1. Executive Summary",
    "## 2. Inspected Sources",
    "## 3. Project Areas and Responsibility Boundaries",
    "## 4. Feature Inventory",
    "## 5. Placeholder, Stub, and Skeleton Analysis",
    "## 6. Technical Debt and Maintenance Risks",
    "## 7. Broken or Missing Integrations",
    "## 8. Test, CI, and Validation Gaps",
    "## 9. Security, Secret, and Governance Findings",
    "## 10. Operational Readiness and Observability",
    "## 11. Alignment with the Main Plan",
    "## 12. Autopsy Feedback for Step 2",
    "## 13. Prioritized Remediation and Planning Signals",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class SkillContentTests(unittest.TestCase):
    def test_planner_references_repo_aware_intake(self) -> None:
        skill = read(SKILLS / "cursorqb-planner/SKILL.md")
        self.assertIn("references/repo-aware-intake.md", skill)
        self.assertIn("repo-aware", skill.lower())

    def test_repo_aware_intake_keeps_stable_four_fields(self) -> None:
        intake = read(REFERENCES / "repo-aware-intake.md")
        for field in ["PROJECT_NAME", "PROJECT_INTENT", "TARGET_END_STATE", "KNOWN_CONSTRAINTS"]:
            self.assertIn(field, intake)
        for number in range(1, 5):
            self.assertIn(f"Question {number} / 4", intake)
        self.assertIn("Use plain text only", intake)
        self.assertIn("Pre-Intake Scan", intake)

    def test_first_planner_required_placeholders_remain_stable(self) -> None:
        first_planner = read(SKILLS / "cursorqb-planner/planners/first-planner.md")
        for placeholder in [
            "<WRITE_PROJECT_NAME_HERE>",
            "WRITE_THE_PROJECT_PURPOSE_HERE",
            "WRITE_THE_DESIRED_FINAL_STATE_HERE",
            "WRITE_CONSTRAINTS_HERE",
        ]:
            self.assertIn(placeholder, first_planner)
        # Intentional misspelled output filename must be preserved.
        self.assertIn("Main-Planing.md", first_planner)

    def test_autopsy_is_wired_into_workflow(self) -> None:
        planner = read(SKILLS / "cursorqb-planner/SKILL.md")
        subplanner = read(SKILLS / "cursorqb-subplanner/SKILL.md")
        second = read(SKILLS / "cursorqb-subplanner/second-planner.md")
        autopsy = read(SKILLS / "cursorqb-autopsy/autopsy-planner.md")

        self.assertIn("cursorqb-autopsy", planner)
        self.assertIn("Step 1.5", planner)
        self.assertIn("Autopsy.md", subplanner)
        self.assertIn("Autopsy.md is not a replacement for Main-Planing.md", second)

        for heading in AUTOPSY_HEADINGS:
            self.assertIn(heading, autopsy)

    def test_validator_guidance_uses_plugin_root_not_global_path(self) -> None:
        checked = [
            SKILLS / "cursorqb-planner/SKILL.md",
            SKILLS / "cursorqb-subplanner/SKILL.md",
            SKILLS / "cursorqb-auditor/SKILL.md",
            SKILLS / "cursorqb-autopsy/SKILL.md",
            REFERENCES / "workflow-quality.md",
        ]
        for path in checked:
            text = read(path)
            self.assertNotIn("~/.codex/skills", text, path.name)
            self.assertIn("scripts/validate_planner_docs.py", text, path.name)

    def test_implementer_external_skills_are_optional_with_fallback(self) -> None:
        impl = read(SKILLS / "cursorqb-implementer/SKILL.md")
        fourth = read(SKILLS / "cursorqb-implementer/fourth-planner.md")
        for text in (impl, fourth):
            lowered = text.lower()
            self.assertIn("if installed/available", lowered)
            self.assertIn("superpowers", lowered)
            self.assertIn("review-security", lowered)

    def test_planners_treat_ingested_content_as_untrusted_data(self) -> None:
        # Red-team guard: every prompt that ingests repo content or user answers must frame
        # that content as untrusted data, not instructions, to blunt prompt injection.
        ingesting_prompts = [
            SKILLS / "cursorqb-planner/planners/first-planner.md",
            SKILLS / "cursorqb-subplanner/second-planner.md",
            SKILLS / "cursorqb-autopsy/autopsy-planner.md",
        ]
        for path in ingesting_prompts:
            lowered = read(path).lower()
            self.assertIn("untrusted", lowered, path.name)
            self.assertIn("data, not instructions", lowered, path.name)
            self.assertIn("ignore previous instructions", lowered, path.name)

    def test_implementer_step4_is_transactional(self) -> None:
        impl = read(SKILLS / "cursorqb-implementer/SKILL.md")
        fourth = read(SKILLS / "cursorqb-implementer/fourth-planner.md")
        for text in (impl, fourth):
            lowered = text.lower()
            self.assertIn("git status --porcelain", lowered)
            self.assertIn("snapshot", lowered)
            self.assertIn("auto-revert", lowered)
            # Must forbid whole-tree destructive reverts.
            self.assertIn("git reset --hard", lowered)

    def test_auditor_fix_list_uses_single_line_severity_format(self) -> None:
        auditor = read(SKILLS / "cursorqb-auditor/SKILL.md")
        self.assertIn("AUDIT-FIX-NN | PX", auditor)

    def test_auditor_uses_objective_scored_rubric(self) -> None:
        third = read(SKILLS / "cursorqb-auditor/third-planner.md")
        # Objective, deterministic rubric with measurable checks replaces vague prose.
        self.assertIn("objective scored rubric", third.lower())
        self.assertIn("deterministic", third.lower())
        for check in ("CQ1", "CQ2", "CQ3"):
            self.assertIn(check, third)
        self.assertIn("Structure PASS", third)
        self.assertIn("Substance PASS", third)
        self.assertIn("vague-term denylist", third.lower())

    def test_no_codex_handoff_terms_in_components(self) -> None:
        # Cursor-native: no Codex "Follow the Goal" handoff and no $codexqb invocation.
        for base in (SKILLS, COMMANDS, REFERENCES):
            for path in base.rglob("*.md"):
                text = read(path)
                self.assertNotIn("Hedefi Takip Et", text, str(path))
                self.assertNotIn("$codexqb", text, str(path))

    def test_define_goal_is_automatic_in_orchestrator(self) -> None:
        planner = read(SKILLS / "cursorqb-planner/SKILL.md")
        self.assertIn("define-goal", planner)
        self.assertIn("automatic", planner.lower())

    def test_every_skill_and_command_name_matches_path(self) -> None:
        for skill_md in SKILLS.rglob("SKILL.md"):
            name = _frontmatter_name(read(skill_md))
            self.assertEqual(name, skill_md.parent.name, str(skill_md))
        for command_md in COMMANDS.glob("*.md"):
            name = _frontmatter_name(read(command_md))
            self.assertEqual(name, command_md.stem, str(command_md))


def _frontmatter_name(text: str) -> str | None:
    for line in text.splitlines():
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip()
    return None


if __name__ == "__main__":
    unittest.main()
