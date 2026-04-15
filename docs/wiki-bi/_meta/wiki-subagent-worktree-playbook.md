# wiki subagent worktree playbook

## Purpose

Define how one subagent updates one wiki module in one linked worktree, and how the main session reviews and merges that result.

Worktree authoring happens in the module worktree, primary review happens from a clean checkout in the root worktree, and merges follow `docs/disciplines/git-workflow.md`.

## Hard Rules

- one subagent owns one module and one disjoint write set
- all subagent execution happens in `.worktrees/`
- subagent output never merges to `main` without human review in the root worktree
- open questions may land in `evidence/`, but never as stable findings in concept/standard/domain main prose
- domain pages stay thin navigation pages

## Required Review Gates

- touched evidence pages still expose `结论主题` + `证据记录` + strong/supporting split + `当前证据缺口`
- touched concept and standard pages separate stable findings from implementation trace
- new pages are reachable from an owning page and from `index.md`
- the subagent changed only its assigned file set

## Pilot Exit Criteria

- primary review and merge readiness are judged from the primary checkout, not from the module worktree
- merge sequencing still follows `docs/disciplines/git-workflow.md`
- in a single-module pilot, `index.md`, `log.md`, and the round note may be in the subagent write set only if the round note explicitly assigns them
- acceptance includes same-change closure artifacts (module-owned pages plus the closure entry points required by the workflow)
- reachability is preserved: new/updated pages are linked from an owning page and from `index.md`
- evidence-template preservation holds (no template drift, no loss of strong/supporting split, no loss of `当前证据缺口`)
- stable findings stay separate from implementation trace in concept/standard prose
- write-set compliance is explicit: the change touches only the assigned file set for that module
- for `M1-M4`, code files are second-pass or audit sources after non-code raw sources such as docs, runbooks, config, and background material
- any discovered gaps are disposed (recorded as current evidence gaps, or written back as a current-implementation adjustment when applicable)
- domain pages remain thin navigation pages (no summary-page sprawl)

## Parallel Wave Admission Criteria

- modules are only admitted after the pilots pass and the module map is accepted as stable enough for parallel execution
- `pilot-*` and `parallel-wave` remain scoping markers under the canonical domain-upgrade workflow; they do not replace that playbook
- in parallel-wave execution, `index.md`, `log.md`, and round notes are controller-owned integration files updated after per-module review
- the final integration step still satisfies the required gate that `index.md`/`log.md`/round note land together, but this is performed by the controller as an integration action after module reviews close
