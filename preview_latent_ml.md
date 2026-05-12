<AXIOM_MEGADOC id="md_851120ae2475" construction="latent_diagnostic" split="train" languages="ml" corpus="v0.9D">

<SEGMENT type="task" trust="explanatory" provenance="rationale_template">
Compute the sum of an int list in AxiomML via exhaustive pattern matching. The function is mlistsum0.
</SEGMENT>

<SEGMENT type="source" trust="canonical" provenance="record" record_id="axiom_ml:ml_list_sum:0:valid:none">
```sml
(* @effect: pure *)
(* @recursive: structural *)
fun mlistsum0 (xs:int list) : int =
  case xs of [] => 0 
```
</SEGMENT>

<SEGMENT type="rationale" trust="explanatory" provenance="rationale_template" record_id="axiom_ml:ml_list_sum:0:valid:none" template="ml_exhaustive_pattern_obligation_v01">
A total function over int list must handle every constructor. The two cases below are [] => 0 for the empty list and h::t => h+mlistsum0 t for a non-empty list. MLton enforces this exhaustiveness statically; a missing case is reported as non_exhaustive_pattern. The value returned in [] => 0 is the identity element of the combining operator used in h::t => h+mlistsum0 t, where mlistsum0 recurses on the tail.
</SEGMENT>

<SEGMENT type="source" trust="canonical" provenance="record" record_id="axiom_ml:ml_list_sum:0:valid:none">
```sml
| h::t => h+mlistsum0 t
```
</SEGMENT>

<SEGMENT type="expected_io" trust="extracted" provenance="extractor" record_id="axiom_ml:ml_list_sum:0:valid:none">
input: [1,2,3]
expected_value_json: {"type":"int","value":6}
</SEGMENT>

<SEGMENT type="invalid_mutation" trust="canonical" provenance="record" record_id="axiom_ml:ml_list_sum:0:invalid:wrong_base_case_value">
```sml
(* @effect: pure *)
(* @recursive: structural *)
fun mlistsum0 (xs:int list) : int =
  case xs of [] => 10 | h::t => h+mlistsum0 t
```
</SEGMENT>

<SEGMENT type="diagnostic" trust="checked" provenance="record" record_id="axiom_ml:ml_list_sum:0:invalid:wrong_base_case_value">
SEMANTIC_WRONG_BASE_CASE
</SEGMENT>

<SEGMENT type="repair" trust="explanatory" provenance="rationale_template" record_id="axiom_ml:ml_list_sum:0:invalid:wrong_base_case_value">
Set the empty-list case to the identity of the combining operator (0 for +, 1 for *).
</SEGMENT>

</AXIOM_MEGADOC>