# WorkDataHubPro Framework-Neutral Foundation

Date: 2026-04-14
Status: Active Product-Level Baseline
Scope: All current and future development frameworks for `WorkDataHubPro`

## 1. Why This Layer Exists

`WorkDataHubPro` currently has architecture and planning material produced under more than one workflow framework.

Those framework documents are useful, but they are not the product itself.

This layer exists so that:

- product-level architectural truth does not depend on one planning framework
- future skills and agents can reason from one stable top-level design
- new frameworks can be added later without redefining the system each time

## 2. System Identity

`WorkDataHubPro` is a behavioral rebuild of `WorkDataHub`.

It is not:

- a structural copy of the legacy repository
- a replay-only utility
- a framework-specific delivery project

It is:

- a capability-first data-processing system
- a parity-sensitive rebuild
- an explainable and governable runtime
- a system intended to be operable by both humans and agents

## 3. Product-Level Goals

The system must simultaneously pursue:

1. legacy-equivalent business outcomes
2. architectural clarity
3. explainable runtime behavior
4. governed change and adjudication
5. operator-usable outputs and evidence

When these goals conflict, product-level invariants win over framework convenience.

## 4. Non-Negotiable Invariants

These invariants apply regardless of which development framework is active.

- Business semantics must live in business capability code, not in orchestration glue, hooks, or generic helpers.
- Identity resolution must remain an explicit boundary, not an accidental side effect inside fact processing.
- Reference/master derivation must remain explicit and must not silently own projection behavior.
- Publication must be explicit. Material write paths must declare mode, transaction grouping, and idempotency scope.
- Projection behavior must consume published facts or published derived outputs, never raw intake payloads.
- Operator-facing artifacts are first-class design objects when business or operational workflows depend on them.
- Explicitly retired behavior must not be revived as an implementation shortcut.
- Configuration may tune approved behavior but must not silently redefine business semantics or module boundaries.
- Unexpected output must remain explainable from runtime evidence anchored to a stable accountability key.

## 5. Logical System Model

The system is organized into four product-level layers:

1. Business capabilities
2. Platform runtime
3. Governance control
4. Execution adapters

### 5.1 Business Capabilities

Own:

- source intake
- fact processing
- identity resolution
- reference derivation
- projections

Must not own:

- framework workflow state
- hidden shared side effects
- governance-only adjudication logic

### 5.2 Platform Runtime

Own:

- contracts
- tracing
- lineage
- publication
- storage
- execution helpers

Must not own:

- business meaning
- domain-specific rule semantics

### 5.3 Governance Control

Own:

- evidence indexing
- compatibility adjudication
- config/release control
- explicit deviation handling

Must not own:

- hot-path field derivation
- hidden runtime business decisions

### 5.4 Execution Adapters

Own:

- CLI surfaces
- replay runners
- scheduling/orchestration entrypoints
- operator tools

Must not own:

- transformation semantics
- silent semantic workarounds for missing upstream contracts

## 6. Acceptance Axes

A slice or framework adaptation is not successful merely because code runs.

At product level, success is judged on these axes:

- parity or justified divergence
- explainability
- operator visibility
- explicit artifact and surface governance
- controlled deferral

### 6.1 Parity Or Justified Divergence

The system should preserve legacy-equivalent business outcomes unless an intentional difference is:

- explicit
- tested
- documented
- adjudicated

### 6.2 Explainability

The system must preserve enough runtime evidence that material outcomes can be traced and explained without reverse-engineering opaque flows.

### 6.3 Operator Visibility

If an artifact or surface matters to operational workflows, it must be treated as a governed object rather than dismissed as debug output.

### 6.4 Controlled Deferral

Deferred work is acceptable only when it is explicit, scoped, and prevented from silently leaking into accepted slices.

## 7. Relationship To `docs/wiki-bi/`

`docs/system/` and `docs/wiki-bi/` are complementary.

- `docs/system/` defines product-level architecture, invariants, and authority.
- `docs/wiki-bi/` defines business semantics, standards, evidence, and operator/surface memory.

In practice:

- `docs/system/` answers "what kind of system are we building?"
- `docs/wiki-bi/` answers "what must this system preserve and how do we know?"

## 8. Relationship To Framework Documents

Framework-specific documents are allowed and useful, but they are subordinate to this layer.

Examples include:

- `docs/superpowers/`
- `.planning/`
- future planning or agent framework directories

They may define:

- workflow states
- execution plans
- phase sequencing
- framework-specific review or status models

They must not redefine:

- product-level invariants
- business-semantic truth
- the top-level source-of-truth order

## 9. Rule For New Frameworks

A new development framework may be added only if it can map itself cleanly onto:

- the product-level layers in this document
- the business/evidence layer in `docs/wiki-bi/`
- the runtime truth recorded in code, tests, config, replay assets, and runbooks

If it cannot, the framework is the problem, not the product.

## 10. What This Layer Does Not Define

This layer does not define:

- current phase numbering
- plan/task breakdown
- branch strategy details
- framework-specific progress state
- implementation status by itself

Those belong to lower layers in the document authority model.
