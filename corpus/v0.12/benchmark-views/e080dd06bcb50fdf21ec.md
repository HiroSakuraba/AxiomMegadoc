# Axiom corpus record pair — benchmark-only provenance view
This is NOT a paper-aligned latent diagnostic or a compiler-verified training example. Labels are distinguished from checker observations.

language: axiom_ml
split: dev
family: typed/option/handling
valid_record_id: axiom_ml:ml_option_map:7:valid:none
invalid_record_id: axiom_ml:ml_option_map:7:invalid:non_exhaustive_pattern

## Canonical record labelled valid

```axiom_ml
(* @effect: pure *)
(* @recursive: none *)
fun moptionmap7 (x:int option) : int option =
  case x of NONE => NONE | SOME v => SOME(v+1)
```

## Canonical record labelled invalid

```axiom_ml
(* @effect: pure *)
(* @recursive: none *)
fun moptionmap7 (x:int option) : int option =
  case x of NONE => NONE
```

## Label metadata (not inherently checked)

recorded_diagnostic_codes: ["NON_EXHAUSTIVE_PATTERN_MATCH"]

## Recorded static checker result

validation_static_json: {"datatype_count": 0, "diagnostics": ["NON_EXHAUSTIVE_OPTION_MATCH", "SINGLE_BRANCH_CASE"], "function_count": 1, "status": "fail"}
