# Assessment: develop_4.2 industry breakout sketch — can it be finished, and can it merge into 4.1?

*Prepared 2026-08-20 for Dan O'Brien's review. All findings below are inputs for staff review, not settled conclusions — verify quoted variable names and issue references against the primary sources (EPS.mdl, GitHub) before using them in team decisions.*

## 1. What the branch actually contains

`origin/develop_4.2` is **one commit** by Jeff (758410a7, 2025-10-09): *"Add first draft sketch (without equations) to Industry - Main for chemicals, steel, cement, refining, and direct use of geothermal heat by industry."* It touches only `EPS.mdl` and sits on a base (4d030cea, 2025-10-08) that is now **884 commits behind develop**.

There are **no equations, no input data, no cash flows** — the design content is:

- **134 stub variables** (`A FUNCTION OF(...)` placeholders: names + intended dependency wiring, all units/comments blank), in five labeled regions: **Steel (~46 stubs), Refining (23), Cement (17), Chemicals process CO2 (14), Direct use of geothermal (9)**, plus cross-cutting shared nodes.
- **Two proposed new subscripts** sketched as note-variables: `Steel Production Pathway` and `Cement Raw Material Type`.
- **Design notes** flagging Jeff's own open questions (detailed in §3).

So this is a concept map, not partial implementation. The scope is also wider than "break out iron & steel" — it is the industrial-feedstocks agenda from issue [#181](https://github.com/EnergyInnovation/eps-us/issues/181) (Jeff, 2021) plus [#189](https://github.com/EnergyInnovation/eps-us/issues/189) (endogenize process emissions) and [#388](https://github.com/EnergyInnovation/eps-us/issues/388) (geothermal, Dan's placeholder issue). There is no dedicated GitHub issue for the steel breakout itself; the sketch is the primary design artifact. The `4.2` label carries 19 open issues, several of which interact with this work (#364 production oscillation for energy-intensive industries, #311 clinker↔coal-generation coupling, #339 biofuel production energy).

## 2. Reconstructed design intent, cluster by cluster

### Steel (the core)
Physical-units design: **tons of steel**, not dollars/BTU.

- **Demand:** `Steel demand` → net imports → primary vs. secondary split.
- **Pathways** (the new subscript): traditional BF-BOF, BF-BOF + CCS (incl. retrofits of surviving blast furnaces), NG-DRI, H2-DRI, molten oxide electrolysis, aqueous electrolysis, secondary (scrap/EAF).
- **Allocation mechanic:** target-driven, per Jeff's inline note — *"Allocate clean production pathways to meet target, assume the rest is traditional (or perhaps some secondary steel shifting)."* A `Clean Primary Steel Standard or Target Percentage` lever pulls clean pathways in (cheapest/most mature first, bounded by `Technology maturity based limits`), residual demand defaults to BF-BOF. This is **not** the relative-cost logit the model has since standardized on — a decision point, see §5 Q2.
- **Capacity stock:** `Surviving Steel Production Capacity` with cost-based retirements + an early-retirement policy lever; `Unmet Steel Production Capacity Need` drives new builds.
- **Scrap supply:** three-source availability (forming/fabrication, post-consumer, vehicles/demolition) capping secondary steel — with Jeff's explicit escape hatch: *"OR specify amount of secondary steel growth directly while ignoring scrap availability."*
- **Energy & emissions:** per-ton energy intensity by pathway × fuel → energy use; a coke chain (coke per ton BF-BOF → met coal → coke-oven CO2); process vs. energy CO2 split with an optional "carbon stored in steel" deduction; CCS demand handed to the existing CCS framework.

### Cement
Cement demand → clinker demand (clinker share + substitution lever) → clinker capacity stock → new kilns split **electric vs. combustion-heated** (policy lever), with Jeff's note explaining why it matters: electric kilns emit near-pure calcination CO2 (cheap capture) while combustion kilns mix it with flue gas (costly capture). Calcination CO2 from a raw-material-type subscript (limestone vs. calcium silicates/Brimstone, alternative chemistries); an optional clinker-substitutes cost branch (fly ash, silica fume — distinguished from clinker raw materials). Red-flagged to-do: route both CO2 streams through the existing new + retrofit CCS framework.

### Chemicals (thinnest cluster)
A carbon mass-balance: carbon in feedstocks (fossil vs. bio vs. H2+captured-CO2, chosen via a clean-feedstock standard) minus carbon retained in products (plastics etc., in mass units) = process CO2. Most stubs have no dependencies yet — this is the least developed area.

### Refining
Crude slate → product outputs + RFG/petcoke byproducts (yield ratios, with an open question whether product mix should move them). RFG/petcoke either feeds **blue H2 production with CO2 storage** (clean-refinery-operations lever) or is burned; NG splits between SMR hydrogen and heat, with an electrification-of-heat pathway. Process CO2 again by carbon balance; non-CO2 pollutants by intensity.

### Geothermal direct-use heat
Resource potential + LCOH cost curve (with subsidy lever) compared against last year's deployed industrial-heat LCOH → cost-effective potential → **reduces energy demand of existing equipment without changing production** (Jeff's note). Deliberately narrow (possibly steam/boilers only). Note this is a *different* integration pattern than thermal batteries, which compete inside the fuel-choice logit — the two should probably be reconciled.

## 3. Jeff's own unresolved design questions (verbatim notes in the sketch)

1. *"EITHER separate primary and secondary steel by ISIC code (incl. DLIM, etc.) OR create separate variables to control energy types"* — the IO-layer architecture question.
2. Target-based allocation with *"perhaps some secondary steel shifting"* — allocation mechanic not settled.
3. *"Check whether the output product mix affects the ratio of byproduct (RFG and petcoke) to crude oil consumed."*
4. Scrap-availability modeling vs. direct secondary-steel override.
5. Cement CCS: tie both CO2 streams *"to the existing CCS framework, including new and retrofit CCS"* (red flag = to-do, not done).

## 4. Compatibility with the current 4.1 model (develop)

**A git merge of the branch is not viable and not worth attempting.** The commit is sketch-only, its base predates the entire 4.1 industry program, and it wholesale-repositioned the Industry - Main view — which develop has since redrawn again (temp bands, thermal batteries, WHR regions). The value of the branch is 100% design; the path is **re-implementation on the 4.1 base using the sketch as the spec**, keeping `develop_4.2` as a frozen reference.

**What the current model gives the design (better than its Oct-2025 base did):**
- `iron and steel 241`, `cement and other nonmetallic minerals 239`, `chemicals 20`, `refined petroleum and coke 19` are already standalone Industry Categories — IO linkages, trade (incl. the new IESE/EMSbIC CES share equations), financing (BCoISC + instrument accounting), and carbon-tax plumbing all exist per category.
- The temperature-band `Industrial Process` restructure gives real heat-demand granularity (`heat above 1000 C` etc.) to hang route-specific heat on.
- The vintaged equipment stock (`Model Run Vintage`) and the individual-site retirement profile (`BIISRP` — whose documentation literally cites the lumpy retirement of "one integrated steelmaking plant") are ready-made capacity/retirement machinery.
- The thermal-battery project established the full pattern the steel module needs for **cash flows**: parallel adoption stock outside `Industrial Fuel`, entity-ledger booking, ISIC expenditure routing, GRA subsidy types + FoPITY policy elements across 18 schedule CSVs, financing-repayment ladders, dedicated supplemental outputs, and a validation-gate discipline.
- The relative-cost logit (now the house standard for fuel/equipment choice) is a natural allocation mechanic for pathway competition.

**The hard structural gaps (in rough order of difficulty):**

1. **No physical production units exist anywhere in the model.** Output is dollars by ISIC + BTU; there is no tonnage variable of any kind (verified by grep). Steel-by-pathway requires a tons layer plus a mapping back to `Output by ISIC Code` and to the demand-side feedbacks (`Percent Change in Production due to Policies`, IESE trade shifts, the material-efficiency lever which already covers steel & cement). Getting the tons↔dollars↔energy triangle consistent — in both BAU and Policy twins — is the central design problem.
2. **Double-counting boundary with the generic industry structure.** `iron and steel 241` currently gets all its energy through the generic fuel-choice logit / temp bands / vintage stock, and is eligible for WHR, thermal batteries, clean-heat subsidies, electrification levers, IFSR fuel shifting (there's an `IFSR-ironsteel.csv`). A route-based module must carve steel's route-determined energy *out* of that structure (or restrict itself to the route-differentiating processes and leave e.g. machine drive/HVAC generic). Every existing industry lever needs an explicit answer for how it now reaches steel.
3. **BAU calibration replaces bit-identity.** Unlike thermal batteries (a new option shipped disabled → bit-identical gate), a steel breakout *replaces* steel's BAU representation. The validation gate has to become "BAU emissions/energy/output for 241 match the current model / AEO within tolerance," which is a calibration exercise, not a diff.
4. **Process emissions become endogenous for steel** (coke/calcination chemistry) — which is exactly #189, but means reconciling with the exogenous `BPE` series and the absence today of any steel entry in `industries with process emissions policies`.
5. **New fuels/commodities:** coke and met coal as tracked intermediates (currently only `hard coal if`), scrap as a resource, blue-H2-from-RFG in refining — each touches the Fuels layer, pollutant intensities, and supplier cash-flow entities.
6. **Input data from scratch**, per-pathway: energy intensity by fuel, capex/O&M per ton, maturity limits, scrap supply by source, coke ratios, clean-steel-standard schedules; cement raw-material chemistry and costs; refinery yields; geothermal potential/cost curves. All sourceable (AISI/USGS, IEA, Mission Possible Partnership, EPA GHGRP/FLIGHT, NREL) but weeks of curation to house workbook standards, and every geography inherits the schema.
7. **#364 risk:** adding a capacity-stock/allocation loop for the most energy-intensive industry interacts with the known output-oscillation issue for energy-intensive industries — worth designing the smoothing/lag structure deliberately.

## 5. Questions for Dan / the team before building

1. **Scope of v1.** Steel only (recommended — cleanest boundary, matches your framing), or steel + cement (they share the capacity-stock/CCS pattern)? Chemicals and refining are much less developed in the sketch; geothermal (#388) is separable and could follow the thermal-battery playbook independently.
2. **Allocation mechanic.** Jeff sketched target-driven allocation (standard pulls clean pathways, remainder BF-BOF). Since then the model standardized on relative-cost logits. Recommendation: cost-logit competition among pathways for new capacity (BAU-consistent, carbon-tax-responsive) with the Clean Steel Standard as a constraint overlay — same architecture as electricity dispatch vs. RPS. Does Jeff agree, or does he want pure target allocation?
3. **IO-layer architecture** (Jeff's EITHER/OR note). Recommendation: keep a single `iron and steel 241` ISIC category and do the primary/secondary/pathway split in new internal variables (no DLIM/TLIM surgery, no ISIC subscript change); map pathway costs into the existing expenditure/revenue chains. Splitting the ISIC code would ripple through every IO input for every geography.
4. **Carve-out boundary.** Which of steel's processes leave the generic structure? Option A: all of 241 becomes route-based (clean, but WHR/thermal-battery/clean-heat levers need re-plumbing to reach it). Option B: only ironmaking/steelmaking heat (`heat above 1000 C` + coke chain) is route-based; lower-temp heat, machine drive, HVAC stay generic (smaller blast radius, but a subtler boundary to keep consistent). This is the decision that most determines effort.
5. **Tons↔dollars mapping.** Fixed start-year $/ton per pathway-agnostic steel output, with tonnage driven off ISIC output changes (as production-quantity proxy, like the fuel-industries convention)? Or let tonnage drive dollars? Needs one clear direction of causality to avoid circularity with the IO feedbacks.
6. **Does Jeff have anything beyond the sketch** — notes, a memo, a spreadsheet of intended pathway parameters? Ten minutes of his context could save days of reverse-engineering (and this assessment should be checked with him regardless).
7. **Sequencing vs. 4.1.** Is 4.2 work gated on 4.1 shipping (and AEO26 calibration landing)? Building on a moving develop is fine with the phased approach below, but calibration targets should be frozen first.
8. **Pathway list for v1.** Suggest: BF-BOF, BF-BOF+CCS (incl. retrofit), NG-DRI+EAF, H2-DRI+EAF, scrap-EAF as full pathways; MOE and aqueous electrolysis as maturity-capped placeholders (zero potential until unlocked).

## 6. Proposed plan (steel-first, phased, each phase gated)

- **Phase 0 — Design memo** (no model edits): resolve §5 with Jeff/team; specify subscripts, variable inventory, tons↔dollars↔energy accounting, carve-out boundary, BAU data sources, validation gates. Deliverable: `Steel_Breakout_Design.md` for sign-off. *This is the only phase that should start before the questions are answered.*
- **Phase 1 — Physical core:** `Steel Production Pathway` subscript; tonnage demand chain; capacity stock with vintages + retirements (reusing MRV/BIISRP patterns); scrap supply; pathway allocation (logit + standard); per-ton energy intensities → steel's contribution to `Industrial Fuel Use`; carve-out per Q4. Gate: BAU-equivalence for 241 energy/output vs. current develop within tolerance; all other industries bit-identical.
- **Phase 2 — Emissions & CCS:** endogenous coke/process CO2 (retiring steel's exogenous BPE share), energy CO2 by pathway, CCS new-build + retrofit via existing framework, carbon-tax exposure incl. border adjustment/process-exemption toggles. Gate: BAU 241 emissions match GHGRP/EPA benchmarks; policy-response sanity runs.
- **Phase 3 — Cash flows:** capex/O&M per pathway through the financing ladders and instrument accounting; fuel + coke/scrap expenditures by entity; clean-steel-standard compliance costs; early-retirement stranding; GRA types + FoPITY elements; IO handoff. Gate: entity-ledger balance check (the TB ledger-audit method, `TB_checks.lst` style).
- **Phase 4 — Input data & calibration:** sourced workbooks per house conventions for every new input; AEO/AISI/GHGRP calibration; IES shareweight adjustments for the carve-out.
- **Phase 5 — Surface area:** sketch views (a dedicated "Industry - Steel" view rather than crowding Industry - Main), WebAppData, policy schedule CSVs, docs; then cement as the next module reusing the pattern.

**Effort calibration:** Phase 1–4 for steel alone is plausibly 2–3× the thermal-battery project (which was one technology inside an existing choice structure; this replaces a sector's production representation). Cement adds maybe half that again by reuse. Chemicals/refining need real design work before they're estimable.

## 7. Bottom line

1. **Can this be finished?** Yes — but "finishing the branch" is the wrong frame. The branch is a valuable design sketch with Jeff's open questions embedded in it; the work is a fresh, phased build on develop using it as the spec. Nothing in it is beyond the patterns this codebase already has (capacity stocks, logits, CCS hooks, entity cash flows) — the genuinely new element is the physical-tonnage layer and its reconciliation with the dollar/BTU world.
2. **Merge potential into 4.1?** As code: none; don't try. As design: high — the 4.1 industry structure (temp bands, vintages, cost logits, TB cash-flow patterns) is a *better* foundation than the base Jeff sketched on. The two real merge risks are the double-counting boundary with the generic industry structure and BAU recalibration replacing bit-identical validation.
