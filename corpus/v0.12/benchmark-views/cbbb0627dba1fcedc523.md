# Axiom corpus record pair — benchmark-only provenance view
This is NOT a paper-aligned latent diagnostic or a compiler-verified training example. Labels are distinguished from checker observations.

language: axiom_prolog
split: train
family: logic/tree/path
valid_record_id: axiom_prolog:prolog_tree_path:8:valid:none
invalid_record_id: axiom_prolog:prolog_tree_path:8:invalid:unsafe_negation

## Canonical record labelled valid

```axiom_prolog
%!ptree_path8(+Node,+Tree,-Path).
ptree_path8(Node,node(Node,Left,Right),[Node]).
ptree_path8(Node,node(Root,Left,Right),[Root|Path]) :- ptree_path8(Node,Left,Path).
```

## Canonical record labelled invalid

```axiom_prolog
%!ptree_path8(+Node,+Tree,-Path).
ptree_path8(Node,node(Node,Left,Right),[Node]).
ptree_path8(Node,node(Root,Left,Right),[Root|Path]) :- ptree_path8(Node,Left,Path).
ptree_path8(X) :- \+ other(X).
```

## Label metadata (not inherently checked)

recorded_diagnostic_codes: ["UNSAFE_NEGATION_WITH_VARIABLES"]

## Recorded static checker result

validation_static_json: {"clause_count": 3, "diagnostics": ["SINGLETON_VARIABLE:Left", "SINGLETON_VARIABLE:Right", "NON_DECREASING_RECURSIVE_CALL", "MODE_ARITY_MISMATCH", "UNSAFE_NEGATION_WITH_VARIABLES"], "mode_count": 1, "status": "fail"}
