# Maintaining CursorQB

## Validate locally

```bash
make check   # manifest + required files + frontmatter + traversal/handoff scan + tests
make test    # unit tests only (verbose)
```

`make check` runs `scripts/validate.sh`, which:

1. parses `.cursor-plugin/plugin.json` and checks `name == "cursorqb"`;
2. confirms every required file exists (skills, bundled planner specs, references, scripts, commands, docs);
3. checks that each skill's frontmatter `name` equals its directory and each command's `name` equals its filename stem;
4. fails on `../` traversal or Codex handoff residue (`Hedefi Takip Et`, `$codexqb`) in component docs;
5. runs the test suite under `tests/`.

## How the validator works

`scripts/validate_planner_docs.py` is read-only. Run it against a target project's `Planner-docs/`:

```bash
python3 scripts/validate_planner_docs.py --root /path/to/project --mode step2 --strict
```

Modes: `step1` (Main-Planing.md sections + phase roadmap), `step2` (phase folders, sub-plan
structure, full-path index references, optional `Autopsy.md` heading order, duplicate/gap
numbering), `step3` (audit heading order), `step4` (audit status + `AUDIT-FIX-NN | PX` severity
gating). It also runs a length-bounded secret scan in every mode. `--strict` turns quality
warnings (repeated/generic sections) into failures.

Key invariants the tests guard (`tests/`):

- Step-4 severity counting is driven by `AUDIT-FIX-NN | PX` finding headers, so negative prose like "P0/P1 yok" is never miscounted.
- The roadmap phase count comes from the `## 6` table, ignoring historical phase mentions.
- Optional `Autopsy.md` is validated only when present.
- Index references must be full relative paths.

## Editing the bundled prompts

The bundled planner specs are the source of truth for each step and must stay faithful to the
upstream prompts:

- `skills/cursorqb-planner/planners/first-planner.md` (Step 1)
- `skills/cursorqb-autopsy/autopsy-planner.md` (Step 1.5)
- `skills/cursorqb-subplanner/second-planner.md` (Step 2)
- `skills/cursorqb-auditor/third-planner.md` (Step 3)
- `skills/cursorqb-implementer/fourth-planner.md` (Step 4)

When editing them: preserve the misspelled output filenames (`Main-Planing.md`,
`Sub-Planing-Index.md`, `Sub-Planing-Audit.md`), keep all required section headings and order (the
validator and `tests/test_validate_planner_docs.py` enforce them), keep the four Step-1
placeholders, and keep the workflow Cursor-native (no `Hedefi Takip Et`, no `$codexqb`).

## Conventions

- One skill per directory under `skills/`; frontmatter `name` must equal the directory name.
- One command per file under `commands/`; frontmatter `name` must equal the filename stem.
- Shared, read-only assets live in `references/` and `scripts/`; skills resolve them relative to
  the plugin root (walk up to `.cursor-plugin/`), never with `..` in component docs.
- Bump `version` in `.cursor-plugin/plugin.json` and add a `CHANGELOG.md` entry for every change.
