<AXIOM_MEGADOC id="md_ff044e1fcbfd" construction="latent_diagnostic" split="dev" languages="scheme" corpus="v0.9D">

<SEGMENT type="task" trust="explanatory" provenance="rationale_template">
Compute the sum of a list of exact integers using structural recursion in AxiomScheme. The function is slist_sum8.
</SEGMENT>

<SEGMENT type="source" trust="canonical" provenance="record" record_id="axiom_scheme:scheme_list_sum:8:valid:none">
```scheme
(define (slist_sum8 xs)
  (@effect pure)
  (@resource none)
  (@recursive structural)
  (if (null? xs)
    0
```
</SEGMENT>

<SEGMENT type="rationale" trust="explanatory" provenance="rationale_template" record_id="axiom_scheme:scheme_list_sum:8:valid:none" template="scheme_structural_recursion_obligation_v01">
The (@recursive structural) annotation creates an obligation: every recursive call to slist_sum8 must apply the function to a syntactic subterm of xs. The base case below tests (null? xs) — at the moment this branch fires, xs is empty and slist_sum8 must return the identity element of the combining operator below.
</SEGMENT>

<SEGMENT type="source" trust="canonical" provenance="record" record_id="axiom_scheme:scheme_list_sum:8:valid:none">
```scheme
    (+ (car xs) (slist_sum8 (cdr xs)))))
```
</SEGMENT>

<SEGMENT type="expected_io" trust="extracted" provenance="extractor" record_id="axiom_scheme:scheme_list_sum:8:valid:none">
input: '(8 1 2)
expected_value_json: {"type":"int","value":11}
</SEGMENT>

<SEGMENT type="invalid_mutation" trust="canonical" provenance="record" record_id="axiom_scheme:scheme_list_sum:8:invalid:banned_mutation">
```scheme
(define (slist_sum8 xs)
  (@effect pure)
  (set! xs xs)
  (@resource none)
  (@recursive structural)
  (if (null? xs)
    0
    (+ (car xs) (slist_sum8 (cdr xs)))))
```
</SEGMENT>

<SEGMENT type="diagnostic" trust="checked" provenance="record" record_id="axiom_scheme:scheme_list_sum:8:invalid:banned_mutation">
BANNED_SET_MUTATION
</SEGMENT>

<SEGMENT type="repair" trust="explanatory" provenance="rationale_template" record_id="axiom_scheme:scheme_list_sum:8:invalid:banned_mutation">
Remove the `(set! ...)` form. AxiomScheme bans mutation; effect annotation is `pure`.
</SEGMENT>

</AXIOM_MEGADOC>