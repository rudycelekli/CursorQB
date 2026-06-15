# Faz 1.2 — Relative Link Resolver and Reporter

## 1. Context

This sub-phase builds on the extraction core from Faz 1.1 to resolve relative links against the
filesystem and report broken ones. It completes Phase 1 (Offline Link Checker) from
`Planner-docs/Main-Planing.md` and produces the first user-visible behavior.

## 2. Goal

Given extracted links and a scanned root directory, determine which relative links point at files
that do not exist and emit a deterministic, line-numbered report with a non-zero exit code when
any link is broken.

## 3. Description

This sub-phase turns structured links into an actionable result for the user. It belongs after
extraction because resolution needs the link records as input. It reduces project risk by locking
the output format early with snapshot tests, so downstream CI consumers get stable results. It
prepares Phase 2 by defining the reporting interface that HTTP checking will later reuse without
changing the offline path.

## 4. Scope

- Resolve relative link targets against the scanned root, read-only.
- Classify each link as ok or broken with its file and line number.
- A text report and a `--json` report sharing one result model.
- A non-zero process exit code when broken links are present.

## 5. Out of Scope

- HTTP link checking and concurrency (Phase 2).
- Following links outside the scanned root.
- Auto-fixing or rewriting broken links.

## 6. Current Repository Evidence

Relevant evidence is the link record type and fixtures introduced in `Faz1.1-link-extraction-core.md`.
No resolver or reporter exists yet, and the `src/` tree still has no I/O layer, so this sub-phase
adds the first filesystem adapter.

## 7. Planned Work Breakdown

- f1.2-01 — Implement the relative-link resolver.
  - description: map a link target plus its source file path to an absolute path and test
    existence read-only.
  - output: a resolver that classifies links as ok or broken.
- f1.2-02 — Implement the text reporter.
  - description: format broken links as `file:line target` lines in stable order.
  - output: deterministic human-readable output.
- f1.2-03 — Implement the `--json` reporter and exit code.
  - description: emit the same result model as JSON and set a non-zero exit on findings.
  - output: machine-readable output plus CI-gating behavior.

## 8. Acceptance Criteria

- `make test` passes, including a snapshot test of the text report on a mixed fixture tree.
- A fixture with one broken relative link yields exactly one reported finding and a non-zero exit
  code.
- The `--json` output validates against the documented result schema and lists the same findings
  as the text report.

## 9. Validation and Test Approach

Local validation is `make test` for unit and snapshot tests over the fixture tree. Document
validation covers the `--json` schema description. Live readiness is explicitly not addressed here
because no network access exists. Security validation confirms file access stays read-only and
within the scanned root.

## 10. Dependencies and Sequencing

Depends on the link record type and extraction tests from Faz 1.1. Must complete before Phase 2,
because HTTP checking reuses the reporter and exit-code contract defined here.

## 11. Risks and Mitigations

- Risk: unstable report ordering causes noisy diffs. Impact: CI churn. Mitigation: sort findings
  deterministically and lock the format with snapshot tests.

## 12. Desired End State

A working offline checker: `linkcheck <dir>` reports broken relative links with file and line
numbers, supports `--json`, exits non-zero on findings, and is green under `make test`.

## 13. Transition Criteria to the Next Sub-Phase

The offline path is fully green under `make test`, the report format and exit codes are locked by
snapshot tests, and the reporter interface is stable, so Phase 2 can add HTTP checking without
touching the offline path.
