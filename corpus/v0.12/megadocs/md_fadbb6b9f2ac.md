<AXIOM_MEGADOC id="md_fadbb6b9f2ac" construction="latent_diagnostic" split="train" languages="ml" corpus="v0.9D">

<SEGMENT type="task" trust="explanatory" provenance="rationale_template">
Compute the sum of an int list in AxiomML via exhaustive pattern matching. The function is mlistsum6.
</SEGMENT>

<SEGMENT type="source" trust="canonical" provenance="record" record_id="axiom_ml:ml_list_sum:6:valid:none">
```sml
(* @effect: pure *)
(* @recursive: structural *)
fun mlistsum6 (xs:int list) : int =
  case xs of [] => 0 
```
</SEGMENT>

<SEGMENT type="rationale" trust="explanatory" provenance="rationale_template" record_id="axiom_ml:ml_list_sum:6:valid:none" template="ml_exhaustive_pattern_obligation_v01">
A total function over int list must handle every constructor. The two cases below are [] => 0 for the empty list and h::t => h+mlistsum6 t for a non-empty list. MLton enforces this exhaustiveness statically; a missing case is reported as non_exhaustive_pattern. The value returned in [] => 0 is the identity element of the combining operator used in h::t => h+mlistsum6 t, where mlistsum6 recurses on the tail.
</SEGMENT>

<SEGMENT type="source" trust="canonical" provenance="record" record_id="axiom_ml:ml_list_sum:6:valid:none">
```sml
| h::t => h+mlistsum6 t
```
</SEGMENT>

<SEGMENT type="expected_io" trust="extracted" provenance="extractor" record_id="axiom_ml:ml_list_sum:6:valid:none">
input: [1,2,3]
expected_value_json: {"type":"int","value":6}
</SEGMENT>

<SEGMENT type="invalid_mutation" trust="canonical" provenance="record" record_id="axiom_ml:ml_list_sum:6:invalid:bad_effect_annotation">
```sml
(* @effect: mut *)
(* @recursive: structural *)
fun mlistsum6 (xs:int list) : int =
  case xs of [] => 0 | h::t => h+mlistsum6 t
```
</SEGMENT>

<SEGMENT type="diagnostic" trust="checked" provenance="record" record_id="axiom_ml:ml_list_sum:6:invalid:bad_effect_annotation">
BAD_EFFECT_MUT
</SEGMENT>

<SEGMENT type="repair" trust="explanatory" provenance="rationale_template" record_id="axiom_ml:ml_list_sum:6:invalid:bad_effect_annotation">
Restore the matching effect annotation.
</SEGMENT>

</AXIOM_MEGADOC>