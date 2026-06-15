# Faz 2.1 — Opt-in HTTP Checking and Packaging

## 1. Context

This sub-phase implements Phase 2 (Network Checking and Packaging) from
`Planner-docs/Main-Planing.md`. It assumes the offline checker from Phase 1 is complete and green,
and it adds opt-in HTTP link checking plus a single-binary distribution.

## 2. Goal

Add a `--http` flag that probes absolute links concurrently with bounded timeouts and folds the
results into the existing report, then package the tool as one distributable binary.

## 3. Description

This sub-phase extends the checker to catch dead external links while preserving the fast, offline
default. It belongs last because network checking is slower and flakier than local resolution, so
it must stay opt-in and must not destabilize the offline path. It reduces risk by isolating the
HTTP client behind an interface the offline path never imports, and it prepares real-world adoption
by shipping a binary that runs in CI.

## 4. Scope

- A `--http` flag that enables absolute-link probing.
- A concurrent, timeout-bounded HTTP client behind an interface.
- Merging HTTP results into the Phase 1 report and exit-code logic.
- A packaging target that produces a single binary.

## 5. Out of Scope

- Crawling pages beyond the links found in the scanned files.
- Authenticated requests or following redirects past a small bound.
- Any change to the offline resolution path's behavior.

## 6. Current Repository Evidence

Relevant evidence is the reporter and exit-code contract from `Faz1.2-relative-link-resolver.md`
and the extraction core from `Faz1.1-link-extraction-core.md`. No HTTP client and no packaging
configuration exist yet, so this sub-phase introduces both behind the existing interfaces.

## 7. Planned Work Breakdown

- f2.1-01 — Define the HTTP probe interface.
  - description: an interface returning reachable or unreachable for an absolute URL, isolated so
    the offline path never imports it.
  - output: a seam that keeps the default path network-free.
- f2.1-02 — Implement the concurrent, timeout-bounded probe.
  - description: probe absolute links in parallel with per-request timeouts and a concurrency cap.
  - output: a bounded HTTP checker behind the interface.
- f2.1-03 — Wire `--http` and packaging.
  - description: merge HTTP findings into the report and add a single-binary build target.
  - output: opt-in network checking and a shippable binary.

## 8. Acceptance Criteria

- `make smoke` checks at least one known-good and one known-bad URL behind `--http` and exits with
  the expected status for each.
- With `--http` absent, the tool performs zero network requests, verified by a test that fails if
  the HTTP interface is invoked.
- `make build` produces a single runnable binary that prints a version string.

## 9. Validation and Test Approach

Local validation is `make test` for the merge logic using a stubbed HTTP interface. Live readiness
is validated separately by `make smoke`, which performs real network probes and is the only target
that touches the network. Document validation covers the `--http` usage notes. Security validation
confirms network access happens only under `--http`.

## 10. Dependencies and Sequencing

Depends on the completed, green offline checker from Phase 1, specifically the reporter and
exit-code contract. Live smoke validation depends on outbound network access being available in the
environment where it runs.

## 11. Risks and Mitigations

- Risk: flaky external endpoints make `make smoke` unreliable. Impact: CI noise. Mitigation: keep
  network checks opt-in, bound timeouts and concurrency, and pin smoke URLs to stable endpoints.

## 12. Desired End State

`linkcheck <dir> --http` checks both relative and absolute links, the offline default stays fast
and network-free, `make smoke` exercises live URLs, and `make build` ships a single binary.

## 13. Transition Criteria to the Next Sub-Phase

Phase 2 is the final phase; the project is complete when the offline suite is green, `make smoke`
passes against pinned URLs, and the packaged binary runs, so no further sub-phase is required.
