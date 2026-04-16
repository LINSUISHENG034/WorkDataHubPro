# WorkDataHub Legacy Semantic Map Design

Date: 2026-04-16
Status: Proposed Design
Target Workspace: `E:\Projects\WorkDataHubPro`
Legacy Source Workspace: `E:\Projects\WorkDataHub`

---

## 1. Purpose

This document defines a discovery-first semantic mapping system for the legacy
`WorkDataHub` repository.

The goal is not to write wiki pages directly. The goal is to create a structured,
machine-friendly semantic map that lets agents and subagents:

- discover legacy business semantics without being led by current wiki structure
- parallelize source analysis without repeatedly rediscovering the same runtime paths
- track what has already been mapped, what remains unmapped, and what boundary issues were found
- hand off a structured semantic inventory to a later `Phase B: consume/absorb` workflow that decides what belongs in `docs/wiki-bi/`

This map is an internal discovery ledger, not a durable wiki content asset.

`docs/wiki-bi/` remains the only long-term human-facing knowledge layer.

The semantic map exists to help `wiki-bi` cover legacy business semantics that
would otherwise remain buried in implementation details.

Once the relevant wiki coverage is complete and the absorption wave is closed,
the semantic map may be archived.

---

## 2. Design Goals

- maximize coverage of legacy semantic surfaces before making wiki-consumption decisions
- make agent work parallelizable with low merge conflict risk
- favor execution-truth and source coverage over directory aesthetics
- preserve traceability from discovered semantic objects back to legacy source files
- make missing coverage mechanically visible
- keep the semantic map close enough to `wiki-bi` that discovery and absorption do not drift apart
- let subsystem boundaries evolve through structured candidate backfill instead of requiring a perfect up-front decomposition

When these goals conflict, coverage and traceability take precedence over early neatness.

---

## 3. Non-Goals

This design does not:

- decide which findings become durable wiki pages
- classify findings into final wiki categories such as concept, standard, surface, or evidence
- adjudicate whether a legacy behavior should be retained, deferred, or retired in `WorkDataHubPro`
- optimize for a compact human-only narrative format
- require early semantic certainty before recording an object
- create a second durable knowledge layer that competes with `docs/wiki-bi/`
- require the semantic map to remain a permanently maintained artifact after the relevant absorption wave closes
- replace the existing `wiki-bi` index, log, lint, or durable page model

Those actions belong to a later `Phase B: consume/absorb` workflow.

---

## 4. Core Design Decision

The semantic map uses a three-layer model:

1. execution graph
2. subsystem graph
3. semantic object graph

The execution graph is the primary discovery axis.

The subsystem graph is the primary parallel work axis.

The semantic object graph is the primary downstream consumption axis.

This ordering is intentional:

- execution paths show what the system truly does
- subsystems give agents stable parseable responsibility zones
- semantic objects become the durable units that can later be consumed by wiki updates

---

## 5. Placement And Boundary Rule

The semantic map should live under:

`docs/wiki-bi/_meta/legacy-semantic-map/`

This location is intentional because the map is operationally upstream of
`wiki-bi` absorption, but the location does not change its artifact class.

The semantic map is a machine-facing discovery ledger stored adjacent to the
wiki schema, not a durable wiki page family.

Therefore:

- files under `docs/wiki-bi/_meta/legacy-semantic-map/` are not durable wiki content
- they do not enter the durable page catalog in `docs/wiki-bi/index.md`
- they do not require ordinary concept, standard, domain, surface, or evidence page templates
- they do not need human-facing prose optimization beyond what is required for safe agent and maintainer review
- they are excluded from ordinary durable-page lint expectations except where a dedicated semantic-map rule says otherwise
- they may be linked from `_meta` governance documents when useful, but they must not become the primary answer surface for business-semantic questions once absorption is complete
- `docs/wiki-bi/_meta/wiki-maintenance-lint-checklist.md` must explicitly exclude this subtree from durable-page reachability and template checks
- `docs/wiki-bi/index.md` must never catalog this subtree, even when `_meta` governance docs mention it
- `docs/wiki-bi/_meta/legacy-semantic-map/README.md` must declare the active owner, archive trigger, and non-durable boundary so the placement exception stays visible in-tree

The only long-term human-facing knowledge layer remains `docs/wiki-bi/` outside
this semantic-map subtree.

### 5.1 Tooling Boundary Rule

If helper code is needed to seed, validate, compile, or report on the semantic
map, that code should live under:

`scripts/legacy_semantic_map/`

This is intentional:

- semantic-map tooling is temporary wiki-adjacent support code, not `WorkDataHubPro` runtime behavior
- it must not be added under `src/work_data_hub_pro/`
- application modules under `src/work_data_hub_pro/` must not import from `scripts/legacy_semantic_map/`
- the checked-in semantic-map facts remain under `docs/wiki-bi/_meta/legacy-semantic-map/`, while executable helpers stay outside the durable/runtime package tree
- when the absorption work is complete and the semantic map is archived, the related `scripts/legacy_semantic_map/` tooling should be removable without affecting the main application package

### 5.2 Governance Safeguards

The semantic map requires explicit anti-drift safeguards because its path sits
beside durable wiki governance files.

Required safeguards:

- the active owner is the main-thread maintainer for the current semantic-map wave, not a broad `wiki-bi` page-maintenance pool
- `README.md` must restate that the subtree is an internal discovery ledger and name the current wave owner
- `README.md` must define the archive trigger: once the target absorption wave's required durable wiki updates are accepted and remaining map findings are either absorbed, deferred, or retired for that wave, the corresponding semantic-map claims and generated helpers become archive candidates
- if no active semantic-map wave remains, the subtree and `scripts/legacy_semantic_map/` tooling should be eligible for archival or removal together rather than being left as a passive second knowledge layer

---

## 6. Discovery Scope

The search surface is the full legacy repository, not only first-wave domain folders.

However, the map must distinguish between:

- full search visibility
- deep-analysis priority

The whole repository enters the search surface so that important semantic sources
are not excluded early.

Deep analysis priority should start with first-wave-related execution paths and
their adjacent runtime, verification, config, and output surfaces.

Phase A should seed its initial mapping backlog from:

- the first-wave legacy coverage matrix
- the active refactor program cross-cutting tracks
- already accepted or deferred high-signal `wiki-bi` surfaces and evidence clusters

If a discovery falls outside those seeded governance surfaces, it may be
registered immediately only as:

- a source family
- a candidate subsystem
- a candidate object
- a deferred deep-analysis target

It must not silently expand the deep-analysis scope until main-thread triage
admits it.

This means:

- full repository visibility is broad
- first-wave deep analysis is prioritized
- low-priority or adjacent regions may be registered early without receiving the same depth of semantic decomposition in the first pass

---

## 7. Execution Graph Model

### 7.1 Root Structure

The execution graph begins at `execution_entry_surface`, with two top-level
entry families:

- `manual_cli_entrypoints`
- `scheduled_orchestrated_entrypoints`

This avoids over-privileging either manual CLI execution or Dagster/orchestration
execution.

### 7.2 Second-Layer Decomposition

Below each entry family, discovery should first branch by domain or special
runtime surface, not by execution stage.

Examples:

- `annuity_performance`
- `annuity_income`
- `annual_award`
- `annual_loss`
- `company_lookup_queue`
- `reference_sync`
- `customer_mdm`
- other operator-facing or runtime-facing entry surfaces when discovered

### 7.3 Stage Expansion

Inside each path, discovery then expands by execution stage.

Typical stages include:

- command dispatch
- file discovery
- workbook read / sheet merge
- transform / domain processing
- identity / enrichment
- reference derivation / backfill
- load / publication
- post-ETL hooks
- snapshot / status refresh
- validation / parity
- operator artifact generation
- retry / recovery

Stage names are a discovery aid, not a hard-coded universal taxonomy.

### 7.4 Why Execution Is Primary

Execution-first mapping is preferred because it:

- follows real system behavior instead of static folder organization
- makes branching and side effects visible
- reduces the chance that agents get trapped in helper files or implementation-local abstractions
- naturally exposes hook paths, manual operator commands, queue paths, schedules, parity tooling, and output write surfaces

---

## 8. Subsystem Graph Model

### 8.1 Subsystem Definition

A subsystem is the minimum parallelizable semantic responsibility cluster.

It is not:

- a single file
- a whole top-level directory by default
- a wiki-target grouping

It should represent a distinct responsibility zone with:

- a stable semantic scope
- a reasonably concentrated source family
- identifiable inputs, outputs, or runtime surfaces
- enough internal cohesion that one agent can audit it without constantly editing another subsystem's ownership

### 8.2 Boundary Rules

A subsystem boundary is justified when at least most of the following are true:

- the responsibility is semantically distinct
- the primary source set is relatively compact
- the execution graph touches it as a recognizable node or node family
- it owns or influences a meaningful surface, contract, output, or operator flow
- it can be analyzed independently enough to support agent parallelization

### 8.3 Boundary Evolution

The first subsystem list is expected to be incomplete or imperfect.

The design therefore requires:

- seeded subsystems
- candidate subsystem reporting
- main-thread triage and boundary refinement

A subsystem map is not considered broken if it starts incomplete.

It is considered broken if newly discovered subsystem candidates cannot be reported,
tracked, and integrated.

---

## 9. Semantic Object Graph Model

### 9.1 Object Role

A semantic object is any discrete discovered unit of meaning that may later be
consumed by wiki work.

Examples include:

- business statuses
- identity concepts
- config contracts
- output entities
- operator artifacts
- runtime mechanisms
- validation assets

### 9.2 Discovery-First Object Policy

Phase A uses complete registration priority.

That means:

- objects should be recorded once they are named and distinguishable
- strong final adjudication is not required
- source references, confidence, and open questions are required

Phase A must not require that an object already have a stable wiki home.

### 9.3 Inline-Then-Promote Rule

Objects should start inline inside subsystem files or claim artifacts.

An object may be promoted into its own file only when all of the following are true:

- it has a stable name
- it has a clear semantic summary
- it has explicit source references
- it has explicit relationships

In addition, at least one of the following must be true:

- it appears across more than one subsystem
- it has been rediscovered in more than one claim or wave
- it is needed as a first-class downstream absorption unit

Promotion should be conservative. Early map usefulness comes from coverage, not
from creating many standalone object files.

---

## 10. Physical Layout

Recommended structure:

```text
docs/wiki-bi/_meta/legacy-semantic-map/
├── README.md
├── manifest.json
├── execution/
│   ├── entry-surfaces.yaml
│   ├── paths/
│   └── stages/
├── subsystems/
│   ├── index.yaml
│   └── *.yaml
├── objects/
│   ├── index.yaml
│   └── *.yaml
├── edges/
│   ├── execution-to-subsystem.yaml
│   ├── subsystem-to-object.yaml
│   ├── object-to-object.yaml
│   └── source-to-node.yaml
├── sources/
│   ├── index.yaml
│   └── families.yaml
├── candidates/
│   ├── subsystem-candidates.yaml
│   └── object-candidates.yaml
├── claims/
│   └── <wave_id>/
│       ├── execution/
│       ├── subsystems/
│       └── objects/
├── waves/
│   └── index.yaml
└── reports/
    ├── current/
    │   ├── coverage-status.json
    │   └── integrity-status.json
    └── waves/
        └── <wave_id>/
            ├── coverage-status.json
            └── integrity-status.json
```

This is a mixed registry design:

- fact sources are split across files
- claim artifacts are wave-local and append-friendly
- generated summaries live separately from canonical facts
- associated helper code, when needed, lives in `scripts/legacy_semantic_map/` rather than `src/work_data_hub_pro/`

The manifest must not become a second manual fact source.

---

## 11. Registry Ownership Model

The design intentionally separates agent-writable, main-thread-managed, and
generated-only artifacts.

### 11.1 Agent-Writable Artifacts

Distributed agents may write only:

- `claims/<wave_id>/execution/*.yaml`
- `claims/<wave_id>/subsystems/*.yaml`
- `claims/<wave_id>/objects/*.yaml`

These files are task-local claim or delta artifacts.

### 11.2 Main-Thread-Managed Canonical Artifacts

Only the main session may directly update:

- `execution/paths/*.yaml`
- `subsystems/*.yaml`
- `objects/*.yaml`
- `edges/*.yaml`
- `candidates/*.yaml`
- `sources/*.yaml`
- `waves/index.yaml`

This rule keeps canonical state coherent even when many mapping tasks are run in
parallel.

### 11.3 Generated-Only Artifacts

The following files are generated summaries and must not be treated as manual
fact sources:

- `manifest.json`
- `reports/current/*.json`
- `reports/waves/<wave_id>/*.json`

### 11.4 Tooling Artifacts

Helper code that seeds or validates the semantic map:

- may read and write the semantic-map subtree
- belongs under `scripts/legacy_semantic_map/`
- is not part of the `WorkDataHubPro` runtime package boundary
- should be treated as archiveable support tooling tied to the semantic-map lifecycle, not as permanent governance runtime

### 11.5 Claim Lifecycle

Claim artifacts should remain immutable once accepted into a wave closeout.

They are retained for provenance, compile traceability, and later archive review.

Canonical files represent the currently accepted discovery state for the active
wave set. Claim files represent how that state was reached.

---

## 12. Registry Fact Model

### 12.1 Subsystem Files

Each canonical subsystem file should minimally include:

- `subsystem_id`
- `title`
- `status`
- `semantic_scope`
- `source_families`
- `primary_sources`
- `secondary_sources`
- `execution_nodes`
- `owned_surfaces`
- `owned_outputs`
- `discovered_objects`
- `candidate_objects`
- `candidate_subsystems`
- `upstream_dependencies`
- `downstream_dependencies`
- `claim_type`
- `source_type`
- `evidence_strength`
- `coverage_state`
- `open_questions`
- `confidence`
- `last_verified`
- `last_audited_at`

### 12.2 Object Files

Each promoted canonical object file should minimally include:

- `object_id`
- `title`
- `status`
- `object_type`
- `summary`
- `source_refs`
- `seen_in_subsystems`
- `related_objects`
- `claim_type`
- `source_type`
- `evidence_strength`
- `coverage_state`
- `confidence`
- `last_verified`
- `open_questions`

### 12.3 Execution Path Files

Each canonical path file should minimally include:

- `path_id`
- `entry_surface`
- `domain_or_surface`
- `stages`
- `touches_subsystems`
- `touches_outputs`
- `branches_to`
- `rebuild_target_boundary`
- `rebuild_capability`
- `governance_relevance`
- `source_refs`
- `source_type`
- `claim_type`
- `evidence_strength`
- `coverage_state`
- `confidence`
- `last_verified`
- `open_questions`

### 12.4 Candidate Files

Subsystem candidates should minimally include:

- `candidate_id`
- `proposed_name`
- `candidate_type`
- `discovered_from_subsystem`
- `discovered_from_claim`
- `trigger_files`
- `reason`
- `source_type`
- `claim_type`
- `confidence`
- `triage_status`
- `first_seen_wave`
- `last_verified`

Object candidates should use a parallel structure.

### 12.5 Claim Files

Each claim file should minimally include:

- `claim_id`
- `wave_id`
- `claim_scope`
- `claim_target_id`
- `sources_read`
- `objects_discovered`
- `edges_added`
- `candidates_raised`
- `open_questions`
- `compiled_into`
- `submitted_at`

### 12.6 Minimum Discovery Metadata Rule

Every newly recorded discovery unit must have at least:

- source references
- source type
- claim type
- evidence strength
- coverage state
- confidence
- last verified date or explicit `not_yet_verified` marker
- open questions

This keeps Phase A permissive but not untraceable.

---

## 13. Controlled Vocabulary And ID Rules

The semantic map should use explicit controlled vocabularies so that multiple
agents do not invent incompatible states.

### 13.1 `status`

Allowed values:

- `seeded`
- `active`
- `candidate`
- `deferred`
- `archived`

### 13.2 `claim_type`

Allowed values:

- `direct_observation`
- `inferred_from_sources`
- `compiled_summary`
- `open_question`

### 13.3 `source_type`

Allowed values:

- `legacy_doc`
- `legacy_config`
- `legacy_test`
- `legacy_code`
- `current_spec`
- `current_audit`
- `current_wiki`
- `current_reference_asset`

These values intentionally align with the existing `wiki-bi` evidence model where
possible so the later absorption step does not need a separate translation layer.

### 13.4 `evidence_strength`

Allowed values:

- `strong`
- `supporting`
- `weak`

### 13.5 `coverage_state`

Allowed values:

- `seeded`
- `mapped`
- `partial`
- `closed`
- `deferred`

### 13.6 `confidence`

Allowed values:

- `high`
- `medium`
- `low`

### 13.7 `triage_status`

Allowed values:

- `new`
- `accepted`
- `rejected`
- `deferred`
- `merged`

### 13.8 ID Grammar

Use stable lowercase kebab-case identifiers with fixed prefixes:

- `path_id`: `ep-<entry-family>-<surface>-<slug>`
- `subsystem_id`: `ss-<slug>`
- `object_id`: `obj-<slug>`
- `candidate_id`: `cand-<type>-<slug>`
- `claim_id`: `claim-<wave-id>-<slug>`
- `wave_id`: `wave-YYYY-MM-DD-<slug>`

File names should follow the ID when practical so that diff review stays
predictable.

---

## 14. Agent Operating Model

### 14.1 Work Unit

An agent should normally own one of:

- an execution path claim
- a subsystem claim

An agent should not be assigned an arbitrary folder without relation to one of
those map units.

### 14.2 Required Agent Outputs

Every mapping task must produce:

- `sources_read`
- `objects_discovered`
- `edges_added`
- `candidates_raised`

This is mandatory even when the mapping result is small.

### 14.3 Canonical Write Rule

Distributed agents should not write directly into shared canonical registry files.

The parallel write model is:

1. the agent claims one execution path or subsystem
2. the agent writes task-local claim artifacts
3. the main session triages and compiles those artifacts into canonical subsystem, object, edge, and report files

This is required so that parallel discovery remains low-conflict in practice,
not only in theory.

### 14.4 Required Agent Flow

Each mapping task follows this sequence:

1. claim an execution path or subsystem
2. enumerate and read actual source files
3. write or update the task-local claim artifact
4. register discovered objects inline in the task-local artifact
5. add proposed edges
6. raise candidate subsystem or object records when the current map boundary is insufficient

Agents must not silently widen or reinterpret the map without recording the
boundary issue through candidates or open questions.

### 14.5 Main-Thread Triage Model

The main session owns:

- claim compilation into canonical registry files
- candidate subsystem triage
- object promotion decisions
- edge normalization
- manifest regeneration
- integrity and coverage report generation

This keeps distributed discovery and central map governance separate.

---

## 15. Wave Model

The semantic map should operate in explicit audit or absorption-adjacent waves,
not as one unbounded stream of discovery.

### 15.1 Wave Role

A wave is the bounded unit used for:

- seeding discovery scope
- assigning claim work
- measuring candidate staleness
- generating closeout reports
- deciding archive eligibility

### 15.2 Wave Registry

`waves/index.yaml` should register at least:

- `wave_id`
- `title`
- `status`
- `seeded_entry_surfaces`
- `seeded_high_priority_source_families`
- `admitted_subsystems`
- `opened_at`
- `closed_at`

### 15.3 Seed Catalog Rule

Coverage metrics must use explicit seeded denominators.

The authoritative denominator files are:

- `execution/entry-surfaces.yaml` for seeded execution entry coverage
- `sources/families.yaml` for source-family coverage
- `waves/index.yaml` for active wave identity and candidate age calculations

### 15.4 Candidate Staleness Rule

`untriaged_candidate_age_by_wave` should be calculated from:

- the current active wave ordinal in `waves/index.yaml`
- minus the candidate's `first_seen_wave` ordinal

Candidates are stale only relative to explicit wave progression, not by informal
elapsed time alone.

---

## 16. Coverage Strategy

### 16.1 Complete Registration Priority

Phase A optimizes for map coverage, not early cleanliness.

Therefore:

- discovering a semantic object is more important than perfectly classifying it
- discovering that a new subsystem boundary is needed is more important than forcing it into the wrong current subsystem
- broad registration is preferred to silent omission

### 16.2 High-Priority Initial Focus

Initial deep mapping should prioritize first-wave-relevant execution paths and
their adjacent surfaces, including:

- first-wave fact domains
- identity chain
- reference/backfill
- post-ETL hooks
- snapshot/status
- validation/parity
- operator artifacts
- queue/schedule/sync control surfaces
- output entities and schema-bearing write surfaces

### 16.3 Low-Priority Registration

Low-priority or adjacent regions may still be registered early as:

- source families
- adjacent subsystems
- candidate subsystems
- deferred deep-analysis targets

That is acceptable as long as they are visible in the map.

---

## 17. Integrity And Coverage Checks

The map should generate at least these checks:

### 17.1 Source Family Coverage

Every high-priority source family seeded in `sources/families.yaml` must map to
at least one subsystem.

### 17.2 Execution Entry Coverage

Every seeded manual CLI entrypoint and seeded scheduled/orchestrated entrypoint
in `execution/entry-surfaces.yaml` must map to at least one execution path.

### 17.3 Subsystem Source Coverage

Every subsystem must have at least one primary source.

### 17.4 Object Attachment

Every promoted object must attach to at least one subsystem.

### 17.5 Edge Completeness

Newly registered promoted objects should not remain edge-less.

### 17.6 Candidate Drain

Candidate subsystem and object files must not accumulate indefinitely without triage.

### 17.7 Orphan Source Detection

Read source files should not remain unmapped to any node.

### 17.8 Noise Control

Clearly adjacent, low-priority, or one-off materials should be marked as such
instead of being silently treated as core semantic surfaces.

### 17.9 Status Output

Integrity and coverage reporting should produce at least:

- `red`
- `yellow`
- `green`

Interpretation:

- `red`: critical high-priority entry or source families remain unmapped
- `yellow`: mapped but incomplete, candidate-heavy, or weakly connected
- `green`: currently closed for the target wave

### 17.10 Mechanical Metrics

At minimum, reporting should calculate:

- `entrypoint_coverage_pct`
- `high_priority_source_family_coverage_pct`
- `object_edge_coverage_pct`
- `orphan_high_priority_source_count`
- `stale_high_priority_candidate_count`
- `untriaged_candidate_age_by_wave`

Metric denominators must come from the seeded wave inputs, not from ad hoc
human judgment.

### 17.11 Minimum Status Thresholds

For a target wave:

- `green` requires:
  - `entrypoint_coverage_pct = 100`
  - `high_priority_source_family_coverage_pct = 100`
  - `orphan_high_priority_source_count = 0`
  - `object_edge_coverage_pct >= 95`
  - `stale_high_priority_candidate_count = 0`
- `yellow` means:
  - high-priority entry surfaces and source families are mostly mapped, but one or more of the green thresholds is not yet met
  - no critical unmapped high-priority entry surface is being ignored
- `red` means any of:
  - a high-priority entry surface remains unmapped
  - a high-priority source family remains unmapped
  - orphan high-priority sources exist
  - a high-priority candidate has remained untriaged for more than one audit wave

---

## 18. Recommended Implementation Slices

This spec should not be executed as one monolithic implementation plan.

The recommended slice sequence is:

### 18.1 Slice 1: Registry Bootstrap

Scope:

- create the directory structure
- define controlled vocabularies
- define seed catalogs
- define wave registry shape

Success condition:

- the map has stable schemas and seeded denominators before parallel discovery begins

### 18.2 Slice 2: Claim Workflow And Canonical Compiler

Scope:

- implement claim-file creation rules
- implement canonical compilation rules
- enforce ownership boundaries between agent claims and main-thread registries

Success condition:

- parallel claim artifacts can be produced without direct writes into canonical files

### 18.3 Slice 3: Reporting And Wave Closure

Scope:

- implement integrity and coverage reports
- implement candidate staleness calculation
- implement wave closeout and archive readiness checks

Success condition:

- the system can mechanically tell whether a wave is red, yellow, or green

### 18.4 Slice 4: First-Wave Pilot

Scope:

- run the model on a first-wave-biased subset of legacy surfaces
- verify that claim output, canonical compilation, and reporting all work together

Success condition:

- the map proves discovery usefulness without becoming a second durable knowledge layer

### 18.5 Branch Strategy For Multi-Plan Execution

Because these implementation plans are intentionally staged and later slices
depend on earlier semantic-map contracts, they should not all merge directly to
`main` as they complete.

Recommended branches:

- `slice/semantic-map-integration`
- `slice/semantic-map-registry-bootstrap`
- `slice/semantic-map-claim-workflow`
- `slice/semantic-map-reporting-wave-closeout`
- `slice/semantic-map-first-wave-pilot`

The current bootstrap branch may keep its existing historical name
`slice/legacy-semantic-map-registry-bootstrap-closure` if it is already in use.
Do not rename an active branch mid-slice only to match the newer convention.
Apply the `slice/semantic-map-<slice-name>` pattern to new slice branches.

Branch responsibilities:

- `main` remains the clean long-lived branch and does not receive partial semantic-map work
- `slice/semantic-map-integration` is the semantic-map integration baseline and the only pre-`main` branch that should accumulate accepted semantic-map slices
- each slice branch owns one approved implementation plan and should stay narrow to that plan's boundary

### 18.6 Operation Order For Dependent Slices

The semantic-map plans should be executed in this order:

1. implement the earliest required foundation slice on its own branch and verify that slice-specific contracts pass
2. merge that completed slice branch into `slice/semantic-map-integration`, not `main`
3. cut the next dependent slice branch from the current `slice/semantic-map-integration` head rather than from `main` or from another developer's in-flight slice branch
4. complete and verify the next slice on its own branch, then merge it back into `slice/semantic-map-integration`
5. repeat this pattern until all semantic-map plans and their cross-slice fixes are integrated
6. run the full semantic-map acceptance review on `slice/semantic-map-integration`
7. merge `slice/semantic-map-integration` to `main` only after the whole semantic-map package is accepted

Additional guards:

- do not implement new semantic-map features directly on `slice/semantic-map-integration`; use it only for integrating completed slice branches, resolving cross-slice conflicts, and running larger verification
- if a slice changes shared contracts such as `models.py`, manifest shape, or canonical registry schema, avoid opening multiple concurrent slices that edit the same shared contract surface
- if a foundational slice is still volatile, delay downstream slices until the integration baseline stabilizes enough to avoid repeated rebases and schema churn

---

## 19. Relationship To Wiki Consumption

This map is intentionally upstream of wiki maintenance.

`Phase B: consume/absorb` should use the map to answer:

- which semantic objects are stable enough to absorb
- which source families have already been mined
- which open questions still block durable conclusions
- which legacy surfaces are still under-mapped

This keeps discovery and wiki consumption decoupled:

- Phase A builds the semantic inventory
- Phase B decides what to absorb and how

That separation is a core design rule, not an implementation detail.

Additional source-of-truth rules:

- `docs/wiki-bi/` remains the sole durable human-facing knowledge layer
- the semantic map is an internal discovery ledger that feeds `wiki-bi`
- once a finding is absorbed into the durable wiki, agents should prefer the wiki page for future semantic answers unless provenance or coverage-gap review specifically requires consulting the map
- facts absorbed into `wiki-bi` must not require the semantic map to remain a parallel maintained truth source
- once the target absorption wave is accepted and the required wiki updates are complete, the corresponding semantic-map wave may be archived

---

## 20. Risks

### 20.1 Registry Drift

If the manifest becomes a hand-maintained truth source, the map will fork into
two competing realities.

Mitigation:

- keep generated summaries generated
- keep facts in split canonical registry files

### 20.2 Over-Fragmentation

If agents promote objects too early or split subsystems too aggressively, the
map becomes noisy.

Mitigation:

- objects begin inline
- promotion thresholds are explicit
- candidates require central triage

### 20.3 Hidden Omission

If agents only report conclusions and not sources read or candidates raised,
coverage holes become invisible.

Mitigation:

- require `sources_read`, `objects_discovered`, `edges_added`, and `candidates_raised`

### 20.4 Discovery Contaminated By Consumption Goals

If Phase A starts deciding wiki placement too early, the map will be biased by
current wiki structure.

Mitigation:

- prohibit wiki-target classification in Phase A

### 20.5 Path Confusion

If later agents treat `docs/wiki-bi/_meta/legacy-semantic-map/` as durable wiki
content merely because of its path, the repository will grow a second long-lived
knowledge layer.

Mitigation:

- make the placement exception explicit
- exclude the semantic-map subtree from normal durable-page expectations
- archive wave-local claims and reports once absorption closure is complete

---

## 21. Validation Approach

This design should be considered valid only when:

- the execution graph can represent both manual and scheduled entry surfaces
- agents can add discoveries in parallel with low conflict risk
- subsystem candidates can be raised without breaking the registry model
- object promotion from inline to standalone files works without losing source traceability
- integrity reports can mechanically identify unmapped entrypoints, orphan sources, and stalled candidates
- the seeded first-wave governance scope can be mapped without uncontrolled scope expansion
- absorbed findings can move into `docs/wiki-bi/` without forcing long-term dual maintenance of both systems
- the semantic-map subtree can coexist under `docs/wiki-bi/_meta/` without being mistaken for durable wiki content

Early implementation should prove these properties on a first-wave-biased subset
of the legacy repository before broader rollout.

---

## 22. Final Position

The most effective way to build a more complete semantic map of
`E:\Projects\WorkDataHub` is not to start from current wiki pages and not to
start from directory scanning alone.

It is to build a discovery-first semantic map that:

- follows legacy execution paths first
- decomposes findings into parallelizable subsystems
- records semantic objects without early absorption pressure
- keeps source traceability explicit
- evolves subsystem boundaries through structured candidate backfill
- stays close to `wiki-bi` without becoming a second durable wiki

This design should become the discovery layer that later wiki-absorption agents
consume, rather than asking each future agent to rediscover legacy semantics
from scratch.
