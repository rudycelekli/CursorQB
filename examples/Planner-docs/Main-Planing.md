# Main Planing

## 1. Executive Summary

This is a worked example of a CursorQB Step 1 master plan for a small, real project: `linkcheck`,
a single-binary command-line tool that scans a directory of Markdown files and reports broken
relative links and dead HTTP links. The example exists so new users can see what a grounded,
non-generic plan looks like before they run CursorQB on their own repository.

The project is greenfield: the repository currently contains only a README sketch and an empty
`src/` directory. Current maturity is M1 (the contract is described in prose, nothing is built).
The main planning conclusion is that delivery should be split into a local-correctness phase
(parsing and relative-link checking, fully offline and testable) followed by a network phase
(HTTP link checking behind explicit opt-in flags). The most important next milestone is a
deterministic offline link checker that passes `make test` on a fixture tree.

## 2. Project Vision

`linkcheck` should make it trivial for a documentation author to catch broken links before
publishing. The intended users are technical writers and engineers running it locally or in CI.
Its engineering value is a fast, dependency-light checker that produces stable, diff-friendly
output. When finished, a user can point it at any docs folder and get an exact list of broken
links with file and line numbers. What must never be compromised: it must never mutate the files
it scans, and network access must always be explicit and opt-in.

## 3. Current State Analysis

The repository today contains `README.md` (a one-paragraph description) and an empty `src/`
directory. There is no build configuration, no tests, no CI, and no link-parsing logic. There is
no configuration file and no operational tooling. Security posture is trivially clean because no
code exists yet. Production readiness is M0 for anything beyond the written intent. The critical
missing components are: a Markdown link parser, a relative-link resolver, a reporting format, a
test fixture tree, and a `make` target wiring it together. Evidence beyond the README is limited
and is stated as such.

## 4. Target End State

Functionally, `linkcheck <dir>` walks Markdown files, extracts links, and reports broken relative
links and (with `--http`) dead HTTP links. Technically, it is a single executable with a small,
well-tested core and no heavy runtime dependencies. Operationally, it returns a non-zero exit code
when broken links are found so it can gate CI. The security target is read-only file access and
opt-in network access only. The testing target is a fixture-driven suite covering valid links,
broken relative links, and anchor links. The observability target is clear, line-numbered output
and a `--json` mode for machine consumption.

## 5. Architectural Direction and Key Decisions

The core domain is link extraction and resolution, kept pure and independent of I/O so it can be
unit tested directly. File walking and reporting are thin adapters around that core. The
source-of-truth for "is this link broken" is the filesystem for relative links and an explicit
HTTP probe for absolute links. State ownership is trivial: the tool is stateless between runs.
The integration boundary is the optional HTTP client, which is isolated behind an interface so the
offline path never imports it. Security boundary: the scanner opens files read-only and never
follows links outside the scanned root. Human-approval boundaries do not apply to this tool.

## 6. Phased Master Roadmap

The repository is greenfield, so the roadmap starts at Phase 1 (local correctness) and ends at
Phase 2 (network checking and packaging). Each phase carries a maturity estimate using the M0-M7
model.

| Phase | Phase name | Goal | Approx. maturity | Key acceptance signals |
|---|---|---|---|---|
| 1 | Offline Link Checker | Parse and resolve relative links with full test coverage | M3 | `make test` green on the fixture tree |
| 2 | Network Checking and Packaging | Add opt-in HTTP checking and ship a single binary | M5 | `make smoke` checks a live URL behind `--http` |

## 7. Critical Risks and Gaps

- Risk: Markdown link parsing edge cases (reference-style links, inline HTML). Why it matters:
  false negatives erode trust. Impact: high. Mitigation: build the fixture tree first and grow it
  with each discovered edge case.
- Risk: network checks make runs slow and flaky. Why it matters: a flaky checker gets disabled in
  CI. Impact: medium. Mitigation: keep HTTP checking opt-in, concurrent, and timeout-bounded.
- Risk: scope creep into a full site crawler. Why it matters: it would balloon maintenance.
  Impact: medium. Mitigation: hold the "no crawling outside the scanned root" boundary firmly.

## 8. Prioritized Next Steps

1. Stand up the build configuration and a failing first test for relative-link resolution.
2. Implement the pure link-extraction core against the fixture tree.
3. Add the relative-link resolver and broken-link reporter with line numbers.
4. Wire a `make test` target and a small fixture tree of valid and broken links.
5. Draft the reporting format (text and `--json`) and lock it with snapshot tests.
6. Defer all HTTP work to Phase 2 and record the interface boundary now.

## 9. Preparation Notes for Step 2

Phase 1 should be decomposed first because it is fully offline and unblocks everything else.
Phase 2 should not be expanded in detail until the offline core is green. Step 2 should collect
evidence on the chosen language's Markdown parsing options and the exact reporting format. The
decision that needs human confirmation before implementation is the output schema for `--json`,
since downstream CI consumers will depend on its stability.

## 10. Repository Inspection Notes

- Files inspected: `README.md` (one-paragraph intent), empty `src/` directory.
- Commands run: `ls`, `git status --short`, `git log --oneline`.
- Existing docs found: only the README sketch; no architecture or runbook docs.
- Assumptions made: the project is greenfield and starts at Phase 1.
- Not verified: the target language/toolchain, since no manifest exists yet.
