# WorkDataHubPro Document Authority Model

Date: 2026-04-14
Status: Active Product-Level Baseline
Scope: How to choose authoritative sources across system docs, wiki, framework docs, and runtime evidence

## 1. Purpose

Different document sets in this repository answer different questions.

This model exists so agents and humans do not:

- confuse framework workflow state with product architecture
- confuse business semantics with implementation status
- confuse planning intent with runtime truth

## 2. Authority Layers

Use this order by question type, not as one flat universal ranking.

### Layer A: Product-Level System Design

Location:

- `docs/system/`

Answers:

- what the system is
- which top-level boundaries are invariant
- what kinds of constraints all frameworks must respect

Use this layer for:

- top-level architecture guidance
- boundary reasoning
- framework-neutral design decisions
- skill default architecture references

### Layer B: Business Semantics And Evidence

Location:

- `docs/wiki-bi/`

Answers:

- what a business concept means
- what counts as correct output
- which surfaces and artifacts are governance objects
- what legacy evidence supports a conclusion

Use this layer for:

- slice-admission constraints
- negative constraints
- operator artifact significance
- semantic review
- acceptance reasoning

### Layer C: Framework-Specific Design And Workflow

Locations:

- `docs/superpowers/`
- `.planning/`
- future framework-specific directories

Current framework-to-skill-family mapping:

- `docs/superpowers/` corresponds to the `using-superpowers` family of skills
- `.planning/` corresponds to the `gsd-*` family of skills

Answers:

- how one framework organizes planning, phases, specs, reviews, and workflow state
- framework-specific execution order
- framework-specific status language

Use this layer for:

- active workflow context
- plan/runbook lookup within that framework
- framework-specific operational questions
- deciding which framework-specific skill family should be active for a given workflow

Do not use this layer as the default product-architecture source.

### Layer D: Runtime Truth

Locations:

- `src/`
- `tests/`
- `config/`
- `reference/`
- committed runbooks

Answers:

- what is actually implemented now
- what is actually tested now
- what replay baselines and assets actually exist now

Use this layer whenever a question depends on:

- current support
- behavior now
- mismatch between docs and implementation

## 3. Conflict Resolution Rules

### 3.1 Product Architecture Conflicts

If `docs/system/` and a framework-specific doc disagree about top-level architecture:

- `docs/system/` wins

### 3.2 Business-Semantic Conflicts

If `docs/wiki-bi/` and a framework-specific doc disagree about business semantics or acceptance meaning:

- `docs/wiki-bi` wins unless runtime evidence disproves the wiki

### 3.3 Current-State Conflicts

If docs disagree with code/tests/config/reference assets about current support:

- runtime truth wins

### 3.4 Framework-State Conflicts

If two framework-specific document sets disagree about workflow status:

- do not let either override Layer A or Layer B
- use runtime truth to resolve actual support
- report the disagreement explicitly instead of guessing

## 4. Reading Patterns By Task

### Architecture Question

Read:

1. `docs/system/`
2. relevant `docs/wiki-bi/` pages
3. runtime truth if the question touches current support

### Slice Admission Or Next-Step Planning

Read:

1. `docs/system/`
2. relevant `docs/wiki-bi/` evidence/domain/standard pages
3. coverage matrix / refactor program
4. runtime truth if needed
5. only then framework-specific planning docs

### Current Status Question

Read:

1. runtime truth
2. framework-specific status docs
3. report conflicts explicitly

Do not answer current-status questions from wiki alone.

### Wiki Maintenance

Read:

1. relevant `docs/wiki-bi/` pages
2. `docs/system/` for top-level consistency
3. runtime truth for implementation-backed evidence

## 5. Rules For Skills

Project skills should follow this default reference pattern:

1. `docs/system/`
2. `docs/wiki-bi/`
3. framework-specific docs only as needed
4. runtime truth when support questions matter

Skills should not default to:

- `.planning/` as the product architecture source
- `docs/wiki-cn/` as the default durable knowledge layer
- one framework's spec directory as if it were the product itself

## 6. Rules For New Frameworks

When a new framework is introduced, it should add its own documents under a distinct framework-specific layer.

It should not:

- replace `docs/system/`
- replace `docs/wiki-bi/`
- redefine the authority model

Instead, it should declare how its own docs map onto:

- system design
- business/evidence knowledge
- runtime truth

## 7. Anti-Patterns

Avoid these mistakes:

- using framework workflow docs as the top-level architecture source
- using wiki pages as proof of current implementation without checking code/tests
- letting one framework's status model redefine product-level priorities
- silently switching from a docs/governance task into implementation because a plan exists
- treating operator-facing artifacts as optional because they are not fact-table fields
