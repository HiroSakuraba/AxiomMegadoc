# Axiom corpus record pair — benchmark-only provenance view
This is NOT a paper-aligned latent diagnostic or a compiler-verified training example. Labels are distinguished from checker observations.

language: axiom_prolog
split: dev
family: logic/dcg/token-run
valid_record_id: axiom_prolog:prolog_dcg_run:9:valid:none
invalid_record_id: axiom_prolog:prolog_dcg_run:9:invalid:extra_clause

## Canonical record labelled valid

```axiom_prolog
%!pdcgrun9(+S0,-S,+T,-N).
pdcgrun9(S,S,_,0).
pdcgrun9([T|S0],S,T,N) :- pdcgrun9(S0,S,T,N0), N is N0+1.
```

## Canonical record labelled invalid

```axiom_prolog
%!pdcgrun9(+S0,-S,+T,-N).
pdcgrun9(S,S,_,0).
pdcgrun9([T|S0],S,T,N) :- pdcgrun9(S0,S,T,N0), N is N0+1.
pdcgrun9([_|S],S,_,0).
```

## Label metadata (not inherently checked)

recorded_diagnostic_codes: ["SEMANTIC_EXTRA_CLAUSE"]

## Recorded static checker result

validation_static_json: {"clause_count": 3, "diagnostics": ["NONGROUND_ARITHMETIC_RHS"], "mode_count": 1, "status": "fail"}
