# Waste Heat Recovery & Process Efficiency Measures — Restructure Plan (v2)

## IMPLEMENTATION STATUS (2026-07-27, end of session) — Phases A–E APPLIED, uncommitted

All model phases are implemented in the working tree and pass headless `LOADMODEL` checks (clean error log; only the two pre-existing benign graph STOPs that the unmodified model also emits). **Simulation checkpoints T1–T7 are still queued**: the tree cannot simulate until the temp-band data repopulation finishes (verified blocker; `IECCpUAEU.csv` still 10 process rows as of end of session — `BIEEI` was repopulated to 11 during the day). Run T1–T7 per §10 as soon as a default run completes.

What was applied:
- **A:** `InputData/indst/PEaWHRP/` (xlsx moved in + `ExportPEaWHRP.py` + 12 CSVs, capex/opex ÷1e6, Key column added at export, commas in text sanitized to ';'); 5 subscripts, 10 long-form reads, 10 `INITIAL(VECTOR ELM MAP(...))` remaps, MCLM/MCLS/SoCEMDSiaY/MHRP/`BTU per MMBtu`. Ingestion verified quantitatively via `PEaWHRP_ingest_test.mdl` (standalone; all sums/spot values match the xlsx — kept as a regression harness with `IngestTest.cmd`/`IngestTestVars.lst`).
- **B:** blends (+BAU twins, policy-case weights), heat vs total geometry, CRF on WACC+MHRP, LCOS (INITIAL, decision-only MCLM), counterfactual screen with empty-slot guards, deployment/retirement stocks, 4 levers + This Year schedule wiring; +100 FoPITY rows (4 blocks cloned from the WHR block, contiguous, industry-major).
- **C:** `WHR Measure Energy Use Multiplier` (heating slices, per-fuel) and `Efficiency Measure Energy Use Multiplier` (all processes) replace the old WHR/process-improvement factors at all 5 application points (both equipment chains' two stages + clean-heat subsidy, which now gets per-fuel multipliers inside the SUMs — an improvement over the old scalar); waste heat availability index (fuel-based heating intensity vs start year, capped at 1).
- **D:** pro-rata standards floor inside `New ... Deployment This Year` (built with B).
- **E:** bases ×4, per-set savings/OM/subsidy/capex, combined totals, financing machinery (SoICETAF split; CRF on `BCoISC FIR` over `RPfFISCC[other processes]`; own expiring term — the retired WHR chain's expiring variable was the typo'd `...Reqayments...`, deleted with it); 7 consumer equations rewired (Misc, Upfront ×2, Capital-and-OM +OM SUM, Subtotal Capex, ISIC 64T66, Revenue by Entity); Govt side: new `Govt Cash Flow Type` element `indst efficiency subsidy` + element equation + `[remainder]` line + GRA pair + weights equation + `GRA-indsteffmeasures.csv` + 5 `GRA indst efficiency subsidy X *` FoPITY rows; industry-side credits in both Government Subsidy Payments equations; **deleted**: 20 equation blocks (19 planned + the typo'd expiring var) and ~90 sketch lines across 5 views; 325 old FoPITY rows removed from all 19 CSVs; `InputData/indst/WHRPbI/` + `WHRCC/` folders removed; `US_ClimateAmbition.cin` 19 lever lines remapped to `Min Fraction of Waste Heat Measure Potential Deployed = 1`; `CreateCombinationsScript.py`/`CreateContributionTestScript.py` stale cogen/WHR entries replaced with the 4 new levers.

Backups at repo root: `EPS.mdl.pre-peawhrp.bak` (pre-session), `EPS.mdl.phaseA.bak`, `EPS.mdl.phaseE-pre-delete.bak`, plus `EPS_base0_model.mdl` (runnable pre-session copy for the eventual T1 diff).

### Run-blocker diagnosis (2026-07-27 evening) — NOT caused by this restructure

The tree still cannot simulate. Vensim shows only a generic "Model has errors and cannot be simulated" modal with nothing in `vensimdp.err`; the failing-variable name and error text were extracted by scripting the dialog (`scratchpad/probe_error2.ps1` pattern: click Yes, then read the equation editor's `Errors:` combobox). **The pre-change model (`EPS_base0_model.mdl`) fails identically against the same inputs, so the measure restructure is not the cause.** Two independent, pre-existing data-side blockers:

**(A) Eight CSVs still carry the OLD 10-element `Industrial Process` structure** (verified by direct inspection — their labels literally read `Boilers`, `Nonboiler low/med/high temp`). Model expects 11. These need Dan's data (code-only scope stands — no values were invented):

| File | expected | actual |
|---|---|---|
| `InputData/indst/IEMUEF/IEMUEF.csv` | 12 × 11 | 12 × 10 |
| `InputData/indst/PIFURfE/PIFURfE.csv` | 25 × 11 | 25 × 10 |
| `InputData/indst/RPfFISCC/RPfFISCC.csv` | 11 rows | 10 process rows |
| `InputData/indst/IESD/IESD-AAaWER.csv` | 11 rows | 10 |
| `InputData/indst/IESD/IESD-FoIERbA.csv` | 11 rows | 10 |
| `InputData/indst/IESD/IESD-FoPERNbA.csv` | 11 rows | 10 |
| `InputData/elec/SHELF/SHELF-indstproc-summerpeak.csv` | 11 × 24 | 10 × 24 |
| `InputData/elec/SHELF/SHELF-indstproc-winterpeak.csv` | 11 × 24 | 10 × 24 |

Found with a reusable auditor: `scratchpad/check_getdirect_shapes.py` compares every `GET DIRECT` call's expected shape (from subscript family sizes, honoring transposed `B2*` and fixed elements) against the actual CSV — it parsed all 1343 reads with zero parse failures and is worth keeping in the KB for future subscript restructures.

**(B) The 13 `BPFUbIP-*.csv` files silently read as MISSING VALUES.** The full model hard-errors on `BPFUbIP BAU Percentage Fuel Use by Industrial Process` with *"Unable to get constant values."* Isolation tests (single-variable probe models, real file vs. reshaped copies) established:
- Real file (25 industry rows × 11 process cols **plus 3 trailing rows**: one all-empty, then `EPS fuel type`, then the fuel name) → sum = **-3.5697E+35** (Vensim's missing-value sentinel), no error raised in isolation.
- Identical values with the 3 trailing rows stripped → sum = **25.0** (correct: each industry row sums to 1).
- Alternative layouts (275 × 1 flattened, 11 × 25 transposed) → hard failure. So 25 × 11 is the right shape; only the trailing rows are wrong.
- Not a generic footer problem: `SYIEUEFbIPaF.csv` has a single all-empty trailing row and reads correctly (234.148 either way). The BPFUbIP case differs in having **three** trailing rows, two of which carry text in column A.

Fix is a one-line strip of the trailing rows in all 13 files, but the durable fix belongs in whatever xlsx→CSV export produced them (it will re-add the footer next regeneration). **Not applied** — these are Dan's generated data files, and stripping them alone would not yield a run while (A) stands. Worth checking whether other regenerated files in this restructure share the pattern.

**Still open / for Dan:**
1. T1–T7 simulation checkpoints once (A) and (B) are resolved (§10). Note `AllVars.lst` is stale (~459 dead names incl. pre-restructure ones) — regenerate before using it as the T1 savelist. `EPS_base0_model.mdl` at repo root is the pre-change baseline for the T1 diff.
2. `PEaWHRP-MHRP.csv` placeholder 0.07 values — clean up before release.
3. WebAppData.xlsx — manual: retire the WHR lever row, remap "Industrial Energy Efficiency Standards" to `Min Fraction of Process Efficiency Measure Potential Deployed`, add the 3 other levers; also check whether any web-app output mapping is positional over `Govt Cash Flow Type` (new element inserted after `indst clean heat subsidy`).
4. Docs repo (Phase F, §9 list) — drafts pending, staff review before publication.
5. FoPITY generator .py files still emit pre-temp-band content (pre-existing drift; the CSVs are source of truth). The 4 new lever blocks + GRA rows exist only in the CSVs — fold into the generators when they get fixed.
6. R2 sign-off (PM lever semantics change for web-app continuity) — now applied in the model; confirm before release.
7. Flagged in passing (pre-existing, unverified): possible BAU/policy transposition in `Industry Sector Carbon Tax Rebate due to CCS`; `Value of CCS` adds T&S subsidy without netting T&S cost; `GRA-CCSsubsidy.csv` header cell mislabeled "fuel subsidy"; `SYIEUEFbIPaF.csv` has 13 data rows where 12 fuels are expected (check for a stray row).


**Session dates:** 2026-07-27 (v1), revised same day after Dan's answers · **Status: PLANNING ONLY — no model, input, or doc changes made.**
**Input data source:** `C:\Users\DanOBrien\Downloads\PEaWHRP.xlsx` (4 tabs)
**Scope:** Replace the single-potential WHR lever (`WHRPbI`/`WHRCC`/`Perc of Waste Heat Recovery Potential Achieved`) with a measure-level, endogenous cost-based deployment structure mirroring industrial CCS, plus a parallel structure for process-efficiency measures. The existing `Percentage Improvement in Industrial Process Efficiency above BAU` lever is **also retired** and replaced by the new efficiency-measure standards lever (decided v2, §7.1). Burner-integral heat recovery is already in the unit-efficiency inputs (SYIEUEFbIPaF/IEMUEF/BIEEI) and is **excluded** from everything below.

Draft for Dan's review; data values cited from input files should be verified against source workbooks.

### v2 decision log (from Dan, 2026-07-27)

1. Hurdle rate = `BCoISC Weighted Average Cost of Capital by Industry` **plus a hurdle premium** (new input; WACC values are base cost of capital, 0.037–0.058). Proposed default premium **+0.05** (→ ~9–11% effective decision rate) — Dan to confirm value.
2. Carbon-tax-inclusive `Industrial Fuel Cost per Unit Energy` used directly, no separate carbon term — **confirmed**.
3. Denominators/application: **WHR percentages are shares of heat demand** (heating-process energy); **efficiency-measure percentages are shares of total energy demand**. Application geometry updated accordingly (§3.2, §5). Elec base = total industry electricity (both sets, per the "% elec base" column header) — *residual verify against Dan's derivation for the 6 WHR elec-savings rows* (§12-R3).
4. Retirement: Dan open either way → **recommendation: retire via `DELAY FIXED(deployment, lifetime)`** (§5.1).
5. Zero-policy expectation: **recommendation: keep the counterfactual screen; zero-policy run deploys nothing** (§6.1).
6. Start rate `SoCEMDSiaY` = 0.2/yr, **one shared scalar** for both measure sets.
7. Cost-level defaults kept: 5 levels, multipliers [0.62, 0.84, 1.00, 1.16, 1.38], 20% shares (re-evaluated §4.5).
8. Standards fill order: cheapest-first vs pro-rata **still open** — plain-language explanation in §7; recommendation cheapest-first with pro-rata fallback (§12-R1).
9. **No construction conveyor.**
10. Capacity basis: current-year base (explained and adopted, §8.1).
11. **Separate** subsidy + standards lever pairs for WHR vs efficiency; **new `Govt Cash Flow Type` element** `indst efficiency subsidy`.
12. Capex **booked in-year**, financed like industrial equipment (`SoICETAF` split + CRF repayment machinery) — no `DEPRECIATE STRAIGHTLINE` smoothing.
13. Old lever's ratchet replaced by stock persistence (explained §5.2 — behaviorally near-identical; recommend accept).
14. **Input CSVs stay in long form** — read with the FoPITY pattern (flattened row subscript + `VECTOR ELM MAP` remap), no pivot needed (§4.3, verified against `FoPITY ... = GET DIRECT LOOKUPS(..., 'E2')` at EPS.mdl:33287).

### v3 decision log (from Dan, 2026-07-27, second round)

15. **`MHRP` = 0.07, per-industry file GENERATED** at `InputData/indst/PEaWHRP/PEaWHRP-MHRP.csv` (25 rows, all 0.07, verified against declaration order). ⚠️ **FLAG: placeholder values — Dan will clean up the file before release.** The only implementation artifact created so far; everything else remains unbuilt.
16. WHR elec-savings denominator = **heating-process electricity** (R3 resolved): WHR elec fractions apply to the electricity slice of `industrial heating process` only, and the WHR elec capacity base is heating-process electricity. `heat if`/`hydrogen if` confirmed inside the denominators (zero-valued today, so no data impact).
17. Cost-level multipliers: the ±30% σ came from **Dan's original task brief** ("approximating a ±30%-σ spread"); the five multipliers/shares are plain CSVs (σ itself is not an input). Role narrowed (v3): **MCLM affects the deployment decision (LCOS) only — all cash-flow accounting uses the unadjusted input capex/opex** (§4.5, §8). With the symmetric defaults, Σ(share × mult) = 1.0 exactly, so fully-deployed measures cost the same either way; only partially-deployed measures differ (slight overstatement of cheap-tranche cost, understatement of expensive-tranche cost).
18. **Standards fill order: pro-rata** (R1 resolved) — the lever deploys X% of every tranche uniformly; compliance cash flows use the unadjusted input capex/opex (consistent with #17, and exactly cost-correct under pro-rata since the multipliers average to 1). The cheapest-first `VECTOR SORT ORDER` machinery is dropped from scope.
19. **R7 waste-heat availability index: include** (§5.3); revisit after first results.
20. Retirement (`DELAY FIXED`) and the zero-policy invariant (screen ⇒ zero deployment at zero levers) stand as decided-by-delegation (Dan: "depending on what you think" / "what do you think" → recommendations adopted). R5/R6 closed.

---

## 1. What the data contains (verified from the xlsx)

| Tab | Shape | Content |
|---|---|---|
| `PEaWHRP-WM` | 7 rows | subscript elements `waste heat measure 1..7` |
| `PEaWHRP-PM` | 18 rows | subscript elements `efficiency measure 1..18` |
| `PEaWHRP-WMD` | 175 data rows (25 industries × 7 slots) | per-slot: fuel savings, elec savings, capex intensity, opex intensity, lifetime, source |
| `PEaWHRP-PMD` | 450 data rows (25 × 18) | same columns |

Facts that shape the design:

- The 25 industries **match the `Industry Category` subscript exactly, in declaration order** (EPS.mdl:40195), industry-major with measures minor — exactly the row order the `VECTOR ELM MAP` remap needs.
- Savings columns are stored as **fractions (0–1)**, not percents, despite the "%" headers (max fuel savings 0.219 in WMD, 0.053 in PMD).
- Per Dan (v2): WMD fuel-savings fractions are shares of **heat demand**; PMD fractions are shares of **total energy demand**; elec columns are shares of total industry electricity (verify R3).
- WMD: 41 nonzero rows (13 Bianchi fill, 28 measure-level); capex 8.2–211.5 $/MMBtu-yr; opex 0–10.6; lifetimes {10, 15, 20, 30}. Empty slots carry lifetime 20 (harmless).
- PMD: 63 nonzero rows; capex 0–883.6; **opex −19.1 to +105.7 — negative opex exists** and is handled naturally by the LCOS math (§4.4).
- **Three PMD rows have zero capex + zero opex with nonzero savings** (cement) → always BAU-cost-effective → **standards-only** under the screen (§6).
- Mix: WMD 34 fuel-only / 6 elec-only / 1 both; PMD 43 / 14 / 6.
- Text columns (`Measure`, `Source`) stay in the exported CSVs — the long-form read skips them (like FoPITY skips columns A–D), so the model-read file keeps its own documentation.

---

## 2. The CCS pattern (what we mirror, what we deviate from)

Chain summary (policy case):

```
CECRCbI supply curve (GET DIRECT LOOKUPS; x = $/ton, y = cumulative fraction cost-effective)
Carbon Tax Rate + Industry Sector CCS Subsidy (BCS/NBICS, 45Q-style) + Industrial CCS T&S Subsidy
   → Value of CCS [$/tCO2e]                                        (EPS.mdl:63393)
   → CCS Retrofit Capacity Desired = LOOKUP BACKWARD(curve, value) (23025)
   → gap = MAX(desired − last-yr deployed+pipeline, 0)             (28363)
   → Started This Year = MIN(gap, MAX(desired − start-yr BAU, 0) × SoCECRCSiaY)  (23008; SoCECRCSiaY = 0.2/yr)
   → DELAY FIXED conveyor, CRDT = 5 yr → cumulative stock (Last Year DELAY FIXED; NO retirement)
   → Fraction of CO2 Captured = MAX(economic, Industry Sector Minimum Fraction of CCS Achieved This Year)  (33794)
```

Cash flows: capex from *increase* in tons × capital cost (endogenous learning); O&M from level; financed share `SoICETAF`, CRF on `BCoISC Financing Interest Rate by Industry` over `RPfFISCC[other processes]`; opex+repayments → `Change in Miscellaneous Expenditures by Industry` (25405); capex → `Change in Upfront Capital Expenditures by Industry for {Financed|Non Financed} Equipment` (26138/26155); subsidy → `Change in Government Cash Flow by Cash Flow Type[CCS subsidy]` (25171).

### Mirror / deviate table (v2-final)

| CCS element | Decision | New-structure counterpart |
|---|---|---|
| Value stack = carbon price + subsidy, current-year snapshot | **Mirror** (concept) | Value per BTU saved = avoided-energy price blend (carbon-tax-inclusive) + subsidy lever (§4.4) |
| `CECRCbI` pre-binned cumulative lookup curve | **Deviate** | Explicit measures × `Measure Cost Level` subscript; direct value-vs-LCOS comparison |
| `SoCECRCSiaY` = 0.2/yr start rate | **Mirror** | `SoCEMDSiaY` = 0.2, one shared scalar (decided) |
| `CRDT` 5-yr construction conveyor | **Deviate (decided)** | No conveyor; deployment effective the year after the start decision via the Last Year stock pattern |
| No retirement | **Deviate (recommended)** | `DELAY FIXED(new deployment, lifetime)` retirement re-opens potential (§5.1) |
| Full BAU economic-deployment twin | **Deviate (decided)** | No BAU deployment; counterfactual screen in the policy case (§6); zero BAU twin variables |
| Mandate via `MAX`, instant, costed, un-capped vs potential | **Mirror + fix** | Standards lever via MAX per tranche, capped at potential by construction; fill order §7 |
| Capex on increase, opex on level, `SoICETAF`/CRF financing | **Mirror (decided)** | Same machinery, reusing the WHR financing skeleton; capex booked in-year |
| `DEPRECIATE STRAIGHTLINE` + `STfCCE` smoothing | **Not used (decided)** | — |
| Endogenous learning on capital cost | Not planned | Static measure costs |
| Decision discount rate | **Deviate (decided)** | CCS embeds costs in the curve; we build an explicit CRF on `BCoISC WACC + MHRP hurdle premium` (§4.4) |

CCS-side observations flagged for separate follow-up (unverified, out of scope): possible BAU/policy transposition in `Industry Sector Carbon Tax Rebate due to CCS` (40381 vs 8960); `Value of CCS` adds T&S subsidy without netting T&S cost.

---

## 3. Current structures being retired, and the energy chain

### 3.1 Current WHR (retirement inventory in §9)

Lever `Perc of Waste Heat Recovery Potential Achieved[Industry Category]` (51701; ratcheted `This Year` variant 51730; FoPITY block `indst waste heat recovery X <industry>`, 25 contiguous rows at lines 1268–1292 of every FoPITY CSV, position-load-bearing via `VECTOR ELM MAP`). Reduction = `WHRPbI × Perc Achieved This Year` (60917), applied to the `industrial heating process` subrange in the total-equipment chain (39751), the new-equipment chain (46265), and inside `Industrial Clean Heat Production Subsidy Amount Paid` (39576/39590/39609 — **the new multipliers must be substituted here** or clean-heat subsidy is paid on eliminated energy). Cash-flow side: `New Waste Heat Recovery Equipment Capital Expenditures` (46823) + financed split + CRF (22294) + repayment stock (32149/41835) → Miscellaneous (25412) and Upfront Capex (26144/26155) + cost-output SUMs (40450/40862/40914/41062). No BAU twin, no opex, no retirement.

### 3.1a Existing process-efficiency lever (retired per Dan's 11a)

`Percentage Improvement in Industrial Process Efficiency above BAU[Industry Category, Industrial Fuel]` (52856, default 0) → `...This Year` (52887, FoPITY block `indst process efficiency X <industry> X <fuel>`, **300 rows**, 25×12) → `This Year Industrial Energy Use Reduction Due to Process Improvements` = 1/(1+x) (60763), applied at the end of the equipment chain (39742) and inside the clean-heat subsidy (39592/39611). **Verified: this lever has no cost wiring** — the `EoIEPwEEI` price elasticity (31360) is consumed only by `Price Increase for New Indst Eqpt Due to Eff Standards` (54107), which is driven by `Improvement in New Industrial Eqpt Energy Intensity vs BAU` (38925) — the *equipment-intensity* standards channel, a different lever. Also verified: `US_ClimateAmbition.cin` does not set it, and the Create*Script.py generators don't reference it. So replacing it with the measure-based standard upgrades a costless free-savings lever to one with real capex/opex, at the cost of a semantics change: per-fuel arbitrary-% → per-industry, potential-capped fraction (§12-R2 sign-off). `EoIEPwEEI` and the equipment-intensity standards channel are untouched.

### 3.2 Insertion point and calculation order (confirmed)

```
vintaged equipment stock output × fuel-type shares × energy intensity        ← SYIEUEF/BIEEI/IEMUEF + equipment stds
   (electrification / fuel switching inside the vintage fuel shares)            act HERE, upstream
→ Industrial Equipment Energy Use by Fuel Type and Process before Waste Heat Recovery   (39765; to be renamed)
→ [WHR + process-improvement multipliers]                                    ← REPLACED by the two measure-set multipliers
→ Industrial Equipment Energy Use by Fuel Type and Process                   (39742)
→ SUM over process → Industrial Fuel Use for Energy before CCS and Methane Capture → ... → Industrial Fuel Use
```

Measure savings applied at this slot are after unit-equipment efficiency and after electrification, multiplicative — the required no-double-count ordering. Avoided-energy expenditure, emissions, and macro feedbacks flow automatically from reduced `Industrial Fuel Use`; only capex/opex/subsidy need new wiring.

**Application geometry (v2, per Dan):**

| | Fuel-savings fraction applies to | Elec-savings fraction applies to | Capacity base for costing |
|---|---|---|---|
| **WHR measures** | nonelectricity-fuel slices of `industrial heating process` subrange | electricity slice of `industrial heating process` **(v3, R3 resolved)** | heat-demand base: `SUM(...before measures[i, nonelec f!, industrial heating process!])`; elec: heating-process electricity |
| **Efficiency measures** | nonelectricity-fuel slices of **all** processes | electricity slice, all processes | total-combustion base: `SUM(...[i, nonelec f!, Industrial Process!])`; elec: total elec base |

Composition is multiplicative and order-free: heating nonelec slices × (1−F_whr)(1−F_pem); other nonelec slices × (1−F_pem); heating electricity × (1−E_whr)(1−E_pem); other-process electricity × (1−E_pem). `nonelectricity industrial fuel` (47170) includes `heat if` and `hydrogen if` — confirmed inside the denominators (zero-valued today). PM elec base = electricity over all processes incl. facility HVAC/lighting.

---

## 4. Measure economics

### 4.1 New subscripts

```
Waste Heat Measure:            GET DIRECT SUBSCRIPT('InputData/indst/PEaWHRP/PEaWHRP-WM.csv', ',', 'A2', 'A', '')
Process Efficiency Measure:    GET DIRECT SUBSCRIPT('InputData/indst/PEaWHRP/PEaWHRP-PM.csv', ',', 'A2', 'A', '')
PEaWHRP WM Row:                GET DIRECT SUBSCRIPT('InputData/indst/PEaWHRP/PEaWHRP-WMD.csv', ',', 'K2', 'K', '')   { 175 flattened rows }
PEaWHRP PM Row:                GET DIRECT SUBSCRIPT('InputData/indst/PEaWHRP/PEaWHRP-PMD.csv', ',', 'K2', 'K', '')   { 450 flattened rows }
Measure Cost Level:  cost level 1, ..., cost level 5     (inline; structural)
```

The flattened row subscripts mirror `Policy Element`: one element per (industry × measure) row, named from a new **Key column K** added to the WMD/PMD tabs (e.g. `01T03 X waste heat measure 1` — must be unique; concatenate Code + Slot). Rows must stay industry-major in `Industry Category` declaration order with measures minor — same position-dependence FoPITY already lives with.

### 4.2 Input variables

**Long-form reads** (five 1-D constants per set, one per data column, skipping text columns exactly as FoPITY's `'E2'` start does; `'*'` = read down the column):

```
Flat WHM Fuel Savings Potential[PEaWHRP WM Row]  = GET DIRECT CONSTANTS('...PEaWHRP-WMD.csv', ',', 'E2*')   { Dmnl }
Flat WHM Elec Savings Potential[PEaWHRP WM Row]  = ... 'F2*'    { Dmnl }
Flat WHM Capital Cost[PEaWHRP WM Row]            = ... 'G2*'    { $/BTU; ÷1e6 at export, §4.3 }
Flat WHM OM Cost[PEaWHRP WM Row]                 = ... 'H2*'    { $/BTU }
Flat WHM Equipment Lifetime[PEaWHRP WM Row]      = ... 'I2*'    { years }
   + the five Flat PEM ... [PEaWHRP PM Row] equivalents
```

**Remaps into natural 2-D form** (one per field, wrapped in `INITIAL()`; everything downstream uses these):

```
WHMFSP Waste Heat Measure Fuel Savings Potential[Industry Category, Waste Heat Measure] = INITIAL(
    VECTOR ELM MAP( Flat WHM Fuel Savings Potential[<first key element>],
                    (Industry Category − 1) × ELMCOUNT(Waste Heat Measure) + (Waste Heat Measure − 1) ))
   { likewise WHMESP, WHMCC, WHMOC, WHMEL and PEMFSP, PEMESP, PEMCC, PEMOC, PEMEL }
```

**Shared inputs:**

| Variable | Subscripts | Default | Purpose |
|---|---|---|---|
| `MCLM Measure Cost Level Multiplier` | [Measure Cost Level] | 0.62, 0.84, 1.00, 1.16, 1.38 | scales levelized cost |
| `MCLS Measure Cost Level Share` | [Measure Cost Level] | 0.20 × 5 | splits each measure's potential |
| `SoCEMDSiaY Share of Cost Effective Measure Deployment Started in a Year` | scalar | 0.2 | shared by both sets (decided) |
| `MHRP Measure Hurdle Rate Premium` | [Industry Category] | **0.07 (placeholder — Dan to clean up)** | added to WACC in the decision CRF only (§4.4); **file generated**: `PEaWHRP-MHRP.csv`, read `'B2*'` |

### 4.3 Input CSV target layout — long form, no pivot (v2)

`InputData/indst/PEaWHRP/`, four CSVs, exported tab-for-tab from the xlsx:

```
PEaWHRP-WM.csv    A1 header; A2:A8 measure names          (subscript)
PEaWHRP-PM.csv    A1 header; A2:A19 measure names         (subscript)
PEaWHRP-WMD.csv   header row 1; 175 data rows; columns A Industry, B Code, C Slot, D Measure(text),
                  E Fuel savings, F Elec savings, G Capex ÷1e6, H Opex ÷1e6, I Lifetime, J Source, K Key(new)
PEaWHRP-PMD.csv   same, 450 rows
PEaWHRP-MCL-mult.csv / -share.csv / MHRP + SoCEMDSiaY CSVs   (small constants)
```

Only two changes to the xlsx: **add the Key column** and **export capex/opex ÷ 1e6** ($/MMBtu-yr → $/(BTU/yr), `IECCpUAEU` unit convention, unit line `$/BTU`; values ~1e-5). All 2012$, consistent with model dollars. Text columns ride along unread — the CSV stays self-documenting.

### 4.4 Levelized cost and value

Decision rate (decided): `BCoISC Weighted Average Cost of Capital by Industry` (0.037–0.058) **+ `MHRP[Industry Category]`** — the WACC is a base financing cost; the premium represents the elevated returns firms demand from efficiency retrofits. **v3: 0.07 for all industries (placeholder file generated; ⚠️ Dan to clean up values before release).** Effective decision rate ~11–13%. Financing *cash flows* still use `BCoISC Financing Interest Rate by Industry` (repayment accounting, §8). The premium applies identically inside and outside the BAU screen, so it cannot break the zero-policy invariant (§6.1).

```
Waste Heat Measure Capital Recovery Factor[Industry Category, Waste Heat Measure] = INITIAL(
    (WACC[i] + MHRP[i]) / (1 − (1 + WACC[i] + MHRP[i])^(−WHMEL[i,m]/One Year)) )

Levelized Cost of Waste Heat Measure Energy Savings[i, m, Measure Cost Level] = INITIAL(
    (CRF[i,m] × WHMCC[i,m] + WHMOC[i,m]) × MCLM[cl] )        { $/BTU saved; time-invariant; DECISION ONLY —
                                                               cash flows use unadjusted WHMCC/WHMOC (v3, §8) }
```

Negative PEM opex simply lowers LCOS; negative-total-LCOS tranches behave like the zero-capex case (standards-only under the screen).

```
Blended Industrial Heat Fuel Cost per Unit Energy[i] =        { WHR value; weights = heating-process fuel use }
    ZIDZ( SUM(Last Year heating-process fuel use[nonelec f!] × Industrial Fuel Cost per Unit Energy[i, nonelec f!]),
          SUM(Last Year heating-process fuel use[nonelec f!]) )
Blended Industrial Combustion Fuel Cost per Unit Energy[i] =  { PEM value; weights = all-process fuel use }

Value of Waste Heat Measure Energy Savings[i, m] =
    ZIDZ( WHMFSP × Blended Heat Fuel Cost + WHMESP × Industrial Fuel Cost per Unit Energy[i, electricity if],
          WHMFSP + WHMESP )
    + Waste Heat Measure Deployment Subsidy This Year[i]      { $/BTU saved }

Waste Heat Measure Value at BAU Prices[i, m] =
    same with BAU Industrial Fuel Cost per Unit Energy (8814) and BAU (last-year) fuel-use weights, NO subsidy
```

**Carbon price (confirmed):** `Industrial Fuel Cost per Unit Energy` (39901) is carbon-tax-inclusive (pretax + `Industrial Fuel Total Tax or Subsidy Amount per Unit Energy` 39963, which contains the carbon-tax adder 39882) → no separate carbon term. The BAU screen picks up the BAU carbon tax via the BAU twin.

**Loop caution:** blend weights use **Last Year** fuel use; if Vensim flags a simultaneous loop through the endogenous industrial electricity price, lag that too.

### 4.5 Cost-level defaults (v3-final)

Purpose: stage each measure across five cost variants so deployment ramps in as the value signal rises instead of switching whole measures at once. **Provenance of the 30%:** Dan's original task brief specified "approximating a ±30%-σ spread"; the five multipliers are its equal-probability quintile-midpoint discretization (Φ⁻¹ at the 10/30/50/70/90th percentiles × 0.30 + 1). σ is *not* an input — only the resulting multiplier and share vectors are, as plain CSVs (`PEaWHRP-MCL-mult.csv` / `-share.csv`), editable without touching the discretization story.

**Role (v3, decided): decision-only.** MCLM scales the LCOS used in the cost-effectiveness screen and deployment; **all cash-flow accounting (capex, opex) uses the unadjusted input capex/opex**. Because the symmetric defaults satisfy Σ(MCLS × MCLM) = 1.0 exactly, a fully deployed measure books identical total cost under either convention; during partial economic deployment the unadjusted accounting slightly overstates the cheap tranches' cost and understates the expensive ones'. If Dan later edits the multipliers asymmetrically, note that Σ(share × mult) ≠ 1 would introduce a systematic gap between decision economics and booked cost — acceptable, but worth knowing.

(One consequence worth knowing: the bottom quintile at 0.62× makes *some* tranche cost-effective at ~38% lower value than the headline cost — the intended smoothing — and correspondingly grows the screen's "BAU-cost-effective" region at the cheap end.)

---

## 5. Deployment (potential → stock → savings)

Per tranche `[Industry Category, Measure, Measure Cost Level]`; tranche potential share of its measure = `MCLS[cl]`. Last Year `DELAY FIXED` stock pattern throughout.

```
Waste Heat Measure Tranche Economically Deployable[i,m,cl] =
    IF THEN ELSE( WHMFSP[i,m] + WHMESP[i,m] <= 0, 0,                               { empty-slot guard }
      IF THEN ELSE( Value[i,m] >= Levelized Cost[i,m,cl]
                    :AND: Value at BAU Prices[i,m] < Levelized Cost[i,m,cl], 1, 0 ) )

New Waste Heat Measure Deployment This Year[i,m,cl] =
    MAX( Economically Deployable × SoCEMDSiaY × MAX(0, 1 − Last Year Deployed Fraction),   { econ channel }
         MAX(0, Mandated Deployed Fraction This Year[i,m,cl] − Last Year Deployed Fraction) )  { standards floor }

Waste Heat Measure Deployment Retired This Year[i,m,cl] = DELAY FIXED(New Deployment, WHMEL[i,m], 0)

Deployed Fraction of Waste Heat Measure Potential[i,m,cl] =
    MIN(1, MAX(0, Last Year Deployed Fraction + New Deployment − Retired This Year))
    { Last Year twin = DELAY FIXED(…, 1, 0); zero initial — no deployment at model start }
```

### 5.1 Retirement — recommendation: **retire** (Dan open either way)

Reasons: (a) PM lifetimes go down to 5–6 years — without retirement, a 2027 deployment incurs capex once in 25 model years, materially understating recurring cost for exactly the short-lived measures where opex/capex accuracy matters; (b) retirement makes the standards floor meaningful (mandate maintains the level by backfilling, correctly re-incurring capex); (c) potential stays conserved — retired tranches re-open and refill automatically at `SoCEMDSiaY` if still screen-eligible, so long-lived measures (20–30 yr) barely churn within the 2025–2050 horizon while short-lived ones cycle as they should. Cost: one `DELAY FIXED` per set + a mild sawtooth on refill. The simpler alternative (CCS-style no retirement) is defensible only if we also accept understated costs on the 5–15 yr measures; not recommended.

### 5.2 Ratchet → stock persistence (Dan's 11c, explained)

The old lever hard-ratcheted: `MAX(lever × schedule, Last Year)` — once up, never down within a run, even if the lever's schedule declined. In the new structure persistence lives in the deployed stock: deployed tranches stay deployed until end-of-life regardless of later value/lever changes; the only "decline" path is a lowered *standards* lever letting mandated-but-uneconomic tranches lapse at retirement rather than being replaced (no instant un-deployment exists anywhere). Behaviorally near-identical to the ratchet for any monotone policy schedule; recommend accepting.

### 5.3 Interaction with rising unit efficiency — waste-heat availability index (v2 addition, Dan's note 2026-07-27)

The fraction-based application already scales *absolute* measure savings, opex, and new-deployment capex one-for-one with the energy base, so unit-efficiency improvements (BIEEI trends, the equipment-intensity standards lever) and electrification automatically shrink deployed savings proportionally. What static percentages miss: as unit efficiency η rises, waste heat per unit of *remaining* fuel falls by (1−η′)/(1−η) — the recoverable *fraction* erodes on top of the base. This matters for the WHR set (burner-integral recovery in the unit-efficiency files taps the same flue-gas stream as the system-integration measures — the gap-fill economizer/recuperator rows), and is roughly the same order as the proportional effect for plausible efficiency gains. It is *not* worth modeling for the PM set (discrete curated interventions, small potentials — proportional-only is fine).

**Proposed (R7, recommended):** scale WHM potentials by a per-industry index:

```
Waste Heat Availability Index[i] = MIN(1, ZIDZ( heating-process nonelec fuel use per unit output[i],
                                                Start Year heating-process nonelec fuel use per unit output[i] ))
   { policy case; fuel-only to avoid double-counting electrification; start-year anchor so BAU-trend
     efficiency also erodes potential (Bianchi/Kermeli potentials are snapshots of today's stock);
     for base efficiency near 0.5 the intensity ratio ≈ the (1−η′)/(1−η) erosion factor — first-order proxy }
```

applied as `WHMFSP_effective[i,m] = WHMFSP[i,m] × Index[i]` (and WHMESP for the WHR set) in the roll-up, capacity bases, and standards-potential denominator. No new input data. T3's asymptote checkpoint compares against the index-scaled potential.

**Savings roll-up** (both sets):

```
Fraction of Industrial Heat Fuel Use Avoided by WHR Measures[i]        = SUM(WHMFSP[i,wm!] × SUM(MCLS[cl!] × Deployed[i,wm!,cl!]))
Fraction of Industrial Heat Electricity Use Avoided by WHR Measures[i] = (same with WHMESP)
Fraction of Industrial Combustion Fuel Use Avoided by PEM Measures[i]  = (same with PEMFSP)
Fraction of Industrial Electricity Use Avoided by PEM Measures[i]      = (same with PEMESP)

Application (§3.2 geometry, v3):
  heating-process nonelec slices      × (1 − F_whr[i]) × (1 − F_pem[i])
  other-process nonelec slices        × (1 − F_pem[i])
  heating-process electricity slice   × (1 − E_whr[i]) × (1 − E_pem[i])
  other-process electricity slices    × (1 − E_pem[i])
  { identical treatment in the New-equipment chain (46265) and the clean-heat subsidy multiplier (39576) }
```

Bound check in QA: max Σ WHR fuel potential ≈ 0.22 of heat demand, PM ≈ 0.05 of total — (1−F) stays well positive.

---

## 6. BAU rule — counterfactual screen (decided; recommendation on the open sub-question)

No economic deployment in BAU; no BAU twin machinery at all. The screen lives in the policy case: a tranche deploys economically **only if** not cost-effective at BAU prices but cost-effective under the policy-inclusive value.

### 6.1 Zero-policy expectation — recommendation: **zero deployment** (Dan asked "what do you think")

Keep the screen and accept that a zero-policy run deploys *nothing* — including cost-negative and zero-capex tranches (BAU-cost-effective ⇒ standards-only). Reason: the fundamental EPS invariant is that a Policy run with no levers set **equals BAU exactly** — every output is a Policy−BAU delta, and any zero-lever deployment would manufacture free-lunch abatement deltas in every scenario and break the regression baseline permanently. The brief's original "zero-policy test showing only cost-negative measures deploying" belongs to the rejected hurdle-premium-only alternative. With v2's `MHRP` premium the screen is unchanged (premium raises LCOS on both sides symmetrically). Test T2 expectation: `Deployed Fraction ≡ 0` in a zero-lever run; Policy = BAU bit-identical.

Consistency with BIEEI: all autonomous efficiency improvement stays in BIEEI upstream; the screen guarantees zero structural overlap. Data-level curation (burner-integral exclusions) already handled by Dan.

**Alternative (recorded, not planned):** calibrated behavioral hurdle premium *instead of* the screen — continuous policy response on every tranche, but a per-industry free parameter to calibrate and BAU-recalibration fragility. The screen is parameter-free at the cost of a knife-edge softened by the five cost levels.

---

## 7. Standards channel

Two levers (per measure set), FoPITY-scheduled (25 elements each):

```
Min Fraction of Waste Heat Measure Potential Deployed[Industry Category]          { Dmnl [0,1], default 0 }
Min Fraction of Process Efficiency Measure Potential Deployed[Industry Category]
```

### 7.1 The PM standards lever replaces `Percentage Improvement in Industrial Process Efficiency above BAU` (decided, Dan's 11a)

Retire the old lever, its `This Year` variant, its 1/(1+x) multiplier, and its 300 FoPITY rows; the new lever takes its Policy Control Center slot and web-app identity ("Industrial Energy Efficiency Standards" or renamed). Gains: real capex/opex where the old lever had none (verified §3.1a); potential-grounded ceiling. Semantics change (per-fuel arbitrary % → per-industry capped fraction) — R2 sign-off. No scenario fallout: `US_ClimateAmbition.cin` doesn't set the old lever.

### 7.2 Fill order — **pro-rata (decided v3)**

The lever deploys X% of *every* tranche uniformly:

```
Mandated Deployed Fraction This Year[i,m,cl] = Min Fraction of ... Potential Deployed This Year[i]
    { same value for every (m, cl); composes with the economic channel via the MAX in §5 }
```

~4 simple equations per set; the cheapest-first `VECTOR SORT ORDER` machinery is out of scope. Cost accounting for mandated deployment uses the **unadjusted input capex/opex** (v3 decision #17/#18) — under pro-rata this is exactly cost-correct, since uniform deployment across cost levels averages the multipliers to Σ(share × mult) = 1.0. Known bias accepted: compliance cash flows are cost-*averaged* rather than cheapest-first, so a modest standard books the measure-average cost instead of the low-hanging-fruit cost.

Properties: reaches BAU-cost-effective and cost-negative tranches (uniformly); never exceeds total potential (lever ≤ 1 ⇒ tranche ≤ 1); no double fill with the economic channel (MAX); mandated cost-negative measures show net savings to industry (negative opex flows through as credits).

---

## 8. Cash flows

All flows policy-only (BAU = 0) → no "Change in" subtraction. Capex **booked in-year** (decided), financed like industrial equipment:

```
New Measure Savings Capacity Deployed This Year[i] { BTU/yr } =
    Σ_m,cl New WHM Deployment × MCLS × (WHMFSP × Heat Fuel Base[i] + WHMESP × Heat Elec Base[i])
  + Σ_m,cl New PEM Deployment × MCLS × (PEMFSP × Combustion Fuel Base[i] + PEMESP × Elec Base[i])
      { bases = pre-measure SUMs per §3.2 geometry, current year }

New Measure Capital Expenditures[i]       = same sums weighted by CC   { $; UNADJUSTED capex — no MCLM (v3) }
Measure OM Expenditures[i]                = same structure on the Deployed-Fraction level × OC (no MCLM)
Measure Deployment Subsidy Amount Paid[i] = deployed savings BTU × subsidy lever[i]  (per set)
```

- **Financing (decided — "like industrial equipment"):** `SoICETAF Share of Industry Capital Expenditures That Are Financed` split; financed portion amortized via CRF on `BCoISC Financing Interest Rate by Industry` over `RPfFISCC[other processes]` with the Annual-Repayment / Expiring / Last-Year stock pattern (reuse the retiring WHR machinery's skeleton: 22294/1311/32149/41835). Non-financed capex → `Change in Upfront Capital Expenditures by Industry for Non Financed Equipment` (26155); financed → (26144); repayments + opex → `Change in Miscellaneous Expenditures by Industry` (25412, replacing the WHR term). Cost-output SUMs at 40450/40862/40914/41062 swap to new names. Negative PEM opex flows through as a Miscellaneous credit.
- **Subsidy levers** (per set, per industry, $/BTU saved; web-app can display $/MMBtu): value-side adder (§4.4) + government outlay → new `Govt Cash Flow Type` element **`indst efficiency subsidy`** (decided; precedent `indst clean heat subsidy` 35390) + one `GRA-*.csv` weights file (`InputData/ctrl-settings/GRA/`). Both sets' subsidies share the one Govt type.
- Entity allocation unchanged (nonenergy industries / coal suppliers / natural gas and petroleum suppliers split rides existing aggregations).

### 8.1 Capacity basis — explanation (Dan's Q9) and the adopted convention

Deployment is stored as a *fraction* of potential; dollars need BTU. The BTU value of a tranche = fraction × the industry's energy base, and the base moves every year (production growth, electrification). Adopted convention (option a): **new deployment is costed at the deployment-year base; opex and subsidy on the whole deployed stock are costed at the current-year base.** Implication: a deployed measure's absolute savings (and opex) scale up/down with the industry's activity — which is exactly what multiplying energy use by (1−F) does anyway, so the fraction representation and the costing stay coherent, with no vintage dimension. The alternative (vintage-locking absolute BTU/yr at install) would fix opex but then absolute savings wouldn't match the (1−F) application without converting back to a time-varying fraction — more structure for no consistency gain. One accepted simplification: growth of the *base* under an already-deployed fraction does not incur incremental capex (second-order; noted for QA awareness).

---

## 9. Retirement list (old structures)

**In EPS.mdl — WHR:** lever pair 51701/51730 + Last Year 42165; `WHRPbI` 64048, `WHRCC` 64039; reduction chain 60917/60109/42283/55829; application points 39751–39763, 46265–46277; clean-heat interaction 39590/39609; capex/financing 46823–46841, 22294, 1311/1398, 32149, 41835, 25412, 26144, 26155, 40450, 40862, 40914, 41062; sketch objects in 5 views (64906; 65610–65614; 77111–77488; 78586–78874 incl. section label; 84679).
**In EPS.mdl — old process-efficiency lever (v2):** 52856, 52887, 60763; consumers at 39746, 39592/39611; its sketch objects (Policy Control Center + Industry views — locate at implementation); FoPITY block `indst process efficiency X <industry> X <fuel>` (300 rows).
*(All line numbers drift — re-grep by name at implementation.)*

**Outside EPS.mdl:**
- `InputData/indst/WHRPbI/`, `WHRCC/` — retire folders (incl. stale `~$` lock file).
- FoPITY: remove the 25-row `indst waste heat recovery` block **and** the 300-row `indst process efficiency` block from `FoPITY-policy-elements.csv` + all 18 schedule CSVs; add new blocks (4 levers × 25 = 100 rows); **regenerate via** `FractionOfPolicyImplementedThisYear.py` (WHR blocks at 4256–4330) and reconcile the duplicate `...new.py` (10808–10882) — never hand-edit (positional `VECTOR ELM MAP` anchors). New subsidy levers don't need future-year projection (current-year value only) — no change to the foresight-policy-element optimization set.
- `US_ClimateAmbition.cin` lines 573–591 — replace with new-lever settings (Dan chooses values).
- `CreateCombinationsScript.py:235` / `CreateContributionTestScript.py:231` — already stale (pre-4.1 cogen/WHR name); replace with new levers.
- `WebAppData.xlsx` — manual Excel task: WHR lever row + "Industrial Energy Efficiency Standards" row remap to the new levers (also delete stale `~$WebAppData.xlsx`).
- Verified no-change: `BAU_Lever_Settings.txt`, `OutputVars*.lst`, `GraphDefinitions.vgd`, `InputData/web-app/*`, `CreateDataLoggingScript.py`, `CreateCarbonCapToTaxScript.py`.
- Docs repo (`Models\EPS\docs`): `cogeneration-and-waste-heat-recovery.md` + `sidebars.js:143`; `industry-ag-main.md:174–178` + `industry-ag-main-CogenWHR.png`; `how-the-eps-avoids-double-counting.md:62`; the industrial-energy-efficiency page (now also the old PM lever's doc); two frozen HTML snapshots under `static/dcs/`. Version-history entries stay. New doc pages drafted at implementation — **staff review before publication**.

---

## 10. Phased implementation sequence & test checkpoints

Baseline first: save pre-change `BAU` and `US_ClimateAmbition` runs (`.vdfx` + key-var `.tab`).

| Phase | Work | Checkpoint |
|---|---|---|
| **A. Inputs & subscripts** | Add Key column + ÷1e6 export to xlsx; write 4 CSVs + small constants; declare 5 subscripts, 10 flat reads, 10 INITIAL remaps, MCLM/MCLS/SoCEMDSiaY/MHRP; **no equation changes** | Model loads; units check passes; `vensimdp.err` clean; BAU **bit-identical**. Spot-check 3 remapped cells against the xlsx (VECTOR ELM MAP index arithmetic) |
| **B. Economics + deployment stocks** | CRF/LCOS/value/screen/stocks + retirement DELAY FIXED — savings not yet applied | T1 BAU identical. T2 zero-policy: Deployed ≡ 0 (screen blocks all — §6.1). T3 extreme carbon tax ($300+/t): deployment ≤ 20%/yr per tranche, asymptotes at potential; only non-BAU-cost-effective tranches admitted |
| **C. Application to energy use** | Replace WHR + process-improvement multipliers at the three application points with the two-set geometry (§3.2); retire reduction-chain + old-PM-lever multiplier variables | T4: forced test deployment moves industry heat-fuel / total-fuel / elec use by exactly the potential×deployed sums (hand-check 2 industries); all slices ≥ 0 |
| **D. Standards channel** | 2 levers + pro-rata mandated-fraction logic (v3) + FoPITY regeneration (remove 325 rows, add 100) | T5: 100% mandate ⇒ full (index-scaled) potential deployed; zero-capex cement tranches deploy **only** via this lever; econ+mandate never exceeds potential; partial mandate books unadjusted (measure-average) costs. Old-lever FoPITY block removal verified against every `VECTOR ELM MAP` anchor below line 1268 |
| **E. Cash flows + retire old structures** | Capex/opex/subsidy/financing wiring; delete WHR + old PM lever equations, inputs, sketch objects; update .cin + python scripts | T6: capex hand-check one industry-year; negative-opex PEM tranche → Miscellaneous credit; subsidy in Govt cash flow under `indst efficiency subsidy`. T7: 5-yr-lifetime tranche under sustained value shows recurring replacement capex. Full units check; BAU bit-identical; updated `US_ClimateAmbition` runs clean |
| **F. Docs + web app** | Doc rewrites, WebAppData.xlsx remap, output lists if new outputs wanted | Staff review before publication |

**Phase D warning:** removing the old process-efficiency FoPITY block shifts every row below it by 300 — *all* `VECTOR ELM MAP` anchors for later policy elements survive only because they reference elements by name; the danger is any hand-maintained artifact keyed to row *numbers*. Regenerate, don't edit; then run the full lever smoke-test (each lever nonzero → nonzero delta).

---

## 11. Resolved decisions

See the v2 decision log at top. Superseded v1 questions: 1, 2, 5, 6, 8, 9, 10, 11b, 11c (and 14 — long-form input reading).

## 12. Remaining open items

All R-items resolved except:

- **R2 — old PM lever semantics sign-off:** replacement lever is per-industry and potential-capped (old: per-fuel, unlimited %). Confirm acceptable for web-app scenario continuity. §7.1.

Standing flags carried into implementation:

- ⚠️ **`PEaWHRP-MHRP.csv` holds placeholder 0.07 values — Dan to clean up per-industry before release** (v3 #15).
- **R7 revisit:** waste-heat availability index is in scope for the first build; re-evaluate after initial results (v3 #19).
- **R3 residual:** `heat if`/`hydrogen if` are inside the denominators but zero-valued today — if future data gives them nonzero heating use, no change needed (they're already in the application slices).

Resolved log: R1 → pro-rata (v3 #18); R3 → heating-process electricity (v3 #16); R4 → 0.07 per-industry, file generated (v3 #15); R5 → retire (v3 #20); R6 → zero-deployment invariant (v3 #20); R7 → include (v3 #19).

---

*Prepared as a working input for Dan's review; nothing here is final or approved for implementation. Data values quoted from input CSVs and the CCS map should be verified against source workbooks before use.*
