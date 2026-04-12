# Governed Commit Batching Skill Design Plan

**Date:** 2026-04-12
**Status:** Draft Design Baseline
**Target Repository:** `E:\Projects\WorkDataHubPro`
**Primary Governing Input:** `docs/disciplines/git-workflow.md`

---

## 1. Goal

Define a practical skill that helps inspect the current branch worktree,
propose coherent commit batches, and execute `git add` / `git commit` under the
repository's git governance rules without overreaching into branch management,
merge orchestration, or push automation.

This design is intended to make day-to-day commit preparation safer and more
consistent while staying aligned with how work actually converges into `main`
through normal PR and merge flow.

---

## 2. Recommended Skill Shape

Recommended skill name:

- `governed-commit-batching`

Recommended trigger description direction:

- use when the current branch contains local changes that need to be reviewed,
  grouped into coherent commit batches, and committed under repository git
  governance rules
- use before committing mixed `docs`, `capabilities`, `platform`,
  `governance`, `apps`, `config`, or slice-closure changes

This should be one primary skill, not a large family of git workflow skills.

Rationale:

- the real recurring problem is commit batching on the current branch
- branch creation, merge, and PR flow already have clear repository rules in
  `docs/disciplines/git-workflow.md`
- bundling commit batching and merge orchestration into one skill would make the
  workflow too broad and too eager

Possible future split only if usage proves it necessary:

- `governed-commit-batching`
- `merge-readiness-check`

Do not split at v1.

---

## 3. Scope

The skill should cover:

- inspecting the current branch name and current worktree status
- reviewing staged and unstaged changes on the current branch
- grouping changed files into recommended commit batches
- explaining each batch by boundary, change type, and validation story
- generating full commit message drafts that match `git-workflow.md`
- executing `git add <files>` and `git commit` after explicit user confirmation
- reporting whether the branch appears merge-ready against explicit repository
  checks and what validation is still missing

The skill should not cover:

- automatic branch creation
- automatic rebasing or merging
- automatic pushing
- PR creation
- mass staging through `git add .`
- silent inclusion of unrelated local changes
- resolving every multi-branch workflow problem in one pass

---

## 4. Core Workflow

The skill should operate in three explicit phases.

### 4.1 Inspect

The skill should gather:

- current branch via `git branch --show-current`
- worktree summary via `git status -sb`
- unstaged files via `git diff --name-only`
- staged files via `git diff --cached --name-only`
- untracked files via `git ls-files --others --exclude-standard`
- targeted diffs for ambiguous files when needed

If the current worktree contains a mix of staged, unstaged, and untracked
changes, the skill should treat those as three separate preservation surfaces.
It should not assume that `git status -sb` alone is enough to safely describe
what must be protected before any staging cleanup, stash, or integration step.

If the user asks for help around merge preparation while local changes are
present, the skill should also record a restoration inventory before doing
anything else:

- staged tracked paths
- unstaged tracked paths
- untracked paths

This inventory exists so the skill can verify restoration later instead of only
assuming that `stash apply` or similar recovery steps brought everything back.

The skill should always read:

- `docs/disciplines/git-workflow.md`

Optional repository guidance should be loaded only when relevant:

- architecture or slice docs if a change appears to be a slice-closure branch
- verification docs if the user asks for merge readiness

### 4.2 Plan

The skill should classify each change batch by:

- `Boundary`
- `Change Type`
- file set
- whether the batch is behavior-changing or docs-only
- config posture: `not-applicable`, `behavior-preserving`, or
  `semantics-changing`
- minimum validation requirement
- recommended commit message

Default batching rule:

- same architectural boundary
- same change type
- same validation story
- same review story

These conditions imply one commit.

The skill should recommend separate commits when:

- boundaries differ
- change types differ
- validation evidence differs
- some changes appear unrelated to the user's stated intent
- config changes look semantics-affecting

### 4.3 Execute

The skill should only execute after explicit user confirmation.

For each approved batch, it should:

1. stage only the approved files
2. state the full intended commit message
3. run or reference the required validation command
4. commit with a governed message

After execution, it may report:

- completed commits
- remaining uncommitted changes
- whether the branch appears ready for PR / merge review

It should not merge or push automatically.

### 4.4 Merge-Readiness Assessment

If the skill reports on merge readiness, it must do so through an explicit
checklist derived from `git-workflow.md`, not intuition.

The skill should check, and render as `yes`, `no`, or `unverified`:

- branch name matches the actual architectural boundary or explicit slice
- cross-boundary work has a named slice-closure reason
- proposed commit message uses an English subject and a real repository scope
- the PR story can be stated as `Boundary`, `Change Type`, `Why`,
  `Validation`, and `Compatibility Impact`
- validation evidence exists for the touched change class
- config-only edits are classified as behavior-preserving or semantics-changing
- unresolved checks remain unresolved instead of being reported as ready

The skill may say `appears merge-ready` only when no checklist item is `no` and
none remain `unverified`.

---

## 5. Safety Boundaries

The skill should enforce these hard rules.

### 5.1 Main Branch Protection

If the current branch is `main`:

- default to analysis only
- do not commit unless the user explicitly confirms that the commit should be
  created on `main`

This follows the repository rule:

- do not start implementation on `main`

### 5.2 No Blind Staging

The skill must never:

- use `git add .`
- stage the full worktree by default
- assume all local changes belong to the same task

### 5.3 Preserve Unrelated Work

If unrelated staged or unstaged changes are present, the skill should:

- flag them explicitly
- exclude them by default from the proposed batch
- ask for confirmation before including them

### 5.4 No Merge Automation

The skill must treat convergence into `main` as a separate review and merge
concern.

It may advise on:

- likely merge strategy
- remaining validation
- whether squash merge is preferable

It must not:

- merge
- rebase
- push

It must also not claim merge readiness from partial evidence. If the repository
checklist cannot be satisfied from the available worktree state, branch
metadata, and validation evidence, the result must stay `not yet merge-ready`
or `unverified`.

### 5.5 Preserve Untracked Work Explicitly

If the workflow temporarily uses `git stash --include-untracked` or any similar
protection step, the skill must not treat `git stash show` as a complete
restoration source of truth.

It should explicitly account for:

- tracked staged changes
- tracked unstaged changes
- untracked files stored in the stash's untracked tree

Restoration is not complete until the skill compares the saved restoration
inventory against the post-restore worktree and confirms that the expected
untracked files are present again.

### 5.6 Dirty Target Branch Integration Guard

If a user asks for merge help and the target branch already has local changes,
the skill should not recommend merging directly in that dirty worktree.

Instead it should default to:

1. preserving local target-branch changes
2. creating an isolated merge-candidate worktree from the committed target-branch HEAD
3. performing and validating the merge in that isolated worktree
4. only then deciding how to reapply the saved local changes onto the updated target branch

If overlap exists between the saved local changes and the merged result, the
skill should distinguish:

- path overlap with identical content
- path overlap with real semantic conflict

Only the second case should be treated as a real merge-resolution problem.

---

## 6. Alignment With Repository Workflow

The skill should reflect the actual repository workflow rather than inventing a
 heavier git operating model.

### 6.1 How Work Should Converge

Normal convergence model:

1. work happens on a short-lived topic or slice branch
2. the skill helps prepare clean commits on that branch
3. normal PR flow merges the branch back into `main`
4. branch deletion happens after merge and verification

The skill should support step 2 only.

### 6.2 Validation Expectations

The skill should not apply one global validation rule to all commit types.

Instead it should map validation to change class:

- docs-only:
  path consistency plus cross-document alignment with blueprint / discipline
  docs
- code semantic change:
  relevant tests and evidence from the touched boundary
- config-only change with no semantic impact:
  config validation plus proof that runtime outputs are unchanged
- config change with semantic impact:
  treat as release-affecting, pair with rule/version update, and include
  validation evidence for the affected boundary
- slice-closure change:
  explicit slice verification path

The skill may recommend final merge-ready validation, but should not pretend
that every intermediate commit must run full-suite verification.

### 6.3 Avoiding Over-Engineering

The skill should not force:

- a separate branch for every small docs change
- a separate commit for every touched file
- artificial splitting when one commit already has one coherent review story

Practical rule:

- if docs are just the natural companion of the same code change, one commit is fine
- if docs are independent governance updates, separate commit is reasonable
- if the change cannot be explained as one boundary or one slice-closure reason,
  split it

---

## 7. Batch Output Format

Each proposed batch should be rendered in a compact structure like:

```text
Batch 1
Boundary: docs
Change Type: docs
Config Posture: not-applicable
Files:
- docs/superpowers/specs/...
- docs/superpowers/reviews/...

Why:
- updates governance wording for annual_loss acceptance

Validation:
- docs alignment check
- any targeted docs contract test

Commit Message:
docs(docs.discipline): align annual_loss governance assets

Clarify the governance-facing commit batching guidance so commit preparation
stays aligned with repository merge and validation rules.

Validation:
- link/path consistency check
- blueprint and discipline alignment review

Refs:
- Spec: docs/superpowers/specs/2026-04-11-workdatahubpro-rebuild-architecture-draft.md
- Spec: docs/disciplines/git-workflow.md

Merge Readiness:
- branch naming: yes
- slice-closure reason needed: no
- validation evidence complete: yes
- unresolved checks: no
```

If there are additional batches, repeat the same structure.

If no split is needed, the skill should say so explicitly instead of inventing
 multiple commits.

---

## 8. Recommended V1 Behavior

Version 1 should be deliberately narrow:

- inspect current branch
- propose batches
- commit approved batches

Do not add in v1:

- PR creation
- merge automation
- rebase helpers
- branch creation helpers
- issue tracker integration

The skill should succeed by being routinely usable, not by modeling the entire
git lifecycle.

---

## 9. Future Extension Triggers

Only consider a follow-on skill or v2 expansion if repeated usage shows one of
these persistent needs:

- merge-readiness checks are repeatedly needed without commit batching
- reviewers need a standardized pre-PR checklist generated from the worktree
- the same repository-specific git reports are being reconstructed repeatedly

If those appear, the next likely addition is:

- `merge-readiness-check`

That should remain separate from commit execution.

---

## 10. Final Position

The right skill is not "a skill that manages git." The right skill is a narrow,
high-judgment helper for preparing coherent commits on the current branch under
the repository's governance rules.

That makes the workflow:

- close to real daily practice
- compatible with normal PR convergence into `main`
- strict where the repository is strict
- lightweight where extra process would only add friction
