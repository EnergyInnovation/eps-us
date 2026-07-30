# Skeptical review of the measures implementation — findings and fixes

**2026-07-28, overnight. For Dan's morning review.**
Scope: everything implemented in the WHR/process-efficiency restructure (Phases A–E), reviewed adversarially for correctness, EPS-convention consistency, and efficiency. Method: two independent Opus review agents (one re-deriving every new equation as written, one auditing cash-flow wiring against the CCS / industrial-equipment / clean-heat conventions), each finding then verified by hand against the file before any change. Re-validation runs follow at the end.

## Fixes applied tonight (verified findings)

**1. The savings bases skipped green and low-carbon hydrogen — fixed. (The one real blocker.)**
The `nonelectricity industrial fuel` subrange the bases and price blends summed over has only 9 fuels; it predates the hydrogen variants and omits both. But the multipliers that deliver the savings apply to *all* 11 non-electric fuels. So in any scenario with meaningful industrial hydrogen, the model would have delivered more physical savings than it charged for — at a 30% hydrogen share, about 43% more. All bases, blends, and the intensity numerator now sum every non-electric fuel (`SUM over Industrial Fuel minus the electricity term`), which also makes the value signal see hydrogen prices. Base-year effect is nil (hydrogen use is ~zero today); this mattered exactly in the decarbonization scenarios the model exists for.

**2. A binding standard no longer collapses for one year at each retirement wave — fixed.**
Both deployment channels measured their gap against *last year's* stock, blind to this year's retirements. Under a 100% standard, a tranche with a 15-year lifetime would deploy in year one, then in year 16 retire completely and show **zero deployment for one year** before snapping back — a sawtooth repeating every lifetime cycle, and `US_ClimateAmbition` (standard = 1 for iron & steel, which has 10- and 15-year measures) would have shown it in-horizon. Both channels now net this year's retirements into the gap, so a binding standard replaces retiring capacity the same year and the economic channel starts refilling immediately at its 20%/yr pace.

**3. Mixed fuel-and-electricity measures were valued with the wrong weights — fixed.**
The value-per-BTU formula weighted fuel vs. electricity prices by the raw savings *fractions*, but those fractions are measured against bases of very different sizes. Sharpest case: iron & steel scrap preheating (fuel fraction 0.0031, elec fraction 0.0313) got a 91% electricity weight even though heating-process electricity is a sliver of that industry's heat energy — and industrial electricity costs ~3× gas per BTU, so the measure's value was materially overstated. All four value equations now weight by the BTU each channel actually delivers (fraction × its base), which also makes the value arithmetic exactly consistent with the quantity and cost arithmetic. Affects the 7 mixed tranches; pure-fuel and pure-electricity measures are unchanged.

**4. The "BAU prices" benchmark now uses true BAU quantities — fixed.**
The screen's benchmark used BAU *prices* but policy-case *fuel-mix weights*, so a policy that shifts the fuel mix would drag the benchmark around and flip tranches in and out of eligibility for reasons unrelated to BAU. It turns out a true BAU energy-use-by-fuel-and-process variable exists in the model, so the benchmark now uses BAU quantities with BAU prices throughout — a clean counterfactual. (Six small BAU helper variables added.)

**5. The waste-heat availability index compared this year's fuel to last year's output — fixed.**
With ~2%/yr output growth that mismatch biased the intensity ratio upward, pinning the index at its 1.0 cap longer than intended. Numerator and denominator are now both lagged one year, and the start-year anchor is consistent with them.

**6. Measure O&M was missing from the OM cost subtotal — fixed.**
`Industry Subtotal Change in OM Expenditures` carried CCS O&M but not measure O&M, while the sibling capex subtotal did carry measure capex. That subtotal feeds the headline `Total Change in CapEx and OpEx` and first-year-NPV outputs — so policy-cost outputs would have counted measure capital but not measure O&M (and some measure O&M is *negative*, so the error's sign depends on the scenario). GDP and jobs were unaffected — the IO model is fed through slots that already had the term. One line added.

**7. Safety caps on the savings roll-ups — added.**
The four industry-level "fraction avoided" variables had no ceiling; today's data keeps them below 0.22, but a future data revision could have pushed `1 − fraction` negative and flipped the sign of energy use. Each is now capped at 1.

**8. The measure financing factor is now computed once at initialization** rather than every step (it's built entirely from constants) — in line with the recent runtime hoisting work.

## Reviewed and found clean (the absence of findings means something here)

Both reviewers worked from checklists and reported what they *couldn't* break: all 20 long-form reads and remaps (offsets, transposition, row order — cross-checked against the shape auditor's 1,343-call pass); all four levers and their schedule wiring; the government subsidy element in every place that subscript is enumerated, including the easy-to-miss `[remainder]` decomposition; QUANTUM placement (the convention quantizes at the totals level, not per-cost-variable — measures conform); payer-vs-recipient double-entry for O&M and capex (mirrors CCS exactly); the financing repayment stock (term-for-term match to the CCS pattern, and unlike the retired WHR chain it has its own expiration term — the old one netted against a typo'd shared variable, a pre-existing bug that died with it); no deleted-variable stragglers; no orphans; no simultaneity; zero-policy invariance by construction; units coherent end to end.

## Documented as accepted approximations (no code change)

- **Efficiency-measure cash flows are metered on a pre-waste-heat base** while the savings physically apply after waste heat measures. Worst case under current data is under 5% of the efficiency cash flows in the most affected industry, and the "fix" would tangle the two measure sets' calculation order. Now documented in the equation comment.
- **The subsidy is a current-year rate compared against a lifetime-levelized cost** — implicitly assumes the subsidy persists. This matches EPS's myopic-expectations convention elsewhere; noted for the docs.
- **Measure equipment spending is distributed to supplier industries with the same fixed shares as CCS and general equipment** (`SoCaOMSbRIC`). Fine unless the team thinks heat-exchanger supply chains differ enough to matter.

## False positives (checked, no action)

- The reviewer flagged the PEM lever pair as missing from `CreateCombinationsScript.py` / `CreateContributionTestScript.py`; all four entries are present (lines 235–238 / 231–234).
- The `Policy:` subscript family doesn't list the new levers — verified that family is referenced by zero equations (web-app-era metadata). Left alone; add entries during Phase F if you want it tidy.

## Still open for your judgment

1. The ramp plan ([PEaWHRP_ShockRamp_Implementation_Plan.md](PEaWHRP_ShockRamp_Implementation_Plan.md)) — reviewed and tightened separately; awaiting your go.
2. Fixes 3–5 slightly move the $300/ton test results (they change which tranches sit near the screen boundary); the re-validation runs below are the fresh baseline. If you want, the barriers memo's partition table can be regenerated from them.
3. MHRP placeholders, WebAppData.xlsx, docs repo, `acronym-key.xlsx` additions — unchanged Phase F list.

## Re-validation (all three passed, run after all fixes)

- **Zero-policy:** every deployment and cash-flow cell exactly zero — the no-double-count invariant survives the BAU-benchmark and value-weighting changes.
- **$300/ton carbon tax:** 80 tranches deploy (same count as before the fixes — the boundary shifts only matter once hydrogen shows up); max deployed fraction 0.994, never above 1.0; no tranche ever adds more than the 0.20/yr cap.
- **100% standards:** all 520 real tranches (205 waste-heat + 315 efficiency) reach 1.000, and **zero sawtooth dips** anywhere — the iron & steel case that previously would have collapsed to zero in year 16 now ramps smoothly to 1.00 and holds, with retirements replaced in-year.

Tree state: `EPS.mdl` loads clean; post-review snapshot at `EPS.mdl.postreview.bak`; everything uncommitted for review.
