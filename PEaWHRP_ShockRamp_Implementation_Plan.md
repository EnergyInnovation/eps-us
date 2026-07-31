> **SUPERSEDED (2026-07-31):** the PSUS shock-ramp mechanism this plan implemented has been replaced by the payback-acceptance curve (PAC) — see `PEaWHRP_PaybackAcceptance_Plan.md`. Kept for history.

# Implementation plan: shock-size ramp for measure deployment

**Status: IMPLEMENTED 2026-07-28 on Dan's go-ahead, uncommitted. All three tests pass.**

Implemented exactly as planned below, with two deviations, both noted in place: (1) two dials rather than one shared scalar, via a new 2-element `Measure Set` subscript and `PSUS Price Signal Unlock Sensitivity[Measure Set]` reading `PEaWHRP-PSUS.csv`; (2) a `1e-06` floating-point deadband inside the unlock term — see the test results for why it is necessary.

**Shipped at the evidence-anchored defaults, not inert:** 0.075 waste heat / 0.10 efficiency. Setting both rows of `InputData/indst/PEaWHRP/PEaWHRP-PSUS.csv` to 0 restores the pure-screen behavior exactly (proven by T-R0).

**Test results:**

| Test | Result |
|---|---|
| **T-R0** dials = 0, $300/t | **Bit-identical** to the pre-ramp run — 7,439 series, zero differing cells. The refactor is provably neutral on its own. |
| **T-R1** dials on, $300/t | 491 tranches deploy (vs 80 under the pure screen); max deployed fraction 0.9941, none above 1.0; max yearly step exactly 0.2000. Waste-heat fuel savings 0.0096 → 0.148; efficiency 0.029 → 0.075; capex $15.1M → $39.6M; O&M $9.4M → $14.1M (2050, summed across industries). |
| **T-R2** dials on, zero policy | **Exactly zero** in every deployment and cash-flow cell — the no-double-count invariant holds. |

**Why the deadband exists (worth keeping in the code comments).** The first T-R2 attempt showed 904 nonzero cells in a zero-policy run. Deployment was exactly zero and the value ratios were exactly 1.0; what leaked was sub-cent cash flow (largest cell **$0.0000028**) because the policy-to-BAU value ratio differs from 1 in the last bit of double precision, and that gets multiplied by trillion-BTU energy bases. The old 0/1 screen was immune to this; a proportional ramp is not. With the `1e-06` deadband, T-R2 is exactly zero and T-R1 changes by at most **$100** on multi-million-dollar flows (largest absolute difference anywhere in the model). One tranche's 2026 value went from 6.66e-18 to 0 — that was the entire "relative difference of 1" the comparison initially flagged.

Post-implementation snapshot: `EPS.mdl.preramp-check.bak` is the state just before the ramp equations went in.

---

*Original plan follows (written overnight 2026-07-27, before implementation).*
Companion to [PEaWHRP_Barriers_Evidence_and_Options.md](PEaWHRP_Barriers_Evidence_and_Options.md) (this is Option C there). Base structure: [WHR_EfficiencyMeasures_Restructure_Plan.md](WHR_EfficiencyMeasures_Restructure_Plan.md).

## The idea in one paragraph

Today, an upgrade that is already profitable at baseline prices can never deploy through the economic channel — the barrier is an infinite wall. This change makes the wall erode in proportion to the price signal: if policy raises the value of saved energy X% above its baseline value, then (sensitivity × X%) of each blocked tranche becomes deployable, and the existing 20%/yr pacing takes it from there. With the sensitivity set to 0, behavior is exactly today's — so the change ships inert and the dial is a data decision, not a code decision.

## Design decisions baked into this plan

1. **The unlock is a ceiling, not a rate multiplier.** A tranche unlocks up to fraction `sensitivity × (value ratio − 1)` of its potential; deployment then approaches that ceiling at 20%/yr. (If we instead scaled the deployment *rate*, any tiny signal would eventually deploy 100% of everything — wrong.)
2. **Zero-lever invariant preserved by construction.** With no levers, policy value = baseline value everywhere, ratio = 1, unlock = 0. No deployment, no double count with BIEEI. This must be re-verified by test, not just argument (T-R2 below).
3. **Subsidies count toward the signal.** The subsidy lever is already added into `Value of ... Energy Savings`, so it raises the ratio and unlocks blocked stock — the subsidy lever becomes a real instrument (today it is nearly inert for the blocked 70–87%).
4. **No un-deployment.** If the signal later falls, the ceiling drops below the deployed stock; the MAX(0, …) gap goes to zero, deployment stops, and the stock persists until lifetime retirement. Same convention as today.
5. **Two dials — one per measure set** (revised 2026-07-28 on the unit-vs-system evidence below), named `PSUS Price Signal Unlock Sensitivity[Measure Set]` over a new 2-element subscript (`waste heat measures`, `process efficiency measures`), or simply two scalars if that reads cleaner. The two sets are not the same population: the waste-heat set is 99.7% system-level heat/gas recovery, while the efficiency set is 38% controls/operational, 33% equipment replacement, 22% feedstock — with a 6× capital-intensity gap between its halves. A single dial averages over populations the evidence says behave differently. Per-industry values remain a later option.
6. **This is an assumption, not a policy lever** — no FoPITY rows, no WebAppData entry, no .cin changes.

## Model changes (4 equation edits + 1 new input)

### New input constant

```
PSUS Price Signal Unlock Sensitivity=
	GET DIRECT CONSTANTS('InputData/indst/PEaWHRP/PEaWHRP-PSUS.csv', ',', 'B2*')
	~	Dmnl
	~	Fraction of barrier-blocked measure potential that becomes deployable per
		unit of proportional increase in the value of saved energy above its BAU
		value. 0 = barriers are absolute (reproduces the pure counterfactual
		screen). Calibration anchor: the 2005-2008 industrial gas price doubling
		produced modest acceleration, suggesting 0.1-0.3. See
		PEaWHRP_Barriers_Evidence_and_Options.md.
	|
```

New CSV `InputData/indst/PEaWHRP/PEaWHRP-PSUS.csv` (same 2-line scalar format as PEaWHRP-SoCEMDSiaY.csv), **initial value 0** so the merge is behavior-neutral.

### Edit 1 & 2 — `Waste Heat Measure Tranche Economically Deployable` (and PEM twin)

Rename concept from a 0/1 flag to a 0..1 **deployment ceiling**. New equation (WHM shown; PEM identical with its variables):

```
Waste Heat Measure Tranche Economically Deployable[Industry Category,Waste Heat Measure,Measure Cost Level]=
	IF THEN ELSE(
	  WHMFSP[...] + WHMESP[...] <= 0,
	  0,                                                          { empty slots stay inert }
	  IF THEN ELSE(
	    Waste Heat Measure Value at BAU Prices[...] < Levelized Cost[...],
	    IF THEN ELSE(Value of Waste Heat Measure Energy Savings[...] >= Levelized Cost[...], 1, 0),
	                                                              { flip rule, unchanged: full unlock }
	    MIN(1, PSUS Price Signal Unlock Sensitivity
	           * MAX(0, ZIDZ(Value of Waste Heat Measure Energy Savings[...],
	                         Waste Heat Measure Value at BAU Prices[...]) - 1))
	                                                              { blocked stock: partial unlock scaled by signal }
	  )
	)
```

Behavior check by case: never-profitable tranches → BAU value < cost and value < cost → 0 (unchanged). Flip tranches → 1 (unchanged). Blocked tranches → `MIN(1, PSUS × (ratio − 1))`, which is 0 whenever PSUS = 0 or ratio = 1. `ZIDZ` guards a zero BAU value (returns 0 → MAX(0, −1) → 0 → conservative no-unlock).

Update the variable's description comment to describe the ceiling semantics and the PSUS=0 special case.

### Edit 3 & 4 — `New Waste Heat Measure Deployment This Year` (and PEM twin)

The economic term currently treats the flag as a gate on the *remaining-potential* pace:

```
flag * SoCEMDSiaY * MAX(0, 1 - Last Year Deployed Fraction)
```

Change it to pace toward the ceiling instead of toward 1:

```
SoCEMDSiaY * MAX(0, Waste Heat Measure Tranche Economically Deployable[...] 
                    - Last Year Deployed Fraction[...])
```

For flip tranches (ceiling 1) this is arithmetically identical to today's expression. For blocked tranches it approaches the partial ceiling at 20%/yr. The standards floor term and the empty-slot guard around the MAX stay exactly as they are; retirement backfill works unchanged (retirement lowers Last Year Deployed below the ceiling → gap reopens → refills).

## Known properties and edge cases (from self-review, 2026-07-27 late)

- **The unlock does not vary by cost level.** Value is computed per (industry, measure) — the ratio is the same for all five cost levels of a blocked measure, so they unlock in equal proportion. The cost-level spread therefore does nothing for blocked stock under the ramp (it still staggers the flip-rule band). If we later want cheaper tranches to unlock first, the ceiling could be scaled by cost level — noted as a possible refinement, not in this version.
- **A boundary jump remains.** A tranche whose cost sits just *above* the baseline value gets a full unlock (ceiling 1) the moment policy value crosses it; a near-identical tranche just *below* baseline value gets only the partial ramp ceiling (e.g. 0.56 at ratio 3.8, sensitivity 0.2). This discontinuity is inherent to keeping the flip rule intact and is smaller than today's (1 vs 0). Acceptable; documented so nobody reads it as a bug.
- **Electricity-heavy measures barely respond to a carbon tax** under the ramp, because the tax barely moves industrial electricity prices, so their value ratio stays near 1. That is the intended economics, not an implementation artifact.
- **T-R0 equivalence is provable, not just hoped:** with PSUS = 0 the ceiling equals the old 0/1 flag, and `0.2 × MAX(0, flag − LY)` equals `flag × 0.2 × MAX(0, 1 − LY)` for flag ∈ {0,1} (flag=1: identical since LY ≤ 1; flag=0: both zero). So T-R0 must be bit-identical; any diff means an editing mistake.
- **Ramp deliberately excludes the "too expensive even with policy" tranches** — the equation branches on the baseline-value test first, so unprofitable measures still need the flip, not the ramp. Barriers and unprofitability stay distinct concepts.

## What does NOT change

Levelized costs, values, the BAU-price twins, cost-level spread, standards channel, all cash-flow wiring, retirement, FoPITY files, WebAppData, scenario files. No BAU twins needed (invariant holds by construction). The availability index interaction is unchanged (it scales potentials, orthogonal to the unlock).

## Tests (run after implementation, ~30 min total)

| # | Run | Expectation |
|---|---|---|
| T-R0 | PSUS = 0, rerun the $300/t test | **Bit-identical** to the existing `MeasCTax` run (regression: the refactor itself is neutral). Compare tabs. |
| T-R1 | PSUS = 0.2, $300/t | Blocked tranches deploy toward ceilings ≈ 0.2 × (ratio − 1); hand-check one industry (e.g. food & beverage 2050: ratio ≈ 3.8 → ceiling ≈ 0.56). Total deployment materially higher than the 20-tranche result; still zero tranches above 1.0. |
| T-R2 | PSUS = 0.2, **zero levers** | Deployment identically zero everywhere (the invariant — the single most important test). |
| T-R3 | PSUS = 0.2, subsidy lever only (e.g. $5/MMBtu, one industry) | Deployment now occurs in that industry (new behavior, by design); government outlay appears; magnitude sanity-check. |
| T-R4 | Units check + LOADMODEL-clean as usual. |

## Calibration evidence for the sensitivity dial (added 2026-07-28, two verified research sweeps)

The dial's units: share of the blocked (already-profitable) stock that becomes deployable per unit of proportional increase in the value of saved energy. Three independent lines of evidence, converted to those units:

**1. The best direct evidence puts price-driven sensitivity near 0.1.** Anderson & Newell studied exactly our population — plants holding audit-identified, mostly-unadopted efficiency measures — and estimated how adoption probability moves with each economic ingredient ([Anderson & Newell 2004](https://doi.org/10.1016/j.reseneeco.2003.07.001); [free version](https://media.rff.org/documents/RFF-DP-02-58.pdf)). A 10% energy-price increase raises adoption by ~0.43 percentage points on a 53%-adopted base. Against the 47-point unadopted backlog, that is ~0.9% of the backlog unlocked per 10% value increase → **sensitivity ≈ 0.09**. Their savings-quantity gradient gives ≈ 0.12 the same way.

**2. Upfront-cost relief works about twice as hard as price signals.** The same study finds a 10% project-cost reduction raises adoption ~0.87 points — roughly double the price effect ("plants are 40% more responsive to initial costs than annual savings," and about 2× more than to price specifically) → **sensitivity ≈ 0.19 for capex-subsidy-type interventions**. Residential subsidy-tier data points even higher (adoption elasticities 0.9–1.8, [Boomhower & Davis 2014](https://doi.org/10.1016/j.jpubeco.2014.03.009)), but 69–84% of marginal claimants there were free-riders, so treat that as a loose upper bound. *Design implication: our single dial treats a $1 subsidy and $1 of carbon-tax value identically; the evidence says the subsidy is worth ~2× per dollar. A split dial (price vs. subsidy) is the natural v2 if the team wants that asymmetry.*

**3. The low anchor is genuinely low.** The one clean plant-level econometric study of price-driven adoption found **existing plants show no significant retrofit response to energy prices at all** — only newly built plants respond, at elasticity ~0.1 ([Linn 2008, *Economic Journal*](https://academic.oup.com/ej/article-abstract/118/533/1986/5057687); [working paper](https://ceepr.mit.edu/wp-content/uploads/2023/02/2006-012.pdf)). Anderson & Newell's firms were audited (informed); Linn's incumbents are everyone. The economy-wide truth for retrofits likely sits between ~0 and ~0.1.

**Coherence check against program outcomes:** at sensitivity 0.1, our $300/ton test (value ratio ≈ 3.8 by 2050) unlocks ~28% of the backlog, paced in at 20%/yr. For comparison, DOE Better Plants partners — firms with a pledge, technical assistance, and management attention — average **2%/yr energy-intensity improvement**, with goal-achievers reaching 15–27% over 7–10 years ([DOE Better Plants 2021 Progress Update](https://www.energy.gov/eere/iedo/better-plants-progress-updates)); German SME audit programs saw **43% of recommended measures adopted** ([EC/Fraunhofer EED Art. 8 study, 2016](https://op.europa.eu/en/publication-detail/-/publication/6f6c4d1a-4c6c-11e6-9c64-01aa75ed71a1), citing Fleiter et al. 2012). A strong sustained signal unlocking a quarter-ish of the backlog over decades is the right order of magnitude against both.

**4. The evidence is mostly about unit-level equipment, and adoption falls as measures get more system-like.** Anderson & Newell's Table 2 breaks their 38,920 audited projects into categories — and the population is dominated by cheap discrete measures, with adoption declining monotonically as projects become larger and more system-embedded:

| Category | Share of projects | Adoption rate | Mean cost |
|---|---|---|---|
| Motor systems (motors, compressors) | 35.4% | **60%** | $5,297 |
| Building & grounds (lighting, ventilation, envelope) | 36.5% | **51%** | $6,217 |
| Combustion systems (ovens, furnaces, boilers) | 6.1% | 56% | $5,131 |
| Operations (maintenance, scheduling, use reduction) | 3.8% | 50% | $2,617 |
| **Thermal systems (steam, heat recovery, cooling)** | 17.4% | **44%** | $9,021 |
| **Industrial design (modify thermal/mechanical systems)** | 0.4% | **38%** | $34,013 |
| **Electrical power (demand mgmt, generation)** | 0.4% | **30%** | $287,100 |
| *Sample average* | | *53%* | *$7,400* |

**~72% of the sample is lighting/ventilation/envelope plus motors** — unit-level swaps averaging $5–6k. The category closest to our waste-heat set ("thermal systems": steam, heat recovery, cooling) adopts at **44% against the 53% average**, at ~1.5× the cost; the two most system-like categories adopt at just **30–38%** at 5–40× the cost. So the pooled ~0.09 sensitivity is predominantly a *unit-equipment* number.

**5. No study isolates heat-recovery or process-integration adoption response.** Four independent leads were checked and none produced a number — a confirmed gap, not a search failure. The literature does recognize the distinction conceptually: Trianni, Cagno & De Donatis identify **"distance to core process"** as a measure attribute governing adoption ([*Applied Energy* 2014](https://doi.org/10.1016/j.apenergy.2013.11.065)), and Thollander & Ottosson report measures are more attractive where energy is less integrated into production — but both treat it qualitatively.

**6. Our measure data carries no adoption realism at all.** The Kermeli/Worrell LBNL inventories our potentials come from are engineering catalogs: measures listed with paybacks, ordered roughly by ease of implementation, with **no adoption-rate, penetration, or practical-vs-technical filter** anywhere. So the CSV potentials are *technical* potentials, and every bit of adoption realism has to come from our structure. That is an argument for the barrier structure existing, and a caution against reading "potential" as achievable.

**Recommended defaults — two dials:**

| Dial | Value | Reasoning |
|---|---|---|
| Waste heat measures | **0.075** | Pooled 0.09 scaled by the thermal-systems adoption gradient (44%/53% ≈ 0.83). Documented range 0.05–0.10. |
| Process efficiency measures | **0.10** | Its halves resemble "operations" (50% adoption) and "motor systems" (60%) — pooled or a touch above. Range 0.08–0.15. |

Two caveats to carry into the documentation, both material:
- The adoption-rate gradient measures **levels, not slopes**. Using it to scale a *response* elasticity assumes measures that are harder to adopt overall are also less price-responsive. That is plausible and directionally supported (the paper finds adoption falls with cost, and system measures cost more), but Anderson & Newell do not report category-specific elasticities — so the scaling is a reasoned assumption, not a measured result.
- Nobody has directly measured "share of profitable backlog unlocked per unit of price signal" for anything, and Linn's null result for incumbent retrofits suggests even these values may be generous for pure price policies. Shipping at 0 and treating 0.075/0.10 as a scenario assumption is the defensible posture.

*(Correction to an earlier draft claim: Better Plants' reported average is 2%/yr, not the 2.5–3%/yr I earlier recalled; and no DOE source was found for a "~1%/yr typical industry baseline" comparator — dropped. Verify all figures against the linked sources before publication, per usual practice.)*

## Decisions for Dan (pre-implementation)

1. Default PSUS after testing: ship at 0 (inert until the team picks a value) or adopt the evidence-anchored ~0.1? I'd ship the code with 0 and change the value only after the team sees T-R1/T-R3 results and the calibration-evidence section above.
1b. Two possible dial splits, and they are independent of each other:
   - **By measure set (now in the plan):** waste-heat 0.075 vs efficiency 0.10, on the unit-vs-system adoption gradient. Recommended for v1 — the evidence for it is the strongest thing we found, and it costs one subscript.
   - **By instrument (still deferred):** a dollar of capex subsidy unlocks ~2× what a dollar of energy-price value does. Not in v1; both signals still flow through the same value ratio. Clean v2 if the team wants it.
1c. **Data question that outranks the dial** (raised by the unit-vs-system review, needs Dan/team): the efficiency set's equipment-replacement third — replacing ball mills with vertical roller mills, efficient refiners, shoepress, roller presses (33% of that set's potential, median capex $67.7/MMBtu-yr, 6× the controls half) — is the kind of upgrade that normally happens at end of equipment life. That is what the BIEEI autonomous-improvement rates are meant to carry. Burner-integral heat recovery was deliberately curated out of the measure list into the unit-efficiency files for exactly this reason; **did the same curation pass consider these equipment-swap measures?** If not, that third may double-count against BIEEI, which would matter more than any dial value.
2. Confirm the linear form `PSUS × (ratio − 1)` — alternatives (log, saturating) can wait until the linear one proves inadequate.
3. Confirm shared-scalar scope (vs per-measure-set) for the first version.

Estimated effort: ~1–2 hours including test runs. No other structures touched.

Housekeeping rider (applies to the whole restructure, noticed during this review): `InputData/acronym-key.xlsx` has not been updated for any of the new acronyms (WHMFSP/WHMESP/WHMCC/WHMOC/WHMEL, PEM* equivalents, MCLM, MCLS, MHRP, SoCEMDSiaY, PEaWHRP, and PSUS if adopted). Excel task — flagged for the Phase F pass.
