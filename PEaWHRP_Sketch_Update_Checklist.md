# Sketch update checklist — PEaWHRP measure structure (2026-07-28)

> **Update 2026-07-31 (payback-acceptance change):** `MHRP Measure Hurdle Rate Premium` and `PSUS Price Signal Unlock Sensitivity` no longer exist — their Industry-Main sketch objects were removed / renamed in-file. Newly drawn on Industry-Main (by direct sketch edit, pending your visual review): `PAC Payback Acceptance Curve` (pink input, at the old PSUS spot, feeding both Tranche Economically Deployable objects) and the four `… Simple Payback Period [at BAU Prices]` variables (white, in the value columns), with rerouted arrows Value→Payback→Ceiling and cost-input→Payback. The stale LCOS→Ceiling and Value→Ceiling arrows were removed (LCOS is now reporting-only). Everything below this line predates that change; read `MHRP`/`PSUS` mentions accordingly.

Derived by diffing `EPS.mdl` against `EPS.mdl.pre-peawhrp.bak` (98 added, 16 removed, 16 modified equations; 7 new subscript ranges). Suggested view placements follow existing conventions; rearrange freely.

## 0. New subscript ranges (no sketch objects needed)

`Waste Heat Measure` (7, data-driven) · `Process Efficiency Measure` (18, data-driven) · `PEaWHRP WM Row` (175) · `PEaWHRP PM Row` (450) · `Measure Cost Level` (5) · `Measure Set` (2) · `policy price signal` (PSUS ramp)

## 1. Policy Control Center — new levers (blue) and deletions

**Add (4 levers):**
- `Waste Heat Measure Deployment Subsidy` [Industry Category, $/MMBtu]
- `Process Efficiency Measure Deployment Subsidy` [Industry Category, $/MMBtu]
- `Min Fraction of Waste Heat Measure Potential Deployed` [Industry Category, Dmnl 0–1]
- `Min Fraction of Process Efficiency Measure Potential Deployed` [Industry Category, Dmnl 0–1]

**Delete (old levers, incl. their Policy Implementation Schedule view ghosts):**
- `Perc of Waste Heat Recovery Potential Achieved` (+ `This Year`, + `Last Year … This Year`)
- `Percentage Improvement in Industrial Process Efficiency above BAU` (+ `This Year`)

## 2. Suggested NEW view: "Industry - Efficiency and Waste Heat Measures"

The deployment machinery is ~45 variables — a dedicated view will be much cleaner than cramming Industry-Main. Logical clusters, left to right:

**Input data (pink/light-green):**
- Flat reads (optional to sketch): `WHM/PEM {Fuel Savings Potential, Elec Savings Potential, Capital Cost, OM Cost, Equipment Lifetime} by Row` (10 vars)
- Remaps used everywhere: `WHMFSP/WHMESP/WHMCC/WHMOC/WHMEL` and `PEMFSP/PEMESP/PEMCC/PEMOC/PEMEL` (10)
- Shared constants: `MCLM Measure Cost Level Multiplier`, `MCLS Measure Cost Level Share`, `MHRP Measure Hurdle Rate Premium`, `SoCEMDSiaY Share of Cost Effective Measure Deployment Started in a Year`, `BTU per MMBtu`, `PSUS Price Signal Unlock Sensitivity`

**Bases & prices:**
- `Industrial Heating Process Fuel Use before Measures`, `Industrial Total Fuel Use before Measures`
- Bases ×8: `[BAU] Industrial {Combustion Fuel, Electricity, Heat Combustion Fuel, Heat Electricity} Base for Measures` (+ `Last Year Industrial Heat Combustion Fuel Base for Measures`)
- Blends ×4: `[BAU] Blended Industrial {Combustion, Heat} Fuel Cost per Unit Energy`

**Economics & screen (per set):**
- `{Waste Heat, Process Efficiency} Measure Capital Recovery Factor`
- `Levelized Cost of {WHM/PEM} Energy Savings`
- `Value of {WHM/PEM} Energy Savings` · `{WHM/PEM} Value at BAU Prices`
- `{WHM/PEM} Tranche Economically Deployable`

**Deployment stocks (per set):**
- `New {WHM/PEM} Deployment This Year` → `Deployed Fraction of {WHM/PEM} Potential` (+ `Last Year …`) ← `{WHM/PEM} Deployment Retired This Year`
- Levers' `This Year` variants: `{subsidy/standard} This Year` ×4

**Savings roll-up & application:**
- `Waste Heat Availability Index` (+ `Industrial Heat Fuel Intensity for Measures`, `Start Year Industrial Heat Fuel Intensity for Measures`)
- `Fraction of Industrial Heat {Fuel, Electricity} Use Avoided by Waste Heat Measures`
- `Fraction of Industrial {Combustion Fuel, Electricity} Use Avoided by Efficiency Measures`
- `WHR Measure Energy Use Multiplier`, `Efficiency Measure Energy Use Multiplier`
- `{WHM/PEM} Energy Savings This Year`

## 3. Industry - Main — modified application points

These equations changed (ghost the two multipliers in):
- `Industrial Equipment Energy Use by Fuel Type and Process before Process Improvements` — heating slice now × `WHR Measure Energy Use Multiplier` (name kept; "before Waste Heat Recovery" upstream variable also keeps its old name)
- `Industrial Equipment Energy Use by Fuel Type and Process` — now × `Efficiency Measure Energy Use Multiplier` (replacing the old process-improvements factor)
- `New Industrial Equipment Fuel Use for Energy before CCS and Methane Capture` — same treatment on the new-equipment chain
- `Industrial Clean Heat Production Subsidy Amount Paid` — old WHR/process-improvement factors replaced by the two multipliers

**Delete from this view:** `This Year Reduction in Industrial Energy Consumption for Heat Generation due to Waste Heat Recovery`, `This Year Change in … Due to Waste Heat Recovery`, `Last Year Reduction in Industrial Energy Use due to Waste Heat Recovery`, `This Year Industrial Energy Use Reduction Due to Process Improvements`, `WHRPbI`, `WHRCC` (all retired; equation-section survivors verified zero).

## 4. Industry - Cash Flow

**Delete the whole "Calculating Change in Waste Heat Recovery Capital Expenditures" block** (section label + ~20 objects): `New Waste Heat Recovery Equipment Capital Expenditures` (+Financed/+Not Financed), `Capital Recovery Factor for Financed Waste Heat Recovery Equipment`, `Annual Financing Repayment for Newly Purchased Waste Heat Recovery Equipment`, `Financing Repayments for Waste Heat Recovery Equipment` (+Last Year), `Reduction in Industrial Energy Use due to New Waste Heat Recovery Equipment`, and the old typo'd `Annual Industrial Equipment Financing Reqayments Expiring After Repayment Period` (replaced with correct spelling).

**Add the replacement block:**
- `New {Waste Heat, Process Efficiency} Measure Capital Expenditures` → `New Measure Capital Expenditures` → `… That Are Financed` / `… That Are Not Financed`
- `Capital Recovery Factor for Financed Measure Equipment` → `Annual Financing Repayment for Newly Purchased Measure Equipment` → `Financing Repayments for Measure Equipment` (+ `Last Year …`, + `Annual Measure Equipment Financing Repayments Expiring After Repayment Period`)
- `{WHM/PEM} OM Expenditures` → `Measure OM Expenditures`
- `{WHM/PEM} Subsidy Amount Paid` → `Measure Deployment Subsidy Amount Paid`

**Modified equations in this view (arrows change):** `Change in Miscellaneous Expenditures by Industry`, `Change in Upfront Capital Expenditures by Industry for {Financed, Non Financed} Equipment`, `Industry Sector Change in Capital and OM Spending`, `Industry Subtotal Change in {Capital, OM} Expenditures`, `Industry Sector Change in {Government Subsidy Amount Paid, Government Subsidy Payments by ISIC Code, Nonenergy Industry Revenue by ISIC Code, Revenue by Entity}`.

## 5. Government / GRA view

- Add `GRA for Industry Efficiency Measure Subsidies` (+ `This Year`)
- Modified: `Change in Government Cash Flow by Cash Flow Type` (new `indst efficiency subsidy` element), `GRA Weights by Government Cash Flow Type by Mechanism`

## 6. Cost Outputs view

- Old ghost `New Waste Heat Recovery Equipment Capital Expenditures` → replace with `New Measure Capital Expenditures` / `Financing Repayments for Measure Equipment` ghosts (the four cross-sector SUM equations were rewired).

*Tip: sketch objects for deleted variables must be removed in the same session as any GUI save — Vensim will otherwise drop them with a warning. The equation side is already consistent (LOADMODEL-clean).*
