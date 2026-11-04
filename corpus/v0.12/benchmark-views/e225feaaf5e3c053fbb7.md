# Axiom corpus record pair — benchmark-only provenance view
This is NOT a paper-aligned latent diagnostic or a compiler-verified training example. Labels are distinguished from checker observations.

language: axiom_scheme
split: dev
family: functional/list/sum
valid_record_id: axiom_scheme:scheme_list_sum:8:valid:none
invalid_record_id: axiom_scheme:scheme_list_sum:8:invalid:banned_mutation

## Canonical record labelled valid

```axiom_scheme
(define (slist_sum8 xs)
  (@effect pure)
  (@resource none)
  (@recursive structural)
  (if (null? xs)
    0
    (+ (car xs) (slist_sum8 (cdr xs)))))
```

## Canonical record labelled invalid

```axiom_scheme
(define (slist_sum8 xs)
  (@effect pure)
  (set! xs xs)
  (@resource none)
  (@recursive structural)
  (if (null? xs)
    0
    (+ (car xs) (slist_sum8 (cdr xs)))))
```

## Label metadata (not inherently checked)

recorded_diagnostic_codes: ["BANNED_SET_MUTATION"]

## Recorded static checker result

validation_static_json: {"diagnostics": ["BANNED_SET_MUTATION", "MISSING_RECURSIVE_ANNOTATION", "MISSING_RESOURCE_ANNOTATION"], "status": "fail"}
