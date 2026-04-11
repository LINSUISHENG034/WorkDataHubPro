# Repository Guidelines

## Project Structure & Module Organization
`WorkDataHubPro` is currently a bootstrap repository. The committed source of
truth lives under `docs/`.

- `docs/superpowers/specs/` holds the active architecture blueprint. Start with `docs/superpowers/specs/2026-04-11-workdatahubpro-rebuild-architecture-draft.md`.
- `docs/disciplines/` contains operating rules such as `git-workflow.md` and `serena-mcp-usage.md`.
- `.serena/` is local Serena state. It is not the repository source of truth and should not be treated as project documentation.
- `.gitignore` currently ignores `.serena/`; do not rely on Serena memory files as committed project artifacts.

There is no application `src/` tree yet. When code is introduced, keep it capability-first and aligned to the blueprint: `capabilities/`, `platform/`, `governance/`, and `apps/`.

When project rules conflict, use this priority order:

1. active architecture blueprint in `docs/superpowers/specs/`
2. discipline documents in `docs/disciplines/`
3. local tool state such as `.serena/`

## Build, Test, and Development Commands
No build, lint, or automated test commands are defined yet. Current validation is document accuracy and alignment.

- `git status -sb` checks working tree state.
- `git remote -v` confirms remote repository configuration.
- `Get-ChildItem -Recurse docs` reviews the documentation tree.
- `Get-Content docs/disciplines/git-workflow.md` reads contribution rules.
- `Get-Content docs/disciplines/serena-mcp-usage.md` reads Serena usage rules.
- `Get-Content docs/superpowers/specs/2026-04-11-workdatahubpro-rebuild-architecture-draft.md` reads the active architecture baseline.

## Coding Style & Naming Conventions
Use clear Markdown with short sections, direct wording, and flat bullet lists. Keep commit messages, PR text, and documentation in English.

For future code and folders:

- preserve capability-first boundaries; do not reintroduce stage-first or hook-centric structure
- keep business logic out of orchestration adapters and generic helpers
- prefer explicit, descriptive names such as `platform/publication` or `governance/compatibility`

## Testing Guidelines
Because the repository is documentation-heavy, testing currently means consistency checks:

- verify paths, filenames, and cross-references
- confirm new guidance matches the active architecture blueprint
- confirm `AGENTS.md`, discipline docs, and the blueprint do not contradict each other
- confirm local-tool guidance does not override committed repository guidance
- document expected validation evidence when proposing new code structure

If runnable code is added, include tests with the same boundary as the change and document the command used to validate it.

## Commit & Pull Request Guidelines
There is no existing commit history yet, so follow the documented standard in `docs/disciplines/git-workflow.md`.

Use commit subjects in the form `<type>(<scope>): <subject>`, for example `docs(docs.discipline): add contributor guide`. Keep branches short-lived and boundary-specific, such as `docs/contributor-guide` or `platform/publication/<topic>`.

Do not commit `.serena/` unless the repository policy is explicitly changed later.

PRs should state:

- `Boundary`
- `Change Type`
- `Why`
- `Validation`
- `Compatibility Impact`

Do not merge changes that cross capability, platform, and governance boundaries without an explicit slice-closure reason.
