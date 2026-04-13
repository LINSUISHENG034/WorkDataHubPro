# Phase 4: Agent Operations & Governance Hardening - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md.

**Date:** 2026-04-13
**Phase:** 04-Agent Operations & Governance Hardening
**Areas discussed:** Operator workflow contract, Lineage and evidence lookup, Evidence redaction, Adjudication lifecycle
**Mode:** Auto

---

## Operator workflow contract

| Option | Description | Selected |
|--------|-------------|----------|
| Extend existing CLI/runbook surface | Reuse current app/runbook entrypoints and add one documented end-to-end operator workflow | ✓ |
| Create separate operator-only tool surface | Add a distinct command tree or new operator app for Phase 4 workflows | |
| Let the agent decide | Defer the surface choice to later planning | |

**Auto choice:** Extend existing CLI/runbook surface
**Notes:** Recommended because Phase 3 already established discoverable replay entrypoints and runbooks, and Phase 4 should harden that surface rather than fork it.

---

## Lineage and evidence lookup

| Option | Description | Selected |
|--------|-------------|----------|
| Add explicit query helpers over trace/lineage/evidence anchors | Keep file-backed evidence but make lookup by ids and anchors first-class | ✓ |
| Leave lookup as manual folder/file browsing | Rely on current JSON layout plus runbook notes | |
| Let the agent decide | Defer lookup shape to planning | |

**Auto choice:** Add explicit query helpers over trace/lineage/evidence anchors
**Notes:** Recommended because roadmap success criteria require reliable output-to-source lookup and executable incident diagnostics.

---

## Evidence redaction

| Option | Description | Selected |
|--------|-------------|----------|
| Redact at the evidence persistence boundary | Centralize masking in evidence writers/readers while preserving audit anchors | ✓ |
| Redact in domain code before events are emitted | Push masking into every domain service individually | |
| Let the agent decide | Defer to implementation | |

**Auto choice:** Redact at the evidence persistence boundary
**Notes:** Recommended because governance concerns are centralized in `file_store.py`, and per-domain masking would fragment the policy.

---

## Adjudication lifecycle

| Option | Description | Selected |
|--------|-------------|----------|
| Extend file-backed `CompatibilityCase` lifecycle | Add severity/owner/closure proof/status transitions while keeping repository-auditable records | ✓ |
| Introduce a new adjudication backend now | Move lifecycle and closure to a new persistence/service layer in this phase | |
| Let the agent decide | Defer to implementation | |

**Auto choice:** Extend file-backed `CompatibilityCase` lifecycle
**Notes:** Recommended because the roadmap asks for governance hardening, not a storage-platform rewrite.

---

## the agent's Discretion

- Exact helper/module names for lookup and redaction surfaces
- Exact closure-proof schema for compatibility cases
- Exact CLI command layout so long as it stays discoverable from committed docs

## Deferred Ideas

- Persistent adapters for evidence/trace storage
- Operator dashboards
- Larger runtime expansion beyond the first documented operations workflow
