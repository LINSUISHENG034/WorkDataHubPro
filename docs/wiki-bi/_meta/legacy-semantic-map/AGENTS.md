# Legacy Semantic Map Guidance

This `AGENTS.md` governs the `docs/wiki-bi/_meta/legacy-semantic-map/` subtree.

## Purpose

- Treat this subtree as a structured discovery ledger for legacy semantic mapping.
- Do not treat it as durable wiki content.
- Do not add it to `docs/wiki-bi/index.md`.

## What the tooling is good at

- Capturing semantic findings from legacy evidence in a structured, compilable form.
- Preserving cross-source business meaning such as:
  - concept boundaries
  - rule definitions
  - non-equivalences
  - lifecycle distinctions
  - source-family splitting
- Turning accepted claim artifacts into canonical semantic-map outputs and reports.

## What the tooling is not

- It is not a fully automatic repo-mining engine.
- It is not a substitute for human semantic judgement.
- It does not discover good claims by itself; the hard part is still:
  - choosing evidence
  - framing the claim
  - naming the semantic node
  - deciding the durable target page

## Recommended working model

- Use this subtree as a semi-automatic semantic extraction pipeline.
- Start from a bounded execution path, subsystem, or mapping question rooted in real runtime flow, not from a top-down semantic checklist.
- Prefer one bounded semantic claim at a time.
- Favor strong primary evidence from the legacy repo:
  - `legacy_config`
  - `legacy_doc`
  - `legacy_code`
- Use current wiki pages as supporting witnesses or durable targets, not as the main source of truth for legacy meaning.

## Discovery ordering

- Keep discovery execution-first.
- Do not begin Phase A discovery from a predeclared "key semantics" list and then force findings into it.
- Do not let current wiki structure or desired durable page layout lead the first-pass discovery process.
- Let execution paths, adjacent runtime surfaces, source families, and discovered boundary issues produce the semantic findings.
- Treat semantic concepts, rules, non-equivalences, lifecycles, fact families, and decision anchors as the canonical synthesis layer after discovery evidence has been gathered.

## Derived semantic inventory rule

- A "key semantic inventory" is valid only as a derived view built from accepted execution-first findings.
- It must not replace execution-first discovery as the primary exploration method.
- It may be used later for:
  - synthesis
  - completeness review
  - durable wiki absorption planning
  - identifying remaining open questions or missing semantic node families
- Prefer bottom-up semantic inventory derivation over top-down semantic checklisting.

## Canonical promotion threshold

- Do not promote a semantic finding into a stable canonical object only because it appears frequently in runtime usage.
- Do not reject a semantic boundary only because legacy runtime surfaces use a shortcut, proxy, or mixed operational label.
- Promote a semantic rule or non-equivalence into stable canonical form only when the business meaning and the conflicting proxy usage are both explained.

### Minimum threshold for stable canonical promotion

- At least one `authoritative_semantic_source` must directly define or strongly constrain the business meaning.
- At least one independent supporting source or runtime witness must show that the distinction matters for accepted projection, status, output, or durable semantic interpretation.
- If conflicting proxy usage exists in legacy runtime surfaces, the map must explicitly explain that usage as one of:
  - operational shortcut
  - historical drift
  - scope-limited alias
  - still-unresolved contradiction
- High-priority open questions that would change rebuild, defer, or retire decisions must be resolved before stable canonical promotion.
- Stub-only, mirror-only, or helper-only primary sources must not be the highest-authority basis for accepted semantic canonical output.

### Must remain claim-level or contested when

- there is only a definition source, but no accepted downstream witness showing why the distinction matters
- there is only high-frequency runtime usage, but no authoritative source defining the semantic meaning
- strong semantic sources and high-frequency runtime usage conflict, but the conflict has not been explained
- unresolved questions would materially change slice admission, defer, retire, or durable wiki absorption decisions

### Practical interpretation

- Frequent runtime proxy usage is evidence, but not semantic authority by itself.
- Projection-, status-, and output-adjacent evidence should generally outrank operator convenience or implementation-local shortcuts when the question is about business meaning.
- A stable canonical object should let a later maintainer explain both:
  - what the business semantic boundary is
  - why legacy runtime usage may have looked different without overturning that boundary

## Agent decision authority

- Agents may auto-adjudicate semantic proposals.
- Agents must not finalize shared governance truth.
- Proposal-making and final acceptance are different responsibilities.

### Agents may do without additional human confirmation

- read execution paths, runtime surfaces, source files, and adjacent evidence
- write or update claim artifacts under `claims/<wave_id>/`
- recommend whether a finding should be treated as:
  - stable canonical candidate
  - contested semantic candidate
  - claim-level only
- write semantic rationale, business conclusions, non-equivalence proposals, and proxy-usage explanations
- write governance implication analysis for:
  - slice admission
  - defer candidates
  - retire candidates
  - durable wiki absorption impact
- run temporary-copy compilation and reporting loops for local validation

### Agents may propose, but must not finalize

- formal promotion of a finding into checked-in shared canonical semantic state
- formal classification of a checked-in semantic object as canonical, contested, absorbed, deferred, or retired
- formal updates to coverage matrices, refactor-program states, or other governance baselines
- formal slice admission, slice exclusion, defer, or retire decisions
- formal wave closeout, archive-ready, or absorption-complete decisions

### Required interpretation

- `defer candidate` does not mean `deferred`
- `retire candidate` does not mean `retired`
- `recommended canonical` does not mean checked-in canonical truth
- `recommended contested` does not mean the shared registry has been formally marked contested

### Preferred status language

When an agent is making a recommendation rather than a final decision, prefer wording such as:

- `recommended stable canonical`
- `recommended contested`
- `defer candidate`
- `retire candidate`
- `absorption-ready candidate`

Do not use final governance wording unless the main thread has actually accepted and recorded that decision.

## Minimal verified loop

The smallest useful loop verified in this repository is:

1. Copy the semantic-map registry to a temporary directory.
2. Read one or two real legacy sources from `E:\Projects\WorkDataHub`.
3. Write one new claim under the active open wave.
4. Compile that new claim together with the wave's existing accepted claims.
5. Generate reports.
6. Re-run once to confirm the output stabilizes.

This loop was successfully used to extract a customer-status semantic rule from:

- `config/customer_status_rules.yml`
- `docs/business-background/客户主数据回填与状态来源分析.md`

## Important operational lessons

- Prefer temporary registry copies for first-pass probing.
- Promote validated claims back into the checked-in registry only after the claim shape, compilation result, and report behavior are confirmed.
- Do not mutate checked-in canonical files during first-pass probing.
- Compile the new claim together with the wave's existing accepted claims, not in isolation.
- Expect the first integrity report after adding a new accepted claim to possibly show:
  - `mutable_accepted_claims_detected`
- This can be a normal warm-up effect when the accepted-claim set changes.
- Re-running the same inputs should remove that immutability warning if the claim set is now stable.
- Coverage and compiled semantic files should remain stable across repeated runs with unchanged inputs.

## Interpretation of report signals

- `wave_status = green` means the compiled registry is mechanically healthy for the current denominator.
- It does not mean the semantic work is complete.
- `durable_wiki_targets_not_accepted` and `findings_disposition_incomplete` are workflow-governance blockers, not compilation failures.
- Treat integrity results as workflow signals, not only as technical pass/fail output.

## Completion model

- Do not treat whole-repository file sweep as the primary completion definition.
- For this tool, discovery closure is wave-scoped and denominator-scoped first.
- Broader semantic completeness should be judged from the derived semantic inventory that emerges from execution-first work, not from a pre-authored semantic checklist.
- A stable semantic-inventory view is a downstream acceptance surface, not an upstream discovery driver.

## Authoring expectations

- Keep claims specific and evidence-backed.
- Prefer semantic precision over breadth.
- Record business conclusions in clear English even when the source evidence is Chinese.
- Avoid collapsing distinct meanings into one node just to reduce artifact count.
- If two business notions are "not the same thing", prefer explicit non-equivalence or separate semantic nodes.

## Safety rules

- Distributed agents may write only under `claims/<wave_id>/`.
- Canonical registry files are main-thread-managed.
- Canonical compilation is a main-thread-only operation.

## Documentation style

- Keep this subtree's guidance compact and operator-focused.
- Capture reusable lessons here only after a loop has been actually verified.
- Do not add speculative rules that have not been tested against real legacy evidence.
