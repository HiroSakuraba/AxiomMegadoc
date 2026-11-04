# Axiom corpus record pair — benchmark-only provenance view
This is NOT a paper-aligned latent diagnostic or a compiler-verified training example. Labels are distinguished from checker observations.

language: axiom_prolog
split: train
family: logic/list/length
valid_record_id: axiom_prolog:prolog_length_rel:7:valid:none
invalid_record_id: axiom_prolog:prolog_length_rel:7:invalid:wrong_arithmetic_step

## Canonical record labelled valid

```axiom_prolog
%!plength7(+List,-N).
plength7([],0).
plength7([_|T],N) :- plength7(T,N0), N is N0+1.
```

## Canonical record labelled invalid

```axiom_prolog
%!plength7(+List,-N).
plength7([],0).
plength7([_|T],N) :- plength7(T,N0), N is N0+2.
```

## Label metadata (not inherently checked)

recorded_diagnostic_codes: ["SEMANTIC_WRONG_STEP"]

## Recorded static checker result

validation_static_json: {"clause_count": 2, "diagnostics": ["NONGROUND_ARITHMETIC_RHS"], "mode_count": 1, "status": "fail"}
