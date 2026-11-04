# Versioned AxiomMegaDoc datasets

The [v0.12 corpus](v0.12/) is published as individual GitHub-browsable files. It is generated from the repository's original `axiom_megadoc_v0_11.zip` by `src/build_v012.py`.

**Content:** 20 verified megadocs (17 narrowly applicable latent diagnostics and three runtime-executed examples), 260 explicitly nontraining provenance views, 520 source records, 20 typed attribute sidecars, train/dev/test JSONL streams, and a provenance manifest. There are **824 generated files** in total.

**Manifest SHA-256:** `665aee08fd8188f1fb78430a062a0decef816a8b80c7d4cc731a630f049e3ce9`

**Original archive SHA-256:** `c2eca398b99ce5f6cbc0806287432bcd32e1f47f9100b72c244882f69b1cd8dd`

**Runtime versions:** Guile 3.0.9, MLton 20210117+dfsg-3, SWI-Prolog 9.0.4. The `runtime_trace` documents were executed and checked against the ledger's expected outputs.

The [publication workflow](../.github/workflows/publish-v012-corpus.yml) regenerates the dataset and verifies its exact manifest against the previously validated artifact before committing to the review branch.

**Trust boundaries:** All `benchmark-views/` files are benchmark-only, not compiler-verified training examples. There are no claims of measured pretraining benefit, external evaluation, or real filesystem cache performance.
