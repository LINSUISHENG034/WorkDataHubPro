# Git Workflow

## Read This When

- creating a branch or choosing a branch name
- setting up or cleaning up a worktree
- committing, merging, rebasing, or preparing a PR
- deciding how to close implementation work after verification

## Do Not Read This When

- the task is only about implementation ordering, toolchain, or runtime validation
- the task is docs-only and does not involve git workflow decisions

## Hard Gates

- do not start implementation on `main`
- do not keep accumulating unrelated work in one dirty worktree once it is clear the work belongs on its own topic branch
- do not merge cross-boundary work without a named slice-closure reason
- verify the merged result before deleting feature branches or worktrees
- do not create topic branches or worktrees by reflex for docs-only work; choose the path after classifying the task

This workflow is for the `WorkDataHubPro` rebuild.
It is aligned with the capability-first rebuild blueprint in
`docs/superpowers/specs/2026-04-11-workdatahubpro-rebuild-architecture-draft.md`.

## 1. Purpose

The git workflow must protect the rebuild from the same failure modes that made
the legacy system hard to reason about:

- hidden cross-module coupling
- oversized branches that mix business semantics, platform concerns, and control-plane changes
- config-only changes that silently alter transformation semantics
- parity or replay differences merged without explicit adjudication
- orchestration- or hook-driven behavior slipping back into the architectural center

Git history should make it easy to answer:

- which architectural boundary changed
- why the change was made
- what validation proved it
- whether the change altered business semantics, config behavior, or compatibility posture

## 2. Core Rules

- `main` is the only long-lived branch.
- Do not use a permanent `develop` branch.
- Each branch should map to one architectural boundary or one explicit slice-closure task.
- The repository root worktree should remain the clean integration worktree for `main`, not the default place for parallel topic work.
- Business capability changes, platform runtime changes, and governance/control-plane changes should not be mixed casually.
- Config changes that alter semantics are release-affecting changes, not harmless housekeeping.
- Replay or parity differences must be explained before merge, not after merge.
- All commit messages must be written in English.
- Spikes are allowed, but spike branches do not merge to `main` without cleanup or a replacement implementation branch.
- If branch isolation is discovered late, isolate the work first and only then continue implementation, merge preparation, or cleanup.

## 3. Branch Strategy

Before creating a branch or worktree, first classify the task:

- `docs-only fast path`
- `isolated implementation path`

Use the fast path only when all of the following are true:

- the change is limited to documentation
- no files under `src/`, `tests/`, or `config/` will change
- the change does not alter runtime behavior
- the work does not need parallel isolation from other ongoing implementation

If any of those conditions stop being true during execution, immediately leave the
docs-only path and switch to the isolated implementation path.

### 3.0 Docs-Only Fast Path

Docs-only changes may be committed directly on `main`.

For docs-only work:

- do not create a topic branch by default
- do not create a worktree by default
- keep the change narrow and documentation-scoped
- validate links, filenames, and document alignment before commit

This path exists to avoid unnecessary branch and worktree churn for small,
bounded documentation updates.

If the task later expands into code, tests, config, verification assets, or any
runtime-affecting behavior, stop using the docs-only path and move to an
isolated branch/worktree before continuing.

### 3.1 Long-Lived Branches

- `main` - protected integration branch; always expected to be coherent and reviewable

No `develop`, `release`, or other permanent integration branches should be introduced unless the rebuild operating model changes materially.

### 3.2 Short-Lived Branches

Use short-lived topic branches merged into `main` through pull requests.

Topic branches are the default for implementation work, but not for docs-only
fast-path work.

Recommended branch prefixes:

- `cap/source-intake/<topic>`
- `cap/fact-processing/<domain>-<topic>`
- `cap/identity-resolution/<topic>`
- `cap/reference-derivation/<topic>`
- `cap/projections/<topic>`
- `platform/contracts/<topic>`
- `platform/tracing/<topic>`
- `platform/lineage/<topic>`
- `platform/publication/<topic>`
- `platform/storage/<topic>`
- `platform/execution/<topic>`
- `governance/compatibility/<topic>`
- `governance/config-release/<topic>`
- `governance/shadow-run/<topic>`
- `app/etl-cli/<topic>`
- `app/orchestration/<topic>`
- `docs/<topic>`
- `chore/<topic>`
- `spike/<topic>`

### 3.3 Slice-Closure Branches

Cross-boundary branches are allowed only when the goal is to close an explicit
validation slice end to end.

Use:

- `slice/annuity-performance-closure`
- `slice/<slice-name>-closure`

Rules for slice branches:

- must name the slice explicitly
- must link the governing blueprint/spec/ADR
- must state which boundaries are intentionally crossed
- must close back down after merge; do not keep slice branches alive as shadow integration branches

### 3.4 Worktree Strategy

Use linked git worktrees under `.worktrees/` as the default isolation model for
non-trivial topic work.

Default expectations:

- keep the repository root worktree on `main` as the clean integration and merge context
- create a linked worktree for topic branches that are expected to last more than one commit, more than one session, or run in parallel with other work
- treat each worktree as the owner of its own untracked files, generated artifacts, and temporary state
- prefer validating and merging from a clean `main` worktree or an explicit temporary merge worktree when the original topic worktree contains unrelated local state

Do not use worktrees for docs-only fast-path work unless the user explicitly
asks for isolation or there is a concrete parallel-work reason.

Recommended examples:

- `.worktrees/docs-wiki-governance-audit-sync`
- `.worktrees/cap-reference-derivation-plan-code-fix`
- `.worktrees/slice-annuity-income-closure`

Worktrees are preferred because they prevent repeated `git switch` cycles from
mixing unrelated untracked files and unstaged edits in one physical directory.

### 3.5 Avoiding Unnecessary Isolation

Do not create a branch or worktree unless the task actually needs isolation.

Examples of unnecessary isolation:

- creating a docs branch for a bounded wiki-only update that can safely commit on `main`
- creating a worktree for a small docs-only sync with no runtime changes
- creating a branch, then deciding to commit the same docs-only change on `main`

If a branch or worktree was created but the task is now clearly docs-only and is
being committed through the fast path:

- stop using the extra branch/worktree
- commit the docs-only change once through the chosen path
- clean up the unused branch/worktree after confirming it contains no unique commits

## 4. Branch Sizing Rules

- One branch should normally touch one of: `capabilities/`, `platform/`, `governance/`, or `apps/`.
- A `docs/` branch may touch documentation across those areas if it does not change runtime behavior.
- If a branch changes both code and config, the PR must state whether config is behavior-preserving or semantics-changing.
- If a branch changes both runtime behavior and compatibility adjudication artifacts, the PR must explain why the pairing is necessary.
- If the change cannot be explained as one boundary or one slice-closure task, the branch is too large.

## 5. Commit Message Standard

Never mention Claude, Codex, AI authorship, or similar tooling in commit messages.
All commit messages must be written in English, including the subject, body,
validation lines, and footer/reference labels.

Format:

```text
<type>(<scope>): <subject>

<why>

Validation:
- <command or artifact>
- <command or artifact>

Refs:
- Spec: <path or id>
- ADR: <path or id>
- Compat: <path or case id>
```

Allowed types:

- `feat`
- `fix`
- `refactor`
- `docs`
- `test`
- `chore`
- `perf`
- `build`
- `ci`
- `revert`

Recommended scopes:

- `source-intake`
- `fact-processing.annuity-performance`
- `fact-processing.annual-award`
- `identity-resolution`
- `reference-derivation`
- `projections`
- `platform.contracts`
- `platform.tracing`
- `platform.lineage`
- `platform.publication`
- `platform.storage`
- `platform.execution`
- `governance.compatibility`
- `governance.config-release`
- `apps.etl-cli`
- `apps.orchestration`
- `docs.architecture`
- `docs.discipline`

Example:

```text
feat(platform.publication): introduce explicit publication plan contract

Replace hidden loader assumptions with an explicit publication boundary so
fact, derivation, and projection writes can be validated independently.

Validation:
- tests/contracts/test_publication_contracts.py
- tests/integration/test_annuity_performance_slice.py

Refs:
- Spec: docs/superpowers/specs/2026-04-11-workdatahubpro-rebuild-architecture-draft.md
```

## 6. Pull Request Rules

Every PR should answer these questions explicitly:

1. Which architectural boundary is changing?
2. Is this a behavior change, a structure-only change, a config release change, or a compatibility/adjudication change?
3. What validation proves the change?
4. Does this change alter legacy parity, replay outputs, or adjudication posture?

PR description should contain:

- `Boundary:` one of capability, platform, governance, apps, docs, or explicit slice
- `Change Type:` behavior, structure, config release, compatibility, docs
- `Why:` the architectural or business reason
- `Validation:` commands, fixtures, replay artifacts, or document checks
- `Compatibility Impact:` none, expected diff, or adjudication required

## 7. Required Validation By Change Class

| Change Class | Minimum Validation Before Merge |
|------|------|
| capability rule change | unit/integration coverage plus golden or replay evidence for the affected slice |
| identity resolution change | fallback-path tests plus explicit evidence that cache, provider, and temp-id behavior remain explainable |
| reference derivation change | derivation tests plus publication-path validation for affected targets |
| projection/status change | cross-domain integration coverage and snapshot assertions |
| platform contract or publication change | contract tests plus one end-to-end slice path |
| governance or compatibility change | replay diff artifact plus explicit human-readable adjudication rationale |
| config-only change with no semantic change | config validation plus proof that runtime outputs are unchanged |
| config change with semantic impact | treat as release-affecting; pair with rule/version update and validation evidence |
| docs-only change | link/path consistency and document alignment with active blueprint/ADR |

## 7.1 Path Selection Checklist

Before commit, confirm which path applies:

### `docs-only fast path`

- current work is documentation-only
- no runtime/config/test behavior is being changed
- commit may happen directly on `main`
- no extra topic branch or worktree should remain active without need

### `isolated implementation path`

- code, tests, config, verification assets, or runtime behavior changed or may change
- commit should not happen directly on `main`
- use a topic branch, and use a worktree when the task is non-trivial or parallel

## 8. Review Routing

Review should follow the architectural boundary, not just file ownership.

- capability PRs require review from the owner of the affected business area
- `platform/*` PRs require platform/runtime review
- `governance/*` PRs require governance/control-plane review
- projection PRs that consume cross-domain facts require reviewers who understand those upstream facts
- slice-closure PRs require review across every intentionally crossed boundary

A PR that touches `capabilities/`, `platform/`, and `governance/` without a
clear slice-closure reason should be split before review.

## 9. Merge Policy

- Rebase onto latest `main` before merge when needed to keep diffs understandable.
- Squash merge is the default for short-lived topic branches.
- Rebase merge is allowed when preserving a small sequence of intentionally structured commits adds architectural clarity.
- Prefer merging from a clean checkout or temporary clean worktree when the original workspace contains unrelated local state.
- Delete the branch after merge.
- Do not merge spike branches directly to `main`.

### 9.1 Dirty-Worktree Merge Guard

Do not perform a topic merge in a `main` worktree that already contains
unrelated local changes.

Allowed responses:

- protect the unrelated local state first, then merge
- create a temporary clean merge worktree from the current `main` HEAD and perform the merge there

Not allowed:

- merging in a dirty `main` worktree and hoping unrelated local state will stay out of the result
- treating repeated `stash` / `unstash` cycles as the normal long-term substitute for worktree isolation

### 9.2 Recovery When Branch Isolation Starts Late

If you realize only after starting work that the change should have been in its
own branch or worktree, stop expanding the mixed state and recover deliberately.

#### Case A: Uncommitted Changes Only

Use this when the work exists only as unstaged, staged, or untracked files.

1. stop adding more edits until the scope is understood
2. decide whether the current worktree state is one topic or a mix of topics
3. if it is one topic, create the topic branch, create a linked worktree for it, and move the working state there using a protected transfer method such as a verified stash restore or an intentional temporary commit
4. if it is mixed, split the state first; do not move the entire dirty worktree wholesale into one branch

Rule:

- a dirty `main` worktree is a staging problem to solve, not a valid merge context

#### Case B: Committed Locally But Not Pushed

Use this when the relevant work already exists as local commits but has not been
shared.

1. create or update a topic branch that points at the relevant local commits before more cleanup
2. decide whether those commits are allowed to remain on `main`
3. if `main` can be rewritten safely because the commits are local-only and not depended on elsewhere, clean it deliberately
4. if rewriting `main` is not clearly safe, create a clean topic branch from the correct base and move the topic commits there with `cherry-pick`

Rule:

- preserve recoverability first; only rewrite `main` when the safety conditions are explicit

#### Case C: Already Mixed With Other Commits

Use this when topic commits and unrelated commits are already interleaved.

1. identify the exact commit set or file set that belongs to the target topic
2. create a clean topic branch from the proper base commit
3. move only the relevant work by `cherry-pick`, selective re-apply, or another explicit extraction path
4. leave unrelated commits on their own path; do not paper over mixed history by merging directly from dirty `main`

Rule:

- once unrelated history is mixed in, extraction is safer than pretending the current `main` state is reviewable as one change

## 10. Tags And Baselines

Use tags for milestones that matter to the rebuild, not for every merge.

Recommended tags:

- `baseline/<date>-<slice>` for accepted replay or golden baselines
- `config-release/<release-id>` for approved config releases
- `milestone/<name>` for major architecture completion points

Reference artifacts should live alongside the code:

- `reference/golden_samples/`
- `reference/historical_replays/`
- `reference/compatibility_cases/`

Git tags should point to the commit that produced the accepted artifact set.

## 11. Anti-Patterns

Avoid these patterns:

- reintroducing `develop` as a permanent dumping ground
- using one physical worktree as the default workspace for multiple parallel topics
- one PR that touches capabilities, platform publication, projections, and governance without a named slice-closure goal
- config-only commits that actually change semantics but are described as cleanup
- merging replay differences without a compatibility decision
- placing business logic into CLI, Dagster wiring, hooks, or generic helpers
- continuing implementation in a mixed or dirty `main` worktree after you already know the work should be isolated
- allowing `spike/*` branches to become unofficial long-lived feature branches

## 12. Minimum Ready-To-Merge Checklist

- branch name matches the actual architectural boundary or slice
- topic work happened in an isolated branch context, and the merge is being performed from a clean `main` worktree or explicit clean merge worktree
- commit messages identify the real scope
- PR explains boundary, change type, validation, and compatibility impact
- validation evidence exists for the touched change class
- no hidden semantics are being smuggled through config-only edits
- no orchestration adapter is becoming the owner of business behavior

If any of the above is false, the branch is not ready to merge.
