# Axiom corpus record pair — benchmark-only provenance view
This is NOT a paper-aligned latent diagnostic or a compiler-verified training example. Labels are distinguished from checker observations.

language: axiom_scheme
split: train
family: functional/list/parity
valid_record_id: axiom_scheme:scheme_even_length:4:valid:none
invalid_record_id: axiom_scheme:scheme_even_length:4:invalid:semantic_mismatch

## Canonical record labelled valid

```axiom_scheme
(define (seven_length4 xs)
  (@effect pure)
  (@resource none)
  (@recursive structural)
  (if (null? xs)
    #t
    (not (seven_length4 (cdr xs)))))
```

## Canonical record labelled invalid

```axiom_scheme
(define (seven_length4 xs)
  (@effect pure)
  (@resource none)
  (@recursive structural)
  (if (null? xs)
    #f
    (not (seven_length4 (cdr xs)))))
```

## Label metadata (not inherently checked)

recorded_diagnostic_codes: ["SEMANTIC_WRONG_BOOLEAN_BASE"]

## Recorded static checker result

validation_static_json: {"diagnostics": [], "status": "pass"}
