# Industry efficiency & waste-heat measures — complete change summary

**Branch:** `develop_tempbands+whr` · **Purpose of this document:** handoff for merging into `develop` (4.1).
**Written 2026-07-31.** Covers the delivered end-state only (abandoned approaches omitted, except where a merge conflict might resurrect a deleted name).

---

## 1. What this project did, in one paragraph

The old waste-heat-recovery representation — a single recoverable-heat potential per industry (`WHRPbI`), one average capital cost (`WHRCC`), and a lever that simply dialed in a fraction of that potential — was replaced with a **measure-level structure with endogenous, cost-based deployment**. 25 industries × (7 waste-heat measures + 17 process-efficiency measures) × 5 cost levels each carry their own savings potential, capital cost, O&M cost, and lifetime, sourced from Kermeli et al. (2022) and the LBNL/ENERGY STAR guide family. Measures deploy when policy shortens their simple payback enough to clear a **payback-acceptance curve** (a distribution of firms' investment thresholds, anchored on DOE Industrial Assessment Center audit data), or when a **standards lever** mandates them. Deployment accumulates in stocks, retires at end of measure lifetime, and reduces industrial fuel and electricity use downstream of unit-equipment efficiency. Capital, O&M, and subsidy flows feed the industry cash-flow accounts. The separate `Percentage Improvement in Industrial Process Efficiency above BAU` lever was retired and replaced by the new efficiency-measure standards lever.

---

## 2. Commits on this branch (since merge-base `2c873fcf`, 2026-07-16)

| Commit | Contents |
|---|---|
| `b96f719b` | Draft code + input files for **two** projects: (1) industrial heat temperature bands, (2) WHR/process-efficiency endogenization |
| `32a660c5` | Sketch objects for the above; level/rate (INTEG) structures where appropriate |
| `1d5edfb1` | Fixes to the prior commit |
| `f4ad5b87` | Retiring measure capacity replaced in full rather than at the annual start rate |
| `2c43ee22` | PSUS/MHRP replaced by the payback-acceptance curve |
| `a897ffa2` | PEaWHRP input files conformed to InputData folder conventions |

⚠️ **This branch carries two projects.** The `Industrial Process` subscript restructure (4 boiler/nonboiler heating elements → 5 temperature bands, 10 → 11 elements) is *also* only on this branch. The merge brings both. See §7.

---

## 3. Model structure (EPS.mdl)

### 3.1 New subscript families

| Family | Elements | Source |
|---|---|---|
| `Waste Heat Measure` | 7 | `GET DIRECT SUBSCRIPT` from `PEaWHRP-WM.csv` |
| `Process Efficiency Measure` | 17 | from `PEaWHRP-PM.csv` |
| `PEaWHRP WM Row` | 175 (25 industries × 7) | from `PEaWHRP-WMD.csv` col K |
| `PEaWHRP PM Row` | 425 (25 × 17) | from `PEaWHRP-PMD.csv` col K |
| `Measure Cost Level` | 5 (`cost level 1..5`) | inline |
| `Measure Set` | 2 (`waste heat measures`, `process efficiency measures`) | inline |
| `Govt Cash Flow Type` | **+1 element**: `indst efficiency subsidy` | inline (existing family extended) |

The two `… Row` families exist because the input CSVs are **long-format** (one row per industry × measure), read with `GET DIRECT CONSTANTS` down a column, then remapped to 2-D via `INITIAL(VECTOR ELM MAP(…, (Industry Category-1)*ELMCOUNT(Measure) + (Measure-1)))`. This mirrors the `Policy Element` / FoPITY pattern. **Row order in those CSVs is load-bearing**: industry-major, measure-minor, in `Industry Category` declaration order.

### 3.2 Input variables (data reads + remaps)

Long-form reads (10): `WHM/PEM {Fuel Savings Potential, Elec Savings Potential, Capital Cost, OM Cost, Equipment Lifetime} by Row`.
`INITIAL()` remaps (10): `WHMFSP`, `WHMESP`, `WHMCC`, `WHMOC`, `WHMEL`, `PEMFSP`, `PEMESP`, `PEMCC`, `PEMOC`, `PEMEL` — all `[Industry Category, <Measure>]`.
Shared parameters (4): `PAC Payback Acceptance Curve[Measure Set]` (lookup), `MCLM Measure Cost Level Multiplier`, `MCLS Measure Cost Level Share`, `SoCEMDSiaY Share of Cost Effective Measure Deployment Started in a Year`. Plus unit constant `BTU per MMBtu`.

### 3.3 Energy bases and prices

Policy-case: `Industrial Heating Process Fuel Use before Measures`, `Industrial Total Fuel Use before Measures` (both `[Industry Category, Industrial Fuel]`), and four scalars-per-industry derived from them — `Industrial {Heat ,}{Combustion Fuel, Electricity} Base for Measures`. Two price blends: `Blended Industrial {Heat ,}Fuel Cost per Unit Energy` (nonelectric fuels, use-weighted; **carbon-tax-inclusive** via `Industrial Fuel Cost per Unit Energy`).
BAU twins of all of the above exist solely to give the counterfactual screen a pure BAU benchmark (BAU quantities *and* BAU prices): `BAU Industrial …`, `BAU Blended Industrial …`.

### 3.4 Economics and the adoption decision

```
Value of {WHM,PEM} Energy Savings[i,m]            = savings-weighted avg of avoided fuel & elec expenditure
                                                   + deployment subsidy      { $/BTU }
{WHM,PEM} Value at BAU Prices[i,m]               = same at BAU prices, no subsidy

{WHM,PEM} Simple Payback Period[i,m,cl]          = MCLM[cl]*capex / (Value - MCLM[cl]*opex), capped at 10 yr
{WHM,PEM} Simple Payback Period at BAU Prices    = same using the BAU value

{WHM,PEM} Tranche Economically Deployable[i,m,cl] =            <-- the deployment ceiling
    MAX(0, (PAC(payback) - PAC(payback_BAU) - 1e-6) / MAX(1e-6, PAC(0) - PAC(payback_BAU)))
```

Policy that shortens the payback wins over the firms whose thresholds lie between the BAU and policy paybacks. The denominator scales that gain against the most any policy could win — `PAC(0) - PAC(payback_BAU)` — so driving the payback to zero unlocks the **full loaded potential**. **At zero policy the two paybacks are identical and the ceiling is exactly 0** — the `1e-6` deadband is required because the two values compute through different paths and differ in their final bits.

> **Changed 2026-08-04.** The denominator was previously `1 - PAC(payback_BAU)`, which implicitly treated the firms accepting the BAU payback as having already adopted, capping the reachable share at ~80% (waste heat) / ~73% (process efficiency) of loaded potential even at an infinite carbon price. That assumption was wrong for the US, where no current policy drives baseline deployment of these measures, and it risked double-counting against Kermeli's own diffusion netting. Baseline deployment is now represented explicitly and per-geography by the BAU deployed share input (§3.5a) instead of being assumed inside the curve.

`Levelized Cost of {WHM,PEM} Energy Savings` and `{WHM,PEM} Measure Capital Recovery Factor` (at `BCoISC Weighted Average Cost of Capital by Industry`) **were deleted on 2026-08-04.** They stopped gating deployment when the PAC curve landed and were kept as `:SUPPLEMENTARY` reporting, but nothing read them — each appeared only in its own definition, and the two capital recovery factors existed solely to feed the two levelized costs. Their descriptions still claimed "affects the deployment decision only", which was the opposite of the truth and a trap for this merge. Removal verified **bit-identical** across 6,725 series at $300/t. Also removed from the local diagnostic savelists and from the four views that drew them (4 objects, 14 arrows).

> **If develop has diverged here:** these four names should not reappear. If the 4.1 side still references them, the reference is stale — the deployment decision now runs entirely through `{WHM,PEM} Simple Payback Period` and the PAC curve. Note the financing-side `Capital Recovery Factor for Financed Measure Equipment` (§3.9) is a **different, live** variable — don't confuse the two.

### 3.5 Deployment, stocks, retirement

```
New {WHM,PEM} Deployment This Year[i,m,cl] =
  MIN( target - post-retirement level,
       retirements + MAX( SoCEMDSiaY * gap-to-ceiling , gap-to-standard ) )
  where target = MIN( potential remaining after BAU deployment,
                      MAX(economic ceiling, standards floor) )
```
Retiring capacity is replaced **in full** (maintenance, not a fresh adoption decision); only genuinely new deployment is rate-limited at `SoCEMDSiaY` (0.2/yr); a binding standard deploys immediately; the outer `MIN` lets a tranche that stops being cost-effective decay by retirement instead of being replaced. Both the economic and standards channels are additionally capped at the potential remaining after BAU-case deployment (§3.5a) — a no-op in the US.

Stocks: `Last Year Deployed Fraction of {WHM,PEM} Potential` = `INTEG(new − retired, 0)`; visible `Deployed Fraction of {WHM,PEM} Potential` = `MIN(1, MAX(0, …))` (clamps are defensive only — documented as such). Retirement: `{WHM,PEM} Deployment Retired This Year` = `DELAY FIXED(new deployment, lifetime, 0)`.

### 3.5a BAU deployment share (added 2026-08-04, inert in the US)

Some geographies' baselines already drive these measures — the EU's Energy Efficiency Directive being the motivating case. Representing that in the potentials themselves would hide it from the model and make near-term acceleration impossible to show, so it is an explicit per-measure input:

- **New CSV column L** on `PEaWHRP-WMD.csv` and `PEaWHRP-PMD.csv`: `BAU deployed share of potential by end year`. **Zero on every US row.**
- Long-form reads `{WHM,PEM} BAU Deployed Share by End Year by Row` → remaps `{WHMBDS,PEMBDS} … BAU Deployed Share by End Year[Industry Category,{Waste Heat,Process Efficiency} Measure]`.
- `{Waste Heat,Process Efficiency} Measure Potential Remaining After BAU Deployment[i,m]` = `1 - BDS * (Time - INITIAL TIME)/(FINAL TIME - INITIAL TIME)` — a linear ramp from zero in the start year to the input value in the final year, expressed in Vensim's own time bounds so it adapts to each geography's run period (US 2025–2050, China 2022–2070, etc.) with no per-region code.
- Caps both deployment channels, as shown in §3.5.

**Scope caution for whoever populates a non-US region:** this column must carry only the **non-price** share of baseline policy. Price-based baseline policy (the EU ETS) is already inside `BAU Industrial Fuel Cost per Unit Energy`, hence already inside each measure's BAU payback and already restricting the ceiling — putting it here too counts it twice. Values are also **not** obtainable from Kermeli et al. (2022): its implementation rates describe an ambitious efficiency scenario, and its reference case does not model measures individually. Use the region's own baseline projection (EU Reference Scenario / PRIMES) or a documented judgment.

### 3.6 Savings application (the hook into industry energy use)

Roll-ups: `Fraction of Industrial Heat {Fuel, Electricity} Use Avoided by Waste Heat Measures`, `Fraction of Industrial {Combustion Fuel, Electricity} Use Avoided by Efficiency Measures` — each `SUM(potential × MCLS × deployed fraction)`, capped at 1. Waste-heat roll-ups are additionally scaled by `Waste Heat Availability Index` (see §3.8). Then two multipliers, `WHR Measure Energy Use Multiplier` and `Efficiency Measure Energy Use Multiplier`, are applied at **three** points:

1. `Industrial Equipment Energy Use by Fuel Type and Process before Process Improvements` — WHR multiplier on the `industrial heating process` subrange
2. `Industrial Equipment Energy Use by Fuel Type and Process` — efficiency multiplier, all processes
3. `New Industrial Equipment Fuel Use for Energy before CCS and Methane Capture` — same treatment on the new-equipment chain
4. `Industrial Clean Heat Production Subsidy Amount Paid` — **both** multipliers, so clean-heat subsidy is not paid on energy the measures eliminated

Ordering is deliberate: this slot is downstream of unit-equipment efficiency (`SYIEUEFbIPaF`/`BIEEI`/`IEMUEF` and equipment standards, which act on energy intensities) and downstream of electrification/fuel-switching (inside the vintage fuel shares), so measure savings are multiplicative and cannot double-count them.

### 3.7 Policy levers (4 new, 2 retired)

New, all `[Industry Category]`, all FoPITY-scheduled:
- `Waste Heat Measure Deployment Subsidy` — `$/MMBtu [0,20,0.25]`
- `Process Efficiency Measure Deployment Subsidy` — `$/MMBtu [0,20,0.25]`
- `Min Fraction of Waste Heat Measure Potential Deployed` — `Dmnl [0,1,0.01]`
- `Min Fraction of Process Efficiency Measure Potential Deployed` — `Dmnl [0,1,0.01]`

Each has a `… This Year` twin applying `VECTOR ELM MAP(Selected Policy Implementation Schedule[…], (Industry Category-1))`. Subsidies divide by `BTU per MMBtu` to reach `$/BTU`.

Retired: `Perc of Waste Heat Recovery Potential Achieved` (+`This Year`, +`Last Year …`), `Percentage Improvement in Industrial Process Efficiency above BAU` (+`This Year`). The standards levers are the intended replacements. Standards deploy **pro rata** across measures and cost levels (cheapest-first was considered and rejected as not worth the complexity).

### 3.8 Waste-heat availability index

`Waste Heat Availability Index[Industry Category]` = `MIN(1, heating-fuel intensity / start-year heating-fuel intensity)`, guarded to return 1 when start-year intensity is 0. Intensity = `Last Year Industrial Heat Combustion Fuel Base for Measures / Last Year Output by ISIC Code`. Purpose: as unit efficiency improves or heat electrifies, less waste heat is recoverable per unit of remaining fuel, so waste-heat *potential* shrinks — not just the absolute savings. Applied to the WHR roll-ups, energy savings, O&M, and capex (consistently, once each). Not applied to process-efficiency measures.

### 3.9 Cash flows

Per set: `New {WHM,PEM} Measure Capital Expenditures` (new deployment × savings capacity × **unadjusted** capex — `MCLM` is decision-only), `{WHM,PEM} Measure OM Expenditures` (on the deployed level), `{WHM,PEM} Measure Energy Savings This Year` (BTU basis for O&M and subsidy), `{WHM,PEM} Measure Subsidy Amount Paid`. Combined into `New Measure Capital Expenditures`, `Measure OM Expenditures`, `Measure Deployment Subsidy Amount Paid`. Financing mirrors industrial CCS: `SoICETAF` split → `Capital Recovery Factor for Financed Measure Equipment` (on `BCoISC Financing Interest Rate by Industry`, `RPfFISCC[other processes]`) → `Annual Financing Repayment …` → `Annual … Repayments Expiring After Repayment Period` (`DELAY FIXED`) → `Last Year Financing Repayments …` (`INTEG`) → `Financing Repayments for Measure Equipment`.

Consumers modified (all pre-existing variables): `Change in Miscellaneous Expenditures by Industry`, `Change in Upfront Capital Expenditures by Industry for {Financed, Non Financed} Equipment`, `Industry Sector Change in Capital and OM Spending`, `Industry Subtotal Change in {Capital, OM} Expenditures`, `Industry Sector Change in {Government Subsidy Amount Paid, Government Subsidy Payments by ISIC Code, Nonenergy Industry Revenue by ISIC Code, Revenue by Entity}`, `Change in Government Cash Flow by Cash Flow Type` (new `indst efficiency subsidy` element), `GRA Weights by Government Cash Flow Type by Mechanism`. New: `GRA for Industry Efficiency Measure Subsidies` (+`This Year`).

### 3.10 Sketch

All objects live on **Industry - Main** (deployment/economics) and **Industry - Cash Flow** (capex/O&M/financing), plus the four levers on **Policy Control Center** and the GRA variables on the government view. The old "Calculating Change in Waste Heat Recovery Capital Expenditures" block was removed. Layout was partly hand-corrected by Dan after an automated pass placed some variables atop existing objects.

---

## 4. Input files

### 4.1 Final folder layout (conforms to InputData conventions: one workbook per folder, export tabs named exactly like the CSVs)

| Folder | Workbook | CSVs |
|---|---|---|
| `InputData/indst/PEaWHRP/` | *Process Efficiency and Waste Heat Recovery Parameters.xlsx* (26 tabs; `Kermeli Data` → `economics` → `dist engine` → export tabs) | `PEaWHRP-PMD.csv`, `PEaWHRP-WMD.csv`, `PEaWHRP-PM.csv`, `PEaWHRP-WM.csv` |
| `InputData/indst/PAC/` | *Payback Acceptance Curve.xlsx* | `PAC.csv` |
| `InputData/indst/MCL/` | *Measure Cost Level Parameters.xlsx* | `MCLM.csv`, `MCLS.csv` |
| `InputData/indst/SoCEMDSiaY/` | *Share of Cost Effective Measure Deployment Started in a Year.xlsx* | `SoCEMDSiaY.csv` |
| `InputData/ctrl-settings/GRA/` | (existing workbook) | **+`GRA-indsteffmeasures.csv`** |

Deleted folders: `InputData/indst/WHRPbI/`, `InputData/indst/WHRCC/`.

### 4.2 The measure data

`PEaWHRP-PMD.csv` / `-WMD.csv` are long-format: `Industry, Code, Slot, Measure, Fuel savings, Elec savings, Capex intensity, Opex intensity, Lifetime, Source, Key`. Savings are **fractions** (0–1) of the relevant base — WHR of heating-process energy, efficiency measures of total energy. Capex/opex are 2012$ per BTU/yr (÷1e6 from the source workbook's $/MMBtu-yr, done in tab formulas). Empty slots carry zero potential and are inert. Text columns have commas replaced by semicolons (Vensim splits CSVs naively; Excel quoting does not protect it).

Provenance: Kermeli et al. (2022), *Energy Efficiency* 15(48), supplementary tables (EU industry). Potentials are net of 2015 diffusion and capped at the paper's 2050 implementation rates. Per-measure footnotes trace to LBNL/ENERGY STAR guides (cement: Worrell/Kermeli/Galitsky 2013; iron & steel: LBNL-4779E; pulp & paper: LBNL-2268E; petrochemical: LBNL-961E), Rutten et al. 2017, Fleiter et al. 2012, Boulamanti & Moya 2017, and a DOE aluminum bandwidth study. **Ten measure rows were excluded** as equipment-replacement (belonging to the vintaged stock/standards/early-retirement channel instead), marked in the workbook's `Kermeli Data` bucket column as `X equip-replace` with a dated rationale note per row: VRM replacement, shoepress ×3, new decoating equipment, endless hot rolling, efficient refiners ×3, vertical shaft kiln.

### 4.3 The payback-acceptance curve (`PAC.csv`)

Two identical rows (one per `Measure Set`) over a payback grid 0–10 years: `0.85, 0.75, 0.65, 0.57, 0.50, 0.44, 0.38, 0.27, 0.19, 0.13, 0.06, 0.035, 0.02, 0.008, 0.003`. Anchored on Anderson & Newell (2004) — implicit threshold 1.25–1.5-year payback, ~half of audit recommendations rejected — and Muthulingam et al. (2013), 89,299 IAC recommendations with mean payback 1.06 yr and mean adoption 50.16%. Same construct as EIA NEMS IDM's `AcceptFrac`, Fraunhofer FORECAST's payback-time-expectation distribution, and PRIMES's threshold-value frequency distribution. NEMS's own values (100% acceptance at 1-year payback) are kept as an optimistic sensitivity bound, not adopted.

### 4.4 FoPITY

Added 100 rows (4 levers × 25 industries) plus 1 GRA row; removed 325 (25 WHR + 300 process-efficiency). Edited **directly in all 19 CSVs**, not via the generator scripts — the generators predate the temperature-band restructure and would regress it. Element order is load-bearing (`VECTOR ELM MAP` anchors on the first row of each block).

---

## 5. Validation state

All headless (`vendss64` + `LOADMODEL`), error log clean. Runs saved as `Pac*.vdfx`/`.tab`.

| Test | Result |
|---|---|
| Zero-policy invariant | **Exactly zero** deployment, energy-use multipliers identically 1, zero cash flows |
| Carbon-tax sweep $50/$100/$300 | Monotone, no cliffs; summed deployed fractions 38 / 65 / 132; visibly responsive at $50 |
| Ceiling respected | No tranche exceeds its ceiling-to-date, any run |
| Deployment declines | Every decline coincides with a genuinely fallen ceiling (0 unexplained, down from 86 before the retirement-backfill fix) |
| 100% standard (iron & steel) | All 95 tranches held at exactly 1.0 through retirement cycles |
| `GET DIRECT` shape audit | 0 mismatches / 0 missing / 0 parse failures across all 1,343 calls (`CheckGetDirectShapes.py`) |
| Sketch lint | Clean (`sketch_lint.py`) |
| Python unit harness | Payback/ceiling formulas verified across regime flips, zero-capex, negative-opex, subsidy-only unlock, endpoint clamps |

**Not yet done:** formal Vensim units check; web-app (`WebAppData.xlsx`) and documentation-repo updates (Phase F).

---

## 6. Known open items (none blocking a merge)

1. **`MCLM` and negative O&M** — the cost-level multiplier scales signed cost, so for the few measures with negative O&M it amplifies the benefit at high cost levels. Decision-only; flagged in the MCL workbook.
2. **Export formatting** — the `PEaWHRP-PMD`/`-WMD` tabs currently carry percent and 2-decimal *display* formats; the CSV Export Tool writes displayed values, so exporting from them yields `0.0000%` and `0.00`. Set columns E–H to General/high-precision before using the tool. The committed CSVs are correct and bit-exact against the workbook's values.
3. **Optional curve hedge** — lifting `PAC` tail values S(4)/S(6) from 0.06/0.02 to ~0.10/0.04 would acknowledge firms with no formal payback criterion (Rohdin et al. 2007).
4. **Retirement lumpiness** — `DELAY FIXED` retires each cohort in a single year, so replacement *capex* spikes every lifetime cycle even though the deployment stock is now smooth. A distributed retirement delay would fix it.
5. **Unrelated but live:** industrial electricity price reached ~$358/MMBtu (~$1.22/kWh) in 2029 in a $300/t carbon-tax run, then collapsed 96%. Carries the fingerprint of the previously documented capacity-market overshoot; it is upstream of this structure but distorts every electricity-touching result in such scenarios.

---

## 7. MERGE GUIDANCE — read before merging into `develop`

`develop` has moved 12 commits since the merge-base (`2c873fcf`, 2026-07-16), including substantial industry/IO work. Verified collision surface:

### 7.1 Subscript families — the main hazard

| Family | On `develop` | On this branch | Merge implication |
|---|---|---|---|
| `Industry Category` | unchanged | unchanged | ✅ **Safe.** All 25-row CSVs and inline lever matrices still align. This is the single most important compatibility fact. |
| `ISIC Code` | **64 elements** (Robbie expanded/disaggregated: `ISIC 01`, `02`, `03`… ) | 52 elements (`ISIC 01T03`…) | ⚠️ Take **develop's** version. Our structure never indexes `ISIC Code` directly. |
| `Industry Category ISIC Code` | 30 elements, new names | 31 elements, old names | ⚠️ Take **develop's**. But `Waste Heat Availability Index` reads `Last Year Output by ISIC Code[Industry Category ISIC Code]` — re-verify that mapping still resolves and that output values are sane after the merge. |
| `Industrial Process` | 10 (boilers/nonboiler) | **11 (temperature bands)** | ⚠️ Take **ours** — this is the temp-band project, which the merge is also delivering. Every heating-dimensioned input CSV must come from this branch, and Robbie's industry-side edits to those files must be re-applied on top of the 11-element shape. |
| `Govt Cash Flow Type` | 14 | 15 (`+indst efficiency subsidy`) | ✅ Simple addition; keep ours, watch the `remainder` element stays last if anything enumerates positionally. |
| `Measure Set`, `Measure Cost Level`, `Waste Heat Measure`, `Process Efficiency Measure`, `PEaWHRP {WM,PM} Row` | absent | new | ✅ Pure additions. |

### 7.2 FoPITY — real conflict, resolve by policy block not by line

`develop` has **3,782** policy elements, this branch **3,701**. Both sides changed the industry region:
- Only on `develop`: `indst material efficiency` (Robbie's new lever), plus `indst waste heat recovery` and `indst process efficiency` (which we deliberately deleted), and the boiler/nonboiler-dimensioned variants of `indst elec efficiency stds`, `indst fuel efficiency stds`, `indst shift to electricity`, `indst shift to alt fuel`, `indst eqpt cost of capital`, `indst clean heat PTC/ITC`, `RnD industry capital cost reduction`.
- Only here: the four new measure levers, the `GRA indst efficiency subsidy` row, and the temperature-band variants of all the process-dimensioned policies.

**Resolution:** rebuild the industry region rather than text-merging. Keep our temperature-band variants, keep our four measure levers + GRA row, **add Robbie's `indst material efficiency` block in the band-dimensioned shape if it is process-dimensioned**, and do not resurrect `indst waste heat recovery` / `indst process efficiency`. Then confirm every `VECTOR ELM MAP` anchor still points at the first row of its block (a smoke test that sets each lever nonzero and checks for a nonzero delta is the reliable check).

### 7.3 Equations that both sides touched

All of our hook points still exist by name on `develop`, but Robbie's IO/industry commits (`126ceb8d` TIOT/material efficiency, `6ea21922` ISIC expansion, `a1c83d4b`, `f4e2404d`, `650a7f6f` induced-respending fixes) rewrote parts of the industry cash-flow and value-added chain. Re-inspect after merging:
`Change in Miscellaneous Expenditures by Industry`, `Change in Upfront Capital Expenditures by Industry for {Financed, Non Financed} Equipment`, `Industry Sector Change in Capital and OM Spending`, `Industry Subtotal Change in {Capital, OM} Expenditures`, `Industry Sector Change in {Nonenergy Industry Revenue, Government Subsidy Payments} by ISIC Code`, `Industry Sector Change in Revenue by Entity`, `Change in Government Cash Flow by Cash Flow Type`, `GRA Weights by Government Cash Flow Type by Mechanism`, `Industrial Clean Heat Production Subsidy Amount Paid`, and the three energy-use application points in §3.6. Our additions to each are single additive terms — easy to re-apply by hand if the surrounding equation was rewritten.

### 7.4 Input files

`IEMUEF.csv` (and the other heating-dimensioned files) differ in shape between branches — 13 rows on `develop` vs 26 here, i.e. the temp-band restructure. Take this branch's shapes and re-apply any of Robbie's *value* changes. `CheckGetDirectShapes.py` at the repo root will list every read whose CSV shape no longer matches its declaration; run it first after the merge, before attempting a simulation. `InputData/CSV Export Tool.xlsm` must never be re-saved by a script (openpyxl damages macros) — take whichever side's copy is newer without rewriting it.

### 7.5 Suggested merge order

1. Merge, taking `develop` for ISIC/IO structures and this branch for `Industrial Process` and everything measure-related.
2. Run `CheckGetDirectShapes.py` → fix shape mismatches (expect heating-dimensioned files to need Robbie's values re-applied at 11-element shape).
3. `LOADMODEL` headless until clean.
4. Rebuild the FoPITY industry region per §7.2; re-run the lever smoke test.
5. Re-run the validation battery in §5 — especially the **zero-policy exact-zero invariant**, which is the fastest detector of a broken merge in this structure.
6. Re-check `Waste Heat Availability Index` values (the ISIC mapping change).

---

## 8. Supporting documents — NOT in the repo

**This file is not in the repo either.** All of these are working notes living in Dan's local working copy at the repo root. They were briefly committed and removed on 2026-08-04, since this repo does not keep working docs at root — and a merge handoff in particular should not be merged into `develop` as a permanent artifact. Untracked files survive branch checkouts, so this document is present in the working directory regardless of which branch the merge runs on; if the merge happens on another machine, copy it across by hand.

**Read them for history only.** Several describe mechanisms that were subsequently deleted: the shock-ramp plan and the payback-acceptance proposal both document `PSUS`, and the restructure plan documents `MHRP` and `WHRPbI`. None of those exist in the model any more. **This document is the authority on current state**; where a companion doc disagrees, it is out of date.

| File | Contents | Stale? |
|---|---|---|
| `WHR_EfficiencyMeasures_Restructure_Plan.md` | Original design plan: the CCS pattern mirrored, variable naming, calculation order, decisions log | yes — MHRP, WHRPbI |
| `PEaWHRP_PaybackAcceptance_Plan.md` | Payback-acceptance mechanism: design, literature anchors, peer-model precedent (FORECAST/NEMS/PRIMES), test plan | partly — pre-dates the denominator change (§3.4) |
| `PEaWHRP_PaybackAcceptance_Proposal.md` | Why PSUS was replaced (the argument, before implementation) | yes — PSUS |
| `PEaWHRP_ShockRamp_Implementation_Plan.md` | The PSUS shock-ramp design | yes — describes a deleted mechanism |
| `PEaWHRP_MeasureType_SourceCheck.md` | Per-measure source verification and the equipment-replacement exclusion decisions | no |
| `PEaWHRP_Sketch_Update_Checklist.md` | Sketch objects added/removed/modified, by view | partly — PSUS/MHRP entries |
| `IndustrialProcess_NewElement_Plan.md` | The temperature-band project's plan (the other half of this branch) | no |
