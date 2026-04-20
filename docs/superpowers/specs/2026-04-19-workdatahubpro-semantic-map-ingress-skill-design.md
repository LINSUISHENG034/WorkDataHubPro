# WorkDataHubPro Semantic Map Ingress Skill Design

Date: 2026-04-19
Status: Proposed Design
Target Workspace: `E:\Projects\WorkDataHubPro`
Legacy Source Workspace: `E:\Projects\WorkDataHub`

---

## 1. Purpose

This document defines a repository-local skill and ingress workflow for writing
legacy business-semantics findings into
`docs/wiki-bi/_meta/legacy-semantic-map/`.

The design exists to solve a specific mismatch in the current semantic-map
workflow:

- the current semantic-map schema contains useful semantic distinctions
- the current semantic-map write path is too heavy to act as the main discovery front door
- the current scripting layer is useful for routing and registry integrity, but
  should not be treated as the mechanism that interprets business semantics

The goal is therefore not to bypass the semantic map.

The goal is to make the semantic map itself easier to populate from legacy
evidence, while keeping it as the only write target for this workflow.

This skill must not write `docs/wiki-bi/` durable pages.

---

## 2. Relationship To Existing Semantic-Map Design

This design supplements
`docs/superpowers/specs/2026-04-16-workdatahub-legacy-semantic-map-design.md`.

It preserves the following existing semantic-map decisions:

- `docs/wiki-bi/_meta/legacy-semantic-map/` remains a non-durable discovery ledger
- `scripts/legacy_semantic_map/` remains the location for helper tooling
- semantic-map outputs remain upstream of any later durable wiki absorption
- semantic canonical files and `claims/<wave_id>/semantic/` remain valid target
  layers

It changes the discovery entry model:

- discovery should no longer begin with a full claim-shaped schema burden
- a new lightweight `ingress` layer becomes the default write front door
- automatic promotion from ingress into `claims/<wave_id>/semantic/` is allowed
  when conservative evidence gates pass

If this document conflicts with the older semantic-map design on semantic
discovery entry workflow, this document wins for ingress-related behavior.

---

## 3. Design Goals

- keep `legacy-semantic-map` as the only output target for this workflow
- reduce discovery friction without losing semantic discipline
- preserve the useful semantic distinctions already present in the semantic-map
  schema
- let a repository-local skill perform discovery-first semantic extraction from
  the legacy repository
- keep routing, wave validation, duplicate detection, and promotion checks
  mechanical and lightweight
- make conservative auto-promotion possible without requiring the full current
  compiler workflow
- prevent circular dependency from `WorkDataHubPro` wiki/spec content back into
  legacy business-semantics evidence

When these goals conflict, evidence provenance and semantic correctness take
precedence over convenience.

---

## 4. Non-Goals

This design does not:

- write or update `docs/wiki-bi/` durable pages
- use `WorkDataHubPro` wiki/spec content as legacy business-semantics evidence
- replace the semantic canonical layer under `semantic/`
- replace existing wave management, reporting, or canonical compilation tooling
- silently merge, overwrite, or repair existing semantic canonical files
- require current heavy semantic-map scripts to perform business-semantic
  interpretation

Later workflows may consume semantic-map findings into durable wiki content, but
that is outside this skill's scope.

---

## 5. Core Design Decision

The semantic-map discovery workflow should use a two-stage model:

1. lightweight ingress
2. conservative auto-promotion to `claims/<wave_id>/semantic/`

The ingress layer captures half-finished but discussion-ready semantic
conclusions.

The claim layer continues to capture promotion-ready semantic findings using the
existing semantic-map claim family.

This ordering is intentional:

- ingress is the discovery front door
- semantic claims remain the first formal semantic-map layer
- canonical semantic files remain downstream of claims, not upstream of them

---

## 6. Hard Boundary Rules

### 6.1 Output Boundary

This skill writes only under:

- `docs/wiki-bi/_meta/legacy-semantic-map/ingress/`
- `docs/wiki-bi/_meta/legacy-semantic-map/claims/<wave_id>/semantic/`

This skill must not write:

- `docs/wiki-bi/`
- `docs/system/`
- `docs/superpowers/plans/`
- any runtime or application code under `src/work_data_hub_pro/`

### 6.2 Evidence Boundary

All business-semantic evidence used by this workflow must come from
`E:\Projects\WorkDataHub`.

Allowed evidence classes include:

- legacy docs
- legacy config
- legacy code
- legacy tests
- legacy runbooks

`WorkDataHubPro` materials may be read only for:

- routing
- duplicate detection
- wave validation
- semantic-map registry awareness

They must not be cited as business-semantic evidence in ingress or promoted
claims.

### 6.3 Circular-Dependency Rule

The semantic map should describe legacy business semantics as discovered from the
legacy repository itself.

It must not become a record of how `WorkDataHubPro` currently interprets the
legacy repository.

### 6.4 Existing-Record Modification Rule

If the agent concludes that an existing file under either of these paths should
be modified:

- `docs/wiki-bi/_meta/legacy-semantic-map/claims/<wave_id>/semantic/*.yaml`
- `docs/wiki-bi/_meta/legacy-semantic-map/semantic/**/*.yaml`

the agent must stop and ask the user before making that change.

The skill may still write a new ingress record that explains the overlap or
conflict while waiting for user direction.

---

## 7. Ingress Layer

### 7.1 Physical Layout

Add this subtree under the semantic map:

```text
docs/wiki-bi/_meta/legacy-semantic-map/
└── ingress/
    └── waves/
        └── <wave_id>/
            ├── index.yaml
            ├── question-clusters/
            └── findings/
```

This subtree is still part of the semantic map and therefore remains non-durable
wiki content.

### 7.2 Allowed Ingress Shapes

The agent may choose either write shape:

- `question-cluster`
- `finding`

The agent should decide based on semantic coupling:

- use `question-cluster` when 2-3 tightly related questions share evidence and
  should be reviewed together
- use `finding` when one conclusion is already stable enough to stand alone

The agent must explain the chosen granularity inside the ingress record.

### 7.3 Ingress Content Model

Each ingress record should capture the minimum semantic structure that proved
useful in the current semantic-map approach, without requiring full governance
ceremony.

Required sections:

- `Questions`
- `Candidate Conclusions`
- `Primary Semantic Sources`
- `Supporting Witness Sources`
- `Possible Non-Equivalences`
- `Proxy Usage Refs`
- `Open Points`
- `Promotion Recommendation`

The ingress layer is not a scratchpad.

It should contain half-finished but discussion-ready semantic conclusions that
can plausibly advance to the semantic claim layer.

---

## 8. Conservative Promotion Model

### 8.1 Promotion Target

When evidence is sufficient, the skill may automatically create a new file under:

`docs/wiki-bi/_meta/legacy-semantic-map/claims/<wave_id>/semantic/`

This auto-promotion creates a new semantic claim artifact.

It does not directly rewrite canonical semantic files under `semantic/`.

### 8.2 Promotion Gates

Auto-promotion is allowed only when all of the following are true:

- at least one `primary semantic source` exists
- at least one additional supporting witness source exists
- all evidence paths come from `E:\Projects\WorkDataHub`
- the conclusion can be stated as a stable proposition rather than only as an
  unresolved suspicion
- at least one semantic node type can be named confidently
- the remaining open points do not overturn the main conclusion
- no existing-record update or merge is required without user confirmation

This gate should be conservative by default.

False negatives are preferred over premature formalization.

### 8.3 Minimum Promoted Claim Fields

The auto-promoted claim should populate only the minimum stable fields needed to
enter the semantic claim layer:

- `semantic_id`
- `semantic_node_type`
- `title`
- `summary`
- `business_conclusion`
- `primary_source_refs`
- `supporting_source_refs`
- `semantic_authority`
- `non_equivalent_to`
- `open_questions`
- `confidence`
- `last_verified`

More elaborate `proposal_governance` fields should not be generated by default.

They should appear only when the finding has already reached that level of
clarity.

---

## 9. Mechanical Guard Script

The repository-local skill should be paired with a lightweight helper under:

`scripts/legacy_semantic_map/semantic_ingress_guard.py`

This helper must not interpret business semantics.

Its job is limited to mechanical checks and routing hints.

Required responsibilities:

- resolve the active or explicitly requested open wave
- validate that the target wave is writable
- validate that cited evidence paths belong to `E:\Projects\WorkDataHub`
- search for similar ingress records, semantic claims, and semantic canonical
  ids
- report whether auto-promotion is blocked, ready, or requires user review
- return allowed write targets for the current task

The helper should answer:

- where the agent may write
- whether the evidence is structurally valid
- whether overlap or modification risk exists
- whether promotion is structurally allowed

It should not answer:

- what the business semantics mean
- which conclusion is correct
- which semantic boundary is most plausible

---

## 10. Duplicate And Overlap Handling

When the helper detects similar ingress records or semantic claims, the agent
must decide which of these situations applies:

- true duplicate
- partial overlap
- neighboring but distinct semantic boundary

Allowed default responses:

- write a new ingress record
- write a new ingress record marked as suspected duplicate
- stop and ask the user before modifying an existing semantic claim or canonical
  semantic file

The agent must explain why the chosen path is correct.

This rule exists to prevent silent semantic drift in a registry that already
contains partially overlapping findings.

---

## 11. Skill Packaging

The skill should live under:

`E:\Projects\WorkDataHubPro\.codex\skills\wdhp-semantic-ingress/`

Recommended contents:

```text
.codex/skills/wdhp-semantic-ingress/
├── SKILL.md
├── references/
│   ├── ingress-template.md
│   ├── promotion-gates.md
│   └── claim-minimum-fields.md
└── scripts/
    └── semantic_ingress_guard.py
```

Recommended division of responsibility:

- `SKILL.md`
  - trigger description
  - workflow steps
  - boundary rules
- `references/`
  - stable human-readable rules and templates
- `scripts/`
  - dynamic route, overlap, and promotion checks

This keeps the skill small in-context while still giving it deterministic help
where determinism is useful.

---

## 12. Workflow

The skill should execute the following sequence:

1. accept one or more tightly related semantic questions, plus optional `wave_id`
2. call the ingress guard helper
3. read only legacy evidence from `E:\Projects\WorkDataHub`
4. decide whether the ingress unit should be a question cluster or a finding
5. write the ingress record and update the ingress index for that wave
6. call the ingress guard helper again for promotion evaluation
7. if all conservative gates pass, create a new semantic claim file
8. if overlap requires modification of existing formal records, stop and ask the
   user

This workflow is intentionally narrow.

It should produce better semantic-map coverage, not a second general-purpose
governance or wiki-maintenance workflow.

---

## 13. Acceptance Criteria

This design should be considered valid only when:

- the skill writes only inside `legacy-semantic-map`
- ingress records are materially lighter than full claim authoring
- business-semantic evidence remains legacy-only
- the helper provides routing and guardrails without performing semantic
  interpretation
- auto-promotion remains conservative and avoids premature formalization
- existing semantic claims and canonical semantic files are not silently edited
- the design does not create a dependency loop from `WorkDataHubPro` wiki
  content back into legacy semantic evidence

---

## 14. Final Position

`legacy-semantic-map` should remain the destination for legacy business-semantic
discovery, but it should gain a lighter ingress front door.

The right model is not to replace the semantic map with free-form notes, and not
to force every discovery through the full current claim/governance burden.

The right model is:

- lightweight ingress for discovery
- conservative promotion into semantic claims
- continued human control over formal record correction and merge decisions

That model preserves the semantic discipline of the existing map while making it
realistic for an LLM-driven workflow to expand legacy semantic coverage.
