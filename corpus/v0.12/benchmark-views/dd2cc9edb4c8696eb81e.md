# Axiom corpus record pair — benchmark-only provenance view
This is NOT a paper-aligned latent diagnostic or a compiler-verified training example. Labels are distinguished from checker observations.

language: axiom_prolog
split: dev
family: logic/dcg/ab-star
valid_record_id: axiom_prolog:prolog_dcg_ab:9:valid:none
invalid_record_id: axiom_prolog:prolog_dcg_ab:9:invalid:banned_cut

## Canonical record labelled valid

```axiom_prolog
%!pdcgab9(+S0,-S,-N).
pdcgab9(S,S,0).
pdcgab9([a,b|S0],S,N) :- pdcgab9(S0,S,N0), N is N0+1.
```

## Canonical record labelled invalid

```axiom_prolog
%!pdcgab9(+S0,-S,-N).
pdcgab9(S,S,0).
pdcgab9([a,b|S0],S,N):- !,fail,.
pdcgab9([a,b|S0],S,N) :- pdcgab9(S0,S,N0), N is N0+1.
```

## Label metadata (not inherently checked)

recorded_diagnostic_codes: ["BANNED_CUT"]

## Recorded static checker result

validation_static_json: {"clause_count": 3, "diagnostics": ["BANNED_CUT", "SINGLETON_VARIABLE:S0", "SINGLETON_VARIABLE:S", "SINGLETON_VARIABLE:N", "NONGROUND_ARITHMETIC_RHS"], "mode_count": 1, "status": "fail"}
