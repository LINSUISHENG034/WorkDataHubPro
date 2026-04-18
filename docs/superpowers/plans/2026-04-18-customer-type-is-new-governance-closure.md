# Customer Type vs Is_New Governance Closure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the next governance round for the `customer_type vs is_new` conflict by turning the current proxy-warning into an explicit durable governance package with semantic-map disposition and report writeback.

**Architecture:** Add one dedicated durable evidence page that explains the non-equivalence, the legacy proxy usage, and the allowed governance outcomes. Then update the affected concept/standard pages and the semantic-map canonical non-equivalence node so the current contested state becomes an explicit adjudication package rather than a vague warning. Finally, regenerate or validate the semantic-map readiness surfaces that currently list this item as blocked.

**Tech Stack:** Markdown, YAML, semantic-map canonical artifacts under `docs/wiki-bi/_meta/legacy-semantic-map/`, pytest contract tests, `uv`

---

## Requirements Summary

- Preserve the stable semantic conclusion: `customer_type` is not `is_new`.
- Make the legacy proxy usage explicit as a governance object, not just a narrative caveat.
- Decide how the wiki should express the three-way disposition space:
  - semantic non-equivalence
  - legacy proxy usage that still existed
  - whether the proxy should be deferred, retired, or kept only as historical context
- Align durable wiki and semantic-map canonical outputs so the current blocked item `sem-non-equivalence-customer-type-vs-is-new` is no longer left as an under-specified contested note.
- Keep current-side runtime uncertainty and retirement decisions separate from semantic truth.

## Acceptance Criteria

1. `docs/wiki-bi/` has a dedicated durable page for the `customer_type vs is_new` governance conflict, not just scattered mentions.
2. `customer-type.md`, `is-new.md`, and `customer-status-semantics.md` all point to the new governance page and use the same conflict vocabulary.
3. The semantic-map canonical node `sem-non-equivalence-customer-type-vs-is-new.yaml` is updated so its recommendation/disposition is explicit and no longer depends on vague contradiction text alone.
4. The successor-wave readiness/discovery outputs are regenerated or otherwise updated so they reflect the new disposition.
5. Relevant docs/semantic-map tests pass.

## File Structure

### Create
- `docs/wiki-bi/evidence/customer-type-is-new-governance-evidence.md` — durable governance page for the semantic split and proxy-disposition package.
- `docs/superpowers/plans/2026-04-18-customer-type-is-new-governance-closure.md` — this plan.

### Modify
- `docs/wiki-bi/concepts/customer-type.md` — shift from generic warning to explicit governance-package entry.
- `docs/wiki-bi/concepts/is-new.md` — clarify that `is_new` may depend on `is_existing` but not on customer-type labels.
- `docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md` — tighten the rule and disposition vocabulary.
- `docs/wiki-bi/evidence/customer-status-annual-identity-evidence.md` — connect the annual identity family to the proxy-conflict boundary.
- `docs/wiki-bi/evidence/status-and-snapshot-evidence.md` — register the new governance page in the aggregate dispatcher.
- `docs/wiki-bi/index.md` — add FAQ/catalog entry for this exact conflict.
- `docs/wiki-bi/log.md` — record the round.
- `docs/wiki-bi/_meta/legacy-semantic-map/semantic/non-equivalences/sem-non-equivalence-customer-type-vs-is-new.yaml` — update the canonical semantic disposition.

### Regenerate / Validate
- `docs/wiki-bi/_meta/legacy-semantic-map/reports/waves/wave-2026-04-17-semantic-governance-reframe/semantic-readiness-status.json`
- `docs/wiki-bi/_meta/legacy-semantic-map/reports/waves/wave-2026-04-17-semantic-governance-reframe/semantic-readiness-summary.md`
- `docs/wiki-bi/_meta/legacy-semantic-map/reports/waves/wave-2026-04-17-semantic-governance-reframe/semantic-discovery-summary.md`

### Test
- `tests/contracts/test_legacy_semantic_map_repo_docs.py`
- `tests/contracts/test_legacy_semantic_map_semantic_reporting.py`
- `tests/contracts/test_legacy_semantic_map_semantic_recommendation_statuses.py`

---

### Task 1: Create the durable governance page for the proxy conflict

**Files:**
- Create: `docs/wiki-bi/evidence/customer-type-is-new-governance-evidence.md`
- Source reads: `E:\Projects\WorkDataHub\docs\business-background\客户主数据回填与状态来源分析.md`, `docs/wiki-bi/concepts/customer-type.md`, `docs/wiki-bi/concepts/is-new.md`, `docs/wiki-bi/_meta/legacy-semantic-map/semantic/non-equivalences/sem-non-equivalence-customer-type-vs-is-new.yaml`

- [ ] **Step 1: Draft the new page skeleton**

Create the page with this structure:

```md
# customer_type vs is_new 治理证据

## 结论主题

## 证据记录

## 稳定语义结论

## legacy proxy usage 的治理处置

## 当前证据缺口

## 相关页面
```

- [ ] **Step 2: Add the evidence table with both semantic and governance sources**

The page should include records with this meaning:

```md
| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-CTN-001 | legacy_doc | strong | absorbed | `customer-type`, `is-new`, `customer-status-semantics` | 2026-04-18 | `客户主数据回填与状态来源分析.md` 明确 `年金客户类型` 与 `is_new` 分属不同层。 |
| E-CTN-002 | current_wiki | supporting | absorbed | `customer-type`, `customer-status-semantics` | 2026-04-18 | 当前 wiki 已写明两者不等价，但尚未把 legacy proxy usage 收紧成治理对象。 |
| E-CTN-003 | semantic_map | supporting | absorbed | `customer-status-semantics` | 2026-04-18 | 当前 semantic-map canonical node 将该对象标为 contested/block，但处置语义仍待主线程收口。 |
```

- [ ] **Step 3: Write the core governance package**

The new page must explicitly separate:

```md
- semantic truth: `customer_type` is not `is_new`
- legacy proxy usage: some adjacent flows treated customer-type labels as an operational proxy
- governance disposition: proxy usage must be classified as `deferred`, `retired`, or `historical_context_only`, rather than left as a vague contradiction
```

Also include a section that asks the exact durable question:

```md
- Does the proxy survive as an accepted compatibility bridge?
- Or is it retained only as historical context and marked retired for future semantic use?
```

### Task 2: Rewire the durable wiki pages around the new governance object

**Files:**
- Modify: `docs/wiki-bi/concepts/customer-type.md`
- Modify: `docs/wiki-bi/concepts/is-new.md`
- Modify: `docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md`
- Modify: `docs/wiki-bi/evidence/customer-status-annual-identity-evidence.md`
- Modify: `docs/wiki-bi/evidence/status-and-snapshot-evidence.md`
- Modify: `docs/wiki-bi/index.md`
- Modify: `docs/wiki-bi/log.md`

- [ ] **Step 1: Update `customer-type.md`**

Add a direct durable pointer with this meaning:

```md
- `customer_type` 与 `is_new` 的冲突处置不只是一句提醒，而是一个独立治理对象。
- 读者应进入 `customer-type-is-new-governance-evidence.md` 查看 semantic truth、proxy history、以及 disposition question。
```

- [ ] **Step 2: Update `is-new.md`**

Add a short section stating:

```md
- `is_new` 的定义依赖年度状态语义（如 `is_existing`），不依赖 customer-type label。
- 若 legacy 输出或相邻流程曾借用 customer-type label，那只是 proxy history，不是公式定义的一部分。
```

- [ ] **Step 3: Update `customer-status-semantics.md`**

Strengthen the standard with a single explicit rule:

```md
- `customer_type` may appear beside status evaluation, but it must never be promoted into semantic truth for `is_new`.
- legacy proxy usage must be expressed as governance disposition, not semantic equivalence.
```

- [ ] **Step 4: Update related evidence/index pages**

Required outcomes:

```md
- `customer-status-annual-identity-evidence.md` should mention that annual identity semantics are adjacent to, but distinct from, customer-type proxy governance.
- `status-and-snapshot-evidence.md` should list the new governance page in its object-level reinforcements or current gaps section.
- `index.md` should add an FAQ/catalog entry for `customer_type vs is_new`.
- `log.md` should record the round using the timestamped format.
```

### Task 3: Adjudicate the semantic-map canonical non-equivalence node

**Files:**
- Modify: `docs/wiki-bi/_meta/legacy-semantic-map/semantic/non-equivalences/sem-non-equivalence-customer-type-vs-is-new.yaml`

- [ ] **Step 1: Replace vague contradiction language with explicit disposition framing**

Update the YAML so the node no longer stops at “proxy conflict exists”. It should carry explicit fields in this spirit:

```yaml
proposal_governance:
  recommendation_status: recommended_defer_review
  contradiction_accounting_status: explicit_governance_disposition_required
  high_priority_governance_questions:
    - Should legacy customer-type proxy usage be retired for future semantic interpretation?
    - If temporary compatibility wording is retained, where is its boundary documented?
```

If the controlled vocabulary does not allow those exact values, adapt to the nearest existing allowed values but keep the meaning explicit.

- [ ] **Step 2: Tighten durable target pages**

The node should target at least:

```yaml
durable_target_pages:
  - docs/wiki-bi/evidence/customer-type-is-new-governance-evidence.md
  - docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md
  - docs/wiki-bi/concepts/customer-type.md
```

- [ ] **Step 3: Update readiness notes**

Replace generic blockage notes with concrete phrasing such as:

```yaml
readiness_notes:
  - Semantic non-equivalence is stable.
  - Remaining work is governance disposition of legacy proxy usage, not semantic discovery.
```

### Task 4: Regenerate successor-wave readiness outputs

**Files:**
- Regenerate: `docs/wiki-bi/_meta/legacy-semantic-map/reports/waves/wave-2026-04-17-semantic-governance-reframe/semantic-readiness-status.json`
- Regenerate: `docs/wiki-bi/_meta/legacy-semantic-map/reports/waves/wave-2026-04-17-semantic-governance-reframe/semantic-readiness-summary.md`
- Regenerate: `docs/wiki-bi/_meta/legacy-semantic-map/reports/waves/wave-2026-04-17-semantic-governance-reframe/semantic-discovery-summary.md`

- [ ] **Step 1: Run the reporting path after canonical update**

Use the existing semantic-map reporting entrypoint rather than hand-editing generated outputs.

Run:

```powershell
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_reporting.py -v
```

Then run the project’s existing semantic-map reporting/regeneration command used for the successor wave. If the current workflow uses the reporting module directly, use that same path rather than inventing a new script.

- [ ] **Step 2: Confirm the readiness summary reflects the new governance framing**

Expected outcomes:

```md
- `sem-non-equivalence-customer-type-vs-is-new` is no longer described as a vague contested discovery
- the summary describes it as a governance-disposition item or a still-blocked retirement/defer decision
```

### Task 5: Verify and commit

**Files:**
- Validate: `tests/contracts/test_legacy_semantic_map_repo_docs.py`
- Validate: `tests/contracts/test_legacy_semantic_map_semantic_reporting.py`
- Validate: `tests/contracts/test_legacy_semantic_map_semantic_recommendation_statuses.py`

- [ ] **Step 1: Run targeted validation**

Run:

```powershell
uv run pytest tests/contracts/test_legacy_semantic_map_repo_docs.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_reporting.py -v
uv run pytest tests/contracts/test_legacy_semantic_map_semantic_recommendation_statuses.py -v
```

Expected:
- PASS for all commands

- [ ] **Step 2: Review scope**

Run:

```powershell
git status -sb
git diff -- docs/wiki-bi docs/wiki-bi/_meta/legacy-semantic-map docs/superpowers/plans/2026-04-18-customer-type-is-new-governance-closure.md
```

Expected:
- only the planned wiki / semantic-map / plan files are changed

- [ ] **Step 3: Commit**

Run:

```powershell
git add docs/wiki-bi docs/wiki-bi/_meta/legacy-semantic-map docs/superpowers/plans/2026-04-18-customer-type-is-new-governance-closure.md
git commit -m "docs(docs.architecture): close customer-type is-new governance package"
```

Expected:
- one docs/governance-scoped commit

---

## Risks and Mitigations

- **Risk:** Treating governance closure as semantic re-discovery.
  - **Mitigation:** Keep semantic truth fixed and only close the proxy-disposition language.
- **Risk:** Over-claiming that the conflict is fully retired without evidence.
  - **Mitigation:** Make the plan require an explicit defer/retire/historical-context disposition.
- **Risk:** Manually editing generated semantic-map reports.
  - **Mitigation:** Require regeneration through the existing reporting path.

## Verification Steps

- `uv run pytest tests/contracts/test_legacy_semantic_map_repo_docs.py -v`
- `uv run pytest tests/contracts/test_legacy_semantic_map_semantic_reporting.py -v`
- `uv run pytest tests/contracts/test_legacy_semantic_map_semantic_recommendation_statuses.py -v`
- `git diff -- docs/wiki-bi docs/wiki-bi/_meta/legacy-semantic-map docs/superpowers/plans/2026-04-18-customer-type-is-new-governance-closure.md`

## Self-Review

### 1. Spec coverage
- New durable governance object page: Task 1.
- Durable wiki rewiring: Task 2.
- Semantic-map disposition closure: Task 3.
- Generated readiness/report writeback: Task 4.
- Validation and commit path: Task 5.

### 2. Placeholder scan
- No `TODO` / `TBD` placeholders remain.
- All planned files are named explicitly.
- All validation commands are concrete.

### 3. Type consistency
- Conflict name is consistently `customer_type vs is_new`.
- New governance page name is consistently `customer-type-is-new-governance-evidence.md`.
- Semantic-map canonical node is consistently `sem-non-equivalence-customer-type-vs-is-new`.
