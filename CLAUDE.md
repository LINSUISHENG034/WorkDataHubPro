# Repository Guidelines

## Project Structure & Module Organization
`WorkDataHubPro` is a capability-first rebuild. The committed source of truth
is split across `docs/`, `config/`, `reference/`, `src/`, and `tests/`.

- `docs/superpowers/specs/` holds the active architecture blueprint. Start with `docs/superpowers/specs/2026-04-11-workdatahubpro-rebuild-architecture-draft.md`.
- when the task involves new slice selection, legacy coverage, or retirement decisions, also read `docs/superpowers/specs/2026-04-11-workdatahubpro-refactor-program.md` and `docs/superpowers/specs/2026-04-11-workdatahubpro-first-wave-legacy-coverage-matrix.md`.
- `docs/superpowers/plans/` holds executable implementation plans for approved slices.
- `docs/disciplines/` holds operational rules. Use the Discipline Router below to decide which file to read.
- `config/` holds governed domain, policy, and release configuration.
- `reference/` holds replay baselines and other accepted comparison artifacts.
- `src/work_data_hub_pro/` is the application package. Keep it split by `capabilities/`, `platform/`, `governance/`, and `apps/`.
- `tests/` mirrors the runtime boundaries with contract, integration, replay, and performance coverage.
- `.serena/` is local Serena state. It is not the repository source of truth and should not be treated as project documentation.
- `.worktrees/` is the project-local git worktree root. Keep it ignored and out of normal repository changes.
- `.gitignore` carries local exclusions such as `.serena/` and `.worktrees/`; do not rely on ignored local state as committed project artifacts.

When project rules conflict, use this priority order:

1. active architecture blueprint in `docs/superpowers/specs/`
2. discipline documents in `docs/disciplines/`
3. local tool state such as `.serena/`

## Discipline Router
Read only the discipline docs that match the current action. Do not bulk-read
all files under `docs/disciplines/`.

- branch creation, commits, merges, PRs, worktrees, branch cleanup:
  `docs/disciplines/git-workflow.md`
- implementation work in general:
  `docs/disciplines/implementation-execution.md`
- toolchain, `uv`, lockfiles, command style, environment noise:
  `docs/disciplines/implementation-toolchain.md`
- slice ordering, contract-first rollout, plan/runbook tracking:
  `docs/disciplines/implementation-slice-workflow.md`
- completion claims, validation evidence, full-suite verification:
  `docs/disciplines/implementation-verification.md`
- Serena-assisted source-code precision work only:
  `docs/disciplines/serena-mcp-usage.md`

If one discipline doc points to a narrower child document, read only that child
document next instead of continuing to load unrelated discipline files.

## Build, Test, and Development Commands
Use `uv` for dependency management, environment management, and command execution.

- `uv sync --dev` creates or refreshes the local development environment.
- `uv run pytest -v` runs the full automated test suite.
- `uv run pytest tests/<path> -v` runs a targeted contract, integration, replay, or performance test.
- `uv run python -m work_data_hub_pro.apps.etl_cli.main replay-annuity-performance <workbook> <period>` runs the replay CLI for the first validation slice.
- `git status -sb` checks working tree state.
- `git remote -v` confirms remote repository configuration.
- `Get-ChildItem -Recurse docs` reviews the documentation tree.
- `Get-Content docs/superpowers/specs/2026-04-11-workdatahubpro-rebuild-architecture-draft.md` reads the active architecture baseline.

## Coding Style & Naming Conventions
Use clear Markdown with short sections, direct wording, and flat bullet lists. Keep commit messages, PR text, and documentation in English.

For future code and folders:

- preserve capability-first boundaries; do not reintroduce stage-first or hook-centric structure
- keep business logic out of orchestration adapters and generic helpers
- prefer explicit, descriptive names such as `platform/publication` or `governance/compatibility`
- preserve progressive disclosure: keep `AGENTS.md` compact and place detailed reusable rules in `docs/disciplines/`

## Testing Guidelines
For documentation changes:

- verify paths, filenames, and cross-references
- confirm new guidance matches the active architecture blueprint
- confirm `AGENTS.md`, discipline docs, and the blueprint do not contradict each other
- confirm local-tool guidance does not override committed repository guidance
- document expected validation evidence when proposing new code structure or workflow changes

For code changes:

- include tests with the same boundary as the change
- run the narrowest relevant test while developing
- run `uv run pytest -v` before claiming a slice or merge candidate is complete
- keep replay baselines and runbooks aligned with the executed validation path

## Commit & Pull Request Guidelines
Follow the documented standard in `docs/disciplines/git-workflow.md`.

Use commit subjects in the form `<type>(<scope>): <subject>`, for example `docs(docs.discipline): add contributor guide`. Keep branches short-lived and boundary-specific, such as `docs/contributor-guide` or `platform/publication/<topic>`.

Do not commit `.serena/` unless the repository policy is explicitly changed later.

PRs should state:

- `Boundary`
- `Change Type`
- `Why`
- `Validation`
- `Compatibility Impact`

Do not merge changes that cross capability, platform, and governance boundaries without an explicit slice-closure reason.

## Project-Specific Guidlines

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

### 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.