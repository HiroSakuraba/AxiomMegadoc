# Axiom corpus record pair — benchmark-only provenance view
This is NOT a paper-aligned latent diagnostic or a compiler-verified training example. Labels are distinguished from checker observations.

language: axiom_prolog
split: train
family: logic/tree/path
valid_record_id: axiom_prolog:prolog_tree_path:0:valid:none
invalid_record_id: axiom_prolog:prolog_tree_path:0:invalid:semantic_expected_mismatch

## Canonical record labelled valid

```axiom_prolog
%!ptree_path0(+Node,+Tree,-Path).
ptree_path0(Node,node(Node,Left,Right),[Node]).
ptree_path0(Node,node(Root,Left,Right),[Root|Path]) :- ptree_path0(Node,Left,Path).
```

## Canonical record labelled invalid

```axiom_prolog
%!ptree_path0Bad(+Node,+Tree,-Path).
ptree_path0Bad(N,node(N,L,R),[N]).
ptree_path0Bad(N,node(Rt,L,R),[Rt|P]) :- ptree_path0Bad(N,L,P).
```

## Label metadata (not inherently checked)

recorded_diagnostic_codes: ["SEMANTIC_EXPECTED_OUTPUT_MISMATCH"]

## Recorded static checker result

validation_static_json: {"clause_count": 2, "diagnostics": ["SINGLETON_VARIABLE:L", "SINGLETON_VARIABLE:R", "NON_DECREASING_RECURSIVE_CALL"], "mode_count": 1, "status": "fail"}
