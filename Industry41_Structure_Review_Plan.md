# Review Plan: 4.1 Industry-Sector Structure (develop) vs 4.0.5

Working plan — draft for staff review, 2026-07-17. This is a plan for a skeptical evaluation,
not the evaluation itself. All quantitative claims below (array sizes, counts) were measured
from the repo and should be re-verified as the working tree evolves.

## 0. What is being reviewed

The 4.1 industry sector on `develop` is a ground-up replacement of the 4.0.5 approach,
in three layers:

**Layer A — Architecture change (the big one).** 4.0.5 modeled industry top-down:
BAU fuel use by industry category (`BIFUbC`) scaled by percent-reduction policy levers
(`PPRiFUfERoIF`, `PPRiFUfICaWHR`, `PPRiFUfIIaIoE`), fuel switching via `IFStFS`, cost
curves via `CtIEPpUESoS`. Only 3 equations were subscripted by `Industrial Process`
(8 elements) — process detail was nearly vestigial. 4.1 replaces this with a bottom-up
**vintaged equipment-stock model**: new `Model Run Vintage` subscript (123 references),
logit fuel choice for new equipment (`IES` shareweights × 12 fuels, `IELC` logit
coefficient), survival/retirement curves (`IESD`), equipment capital cost and financing
(`IECCpUAEU`, `RPfFISCC`), unit energy factors with efficiency-standard response
(`SYIEUEFbIPaF`, `IEMUEF`, `EoIEPwEEI`, `BIEEI`), utilization of installed stock, clean
heat ITC/PTC subsidies (`BCHSR`), and waste-heat recovery (`WHRCC`, `WHRPbI`). Net:
~26 new `InputData/indst/` acronym folders, ~7 retired.

**Layer B — Temperature-band restructure (in flight in the working tree as of
2026-07-16 PM).** `Industrial Process` 8/10 → 11 elements; the four
boiler/nonboiler heating elements become five °C bands per
`IndustrialProcess_NewElement_Plan.md`. Uncommitted: EPS.mdl subscripts + IES blocks,
60 renamed/new IES CSVs, regenerated FoPITY files, `TempBandRestructure_MDL.js` /
`TempBandRestructure_FoPITY.js` scripts.

**Layer C — Runtime-optimization pass (commits 00cce561…2c873fcf, 7/15–16).** FoPITY
read as `GET DIRECT LOOKUPS` with breakpoint-only CSVs; future-year schedules isolated
to a `foresight policy element` subrange and wrapped in `INITIAL`; industrial logit
weight and utilization factor hoisted out of big arrays; discount-factor and 1/2π hoists.

**Review hygiene precondition:** Layer B is uncommitted and mixed with `.bak` files.
Before the review starts, commit (or branch-commit) the band restructure so the review
has a stable target and before/after runs are reproducible.

## 1. Workstream A — Architecture & design choices (staff-judgment questions)

The skeptical questions about whether this was the right structure, independent of
whether the code is correct:

1. **Granularity vs. data support.** The core stock arrays are
   [25 Industry Category × 11 Industrial Process × 12 Industrial Fuel × 26 Model Run
   Vintage] ≈ 85,800 elements, twinned BAU/Policy. MECS/NREL data genuinely resolve far
   fewer cells. Which dimensions carry real information vs. copied-down defaults? Where
   is false precision a communication risk for published results? Deliverable: a table of
   input datasets × the dimensions they actually resolve vs. the dimensions the model asks of them.
2. **Is full vintage tracking necessary?** Vehicles and power plants use vintages because
   standards lock in at purchase and retirement economics matter. Test whether industry
   policy questions (early retirement lever, efficiency-standard lock-in, clean-heat tax
   credits with duration) genuinely need per-vintage state, or whether an aggregate
   stock + average-survival formulation would produce materially identical outputs at a
   fraction of the state space. Proposed test: build a reduced prototype for 2–3
   industries offline and compare lever responses. This is the single biggest
   runtime-vs-fidelity tradeoff in the new structure.
3. **Logit fuel choice.** (a) IIA: 12 fuels include near-substitutes (green H2 / LC H2 /
   generic hydrogen; crude vs. heavy resid) — does the flat logit distort substitution?
   Would nesting (electric vs. combustion, then fuel) be better? (b) Calibration: how were
   `IES` shareweights and `IELC` estimated — fit to observed shares, or asserted? (c)
   Numerics: behavior at extreme cost differentials (exp overflow/underflow guards), and
   the `10000×` scaling convention. Compare against the transportation sector's
   TTS/TTLE precedent for consistency.
4. **Utilization construct.** `MIN(1, output demand / potential output)` spreads
   under-utilization uniformly across vintages and fuels. Skeptical cases: declining
   industries (does old capacity idle before new?), rapid electrification (does fossil
   equipment idle without retiring, and is its capital cost still carried in cash flows —
   stranded-asset accounting?), and the implicit feedback loop via `Last Year Output by
   ISIC Code` → utilization → energy use → macro feedbacks → next-year output. Confirm
   the loop is stable and intentionally one-year-lagged.
5. **Temp bands as the process taxonomy.** Bands are well-suited to electrification
   analysis, but: the boiler→band folding assumptions (steam temperature allocation)
   move real energy between bands; MECS °F splits don't align with the °C bands (genuine
   re-disaggregation); cross-band substitution is impossible by construction (is that
   right for e.g. heat cascading/WHR?); and `RPfFHSCC` (hydrogen sector) still uses the
   old element names in a separate family — decide alignment.
6. **Start-year conservation & BAU calibration.** How is the new structure anchored so
   BAU industrial fuel use matches calibrated history (AEO26 work)? Verify shares sum to
   100% (BPFUbIP) and Start Year `Industrial Fuel Use` by industry × fuel reproduces the
   4.0.5 values.
7. **Cross-model consistency.** Cash-flow entity tagging of equipment capex/financing;
   ISIC mapping into the IO layer (equipment purchases → which supplying industries?);
   whether the industry logit + vintage pattern matches the conventions other sectors
   use (maintainability across geographies — this EPS.mdl ships to every geography, and
   every geography must supply the ~26 new input datasets).

## 2. Workstream B — Implementation correctness audit (code review, largely delegable)

1. **BAU/Policy twinning completeness.** Script-assisted: extract every new
   industry-sector variable; verify each policy-affected one has a `BAU` twin and no
   cross-contamination (policy vars in BAU equations or vice versa). The 7f09728c spot
   review confirmed the pattern holds for the hoisted variables; extend to the full block.
2. **Stock-flow integrity.** For equipment stocks: additions + surviving preexisting −
   retirements ≥ 0 in all cells; early-retirement lever does not double-count natural
   retirement (`IESD` curves vs. `Minimum Share of Start Year Industrial Equipment
   Retired`); vintage bookkeeping at model start/end years.
3. **FoPITY wiring** (order-sensitive, silent-failure-prone). Policy-element cycle order
   in `FoPITY-policy-elements.csv` vs. the 9 `VECTOR ELM MAP` anchors (industry-major
   for six industry×process policies, process-major for `indst eqpt cost of capital`,
   process×fuel for RnD) — re-verify after the Layer-B regeneration. Runtime spot-check:
   VDF2TAB-extract `Selected Policy Implementation Schedule` rows and confirm each
   industry lever ramps the intended element (the classic mis-order symptom is a policy
   silently landing on the wrong process).
4. **Layer B mechanical audit.** Verify `TempBandRestructure_MDL.js`/`_FoPITY.js` output
   against the checklist in `IndustrialProcess_NewElement_Plan.md` §3: 60 IES equation
   blocks, 9 anchors renamed, inline lever matrices at 25×11 / 11×25 / 11×12 / 5, no
   orphaned `boilers`/`nonboiler` references (grep), `.cin` sweep (294 stale SETVAL
   lines expected in `US_ClimateAmbition.cin`, `hydgn.cin`, `procemiss.cin`).
5. **Layer C re-review.** 7f09728c (logit/utilization hoist) already reviewed: algebra
   exact, twinning preserved; two minor cleanups noted (duplicate inline utilization
   expression in `(BAU) Output from Preexisting Industrial Equipment`; hoistable
   denominator `SUM(Weight[Industrial Fuel!])`). Still to review (first attempt aborted):
   FoPITY breakpoint/lookup semantics (linear-interpolation exactness, `INITIAL` safety
   on `Selected Policy Implementation Schedule for Future Years`, completeness of the
   `foresight policy element` subrange), 3ec7ee96 discount/2π hoists, and the
   grab-bag 2c873fcf "runtime code adjustments".
6. **Units audit** on all new industry variables (Vensim units check in GUI, or grep the
   `~` annotations).

## 3. Workstream C — Behavioral validation (headless runs)

All runnable via the standard `.cmd` harness; each produces `.tab` extracts for diffing.

1. **Start-year conservation:** develop BAU vs. `dev_4.0.5_aeo26` BAU, Start Year
   `Industrial Fuel Use` by industry × fuel — should match to calibration tolerance.
2. **BAU trajectory drift:** headline outputs (Total CO2e, Industrial Fuel Use by fuel,
   Total Electricity Demand, GDP, jobs) 2025–2050, develop vs. 4.0.5. Bit-identity is
   not expected (the architecture changed); the deliverable is a drift table with each
   material divergence attributed to a named structural cause. Unattributed drift = finding.
3. **Per-lever smoke tests** (one lever at a time, moderate setting): electrification by
   band, shift to alt fuel, early retirement, cost of capital, fuel & elec efficiency
   stds, clean heat ITC and PTC, WHR, RnD capital-cost reduction. Check sign, rough
   magnitude, monotonicity in lever strength, and FoPITY landing (see B.3).
4. **Stress tests:** 100% electrification of one band (utilization + stranded capital
   behavior); an industry with collapsing output (negative-stock / idle-capacity
   behavior); all-levers-max (numerical stability, echoes of the CES-100% crash class of
   bugs); QUANTUM noise check on `Change in ...` outputs with all levers at 0
   (should be exactly zero everywhere — the cheapest twinning test there is).
5. **Scenario re-run:** after `.cin` remap, `US_ClimateAmbition` develop vs. published
   4.0.5 results; explain deltas.

## 4. Workstream D — Runtime assessment

1. **Measure, don't infer:** initialization time and full-run wall time, develop HEAD vs.
   `dev_4.0.5_aeo26` vs. develop-with-Layer-B, same machine, 3 runs each (the harness
   already exists; `NoSettings` run as the baseline case). Note: the last runtime commit
   (2c873fcf, 7/16 15:39) postdates the last local validation run (NoSettings.vdfx,
   7/16 14:16) — confirm HEAD state actually simulates clean before timing.
2. **Attribute the cost:** the vintaged industry arrays (~85.8k elements × twins ×
   several equation families) are the main new load; quantify their share of the
   develop-vs-4.0.5 runtime delta so the Workstream A.2 vintage question has a price tag.
   Layer B adds ~10% to process-dimensioned arrays (10→11 elements) — measure the increment.
3. **Remaining optimization candidates:** the two 7f09728c leftovers (B.5); any hot
   spots surfaced by comparing init vs. run time; SDEverywhere/web-app compile impact of
   the subscript growth (the develop line exists partly to serve the web build — confirm
   the generated code size and browser runtime stay acceptable).

## 5. Sequencing & division of labor

1. Commit Layer B (stable review target). — Dan
2. Workstream B (code audit) + D.1 timing runs — delegable to Claude sessions, headless.
3. Workstream C runs — Claude executes; Dan/staff judge drift attributions and lever
   plausibility.
4. Workstream A — staff discussion, fed by the B/C/D evidence; A.2 (vintage necessity)
   and A.3 (logit calibration) are the two most consequential design questions.
5. Findings memo for staff review; coordinate architecture-level conclusions with the
   core model team (EPS.mdl is shared across all geographies).

## 6. Early observations already in hand (preliminary, for staff review)

- 7f09728c hoisting: verified algebraically exact, twinning preserved; ~92% reduction in
  exp() calls in the industrial logit and 26× reduction in utilization-factor work.
  Two minor cleanups identified (see B.5).
- The vintage + logit architecture mirrors proven EPS patterns (transportation,
  electricity), which is a maintainability point in its favor; the open question is
  cost/benefit of the vintage dimension specifically (A.2/D.2).
- Everything here is an input for staff review, not a sign-off; data-sourcing claims in
  particular need verification against primary sources.
