<AXIOM_MEGADOC id="md_ed3f2b94aa2b" construction="runtime_trace" split="train" languages="scheme" corpus="v0.9D">

<SEGMENT type="task" trust="explanatory" provenance="rationale_template">
Execute the AxiomScheme function on a concrete input. Lane: Guile.
</SEGMENT>

<SEGMENT type="source" trust="canonical" provenance="record" record_id="axiom_scheme:scheme_list_sum:9:valid:none">
```scheme
(define (slist_sum9 xs)
  (@effect pure)
  (@resource none)
  (@recursive structural)
  (if (null? xs)
    0
    (+ (car xs) (slist_sum9 (cdr xs)))))
```
</SEGMENT>

<SEGMENT type="expected_io" trust="extracted" provenance="extractor" record_id="axiom_scheme:scheme_list_sum:9:valid:none">
input_expr: '(9 1 2)
function_call: (slist_sum9 '(9 1 2))
</SEGMENT>

<SEGMENT type="runtime_result" trust="checked" provenance="extractor" record_id="axiom_scheme:scheme_list_sum:9:valid:none">
lane: scheme
status: pass
stdout: 12
expected_value_json: {"type":"int","value":12}
</SEGMENT>

</AXIOM_MEGADOC>