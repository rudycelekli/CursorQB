# Faz 1.1 — Link Extraction Core

## 1. Context

This sub-phase delivers the pure parsing core for Phase 1 (Offline Link Checker) from
`Planner-docs/Main-Planing.md`. The repository currently has only `README.md` and an empty
`src/`, so this is the first executable slice and every later sub-phase depends on it.

## 2. Goal

Produce a pure function that, given the text of a Markdown file, returns every link it contains
with the link target and the 1-based line number, with no filesystem or network access.

## 3. Description

This sub-phase solves the foundational problem of turning raw Markdown into a structured list of
links that the rest of the tool can reason about. It belongs first because the resolver and the
reporter both consume its output, and getting the extraction contract right early prevents
rework. By isolating extraction from I/O it reduces risk: the trickiest logic becomes directly
unit-testable, and the fixture tree built here becomes the regression net for the whole project.

## 4. Scope

- Inline link extraction (`[text](target)`).
- Reference-style link extraction and definition resolution.
- Capturing the 1-based line number of each link.
- A growing fixture set of Markdown snippets covering each supported syntax.

## 5. Out of Scope

- Filesystem resolution of relative links (Faz 1.2).
- Any HTTP access (Phase 2).
- Rendering or rewriting Markdown.

## 6. Current Repository Evidence

Current repository evidence for this sub-phase is limited: only `README.md` and an empty `src/`
directory exist. There is no parser, no test fixtures, and no build configuration yet, so this
sub-phase creates them from scratch under `src/`.

## 7. Planned Work Breakdown

- f1.1-01 — Define the link record type.
  - description: a small struct of target plus line number that extraction returns.
  - output: a typed record used across the core.
- f1.1-02 — Implement inline link extraction.
  - description: scan a line for inline link syntax and emit records.
  - output: a tested extraction function.
- f1.1-03 — Implement reference-style resolution.
  - description: collect link definitions and resolve referenced labels.
  - output: extraction that handles reference links.

## 8. Acceptance Criteria

- `make test` runs the extraction unit tests and passes on the fixture snippets.
- Given a fixture with three inline links, extraction returns exactly three records with correct
  line numbers.
- Reference-style links resolve to their defined targets, verified by a dedicated fixture.

## 9. Validation and Test Approach

Document validation is by code review of the extraction contract. Local validation is `make test`,
which runs the unit suite against the fixture snippets. There is no live or CI validation in this
sub-phase. Security validation is trivial because the core performs no I/O.

## 10. Dependencies and Sequencing

This is the first sub-phase and has no upstream dependencies beyond standing up the build
configuration. Faz 1.2 depends on the link record type defined here.

## 11. Risks and Mitigations

- Risk: missed Markdown link variants. Impact: false negatives later. Mitigation: start the
  fixture tree here and extend it whenever a new variant is found.

## 12. Desired End State

A pure, dependency-light extraction function with unit tests green under `make test`, returning
accurate link records with line numbers for inline and reference-style links.

## 13. Transition Criteria to the Next Sub-Phase

The link record type is stable and documented, extraction tests pass locally, and no I/O has crept
into the core, so Faz 1.2 can build resolution on top of it.
