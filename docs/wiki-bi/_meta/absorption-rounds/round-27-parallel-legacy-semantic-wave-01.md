# Round 27：parallel legacy semantic wave 01

> 状态：Completed
> 日期：2026-04-16
> 主题簇：parallel-wave / wiki-bi / legacy-semantics

## Modules Executed

- `M1` `annuity_performance`
- `M2` `annuity_income`
- `M3` `annual_award`
- `M4` `annual_loss`
- `M8` operator/runtime/verification governance

## Modules Merged

- `M1`
- `M2`
- `M3`
- `M4`
- `M8`

## Modules Held Back

- none

## Reusable Prompt Pattern

- raw sources first, with domain docs/runbooks/config ahead of code and code treated as second-pass audit evidence
- exact write set per module, with controller-owned integration files kept out of parallel worker ownership
- evidence-first ordering, then contract/surface/domain link tightening
- explicit forbidden page drift so unresolved findings stay in `当前证据缺口`
- merge gates repeated in the worker prompt before review

## Review Failure Patterns

- parallel sibling branches do not remain fast-forwardable after another sibling merges; each later sibling needed a quick rebase onto the updated program branch before `--ff-only` integration
- controller-owned integration files must stay centralized, or the wave immediately reintroduces `index.md` / `log.md` / round-note collision risk
- aggregate evidence pages still need review for dispatcher discipline even when the write set itself is clean

## Next Wave Admission Rules

- keep controller-owned integration files off parallel worker write sets
- require disjoint module write sets plus evidence-template preservation before merge
- require quick rebase onto the current program branch before each `--ff-only` integration when sibling branches have already merged
- only start another parallel wave after the reused prompt shape still yields thin domain pages, stable evidence-first ordering, and no unresolved shared-file ownership drift
