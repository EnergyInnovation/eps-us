# Steel breakout design spec (v0 draft, 2026-08-20)

*Working spec for the iron & steel production-pathway module. Decisions D1–D8 reflect Dan's answers of 2026-08-20; everything else is a proposal open to revision. Background and full option analysis: `Industry_42_IronSteel_Breakout_Assessment.md`. Jeff's original sketch: branch `develop_4.2` (758410a7).*

## Decisions (settled with Dan, 2026-08-20)

- **D1 — Scope:** steel only for v1. Every structural choice gets logged in `Industry_Breakout_Replication_Log.md` so cement (next) and chemicals (maybe after) replicate the pattern.
- **D2 — Allocation mechanic:** relative-cost logit over pathways for new capacity, house power form (same as `Industrial Equipment Fuel Choice Weight`). Clean Steel Standard target arrives later as a constraint overlay (dispatch/RPS pattern).
- **D3 — IO layer:** ISIC unchanged; single `iron and steel 241` category; pathway split lives in new internal variables. Jeff's "split by ISIC incl. DLIM" alternative shelved for later revisit.
- **D4 — Carve-out boundary:** subrange `Industrial Process` into process end uses (5 heat bands, cooling, machine drive, other processes) and nonprocess end uses (facility HVAC, facility lighting, other nonprocess). Steel's **process** end uses are served by the pathway module; **nonprocess** stays in the generic structure. Fallback if the subrange split proves too painful: fully offboard steel.
- **D5 — Design references:** the 4.2-labeled GitHub issues, esp. #181 (feedstocks — BF coal vs H2-DRI is exactly this module), #189 (endogenous process emissions — falls out of the coke/pathway chemistry automatically for steel), #398 (tariffs), #54 (green procurement — future lever on this structure).
- **D6 — Timing:** start now; drafts running; candidate for inclusion in the 4.1 release.
- **D7 — Tons↔dollars direction:** dollars drive tons. BAU steel tonnage is an exogenous input; policy tonnage = BAU × (1 + `Percent Change in Production due to Policies[iron and steel 241]`). The module never writes tonnage back into the IO layer; its costs feed back through the existing expenditure/revenue chains (Phase 3). Avoids circularity.
- **D8 — Validation convention:** Phase 1a is compute-only (nothing consumed by existing variables) → gate stays bit-identical at defaults. From Phase 1b (carve-out wiring) the gate becomes BAU-calibration equivalence for 241 (energy by fuel, emissions, output within tolerance of the current model / AEO), all other industries bit-identical.

### Round-3 decisions (Dan, 2026-08-20 PM)

- **D9 — Feedstock endogenized:** at 1b wiring, the module replaces *both* BIFU streams for iron & steel (energy `BIFUfE` and feedstock `BIFUaF` — coking coal sits in the latter), and steel's process CO2 goes endogenous (coke chemistry) in the same step, retiring 241's share of the exogenous BPE series (#189).
- **D10 — Full BAU twinning:** complete BAU twin chain (BAU logit at BAU fuel costs and BAU demand), implemented in Phase 1a.
- **D11 — Explicit utilization:** stocks are nameplate; `SYSCU` (AISI ~0.76) sizes new builds, grosses up capex per ton produced in the choice cost, and caps the production ration. Held constant as a *target*; realized utilization is emergent (falls in demand slumps). Policies should move utilization only through demand (e.g. tariffs → domestic production) and, later, through composition (merit-order utilization + cost-based stranding under a carbon tax / Clean Steel Standard) — not through a direct utilization lever. Rationale: the sustainable ceiling is ~90% not 100% (maintenance, relines); BFs have little turndown flexibility while EAFs flex, so the realistic decarbonization channel is clean capacity running first and under-used BF capacity becoming uneconomic and retiring — the coal-plant pattern, and the same structure EPS's electricity sector uses.
- **D12 — Same-year commissioning:** new builds produce in their build year (electricity-sector convention), eliminating the one-year-lag shortfall.
- **BSD semantics confirmed:** demand for domestically *produced* steel (production basis, includes exports); trade effects continue to flow through IESE on the dollar side.

### Round-4 decisions (Dan, 2026-08-20 evening)

- **D13 — Carve-out owns all of 241's process energy**, and the start-year calibration target is *actual* energy consumption and emissions inventories (MECS/EIA/GHGRP vintage-current), not necessarily the model's existing BIFU series where that data is stale — i.e., the breakout is also an opportunity to refresh steel's BAU energy accounting against primary inventories.
- **D14 — Lever dispositions:** full ownership to start. WHR and process-efficiency measures get *ported into* the steel module (they map well onto steel). Levers that don't map (e.g. boiler-type energy-intensity standards) stay off steel's process end uses; each remaining lever (thermal batteries, clean-heat ITC/PTC, IFSR, electrification) gets an explicit ask-Dan disposition during 1b rather than a blanket rule.
- **D15 — GEM GIST bulk data in hand** (June 2026 V1, staged untracked at `gem-gist-june-2026/`): Plant-level, Iron unit (incl. "Blast furnace relinings" sheet), Steel unit, and Met-coal/iron-ore production-consumption workbooks. SPRS, SYSPbP, and SYSCU workbooks build from US extracts of these with GEM citations (CC BY 4.0); the met-coal file feeds the Phase 2 coke chain.
- **Checkpoint commit approved** for the working branch (Phase 1a validated state).

## Phase plan

- **1a (this draft): parallel physical core, compute-only.** Subscript, inputs, demand chain, capacity stock, logit allocation with scrap cap, production, energy-by-fuel diagnostic. Model bit-identical at defaults.
- **1b: carve-out wiring.** Steel module energy replaces the generic structure's `[*, iron and steel 241, process end use]` cells; generic levers (WHR, thermal batteries, clean heat, electrification, IFSR) explicitly excluded or re-plumbed for those cells; IES shareweights recalibrated. Calibration gate.
- **2: emissions & CCS.** Coke chain → endogenous process CO2 (retire steel's share of exogenous BPE), energy CO2 by pathway, CCS via existing new+retrofit framework, carbon-tax wiring (incl. border adjustment / process-exemption toggles), Clean Steel Standard lever.
- **3: cash flows.** Capex through financing ladders + instrument accounting; fuel/coke/scrap expenditures by entity; early-retirement stranding; GRA types + FoPITY elements; IO handoff. Gate: entity-ledger balance audit (TB `TB_checks.lst` method → `Steel_checks.lst`).
- **4: input data finalization.** House-standard workbooks for every input; AISI/USGS/AEO/GHGRP calibration.
- **5: surface area.** Dedicated "Industry - Steel" sketch view, WebAppData, docs.

## Phase 1a specification

### New subscripts

```
Steel Production Pathway: traditional BF BOF, BF BOF with CCS, natural gas DRI,
    hydrogen DRI, molten oxide electrolysis, aqueous electrolysis, scrap EAF
ore based steel pathway: (all except scrap EAF)          — subrange, for scrap-cap logic
industrial process end use: heat below 100 C … other processes   (8) — subrange (used from 1b)
industrial nonprocess end use: facility HVAC, facility lighting, other nonprocess (3) — subrange
```

DRI pathways bundle their EAF melting step (industry convention); "scrap EAF" is the secondary route. MOE and aqueous electrolysis ship with zero shareweight until commercially unlocked (maturity gating rides the shareweight time series, like TBS).

### New inputs (InputData/indst/, placeholder CSVs in 1a, workbooks in Phase 4)

| Acronym | Variable | Dims | Units | Form |
|---|---|---|---|---|
| BSD | BAU Steel Demand (total; pathway attribution is endogenous) | — | metric tons/yr | GET DIRECT DATA, time series |
| SYSPbP | Start Year Steel Production by Pathway (stock init + logit calibration anchor) | Pathway | metric tons/yr | GET DIRECT CONSTANTS |
| SPRS | Steel Preexisting Capacity Retirement Schedule (build from GEM Global Iron and Steel Tracker plant-level retirements/relines) | Pathway | metric tons/yr | GET DIRECT DATA, time series |
| SEIbPaF | Steel Energy Intensity by Pathway and Fuel | Pathway × Industrial Fuel | BTU/ton | GET DIRECT CONSTANTS |
| SPCC | Steel Pathway Capital Cost per Unit Annual Capacity | Pathway | $/(ton/yr) | GET DIRECT CONSTANTS |
| SPPL | Steel Pathway Plant Lifetime (model-run additions only) | Pathway | years | GET DIRECT CONSTANTS |
| SPSW | Steel Pathway Shareweight | Pathway | Dmnl | GET DIRECT DATA, time series |
| MASSfS | Maximum Annual Scrap Supply for Steel | — | metric tons/yr | GET DIRECT DATA, time series |

*(Revised 2026-08-20 per Dan: original design had a per-pathway BAU production time series (BSPbP); replaced so only total demand is exogenous — the pathway split is chosen by the cost logit, calibrated to start-year data — and so the preexisting fleet retires on an exogenous GEM-informed schedule instead of a lifetime proxy.)*

All 1a values are placeholders pending the two research syntheses (US production/capacity/scrap; pathway techno-economics) — every CSV is marked DRAFT and must be verified against primary sources before release.

### Equation chain (policy case; BAU twins minimal in 1a)

1. `BAU Total Steel Demand` = BSD — tons.
2. `Total Steel Demand` = BAU Total Steel Demand × (1 + Percent Change in Production due to Policies[iron and steel 241]).
3. Two capacity stocks per pathway: `Preexisting Steel Production Capacity` = INTEG(−scheduled retirements, SYSPbP), drawn down by MIN(SPRS, remaining stock); `Steel Production Capacity Added During Model Run` = INTEG(new builds − stock/SPPL, 0). Total capacity = their sum. (Start-year utilization assumed 1; refine in Phase 4 with AISI capability data.)
4. Early-retirement + cost-based stranding levers arrive in Phase 2/3 on the preexisting stock.
5. `Unmet Steel Production Capacity Need` = MAX(0, demand − SUM(capacity)). Capacity is a stock, so dip-and-recover demand reuses idle capacity (no phantom builds — TB high-water-mark lesson).
6. `Steel Pathway Levelized Cost per Ton` = SPCC/SPPL + Σ_fuel(SEIbPaF × Industrial Fuel Cost per Unit Energy[iron and steel 241, fuel]). Straight-line capex in 1a; upgrade to the financing-annuity basis (BCoISC) in Phase 3. Carbon-tax cost enters in Phase 2.
7. `Steel Pathway Choice Weight` = 10000 × SPSW × (cost / min eligible cost)^IELC — exact clone of the equipment fuel-choice power form, incl. 1e-2 $/ton floors (scaled for per-ton costs), reusing `IELC` (−6) in 1a; a dedicated exponent input if the team wants one later.
8. `Share of New Steel Production Capacity by Pathway` = weight / Σ weights.
9. Scrap cap: preliminary allocation = share × unmet need; scrap-EAF allocation capped by `Scrap EAF New Capacity Headroom` = MAX(0, production supportable by MASSfS − existing scrap-EAF capacity); capped excess reallocated across ore-based pathways in proportion to their weights.
10. `New Steel Production Capacity by Pathway` = capped allocation.
11. `Steel Production by Pathway` = capacity × MIN(1, demand / Σ capacity) — uniform utilization ration (merit-order utilization is a logged upgrade).
12. `Steel Module Energy Use by Fuel Type` = Σ_pathway(production × SEIbPaF) — the 1b handoff quantity and the calibration diagnostic vs. `Industrial Fuel Use[fuel, iron and steel 241]`.

### Explicitly deferred (logged in the replication log)

Coke/met-coal intermediate tracking, process CO2, CCS, Clean Steel Standard, early retirement, net imports of steel tonnage (D7 makes IESE handle trade in dollars; revisit whether tonnage trade needs its own representation), BAU twin chain, financing-annuity cost basis, merit-order utilization, Model-Run-Vintage capacity tracking, acronym-key entries, sketch placement.
