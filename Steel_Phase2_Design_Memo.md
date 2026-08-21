# Steel Phase 2 design memo — emissions, coke chain, and policy levers (DRAFT for review, 2026-08-20)

*What comes after the 1b carve-out. Each section ends with a recommendation; nothing here is implemented yet. Companion docs: `Steel_Breakout_Design.md` (D1–D15), `Steel_1b_Carveout_Memo.md`, replication log.*

## 1. Coke chain and endogenous process CO2 (#189 for steel)

**Structure** (per Jeff's sketch, on the pathway module's physical spine):
- `Coke Demand per Ton of BF BOF Steel` (new input, ~0.45–0.6 t coke/t incl. PCI-adjusted; GEM's met-coal file gives 780 kg met coal/t pig iron as a cross-check) × BF-BOF-family production → coke demand → met coal demand (met-coal-to-coke ratio input; sources conflict 1.3 vs 1.6 — resolve in the workbook).
- Carbon balance per pathway: carbon in (coke + PCI coal + NG + electrodes + fluxes/limestone) − carbon retained in steel (~0.1–1%, small; Jeff's "optionally subtract" — skipped in v1 per default) = **gross process + energy CO2 by pathway**. Split: combustion CO2 stays on the fuel-emissions chain (as today, via fuel use); the *process* residual (reduction chemistry + calcination of fluxes + coke-oven losses) becomes `Steel Process CO2 by Pathway`.
- **Retire steel's share of exogenous BPE for CO2** (subtract a start-year-matched slice, or exclude 241 CO2 from BPE outright and let the module supply it). Non-CO2 process gases (tiny for steel) stay on BPE per the agreed default.
- Calibration anchors: GHGI iron & steel + met coke process CO2 = **40.7 MMT (2022)**; GHGRP Subpart Q facility total = **64.3 MMT (2023)**; AEO2026 Table 30 CO2 = 89.0 MMT (2025, incl. combustion) declining to 62.7 by 2050. The module's BAU (process + combustion) should land in that constellation and the workbook must document which boundary each anchor uses.

**Recommendation:** implement the coke chain as module-internal physical flows (no new `Industrial Fuel` element for coke; met coal rides `hard coal if` for purchases, as EPS convention already books it), with `Steel Process CO2 by Pathway` replacing 241's CO2 share of BPE. The 1b `Steel Fuel Feedstock Share` ratio retires at the same moment.

**IMPLEMENTED (P2-A, 2026-08-20 late) — the feedstock-carbon-balance version, ahead of the full coke chain:** `Steel Process CO2 Intensity per Ton by Pathway` = Σ_fuel intensity × feedstock share × fuel CO2 content; spliced into `Process Emissions before CCS[241, CO2]` (policy) and `BAU Process Emissions after GDP and Fuel Production Adjustment[241, CO2]` (BAU); the choice cost nets the fuel-price carbon tax off feedstock quantities and adds the process-CO2 tax term gated by the exemption/coverage toggles (§2 done in the same stroke). **Gate results:** endogenous 2025 process CO2 = **41.7 MMT vs GHGI's 40.7 anchor** (the old BPE input ran 45.1, ~10% above inventory); the old series *grew* to 62.2 MMT by 2050 while the endogenous one declines to 39.1 — a −23 MMT BAU correction at 2050, the process-emissions analog of the energy-trajectory refresh. Choice costs identical at defaults; zero ripple into any fuel-use variable. The explicit coke/met-coal physical chain (coke ovens, PCI split, byproduct gases) remains open for when coke-oven detail or coke trade matters; the carbon totals it would produce are already captured here. Implementation note for cement replication: the fuel-CO2-intensity lookup required an elementwise mapping variable — a mapped subrange banged inside SUM ranges *independently* of its family (silent 4.8× double-sum, caught by the GHGI gate; now in the KB gotchas).

## 2. Carbon tax into the pathway choice

Add to `Steel Pathway Levelized Cost per Ton`: (combustion CO2e intensity by pathway × industry-sector carbon tax on fuels — already implicit once fuel prices carry the tax, verify no double count) **plus process CO2 intensity × carbon tax**, honoring `BEPEfCT` (process-emissions exemption toggle, per Industry Category) and the border-adjustment/rebate toggles the way the existing process-emissions cost chain does. This is what makes H2-DRI and CCS pathways win under a carbon tax — the module's core policy response.

## 3. Clean Steel Standard (the D2 overlay)

RPS-pattern: `Clean Primary Steel Standard Percentage` (new lever + FoPITY element) = minimum share of *primary* production (Jeff's sketch scopes it to primary; scrap-EAF already near-clean) from qualifying pathways (qualification mask input — H2-DRI, MOE, AE, BF-BOF+CCS at some capture threshold). Mechanics mirror `Elec Portfolio Std`: compute the shortfall vs. the logit outcome, force the marginal reallocation of *new capacity* (and, if needed, early retirement + replacement) from cheapest qualifying pathways, and book the compliance cost premium into the expenditure chains (Phase 3). Green procurement (#54) can later ride the same qualification mask as a demand-side share.

## 4. Endogenous relining, early retirement & merit-order utilization (the stranding machinery)

**Endogenous reline-vs-replace (Dan, 2026-08-20 — replaces the fixed retirement schedule).** The GEM campaign data stops being a retirement schedule and becomes a **decision schedule**: `SPRS` is recast as `Steel Capacity Reaching Campaign End by Pathway` (tons/yr hitting a reline-or-replace decision, from GEM reline years + campaign length — most of the fleet decides 2026–2033, then ~20 years later). At each decision point the model chooses endogenously by cost:
- **Reline** (continue the pathway): reline capex per ton — real anchor: Gary BF14's $350M / 2.54 Mt ≈ **$138/(t/yr)**, roughly a tenth of greenfield — annuitized over one campaign, plus the pathway's ongoing energy + carbon costs.
- **Replace/retire**: the capacity leaves the stock and the resulting unmet need flows into the existing new-capacity pathway logit (which sees the same carbon tax, standards, and subsidies).
The choice is a two-option relative-cost logit (or a threshold rule if the team prefers determinism), fully policy-influenceable: a carbon tax raises the BF reline's lifetime operating cost; a Clean Steel Standard can disqualify relining outright for the marginal tons; an early-retirement lever forces the replace branch. At default (no-policy) costs the reline branch should win nearly everywhere — reproducing observed behavior (GEM shows relines planned across the fleet) — so BAU emerges from the same economics rather than from a hand-authored schedule. New inputs: reline capex per ton by pathway, campaign length (with the GEM-derived decision-year schedule replacing today's SPRS values).

**IMPLEMENTED (P2-B, 2026-08-20 late).** SPRS recast to the decision schedule; relined capacity re-enters the pool one campaign later via a standalone DELAY FIXED (nesting it inside MIN kills LOADMODEL — now in the KB gotchas); reline-vs-replace is the SRSW-weighted two-option logit against the share-weighted new-build cost; decision retirements exit production same-year and are replaced same-year. **Gates:** twins exact at defaults; production = demand every year; recurrence verified (the 9.05 Mt 2027 wave returns as a 7.98 Mt decision in 2047 = relined × share, one campaign later). **BAU:** reline share 0.81–0.88 → BF-BOF erodes 23.5→18.0 Mt by 2050 (EAF share keeps drifting up, consistent with history; the SRSW=25 draft dial sets this erosion rate — calibration review item). **Under the $300/t industry carbon tax, the stranding channel finally fires:** reline share collapses with the tax ramp (0.82 in 2027 while the tax is still phasing in — a realistic vintage effect — then 0.18 by 2033 and 0.02 by 2047); 2050 BF-BOF production falls 18.0→1.1 Mt, coal use 336→20 TBtu, steel process CO2 31.8→4.0 MMT; replacement fills scrap EAF **to exactly the 70 Mt scrap cap** (the availability constraint binds and works), with the overflow going to NG-DRI (5.3 Mt) and H2-DRI (1.4 Mt). BF-BOF-with-CCS stays at zero pending its capture economics (§5).

- **Lever:** `Fraction of Steel Capacity Retired Early` (or tons/yr) remains available as a direct policy instrument on top of the endogenous decisions — same shape as the electricity coal-retirement lever.
- **Merit-order utilization:** replace the uniform production ration with cheapest-first dispatch of capacity (by pathway levelized *operating* cost incl. carbon tax), capped by SYSCU. Under-used capacity then shows falling realized utilization.
- **Cost-based stranding:** capacity whose realized utilization stays below a threshold for N years retires (or: operating-cost > revenue test). This is the endogenous channel Dan endorsed instead of a utilization lever; it interacts with #364-style oscillation risk, so it should carry a lag/smoothing and be tested under aggressive scenarios before shipping.

**Recommendation:** implement merit-order + early-retirement lever in Phase 2; hold cost-based *automatic* stranding for a flagged Phase 2b with dedicated oscillation testing.

## 5. CCS reconciliation

Today industry CCS is a %-of-emissions-captured framework by Industry Category with its own costs and the carbon-tax rebate. The module adds `BF BOF with CCS` as a discrete pathway (capture at the plant) plus retrofits (`Blast Furnaces Retrofitted with CCS This Year` in Jeff's sketch). Two coherent options:
- (a) The pathway's captured tons flow *into* the existing CCS accounting (capacity, fuel-for-CCS, 45Q-style subsidies, tax rebate) as a steel-specific stream — one CCS ledger, no double counting; the generic %-capture lever stops applying to 241.
- (b) Keep the generic %-capture lever for steel and drop the CCS pathway — simpler but loses the retrofit economics and the pathway competition story.

**Recommendation:** (a). The retrofit is modeled as a capacity conversion (traditional → with-CCS at retrofit capex increment, new input) triggered by the logit/standard, with capture energy already in SEIbPaF's CCS column. Needs Jeff's eyes — it touches the CCS framework's conventions.

## 6. Phase 2 new inputs (workbook list)

CDpTS coke demand per ton; MCtCR met-coal-to-coke ratio; SPCI Steel Process CO2 Intensity by pathway (or computed from the carbon balance); CSSQ qualification mask; retrofit capex increment; early-retirement lever schedule elements (FoPITY); carbon content of steel (if the optional term is ever wanted).

## 7. Decisions and open questions

**Settled (Dan, 2026-08-20 evening):** retirement/relining is endogenous per §4 (fixed-schedule SPRS is interim only); the BAU trajectory refresh is accepted and documented (bridging numbers in the 1b memo); Phase 2 implements emissions first (coke chain → process CO2 → carbon tax in the choice), then §4's decision machinery, then the Clean Steel Standard.

**Still open for the team:**
1. Does the Clean Steel Standard cover primary only (Jeff's sketch) or all production?
2. CCS option (a) vs (b) in §5 — Jeff should weigh in.
3. Reline-vs-replace choice form: two-option logit (smooth, calibratable) vs. deterministic cost threshold (lumpy, matches unit-level reality)?
4. Should merit-order utilization feed realized utilization back into the choice cost (endogenous stranding signal), or stay one-way in v1?
