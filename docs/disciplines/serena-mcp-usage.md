# Serena MCP Usage Discipline

## Read This When

- the task involves Serena activation or onboarding
- the task involves Serena local deployment, client wiring, or upgrade procedure
- the task involves symbol-aware source exploration or semantic source edits
- the task involves reference tracing, rename safety, or bounded source inspection

## Do Not Read This When

- the task is docs-only and unrelated to Serena client setup or source-code symbol work
- the task is primarily about git workflow
- the task is a simple shell or asset operation with no code-structure question

## Hard Gates

- complete the Serena startup sequence before Serena-assisted code work
- restrict Serena exploration to the smallest relevant architectural boundary first
- do not bulk-read source files when a bounded Serena query is sufficient

This document defines how Serena MCP should be used in `WorkDataHubPro`.
It is aligned with:

- `docs/superpowers/specs/2026-04-11-workdatahubpro-rebuild-architecture-draft.md`
- `docs/disciplines/git-workflow.md`

## 1. Purpose

Serena is an auxiliary MCP tool for source-code precision in this project.
It is useful when the current task involves source code structure, code
relationships, or targeted code changes.

Serena is not:

- a task category
- a workflow phase that every task must go through
- a replacement for implementation, verification, or git workflow disciplines

Its purpose in this project is to improve precision, reduce blind whole-file
reading, and keep source edits aligned with the capability-first rebuild
architecture.

## 2. Value Model

Serena adds value when it helps answer one of these questions more cheaply than
raw file reading:

- which symbol actually owns this behavior
- which references will be affected by this change
- what is the smallest code boundary I need to inspect or edit

If the task does not involve one of those precision problems, Serena usually
should not be loaded.

## 3. Startup Sequence For Serena-Assisted Code Work

Only when the current task actually requires Serena-assisted code work, follow
this sequence:

1. `activate_project`
2. `check_onboarding_performed`
3. If onboarding is missing, complete `onboarding` and write the required memories
4. Read Serena's manual via `initial_instructions` if it has not already been read in the session

This is the minimum project-safe Serena setup. Do not skip it once Serena is in
use, but do not force it onto non-Serena tasks.

### 3.1 Current Local Deployment Baseline

The current Windows workstation baseline uses a locally installed Serena tool,
not a per-session `uvx --from git+https://github.com/oraios/serena ...`
bootstrap.

- install Serena as a `uv tool` package: `serena-agent`
- executable shims should resolve from `%USERPROFILE%\\.local\\bin\\`
- the current command entrypoints are `serena.exe` and `serena-hooks.exe`
- the `uv tool` environment lives under `%APPDATA%\\uv\\tools\\serena-agent\\`
- the global Serena configuration lives in `%USERPROFILE%\\.serena\\serena_config.yml`
- prefer the local `serena` command for client wiring so Codex and Claude Code
  use the same installed Serena version

Current client wiring for subagent-heavy Codex work:

- start one shared Serena MCP service for this project:
  `serena start-mcp-server --transport streamable-http --port 9121 --project E:\\Projects\\WorkDataHubPro --context codex --open-web-dashboard false`
- Codex user config: `%USERPROFILE%\\.codex\\config.toml`
- Codex server URL: `http://127.0.0.1:9121/mcp`
- Claude Code user MCP config: `%USERPROFILE%\\.claude.json`
- Claude Code may keep its own stdio registration:
  `serena start-mcp-server --context claude-code --project-from-cwd`
- Claude Code Serena hooks remain separate from MCP registration and live in
  `%USERPROFILE%\\.claude\\settings.json`

### 3.2 Shared-Server Rules For Codex

- use `streamable-http` when the main Codex agent and its subagents must share
  one Serena process and one set of language servers
- keep the shared service bound to `127.0.0.1`
- run one Serena instance per active project; do not share one stateful Serena
  service across unrelated projects
- do not use Codex stdio wiring for Serena when subagent fan-out matters;
  stdio starts a separate Serena process per client
- disable dashboard auto-open for the shared service to avoid repeated browser
  launches from restarts

### 3.3 Codex Client Limitation

- Codex MCP registration is exclusive: each `mcp_servers.<name>` entry is
  either a stdio `command`/`args` server or a URL-based server
- Codex does not provide a native fallback that means "connect to this URL, but
  if it is down, run a local startup command and then retry the same URL"
- if on-demand startup is required, manage the shared Serena process outside
  Codex itself with workstation-local automation such as Windows Task
  Scheduler, NSSM, or a user-launched bootstrap script
- for Windows-local supervision, prefer absolute paths or
  `%USERPROFILE%`-derived paths for both the bootstrap script and
  `serena.exe`; do not assume background launchers inherit
  `%USERPROFILE%\\.local\\bin` on `PATH`
- supervise the shared service by checking whether `127.0.0.1:9121` is
  actually listening, not by assuming the first launcher PID returned from
  `Start-Process` is the long-lived Serena server process
- do not document local supervisor state as committed repository source of
  truth; only document the supported wiring pattern and required commands

### 3.4 Update And Repair Flow

For this workstation, Serena updates should happen through `uv tool`, not by
editing the client configs.

Standard upgrade:

- `uv tool upgrade serena-agent`

Required post-upgrade checks:

- `uv tool list`
- `codex mcp get serena`
- `claude mcp get serena`
- `Test-NetConnection 127.0.0.1 -Port 9121`

If the local tool installation is broken or the entrypoints drift, reinstall the
same tool package and preserve the current local install policy:

- `uv tool install --reinstall --prerelease allow --index-url https://mirrors.aliyun.com/pypi/simple serena-agent`

After upgrade or reinstall:

- restart the shared Serena HTTP service if the installed Serena version changed
- restart active Codex and Claude Code sessions
- confirm the local `serena` command still resolves before troubleshooting MCP
  client config
- confirm Codex still points at `http://127.0.0.1:9121/mcp`
- only fall back to `uvx`-based client bootstrapping if the local tool install
  strategy is intentionally abandoned

## 4. When Serena Adds Value

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

## 5. When Serena Should Not Be Used By Default

Do not force Serena into tasks where it is a bad fit.

Use normal repository tools instead when the task is primarily:

- editing markdown discipline/spec documents
- reading or updating non-code assets
- performing git operations
- running shell commands
- making tiny line-level edits where symbol boundaries are irrelevant
- inspecting files that are not yet part of an implemented source tree

Current project note:

- `WorkDataHubPro` now has an executable first slice under `src/work_data_hub_pro/`.
- Serena is useful for symbol-aware work inside that source tree, but it is still not the default tool for markdown discipline documents or git-only tasks.
- Do not fabricate Serena-heavy rituals for tasks that are fundamentally document editing or repository administration.

## 6. Blueprint-Aligned Usage Rules

Serena usage in this repository must reinforce the rebuild blueprint, not work against it.

### 6.1 Boundary-First Rule

Before using Serena to explore or edit code, identify the change boundary:

- `capabilities/`
- `platform/`
- `governance/`
- `apps/`
- explicit validation slice

Serena exploration should be restricted to the smallest relevant boundary first.
Do not start with codebase-wide searches unless the task genuinely crosses boundaries.

### 6.2 Capability-First Rule

When code exists, Serena-assisted edits must preserve these architectural rules:

- business semantics belong in capability modules
- orchestration adapters must not become the owner of business rules
- `platform/` owns technical runtime concerns, not business meaning
- `governance/` owns control-plane decisions, not hot-path field derivation
- `publication` remains an explicit platform boundary, not a hidden side effect

If Serena exploration reveals a change would cross these boundaries, the task
must be reframed as an explicit slice-closure task or split into multiple changes.

### 6.3 Explainability Rule

For changes related to tracing, lineage, compatibility, publication, identity
resolution, or projection behavior, Serena should be used to inspect the exact
symbols and references involved before editing.

This is required because the rebuild blueprint treats explainability and
boundary clarity as first-class constraints, not afterthoughts.

### 6.4 Slice Rule

For first-slice work such as `annuity_performance`, Serena usage should follow
the slice chain defined by the blueprint:

`source_intake -> fact_processing -> identity_resolution -> reference_derivation -> publication -> projections -> runtime evidence -> governance adjudication`

Do not use Serena to patch one node in isolation if the task actually affects
the chain contract across multiple stages.

## 7. Efficient Exploration Rules

Serena should be used economically.

- Prefer `get_symbols_overview` before reading symbol bodies
- Prefer `find_symbol` before reading full files
- Use `find_referencing_symbols` before renames or compatibility-sensitive edits
- Use `search_for_pattern` only when symbol identity is unclear
- Limit searches with `relative_path` whenever the boundary is known
- Avoid full-file reads of source files unless necessary

If the needed information has already been obtained from a full-file read, do
not redundantly repeat the same exploration with Serena symbol tools.

## 8. Editing Rules

When editing source code with Serena:

- use symbol-level edits when changing an entire function, class, or method
- use line-based editing tools when only a few lines inside a larger symbol need to change
- after changing a symbol, ensure backward compatibility or update all affected references
- use Serena reference tracing before renames or signature changes

When editing non-code files such as architecture docs, discipline docs, or
specifications, Serena is optional and usually not the primary editing tool.

## 9. Memory Rules

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

## 10. Review And Verification Rules

Before claiming a Serena-assisted task is complete:

- confirm the explored boundary matches the actual change scope
- confirm the change does not reintroduce stage-first or hook-centric structure
- confirm references were updated if symbol contracts changed
- confirm the supporting blueprint or discipline document still matches the change

For docs-only Serena work, verification means consistency with the active
blueprint and existing discipline documents.

## 11. Anti-Patterns

The following Serena usage is prohibited in this project:

- treating Serena as a task flow instead of an auxiliary tool
- using Serena as a justification for unfocused repository-wide exploration
- reading whole source trees when a bounded symbol query would be enough
- editing across `capabilities/`, `platform/`, and `governance/` without an explicit slice reason
- letting Serena-assisted edits hide publication, tracing, or compatibility behavior inside generic helpers
- expecting a URL-based Codex MCP entry to auto-start Serena when no external
  process manager is in place
- writing volatile task chatter into Serena memories
- treating Serena memory as a replacement for committed project documentation

## 12. Current Practical Guidance

Given the current repository state:

- use Serena only when source-code precision is needed
- use Serena to activate the project and maintain project memories when Serena is actually in play
- use Serena memories to preserve blueprint-level context, not task-by-task scratch state
- for Codex sessions that dispatch subagents, prefer one project-scoped
  `streamable-http` Serena service plus URL-based registration
- do not assume Codex will auto-maintain a shared URL-based Serena service
  without separate workstation-local process supervision
- use normal document editing tools for `docs/disciplines/` and blueprint docs

Serena is a precision tool. In `WorkDataHubPro`, precision means serving the
capability-first rebuild, preserving explainability, and avoiding another
generation of hidden architectural coupling.
