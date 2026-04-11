# Serena MCP Usage Discipline

This document defines how Serena MCP should be used in `WorkDataHubPro`.
It is aligned with:

- `docs/superpowers/specs/2026-04-11-workdatahubpro-rebuild-architecture-draft.md`
- `docs/disciplines/git-workflow.md`

## 1. Purpose

Serena is the preferred semantic exploration and symbol-aware editing tool for
this project when the task involves source code structure, code relationships,
or targeted code changes.

Serena is not a license to explore the repository indiscriminately. Its purpose
in this project is to improve precision, reduce blind whole-file reading, and
keep changes aligned with the capability-first rebuild architecture.

## 2. Mandatory Startup Sequence

At the beginning of work in this repository, follow this sequence:

1. `activate_project`
2. `check_onboarding_performed`
3. If onboarding is missing, complete `onboarding` and write the required memories
4. Read Serena's manual via `initial_instructions` if it has not already been read in the session

This is the minimum project-safe Serena setup. Do not skip it.

## 3. When Serena Must Be Preferred

Prefer Serena over generic file scanning when the task involves:

- locating code by symbol, not by raw text
- understanding a module's top-level structure before editing it
- tracing symbol references before renaming or refactoring
- making targeted edits to a class, function, or method body
- understanding how a change propagates across code references
- exploring a future `src/work_data_hub_pro/` codebase without reading entire files blindly

Preferred Serena tools by intent:

- structure overview: `get_symbols_overview`
- exact or narrowed symbol lookup: `find_symbol`
- reference tracing: `find_referencing_symbols`
- bounded code/text search when symbol names are uncertain: `search_for_pattern`
- project-local file discovery: `find_file`, `list_dir`
- stable project context: `read_memory`, `write_memory`

## 4. When Serena Should Not Be Forced

Do not force Serena into tasks where it is a bad fit.

Use normal repository tools instead when the task is primarily:

- editing markdown discipline/spec documents
- reading or updating non-code assets
- performing git operations
- running shell commands
- making tiny line-level edits where symbol boundaries are irrelevant
- inspecting files that are not yet part of an implemented source tree

Current project note:

- `WorkDataHubPro` is still in a bootstrap stage and currently contains mainly documentation.
- In the current state, Serena is most valuable for project activation, memory management, and future source exploration.
- Do not fabricate code exploration rituals when the repository only contains documents.

## 5. Blueprint-Aligned Usage Rules

Serena usage in this repository must reinforce the rebuild blueprint, not work against it.

### 5.1 Boundary-First Rule

Before using Serena to explore or edit code, identify the change boundary:

- `capabilities/`
- `platform/`
- `governance/`
- `apps/`
- explicit validation slice

Serena exploration should be restricted to the smallest relevant boundary first.
Do not start with codebase-wide searches unless the task genuinely crosses boundaries.

### 5.2 Capability-First Rule

When code exists, Serena-assisted edits must preserve these architectural rules:

- business semantics belong in capability modules
- orchestration adapters must not become the owner of business rules
- `platform/` owns technical runtime concerns, not business meaning
- `governance/` owns control-plane decisions, not hot-path field derivation
- `publication` remains an explicit platform boundary, not a hidden side effect

If Serena exploration reveals a change would cross these boundaries, the task
must be reframed as an explicit slice-closure task or split into multiple changes.

### 5.3 Explainability Rule

For changes related to tracing, lineage, compatibility, publication, identity
resolution, or projection behavior, Serena should be used to inspect the exact
symbols and references involved before editing.

This is required because the rebuild blueprint treats explainability and
boundary clarity as first-class constraints, not afterthoughts.

### 5.4 Slice Rule

For first-slice work such as `annuity_performance`, Serena usage should follow
the slice chain defined by the blueprint:

`source_intake -> fact_processing -> identity_resolution -> reference_derivation -> publication -> projections -> runtime evidence -> governance adjudication`

Do not use Serena to patch one node in isolation if the task actually affects
the chain contract across multiple stages.

## 6. Efficient Exploration Rules

Serena should be used economically.

- Prefer `get_symbols_overview` before reading symbol bodies
- Prefer `find_symbol` before reading full files
- Use `find_referencing_symbols` before renames or compatibility-sensitive edits
- Use `search_for_pattern` only when symbol identity is unclear
- Limit searches with `relative_path` whenever the boundary is known
- Avoid full-file reads of source files unless necessary

If the needed information has already been obtained from a full-file read, do
not redundantly repeat the same exploration with Serena symbol tools.

## 7. Editing Rules

When editing source code with Serena:

- use symbol-level edits when changing an entire function, class, or method
- use line-based editing tools when only a few lines inside a larger symbol need to change
- after changing a symbol, ensure backward compatibility or update all affected references
- use Serena reference tracing before renames or signature changes

When editing non-code files such as architecture docs, discipline docs, or
specifications, Serena is optional and usually not the primary editing tool.

## 8. Memory Rules

Serena memories should contain stable, reusable project knowledge.

Good memory content:

- project purpose
- architecture invariants
- stable workflow rules
- important commands
- completion expectations

Do not store transient noise such as:

- one-off scratch conclusions
- temporary task state
- speculative design branches that are not accepted
- duplicated copies of active documents

If a discipline document becomes the accepted source of truth, memory may
contain a short pointer to it, not a competing parallel version.

## 9. Review And Verification Rules

Before claiming a Serena-assisted task is complete:

- confirm the explored boundary matches the actual change scope
- confirm the change does not reintroduce stage-first or hook-centric structure
- confirm references were updated if symbol contracts changed
- confirm the supporting blueprint or discipline document still matches the change

For docs-only Serena work, verification means consistency with the active
blueprint and existing discipline documents.

## 10. Anti-Patterns

The following Serena usage is prohibited in this project:

- using Serena as a justification for unfocused repository-wide exploration
- reading whole source trees when a bounded symbol query would be enough
- editing across `capabilities/`, `platform/`, and `governance/` without an explicit slice reason
- letting Serena-assisted edits hide publication, tracing, or compatibility behavior inside generic helpers
- writing volatile task chatter into Serena memories
- treating Serena memory as a replacement for committed project documentation

## 11. Current Practical Guidance

Given the current repository state:

- use Serena to activate the project and maintain project memories
- use Serena memories to preserve blueprint-level context
- use normal document editing tools for `docs/disciplines/` and blueprint docs
- expand Serena-heavy workflows after `src/work_data_hub_pro/` becomes real code instead of only planned structure

Serena is a precision tool. In `WorkDataHubPro`, precision means serving the
capability-first rebuild, preserving explainability, and avoiding another
generation of hidden architectural coupling.
