# CursorQB

> Plan any project end to end inside Cursor — turn a fuzzy idea into a clear, reviewed,
> build-ready plan, then ship it one safe slice at a time.

![version](https://img.shields.io/badge/version-0.4.0-blue)
![license](https://img.shields.io/badge/license-MIT-green)
![Cursor](https://img.shields.io/badge/Cursor-plugin-black)
![works with](https://img.shields.io/badge/works%20with-new%20%26%20existing%20repos-orange)

CursorQB is a **Cursor plugin** that runs a guided, five-step planning workflow right in your chat.
You answer a few short questions in your own language; CursorQB inspects your repository, writes a
senior-architect **master plan**, breaks it into detailed **phase sub-plans**, **audits** them for
quality, and (optionally) **implements** one reviewed slice — pausing for your approval at every step.

No CLI, no API key, no setup. Just type `/cursorqb-plan`.

## Why CursorQB?

- **From idea to plan, fast.** No more blank page — get a structured, phase-by-phase plan grounded in your real repository.
- **Repo-aware.** It reads your codebase first and proposes evidence-backed answers, so the plan fits what you already have.
- **Quality-checked.** A built-in auditor and a read-only validator catch missing sections, gaps, and scope drift before you build.
- **You stay in control.** There is an explicit approval gate between every step, and planning never touches your source code.
- **Speaks your language.** Questions are asked in whatever language you write in; the planning documents are written in English.

## Quick start

1. **Install** — symlink the plugin into Cursor's local plugins folder:

```bash
ln -s "/absolute/path/to/CursorQB" ~/.cursor/plugins/local/cursorqb
```

2. **Reload Cursor** — `Cmd/Ctrl + Shift + P` → **Developer: Reload Window**.
3. **Plan** — open the chat in your project and run `/cursorqb-plan` (or just ask, "plan my project").

Then answer the four short questions and approve each step as you go.

## What you'll get

Every artifact lands under `Planner-docs/` in **your** workspace — never in the plugin folder:

```text
Planner-docs/
├── Main-Planing.md         # the master plan                         (Step 1)
├── Autopsy.md              # repo health report for existing projects (Step 1.5)
├── Sub-Planing-Index.md    # map of every sub-plan + coverage check    (Step 2)
├── Sub-Planing-Audit.md    # quality/coverage audit + PASS/BLOCKED     (Step 3)
└── Faz-1-Plans/            # detailed sub-plans, one folder per phase
    ├── Faz1.1-...md
    └── Faz1.2-...md
```

## How it works

```text
You ──/cursorqb-plan──►  Step 1    Master plan          (you answer 4 questions)
                         Step 1.5  Repo autopsy          (existing projects only)
                         ── Gate 1: review & give feedback, then approve ──
                         Step 2    Phase sub-plans
                         ── Gate 2: approve the audit ──
                         Step 3    Quality audit         (PASS / warnings / blocked)
                         ── Step-4 gate: clean audit, no blockers ──
                         Step 4    Implement one slice   (optional, you approve)
```

| Step | Name | What happens | Your part |
|---|---|---|---|
| 1 | Master plan | Repo-aware intake, then a senior-architect plan written to `Main-Planing.md`. | Answer 4 questions |
| 1.5 | Autopsy | For existing projects, a technical health report in `Autopsy.md`. | — (auto / skipped) |
| Gate 1 | Review | Review the plan (and autopsy) together. | Feedback + approve |
| 2 | Sub-plans | Every phase becomes detailed sub-plans + an index. | — |
| Gate 2 | Approve audit | Confirm you want the quality audit. | Approve |
| 3 | Audit | Coverage/quality audit with a `PASS` / `PASS_WITH_WARNINGS` / `BLOCKED` status. | Approve repairs if needed |
| 4 | Implement | One bounded, reversible code slice from a `READY` sub-plan. | Approve (gated) |

## Commands

| Command | What it does |
|---|---|
| `/cursorqb-plan` | Run the full workflow from the start. |
| `/cursorqb-autopsy` | Analyze an existing repository only (Step 1.5). |
| `/cursorqb-audit` | Re-run the quality audit only (Step 3). |
| `/cursorqb-implement` | Implement one reviewed slice (Step 4, gated). |

## You stay in control

- Steps 1–3 only write inside `Planner-docs/` — they never modify your source code, config, tests, or scripts.
- Step 4 is the **only** step that edits code, and only after the audit passes and you approve — one reversible slice at a time.
- It never commits, pushes, opens a PR, or calls external systems unless you explicitly ask.
- No secrets, tokens, or credentials are ever written into a file.
- CursorQB pauses for your explicit approval at every gate.

## Requirements

- **Cursor** with plugin support.
- **`python3`** (optional) — powers the bundled validator and tests, with a manual fallback when it is missing.

## FAQ

**Will it change my code?**
Not during planning. Only Step 4 touches code, and only with your explicit approval.

**What if my repo is brand new or empty?**
The autopsy is skipped automatically — you still get a full master plan and sub-plans.

**What language is the output in?**
Questions follow your language; all planning documents are written in English.

**Why the names `Faz` and `Planing`?**
They are intentional, stable file/folder identifiers that the validator and index references depend on. The document *content* is English.

**Do I need an API key or a terminal tool?**
No. CursorQB runs entirely in-session inside Cursor.

## Development

```bash
make check   # validate the manifest, required files, and frontmatter, then run the tests
make test    # run the unit tests only
```

See [`docs/INSTALLATION.md`](docs/INSTALLATION.md), [`docs/USAGE.md`](docs/USAGE.md), and
[`docs/MAINTAINING.md`](docs/MAINTAINING.md) for details, and [`CHANGELOG.md`](CHANGELOG.md) for release notes.

## License

[MIT](LICENSE) © Alican Kiraz
