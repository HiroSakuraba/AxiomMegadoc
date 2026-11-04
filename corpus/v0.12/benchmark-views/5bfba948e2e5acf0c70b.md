# Axiom corpus record pair — benchmark-only provenance view
This is NOT a paper-aligned latent diagnostic or a compiler-verified training example. Labels are distinguished from checker observations.

language: axiom_scheme
split: train
family: functional/list/conditional-count
valid_record_id: axiom_scheme:scheme_count_positive:0:valid:none
invalid_record_id: axiom_scheme:scheme_count_positive:0:invalid:wrong_base_case_value

## Canonical record labelled valid

```axiom_scheme
(define (scpos0 xs)
  (@effect pure)
  (@resource none)
  (@recursive structural)
  (if (null? xs)
    0
    (if (> (car xs) 0)
      (+ 1 (scpos0 (cdr xs)))
      (scpos0 (cdr xs)))))
```

## Canonical record labelled invalid

```axiom_scheme
(define (scpos0 xs)
  (@effect pure)
  (@resource none)
  (@recursive structural)
  (if (null? xs)
    1
    (if (> (car xs) 0)
      (+ 1 (scpos0 (cdr xs)))
      (scpos0 (cdr xs)))))
```

## Label metadata (not inherently checked)

recorded_diagnostic_codes: ["SEMANTIC_WRONG_BASE_CASE"]

## Recorded static checker result

validation_static_json: {"diagnostics": [], "status": "pass"}
