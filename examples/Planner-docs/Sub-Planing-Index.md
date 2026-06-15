# Sub-Planing Index

## 1. Purpose

This index maps the phases in `Planner-docs/Main-Planing.md` to their detailed sub-plan files for
the `linkcheck` example. It exists so a reader can navigate from the master plan to each delivery
slice and confirm full coverage.

## 2. Source Master Plan

Source: `Planner-docs/Main-Planing.md`.

- Detected phase count: 2.
- Detected phase names: Phase 1 (Offline Link Checker), Phase 2 (Network Checking and Packaging).
- No ambiguity or inconsistency was found in the master plan's phase roadmap.

## 3. Phase and Sub-Plan Map

- Phase 1 — Offline Link Checker — folder `Planner-docs/Faz-1-Plans/`:
  - Planner-docs/Faz-1-Plans/Faz1.1-link-extraction-core.md
  - Planner-docs/Faz-1-Plans/Faz1.2-relative-link-resolver.md
- Phase 2 — Network Checking and Packaging — folder `Planner-docs/Faz-2-Plans/`:
  - Planner-docs/Faz-2-Plans/Faz2.1-http-checking-and-packaging.md

Recommended execution order: Faz 1.1, then Faz 1.2, then Faz 2.1.

## 4. Prioritized Elaboration Order

Elaborate and implement the offline core first because it is fully testable without network access
and unblocks everything else: Faz 1.1 (extraction), then Faz 1.2 (resolution and reporting). Only
after the offline path is green should Faz 2.1 add opt-in HTTP checking and packaging.

## 5. Out-of-Scope or Deferred Topics

Site crawling, authenticated requests, and link auto-fixing are deferred. They depend on demand
that does not yet exist and would expand the maintenance surface beyond the stated vision.

## 6. Coverage Check

- Every main phase from `Main-Planing.md` has a folder: Phase 1 and Phase 2 both do.
- Every main phase has at least one sub-plan: Phase 1 has two, Phase 2 has one.
- Sub-plan filenames follow the `Faz<phase>.<sub>-<slug>.md` convention.
- All generated docs are written in English.
- No source code files were modified to produce this index.
- No secrets were written into any planning file.

## 7. Repository Inspection Notes

- Commands run: `ls`, `git status --short`, reading `Main-Planing.md`.
- Files inspected: the master plan and the three generated sub-plan files.
- Assumptions made: the project is greenfield and starts at Phase 1.
- Not verified: the eventual language/toolchain, since no manifest exists yet.
