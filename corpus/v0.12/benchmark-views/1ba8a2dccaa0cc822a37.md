# Axiom corpus record pair — benchmark-only provenance view
This is NOT a paper-aligned latent diagnostic or a compiler-verified training example. Labels are distinguished from checker observations.

language: axiom_prolog
split: train
family: logic/proof/member-index
valid_record_id: axiom_prolog:prolog_proof_member:7:valid:none
invalid_record_id: axiom_prolog:prolog_proof_member:7:invalid:banned_cut

## Canonical record labelled valid

```axiom_prolog
%!pproofmem7(+Elem,+List,-Index).
pproofmem7(Elem,[Elem|_],0).
pproofmem7(Elem,[_|T],N) :- pproofmem7(Elem,T,N0), N is N0+1.
```

## Canonical record labelled invalid

```axiom_prolog
%!pproofmem7(+Elem,+List,-Index).
pproofmem7(Elem,[Elem|_],0) :- !.
pproofmem7(Elem,[_|T],N) :- pproofmem7(Elem,T,N0), N is N0+1.
```

## Label metadata (not inherently checked)

recorded_diagnostic_codes: ["BANNED_CUT"]

## Recorded static checker result

validation_static_json: {"clause_count": 2, "diagnostics": ["BANNED_CUT", "NON_DECREASING_RECURSIVE_CALL", "NONGROUND_ARITHMETIC_RHS"], "mode_count": 1, "status": "fail"}
