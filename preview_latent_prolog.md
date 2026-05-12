<AXIOM_MEGADOC id="md_143a031dda27" construction="latent_diagnostic" split="train" languages="prolog" corpus="v0.9D">

<SEGMENT type="task" trust="explanatory" provenance="rationale_template">
Append two lists using structural recursion on the first list. The predicate is pappend_det0.
</SEGMENT>

<SEGMENT type="source" trust="canonical" provenance="record" record_id="axiom_prolog:prolog_append_det:0:valid:none">
```prolog
%!pappend_det0(+Left,+Right,-Out).
pappend_det0([],Right,Right).
```
</SEGMENT>

<SEGMENT type="rationale" trust="explanatory" provenance="rationale_template" record_id="axiom_prolog:prolog_append_det:0:valid:none" template="prolog_difference_list_obligation_v01">
The mode declaration %! pappend_det0(+Left,+Right,-Out). fixes which arguments must be ground on entry to pappend_det0. The base clause pattern pappend_det0([],Right,Right). handles the terminal case where the list-structured input has been fully consumed. The recursive clause pappend_det0([Head|Tail],Right,[Head|Out]) :- pappend_det0(Tail,Right,Out). matches one element off the head and recurses on the tail. With the cut excluded and occurs check enabled, this gives a unique proof tree per input.
</SEGMENT>

<SEGMENT type="source" trust="canonical" provenance="record" record_id="axiom_prolog:prolog_append_det:0:valid:none">
```prolog
pappend_det0([Head|Tail],Right,[Head|Out]) :- pappend_det0(Tail,Right,Out).
```
</SEGMENT>

<SEGMENT type="expected_io" trust="extracted" provenance="extractor" record_id="axiom_prolog:prolog_append_det:0:valid:none">
query: pappend_det0([a,b],[c],Out)
expected_solutions_json: [{"Out":{"items":[{"type":"atom","value":"a"},{"type":"atom","value":"b"},{"type":"atom","value":"c"}],"type":"list"}}]
</SEGMENT>

<SEGMENT type="invalid_mutation" trust="canonical" provenance="record" record_id="axiom_prolog:prolog_append_det:0:invalid:semantic_expected_mismatch">
```prolog
%!pappend_det0Bad(+Left,+Right,-Out).
pappend_det0Bad([],R,R).
pappend_det0Bad([H|T],R,[H|O]) :- pappend_det0Bad(T,R,O).
```
</SEGMENT>

<SEGMENT type="diagnostic" trust="checked" provenance="record" record_id="axiom_prolog:prolog_append_det:0:invalid:semantic_expected_mismatch">
SEMANTIC_EXPECTED_OUTPUT_MISMATCH
</SEGMENT>

<SEGMENT type="repair" trust="explanatory" provenance="rationale_template" record_id="axiom_prolog:prolog_append_det:0:invalid:semantic_expected_mismatch">
Restore the predicate name so the query in the driver resolves correctly.
</SEGMENT>

</AXIOM_MEGADOC>