# Promotion Gates

Apply these conservative gates before auto-promotion:

- the target wave resolves to an active writable wave
- every cited source is legacy-only business-semantic evidence from `E:\Projects\WorkDataHub`
- at least one `primary_semantic_sources` entry exists
- at least one `supporting_witness_sources` entry exists
- a promotion draft is present
- `main_conclusion_stable` is `true`
- `open_points_do_not_overturn` is `true`
- `business_conclusion` is non-empty
- `semantic_node_type` is non-empty and valid
- no overlap hit indicates an existing ingress record, semantic claim, or canonical semantic file would need modification

Interpret the helper result conservatively:

- `ready`: promotion may proceed into `claims/<wave_id>/semantic/`
- `blocked`: keep the result as ingress only
- `requires_user_review`: stop and ask before touching formal semantic records
