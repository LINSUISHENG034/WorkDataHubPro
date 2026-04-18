# Wiki Annual Identity Semantics Coverage Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Strengthen `docs/wiki-bi/` so it covers the legacy annual identity semantics around `is_strategic`, `is_existing`, `contract_status`, `status_year`, and the ratchet/proxy boundaries more directly.

**Architecture:** Add one family-level durable evidence page for annual identity semantics, then reconnect the existing concept, standard, evidence, and navigation pages to that new object so the wiki exposes the legacy business meaning without over-splitting into premature atomic pages. Keep runtime/operator uncertainty explicitly separated from stable semantic conclusions.

**Tech Stack:** Markdown, legacy business-background docs, current `wiki-bi` durable pages, pytest contract docs checks

---

## Requirements Summary

- Absorb stable business semantics from `E:\Projects\WorkDataHub\docs\business-background\战客身份定义与更新逻辑.md`.
- Improve `wiki-bi` coverage for the annual identity family: `is_strategic`, `is_existing`, `contract_status`, `status_year`.
- Preserve current durable boundaries:
  - semantic truth stays in concepts / standards / evidence
  - operator command details stay in surfaces / evidence
  - unresolved rebuild-side runtime decisions remain evidence gaps
- Make the `customer_type` vs `is_new` proxy-conflict visible without falsely resolving it.
- Update wiki navigation so a maintainer can discover this topic directly.

## Acceptance Criteria

1. `docs/wiki-bi/evidence/customer-status-annual-identity-evidence.md` exists and summarizes the annual identity family with source-backed conclusions and explicit evidence gaps.
2. `docs/wiki-bi/concepts/customer-status.md` links the annual identity family to the new evidence page and explains the status family more explicitly.
3. `docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md` explicitly states:
   - `status_year` is an annual identity anchor, not `snapshot_month`
   - strategic status carries ratchet semantics
   - `customer_type` is not `is_new`, while legacy proxy usage remains unresolved governance context
4. Existing lifecycle and aggregate evidence pages are updated to reference the new annual identity page without duplicating all details.
5. `docs/wiki-bi/index.md` and `docs/wiki-bi/log.md` reflect the new durable entry and the maintenance round.
6. Relevant docs validation tests pass, and the touched docs remain aligned with the active blueprint and current semantic-map findings.

## File Structure

### Create
- `docs/wiki-bi/evidence/customer-status-annual-identity-evidence.md` — new durable evidence page for the annual identity status family.
- `docs/superpowers/plans/2026-04-18-wiki-annual-identity-semantics.md` — this plan.

### Modify
- `docs/wiki-bi/concepts/customer-status.md` — promote the annual identity family into the primary status narrative.
- `docs/wiki-bi/concepts/customer-type.md` — make the proxy-conflict boundary more explicit and link the new page.
- `docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md` — tighten annual identity semantics and conflict handling.
- `docs/wiki-bi/evidence/customer-mdm-lifecycle-evidence.md` — turn it into the lifecycle companion page and cross-link the new annual identity page.
- `docs/wiki-bi/evidence/status-and-snapshot-evidence.md` — register the new object page in the aggregate dispatcher.
- `docs/wiki-bi/index.md` — add maintainer/reader entrypoints for annual identity semantics.
- `docs/wiki-bi/log.md` — record the maintenance round.

### Validate
- `tests/contracts/test_legacy_semantic_map_repo_docs.py`
- `tests/contracts/test_annuity_income_wiki_guidance_docs.py`

---

### Task 1: Establish the annual identity evidence page

**Files:**
- Create: `docs/wiki-bi/evidence/customer-status-annual-identity-evidence.md`
- Source reads: `E:\Projects\WorkDataHub\docs\business-background\战客身份定义与更新逻辑.md`, `docs/wiki-bi/evidence/customer-mdm-lifecycle-evidence.md`, `docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md`

- [ ] **Step 1: Draft the durable page skeleton**

Create a new page with these sections:

```md
# customer annual identity 证据

## 结论主题

## 证据记录

## 稳定结论

## 非等价 / 易混边界

## 当前证据缺口

## 相关页面
```

- [ ] **Step 2: Populate the evidence table from legacy and current sources**

The page should include at least these source-backed evidence records:

```md
| evidence_id | source_type | evidence_strength | coverage_state | supported_pages | last_verified | notes |
|---|---|---|---|---|---|---|
| E-CAI-001 | legacy_doc | strong | absorbed | `customer-status`, `customer-status-semantics` | 2026-04-18 | `战客身份定义与更新逻辑.md` 明确 `is_strategic`、`is_existing`、`contract_status`、`status_year` 是围绕 `customer.客户年金计划` 的年度身份家族。 |
| E-CAI-002 | legacy_code | strong | absorbed | `customer-status`, `customer-status-semantics`, `customer-mdm-lifecycle-evidence` | 2026-04-18 | `src/work_data_hub/customer_mdm/contract_sync.py`、`year_init.py`、`strategic.py` 共同承接 yearly init、status sync 与 strategic ratchet 语义。 |
| E-CAI-003 | current_wiki | supporting | absorbed | `status-and-snapshot-evidence`, `customer-mdm-lifecycle-evidence` | 2026-04-18 | 当前 wiki 已确认 lifecycle / command / snapshot 分层，但 annual identity family 仍需单独入口。 |
```

- [ ] **Step 3: Write the stable conclusions and unresolved gaps**

The page must explicitly conclude:

```md
- `is_strategic`、`is_existing`、`contract_status`、`status_year` 组成年度身份家族，而不是零散状态字段。
- `status_year` 是年度身份锚点，不等于 `snapshot_month`。
- strategic 身份具有 ratchet-style 语义：允许升级，不应因短期回落自动降级。
- 这组语义主要锚定在 `customer.客户年金计划`，快照负责分析展示而非重新定义年度身份。
```

And it must keep these as gaps instead of over-claiming:

```md
- rebuild-side `status_year` authoritative runtime carrier 仍未闭环
- legacy `customer_type` proxy usage 与 `is_new` 的治理处置仍待后续裁决
```

### Task 2: Reconnect concepts and standards to the new annual identity object

**Files:**
- Modify: `docs/wiki-bi/concepts/customer-status.md`
- Modify: `docs/wiki-bi/concepts/customer-type.md`
- Modify: `docs/wiki-bi/standards/semantic-correctness/customer-status-semantics.md`

- [ ] **Step 1: Update `customer-status.md`**

Add or tighten text so the page explicitly names the annual identity family and points to the new evidence page.

Required outcomes:

```md
- `is_strategic` / `is_existing` / `contract_status` / `status_year` should be described as the annual identity family.
- The page should link to `../evidence/customer-status-annual-identity-evidence.md` in both the main narrative and related evidence section.
- The page should keep formula memory separate from lifecycle/runtime details.
```

- [ ] **Step 2: Update `customer-type.md`**

Add a brief conflict note with this meaning:

```md
- `customer_type` 与 `is_new` 在语义上不等价。
- legacy 存在把 customer-type label 当近似 proxy 的相邻用法，但这不是 durable semantic definition。
- 该冲突目前应显式保留，而不是被静默抹平。
```

Also add a link to `../evidence/customer-status-annual-identity-evidence.md` or `../standards/semantic-correctness/customer-status-semantics.md` where it best fits.

- [ ] **Step 3: Update `customer-status-semantics.md`**

Tighten the standard so it explicitly includes:

```md
- `status_year` is an annual identity anchor and is not interchangeable with `snapshot_month`
- strategic status is governed by ratchet semantics
- `customer_type` must not be silently promoted into `is_new` truth
- when proxy usage exists in legacy adjacent flows, record it as governance context or evidence gap, not semantic equivalence
```

### Task 3: Reconnect aggregate and lifecycle evidence pages

**Files:**
- Modify: `docs/wiki-bi/evidence/customer-mdm-lifecycle-evidence.md`
- Modify: `docs/wiki-bi/evidence/status-and-snapshot-evidence.md`

- [ ] **Step 1: Update the lifecycle page to become a companion dispatcher**

Keep `customer-mdm-lifecycle-evidence.md` focused on lifecycle actions (`yearly-init`, `sync`, `snapshot`, `cutover`, ratchet-style) and add a clear boundary like:

```md
- lifecycle page explains action sequencing and yearly semantics evidence
- annual-identity page explains the status-family object meanings
```

Add the new page to `相关页面` and avoid duplicating the whole annual identity family detail.

- [ ] **Step 2: Update the aggregate dispatcher page**

In `status-and-snapshot-evidence.md`, register the new object page in:

```md
- 本轮已吸收的稳定结论
- 对象级补强页
- 当前证据缺口
```

The aggregate page should say the annual identity family now has a dedicated object page while `status_year` rebuild-runtime closure remains open.

### Task 4: Update maintainer navigation and log

**Files:**
- Modify: `docs/wiki-bi/index.md`
- Modify: `docs/wiki-bi/log.md`

- [ ] **Step 1: Add reader and maintainer entrypoints to `index.md`**

Add at least one FAQ or maintainer-entry bullet covering:

```md
- 如何理解 `is_strategic` / `is_existing` / `contract_status` / `status_year`
- 为什么 `status_year` 不等于 `snapshot_month`
- 为什么 `customer_type` 不能直接当作 `is_new`
```

Link the new evidence page and the tightened standard.

- [ ] **Step 2: Add a timestamped log entry**

Append a new `log.md` entry using the current log format:

```md
## [2026-04-18 HH:MM] maintain | annual identity semantics coverage

- added the annual identity evidence page for `is_strategic` / `is_existing` / `contract_status` / `status_year`
- tightened the customer-status standard around `status_year`, ratchet semantics, and customer-type proxy conflict
- rewired lifecycle and aggregate pages plus index navigation to expose the new durable entry
```

### Task 5: Verify and commit

**Files:**
- Validate: `tests/contracts/test_legacy_semantic_map_repo_docs.py`
- Validate: `tests/contracts/test_annuity_income_wiki_guidance_docs.py`

- [ ] **Step 1: Run targeted docs validation**

Run:

```powershell
uv run pytest tests/contracts/test_legacy_semantic_map_repo_docs.py -v
uv run pytest tests/contracts/test_annuity_income_wiki_guidance_docs.py -v
```

Expected:
- PASS for both commands

- [ ] **Step 2: Review diff scope**

Run:

```powershell
git status -sb
git diff -- docs/wiki-bi docs/superpowers/plans/2026-04-18-wiki-annual-identity-semantics.md
```

Expected:
- only the planned docs files plus the new plan file are changed
- no unrelated runtime/config/test files are modified

- [ ] **Step 3: Commit the docs update**

Run:

```powershell
git add docs/wiki-bi docs/superpowers/plans/2026-04-18-wiki-annual-identity-semantics.md
git commit -m "docs(docs.architecture): tighten annual identity wiki semantics"
```

Expected:
- one docs-scoped commit on `docs/wiki-annual-identity-semantics`

---

## Risks and Mitigations

- **Risk:** Overstating rebuild-side runtime closure for `status_year`.
  - **Mitigation:** Keep rebuild runtime carrier as an explicit evidence gap.
- **Risk:** Repeating lifecycle details across multiple pages.
  - **Mitigation:** Keep lifecycle sequencing on the lifecycle page and object meaning on the new annual identity page.
- **Risk:** Accidentally resolving the `customer_type` proxy conflict without evidence.
  - **Mitigation:** Record it as an unresolved governance/context note, not a settled semantic equivalence.

## Verification Steps

- `uv run pytest tests/contracts/test_legacy_semantic_map_repo_docs.py -v`
- `uv run pytest tests/contracts/test_annuity_income_wiki_guidance_docs.py -v`
- `git diff -- docs/wiki-bi docs/superpowers/plans/2026-04-18-wiki-annual-identity-semantics.md`

## Self-Review

### 1. Spec coverage
- New durable annual identity object page: covered by Task 1.
- Tightened concept + standard semantics: covered by Task 2.
- Lifecycle / aggregate dispatcher rewiring: covered by Task 3.
- Maintainer discoverability and historical trace: covered by Task 4.
- Validation and clean docs-only scope control: covered by Task 5.

### 2. Placeholder scan
- No `TODO` / `TBD` placeholders remain.
- All touched files are named explicitly.
- All verification commands are concrete.

### 3. Type consistency
- The new page name is consistently `customer-status-annual-identity-evidence.md`.
- The annual identity family is consistently `is_strategic` / `is_existing` / `contract_status` / `status_year`.
- The unresolved proxy boundary is consistently described as `customer_type` vs `is_new`.
