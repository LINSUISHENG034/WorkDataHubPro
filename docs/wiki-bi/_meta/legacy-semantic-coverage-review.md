# legacy semantic coverage review
> 状态：Completed
> 日期：2026-04-16
## Subagent Questions

- whether the semantic absorption map was missing legacy source families that would force a ninth module later
- whether `pilot-*` and `parallel-wave` were being read as execution authority instead of scope markers under the canonical domain-upgrade workflow
- whether M1-M4 should start from code or from non-code raw sources when reviewing legacy domain semantics
- whether parallel review could safely touch shared integration files without controller sequencing

## Coverage Findings

- the review kept the exact eight-module model; no `M9` is needed
- discovery and input-contract family belongs to `M8`
- shared cleansing and transform substrate belongs to `M8` for cross-domain execution semantics; domain-specific semantic effects stay with `M1-M4` when their pages cite them
- load and write-contract schema family belongs to `M6`
- reference-sync state family belongs to `M6`
- enrichment-index learning and conflict semantics belong to `M5`
- scheduled and operator runtime surfaces belong to `M8`
- M1-M4 code paths are not mandatory first-read sources; they are second-pass or audit sources after docs, runbooks, config, and other non-code background sources

## Governance Findings

- `pilot-*` and `parallel-wave` labels are scoping markers under the canonical domain-upgrade workflow; they do not replace that playbook
- same-change closure artifacts remain required for module acceptance
- evidence-template preservation and stable-finding separation must be checked during review
- assigned write sets remain enforced per module
- domain pages stay thin
- parallel execution creates shared-file collision risk around `index.md`, `log.md`, and round artifacts, so controller-owned integration files must be updated after per-module review

## Module Map Adjustments

- confirmed the eight-module map as the durable coverage frame
- recorded that listed legacy source paths are relative to the legacy `WorkDataHub` repo unless otherwise noted
- clarified that `parallel-wave` means post-pilot admission target, not immediate permission to start parallel execution
- added an explicit review section for coverage gaps closed by the adjudicated findings
- added an explicit guardrail section so module owners inherit the same review constraints

## Pilot Gate Adjustments

- pilots must prove the review flow from module worktree authoring to primary-checkout review before wider admission
- pilot closure must include same-change closure artifacts, evidence-template checks, stable-finding separation, and write-set enforcement
- pilots must treat M1-M4 code files as second-pass or audit sources after non-code raw sources
- pilots must preserve thin domain pages and record unresolved gaps without promoting them to stable findings
- pilots do not authorize shared-file writes by future parallel workers; controller-owned integration files stay sequenced after per-module review

## Remaining Open Questions

- decision: establish the controller integration template for delayed `index.md`, `log.md`, and round-note updates in parallel waves; owner: primary checkout controller; when the decision is made: before the first pilot is marked ready for parallel-wave admission; done looks like: the governing round note names the controller-owned integration files, defines their delayed update step, and leaves no shared-file ownership ambiguity
- decision: confirm whether any module write sets need finer partitioning before `parallel-wave` admission; owner: pilot review lead; when the decision is made: at pilot exit review for the last pilot in the admission sequence; done looks like: each admitted module has a frozen write set recorded in the round note, with no unresolved overlap against another module or controller-owned integration file
