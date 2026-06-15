---
name: cursorqb-demo
description: Dry-run tour of CursorQB on the bundled example, with no edits to your repo. Shows what a finished Planner-docs/ looks like and how the validator gates each step.
---

# CursorQB Demo (read-only dry run)

Give the user a 30-second feel for CursorQB without touching their repository. This command is
read-only: it inspects the bundled example under `examples/Planner-docs/` and runs the validator
against it. It never creates, edits, or deletes files in the user's workspace.

Resolve `<plugin-root>` by walking up to the folder containing `.cursor-plugin/plugin.json`.

Steps:

1. List the example tree so the user sees a complete, real Step 1-3 output:
   `find <plugin-root>/examples/Planner-docs -maxdepth 2 -type f | sort`
2. Show the master plan's phase roadmap and the index's phase/sub-plan map (read
   `examples/Planner-docs/Main-Planing.md` section 6 and `examples/Planner-docs/Sub-Planing-Index.md`
   section 3).
3. Demonstrate the gate by running the bundled validator against the example in each mode:

   ```bash
   for mode in step1 step2 step3 step4 all; do
     python3 <plugin-root>/scripts/validate_planner_docs.py --root <plugin-root>/examples --mode "$mode" --strict
   done
   ```

   All five runs print `planner_docs_validation=passed` - this is what a healthy plan looks like.
4. Explain the workflow the example illustrates: Step 1 (`/cursorqb-plan`) writes
   `Main-Planing.md`; Step 1.5 (`/cursorqb-autopsy`, existing repos) writes `Autopsy.md`; Step 2
   decomposes phases into `Faz-<n>-Plans/` sub-plans plus `Sub-Planing-Index.md`; Step 3
   (`/cursorqb-audit`) writes `Sub-Planing-Audit.md` with a PASS / PASS_WITH_WARNINGS / BLOCKED
   verdict; Step 4 (`/cursorqb-implement`) implements one audited, reversible slice at a time.
5. Tell the user the next real action: run `/cursorqb-plan` in their own project to generate their
   first `Planner-docs/Main-Planing.md`.

Do not modify anything. The example is a reference artifact, not a target to edit.
