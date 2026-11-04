# AxiomMegaDoc v0.12 — reproducible, checker-grounded corpus

This branch adds the first **materialized corpus** generator to the original v0.11 milestone, using the **original builder and v0.9D ledger inside the committed ZIP** without altering their source bytes.

The v0.11 work has two construction families:
- \`latent_diagnostic\`: the paper-aligned construction, with a structural source split and explanatory rationale, followed by a canonical invalid contrast and diagnostics.
- \`runtime_trace\`: an independently motivated construction requiring actual successful execution in Guile, MLton or SWI-Prolog.

This **first v0.12 batch emits strictly verified latent_diagnostic documents** from the three source families that the v0.11 rationale templates actually describe (Scheme list sum, ML list sum, Prolog deterministic append). It also exports **benchmark-only paired provenance views** of the wider corpus; these do not carry a synthetic rationale, do not claim checked semantic-error labels, and must not be used as training ground truth. It **does not fake or replay runtime output**. See the main README for the distinction between the original paper and the Axiom instantiation. A static checker failure is not an empirically validated pretraining effect.

## Generate locally

\`\`\`sh
python3 src/build_v012.py --output /tmp/axiom-megadocs-v012
python3 -m unittest discover -s tests -p 'test_*.py' -v
\`\`\`

Uses Python standard library only; no language runtimes required. The output must be empty, and no source repository files are modified.

Output:
- \`megadocs/*.md\`: long structured canonical and rationale segments.
- \`attributes/*.json\`: provenance, language/split, hash, validation and source IDs.
- \`records/*.json\`: immutable byte-preserving JSON representations of the selected ledger records.
- \`streams/{train,dev,test}.jsonl\`: a per-split JSONL document stream suitable for corpus/file-system access-pattern experiments.
- \`manifest.json\`: input archive/ledger/builder SHA-256, per-file hashes, counts and exact skip-reason tallies.

**Ground truth gate:** A latent diagnostic is only admitted when the original invalid record has \`validation.static.status == "fail"\` and its claimed diagnostic codes appear in \`validation.static.diagnostics\`. A semantic error label with static status \`pass\` is not given \`checked\` trust. Source hashes, split-group keys, exact source reassembly and render/parse round-trip are also checked.

**Scale limit:** Source has 520 atomic records (260 valid–invalid pairs), not the proposed 5,000. The generator does not duplicate/fabricate examples to manufacture size. The broadened benchmark views are not an expanded validated training corpus. The approximate word count in manifests is a Python whitespace count **not a tokenizer measurement**; no model training or external evaluation is claimed.

CI builds the corpus from the pinned ZIP and uploads it as a workflow artifact. BFS-NG should benchmark **both generated documents and source-record/attribute lookups**; storing the generated data inside BFS-NG Git is intentionally avoided.

## Important remaining work

1. Expand family-specific rationale templates **only after** semantic obligations are independently checked. The current strict whitelist prevents unrelated source families inheriting false task descriptions.
2. Add a separately validated runtime-trace tranche which verifies runtime output against expected values and records runtime versions.
3. Scale the underlying corpus using real validated generators, then run compute-matched atomic-vs-megadoc model experiments with external evaluation.
