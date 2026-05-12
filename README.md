# axiom-megadoc

Long-form, structured training documents built on top of the Axiom Multilingual Corpus (v0.9D). Implements the AxiomMegaDoc v0.11 design: two construction families (`latent_diagnostic`, `runtime_trace`) across all three Axiom languages (Scheme, ML, Prolog), with strict provenance, trust-level tagging, and split-safety inheritance from the underlying atomic records.

This repository is the v0.11 milestone bundle. It contains the design document, a builder implementation, six worked example megadocs (one of each construction per language), a per-example summary report, and validation evidence.

---

## What this is

A megadoc is a single long training document built deterministically from one or more already-validated Axiom records. Megadocs are not new content — they are reorganized views of canonical sources, expected outputs, and verified lane results, with explanatory text inserted in clearly-tagged segments.

There are two construction families in v0.11:

**latent_diagnostic** is the only family that is paper-aligned. It implements the *latent thoughts* construction from Kim & Kotha (2026): a canonical source is split at a structurally meaningful boundary, and a templated rationale articulating the obligation between prefix and suffix is inserted between them. The full document also includes the contrast group — the invalid mutation of the same record, its diagnostic codes, and a templated repair instruction.

**runtime_trace** is independently motivated. It pairs the canonical source with its actual lane execution result on a concrete input: stdout from Guile, MLton, or SWI-Prolog, with expected and observed values surfaced as parallel JSON blocks. The motivation is teaching the source-behavior correspondence explicitly, in line with structured-document pretraining patterns.

The other megadoc families considered in the v0.10 draft — stitched contrast, cross-language semantic, repair ladder, concept chain — are deferred. See `design/axiom_megadoc_v0_11_design.md` Section 4.3 and Section 8 for the reasoning. The short version: stitched contrast can't be tested at 520 atomic records, and cross-language requires a curated semantic mapping that does not yet exist.

---

## What this is *not*

This is not a pre-training corpus at the scale the megadocs paper operates on. The paper trained 300M-parameter models on 200M tokens of real web text with up to 32 generations per document. The Axiom corpus at v0.9D is 520 atomic records, roughly 50K tokens. The v0.11 milestone is infrastructure — schema, builder, validators, examples — not a positive empirical result. The actual megadoc-vs-atomic loss comparison is deferred to v0.12, after corpus scaling.

This is also not a claim that all of the v0.10 megadoc families "work like the paper." Only `latent_diagnostic` is paper-aligned. The framing in the v0.10 draft was overconfident about that analogy; v0.11 corrects it.

---

## Repository layout

```
axiom-megadoc/
  README.md                          (this file)
  design/
    axiom_megadoc_v0_11_design.md    Full v0.11 design document
  src/
    megadoc_builder_batch.py         Multi-language builder
    megadoc_builder_v09d.py          Scheme-only builder (earlier version, retained)
  examples/
    summary.json                     Per-megadoc validation + token counts
    megadocs/
      latent_scheme.md
      latent_ml.md
      latent_prolog.md
      trace_scheme.md
      trace_ml.md
      trace_prolog.md
  source-corpus/
    axiom_v09d_ledger.jsonl          The v0.9D corpus records the megadocs derive from
    axiom_v09d_corpus_README.md      v0.9D origin notes
```

The `source-corpus/axiom_v09d_ledger.jsonl` file is the upstream Axiom corpus. The builder reads from it. None of the megadoc content is invented — every code segment is byte-identical to a record's `canonical_source`, every expected output is byte-copied from the record's `expected_output`, every diagnostic code is byte-copied from the record's `diagnostic_codes`, every runtime output is produced by the installed runtime against the actual source.

---

## Example megadocs in this bundle

Six megadocs, two per language. Token estimates are rough word counts.

| File | Construction | Language | Records used | Tokens |
|---|---|---|---|---|
| `latent_scheme.md` | latent_diagnostic | Scheme | `scheme_list_sum:9:valid` + `scheme_list_sum:9:invalid:missing_base_case` | 188 |
| `latent_ml.md` | latent_diagnostic | ML | `ml_list_sum:0:valid` + `ml_list_sum:0:invalid:wrong_base_case_value` | 222 |
| `latent_prolog.md` | latent_diagnostic | Prolog | `prolog_append_det:0:valid` + `prolog_append_det:0:invalid:semantic_expected_mismatch` | 167 |
| `trace_scheme.md` | runtime_trace | Scheme | `scheme_list_sum:9:valid` (Guile-executed) | 78 |
| `trace_ml.md` | runtime_trace | ML | `ml_list_sum:0:valid` (MLton-compiled) | 82 |
| `trace_prolog.md` | runtime_trace | Prolog | `prolog_append_det:0:valid` (SWI-Prolog-resolved) | 63 |

All six pass the v0.11 validation gates:

- `all_records_same_split` — every record cited shares a split
- `all_canonical_sources_byte_equal` — `prefix + suffix` of the latent_diagnostic reassembles the canonical source byte-for-byte; `source` segment of the runtime_trace equals the canonical source byte-for-byte
- `all_record_refs_resolve` — every `record_id` in a segment resolves to a record in the ledger
- `no_unchecked_source` — code segments carry `trust_level=canonical`; no code is paraphrased or invented
- `rationale_template_ids_known` — every rationale references a registered template

Each megadoc also round-trips through render → parse: the rendered text parses back into the exact segment list it was rendered from. This is checked in the builder.

---

## How to reproduce

The builder reads from `source-corpus/axiom_v09d_ledger.jsonl` and writes to `examples/`. It uses installed runtimes for the runtime_trace family.

```bash
# Requirements
sudo apt install guile-3.0 swi-prolog mlton

# Run
python3 src/megadoc_builder_batch.py
```

The script is self-contained — no external Python packages beyond the standard library. Output is written to `/home/claude/axiom_megadoc_v0_11_batch/` by default; edit the path at the bottom of `megadoc_builder_batch.py` to redirect.

To rebuild against a different upstream corpus version, change the `V09D_LEDGER` constant at the top of the builder. The schema fields used (`record_id`, `canonical_source`, `contrast_group_id`, `split_group_key`, `defect_kind`, `diagnostic_codes`, `semantic`, `expected_output`) are stable across v0.9 sub-versions.

---

## Schema and validation contract

A megadoc is a sequence of typed segments. Each segment carries:

- `segment_type` — `task | source | rationale | expected_io | invalid_mutation | diagnostic | repair | runtime_result`
- `provenance` — `record | extractor | rationale_template`
- `trust_level` — `canonical | checked | extracted | explanatory`
- `record_id` — the source record (or null for headers)
- `rationale_template_id` — the registered template ID (or null)

The trust hierarchy is:
- `canonical` — byte-identical to a record's `canonical_source` field. Never paraphrased.
- `checked` — output of a static checker or runtime lane that has been validated against an expected value.
- `extracted` — deterministic output of a named extractor function (e.g. `expected_output_json`).
- `explanatory` — natural-language rationale text generated from a registered template. Never used as ground truth.

The "no unchecked source" invariant: any segment with `segment_type=source` or `segment_type=invalid_mutation` must have `trust_level=canonical`. The validator enforces this.

The full schema is in `design/axiom_megadoc_v0_11_design.md` Section 3.

---

## Rationale template registry

v0.11 ships three rationale templates, one per language:

| Template ID | Language | Required facts |
|---|---|---|
| `scheme_structural_recursion_obligation_v01` | Scheme | function_name, primary_argument, recursive_annotation, base_predicate |
| `ml_exhaustive_pattern_obligation_v01` | ML | function_name, parameter_type, base_pattern, recursive_pattern |
| `prolog_difference_list_obligation_v01` | Prolog | predicate_name, mode_declaration, base_clause_pattern, recursive_clause_pattern |

A rationale generated from a template must contain every required fact's value as a literal substring. This prevents template-fill bugs from producing rationales that are syntactically valid but semantically about a different program. The validator parses the rendered rationale for the fact tokens and rejects any rationale that doesn't include all of them.

---

## What the next milestone needs

v0.11 is the schema-and-examples milestone. The natural v0.12 work, in priority order:

1. **Scale**: bring the underlying Axiom corpus to 5K records, ≥500K tokens. Without this, the megadoc-vs-atomic experiment cannot be run at meaningful resolution.
2. **External evaluation**: train a small model on `atomic-only` and another on `atomic + latent_diagnostic + runtime_trace` for the same compute budget; continue both on a held-out natural-text corpus (DCLM subset); compare validation-loss trajectories. This is the experiment the megadocs paper actually motivates.
3. **Hyperparameter sweep**: replace the current fixed mixing ratio (which is asserted, not measured) with a local-optimality search over real-stream epochs × megadoc fraction × weight decay × learning rate. Mirror the paper's methodology.
4. **Stitched contrast** as a v0.12 family, once scale supports its evaluation.
5. **Cross-language** as a v0.13 family, after a curated `semantic_object_id` mapping is built.

The plan up to v0.12 is documented in `design/axiom_megadoc_v0_11_design.md` Sections 8 and 10.

---

## Provenance and known limitations

The v0.9D corpus this bundle derives from is itself derived from v0.9B + v0.9C work. The v0.9D `RELEASE_NOTES.md` (included in `source-corpus/`) documents its provenance. The relevant constraint inherited from v0.9D: lane results in the ledger are mostly `status: skipped` because the v0.9D bundle was built in an environment without the runtimes installed. The `runtime_trace` megadocs in this bundle were produced by running the canonical sources against the installed runtimes locally, not by reading lane results from the ledger. This is correct behavior — runtime_trace requires a live runtime — but it means the runtime_trace text is bound to the runtime versions used to produce it (Guile 3.0.9, MLton 20210117+dfsg-3, SWI-Prolog 9.0.4).

The Prolog latent_diagnostic megadoc pairs the variant 0 valid record with the variant 0 invalid record (defect kind `semantic_expected_mismatch`, which is a predicate-rename mutation). The pairing is split-safe because both records share `contrast_group_id` and `split_group_key`. The repair text reflects the rename mutation specifically.

The Scheme latent_diagnostic uses variant 9 of `scheme_list_sum` because variant 9 carries the `missing_base_case` defect, which is the most pedagogically clear demonstration of the recursive-obligation rationale. Other variants would also work but with less directly-corresponding repair text.

---

## License and citation

The design document and builder are MIT-licensed.

If you cite the construction or the framing, please cite Kim et al. 2026 (`arXiv:2603.18534`) for the latent_thoughts paper. The runtime_trace family is independently motivated and is not in any paper.

---

## Repository status

This is a milestone snapshot, not an actively developed mainline. The active development tree is in `axiom_v0_9_patched` (separate repository). Issues and design changes against this snapshot are tracked in the design document changelog (`design/axiom_megadoc_v0_11_design.md` Section 0).
