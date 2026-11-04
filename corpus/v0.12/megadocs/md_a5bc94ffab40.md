<AXIOM_MEGADOC id="md_a5bc94ffab40" construction="latent_diagnostic" split="train" languages="scheme" corpus="v0.9D">

<SEGMENT type="task" trust="explanatory" provenance="rationale_template">
Compute the sum of a list of exact integers using structural recursion in AxiomScheme. The function is slist_sum9.
</SEGMENT>

<SEGMENT type="source" trust="canonical" provenance="record" record_id="axiom_scheme:scheme_list_sum:9:valid:none">
```scheme
(define (slist_sum9 xs)
  (@effect pure)
  (@resource none)
  (@recursive structural)
  (if (null? xs)
    0
```
</SEGMENT>

<SEGMENT type="rationale" trust="explanatory" provenance="rationale_template" record_id="axiom_scheme:scheme_list_sum:9:valid:none" template="scheme_structural_recursion_obligation_v01">
The (@recursive structural) annotation creates an obligation: every recursive call to slist_sum9 must apply the function to a syntactic subterm of xs. The base case below tests (null? xs) — at the moment this branch fires, xs is empty and slist_sum9 must return the identity element of the combining operator below.
</SEGMENT>

<SEGMENT type="source" trust="canonical" provenance="record" record_id="axiom_scheme:scheme_list_sum:9:valid:none">
```scheme
    (+ (car xs) (slist_sum9 (cdr xs)))))
```
</SEGMENT>

<SEGMENT type="expected_io" trust="extracted" provenance="extractor" record_id="axiom_scheme:scheme_list_sum:9:valid:none">
input: '(9 1 2)
expected_value_json: {"type":"int","value":12}
</SEGMENT>

<SEGMENT type="invalid_mutation" trust="canonical" provenance="record" record_id="axiom_scheme:scheme_list_sum:9:invalid:missing_base_case">
```scheme
(define (slist_sum9 xs)
  (@effect pure)
  (@resource none)
  (@recursive structural)
  (if #f
    0
    (+ (car xs) (slist_sum9 (cdr xs)))))
```
</SEGMENT>

<SEGMENT type="diagnostic" trust="checked" provenance="record" record_id="axiom_scheme:scheme_list_sum:9:invalid:missing_base_case">
MISSING_STRUCTURAL_BASE_CASE
</SEGMENT>

<SEGMENT type="repair" trust="explanatory" provenance="rationale_template" record_id="axiom_scheme:scheme_list_sum:9:invalid:missing_base_case">
Replace `#f` with `(null? xs)` — the base predicate of structural recursion on lists.
</SEGMENT>

</AXIOM_MEGADOC>