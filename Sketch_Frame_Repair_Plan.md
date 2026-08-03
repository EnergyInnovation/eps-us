# Sketch coordinate-frame repair plan

**2026-08-03, pending Dan's sign-off.** Repairs the view-layout damage introduced by merge `4c116bd8` (tempbands+whr × develop). Sketch-section edits only — zero simulation impact. One commit on `develop`, revertible with `git revert`.

## Diagnosis (two independent agent passes, cross-checked)

**Mechanism.** Both parents had internally consistent layouts; the branch had panned whole view regions. My conflict-hunk resolution kept views consistent *inside* hunks (branch side), but git's auto-merge took whichever single side had changed each non-conflicted line — splicing two coordinate frames into the same view. All *content* (variables, arrows, equations) is correct; only positions mixed. Both later commits (Robbie's toggle port, Dan's `b75c74b3` industry adjustments) are confirmed byte-identical or clean in the affected views.

**Damage surface (all 30 views audited at current HEAD `b75c74b3`):**

| View | Damage | Evidence | Fix class |
|---|---|---|---|
| **Web Application Support Variables** | Severe — bimodal split: 885 objects at branch coords, 391 at develop coords, offset by exactly **(3006, 1871) with zero dispersion**; 75 new frame-crossing arrows (11 → 86) | Both agents, exact agreement on the offset | **Single uniform translation** of the 391 develop-frame objects by (−3006, −1871) → whole view back in one frame, relative layout preserved |
| **Fuels** | Minor — 15 of 677 objects (ids 1–15: the `BAU … Fuel Cost per Unit Energy` cluster, `GWP by Pollutant`, `Grams per Metric Ton CO2e`, `BS BAU Subsidy…`, `PEI …`) at branch coords in a develop-frame view | Both agents, same 15 objects | Name-matched coordinate restore of the 15 from the develop parent's Fuels view |
| Policy Implementation Schedule | Mild — 15% minority-frame objects, scattered deltas (±~400px), 10 new long arrows (on top of ~35 by design) | Census pass | Per-object restore of minority-frame objects to majority coords by name; grafted merge additions stay put |
| Policy Control Center | Mild — 12% minority-frame, no long arrows, bbox modestly inflated | Census pass | Same as above (or leave for GUI tidy) |
| Industry - Main / Cash Flow | **Not merge damage** — matches Dan's own `b75c74b3` hand re-layout this morning; 6 long arrows remain from the Material-Efficiency grafts | Attribution pass | None planned; visual confirm only. Optional: shorten the 6 graft arrows via `eps-mdl-sketch-edit` |
| Remaining 24 views | Clean (identical in both parents, or one coherent whole-view pan) | Census pass | None |

Per-object classification CSVs and the parser live in the session scratchpad (`view_damage_summary.csv`, `damaged_views_object_classification.csv`).

## Execution plan

1. **Script the repair** (Python, byte-safe, CRLF-preserving — same tooling as the merge):
   a. Web App Support: translate the 391 classified develop-frame objects by (−3006, −1871); translate waypoints of arrows whose BOTH endpoints moved; zero the waypoints of formerly frame-crossing arrows so Vensim redraws them straight.
   b. Fuels: overwrite the 15 objects' (x,y) with the develop parent's values (matched by name within the view).
   c. PIS + PCC: restore minority-frame objects to the majority parent's coordinates by name; objects with no majority-parent counterpart (the merge's grafted levers) untouched.
2. **Verify mechanically**: rerun the census — every repaired view must classify as single-frame with long-arrow counts ≤ parent baselines and bbox ≈ parent; `sketch_lint.py` clean; headless `LOADMODEL` clean; equation section byte-identical (assert).
3. **Dan eyeballs** Fuels + Web App Support (+ PIS/PCC) in the Vensim GUI.
4. Commit on `develop`; push after Dan's OK.

Est. under an hour, one sonnet agent for the script + census rerun, main loop review.

## Process fix so this never recurs

The merge playbook gains a step (goes in the KB merge checklist alongside the dangling-reference scan): **after any `.mdl` merge, run the frame census per view** — bimodal coordinate clusters or new >2000px arrows fail the gate. The auto-merged "no conflict" regions of a sketch are exactly where this hides; conflict-free ≠ layout-coherent.
