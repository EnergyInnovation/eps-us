# Calibration log

Dated record of every calibration performed on this model: which step, what export it used, what
it wrote, the verification result, and any decision taken. Newest first.

## 2026-09-21 — skill build: steps 1 and 2 on eps-us develop_4.0.6 @ ccbb54df (branch calibration-skill)

- Baseline BAU export `runs/base.tab` from `export-vars.lst`.
- Tooling note: Vensim parks at startup (0.3 CPU-s, no LOADMODEL in vensimdp.err) when the command
  file is given as a relative sub-path (`calibration\runs\base.cmd`). A bare filename in the model
  folder (`_calib_base.cmd`) runs normally. The runner now always writes the .cmd at the repo root.
- **Step 1 (SoCDTtiNTY + ANVCV), dry solve then apply.** No sales history in `benchmarks/` yet, so
  every group used the step-free criterion (ANVCV stays 0; MarkLines export pending from Robbie).
  Largest share changes: aircraft/freight 0.0280 → 0.0404 (step before −31%), LDVs/freight
  0.0588 → 0.0667 (−12%), HDVs/passenger 0.0900 → 0.0809 (+11%), HDVs/freight 0.0526 → 0.0488 (+8%).
  motorbikes/freight has no vehicles and was skipped. Rail and ships hand off in 2058–59, checked by
  projection only.
- **Step 2 (SoCEUtiNTY), dry solve then apply.** Largest: residential heating 0.0526 → 0.0468
  (step before +12–13%), commercial cooling 0.0632 → 0.0576 (+10%), commercial heating +7%.
  Residual 1–2 year wobble after the handoff is BCEU input variation replayed L years later, not
  the calibration.
- **Verification run `runs/verify12.tab`** (both steps applied, 70 s): step at handoff = 0.0% for
  all 15 buildings groups and all in-horizon vehicle groups except aircraft (passenger +0.4%,
  freight +2.6% = one airframe of INTEGER rounding on fleets of ~280 and ~40).
- Precision: shares are written with 10 significant digits; copying each cell's old decimal count
  (first attempt) rounded 0.0809 to 0.08 and left a visible step.
- **Step 3a (TTS base-year inversion), built and run.** Logit in this version has no clamp:
  share ∝ TTS × exp(cost/mile × TTLE). Costs at IT come from the shared BAU export (`runs/base3.tab`,
  export list extended), so the inversion needs no extra run. Observed shares seeded from the legacy
  `calibration_parameters.csv` (LDVs, HDVs × passenger/freight, 2024–25) into
  `benchmarks/vehicle-technology-shares.csv`.
  - k-test: existing weights reproduce the pure logit to ≤6e-5 in every group except passenger LDVs
    (ZEV mandate binds at IT in 15 subregions) and passenger rail (9.8e-3 = one vehicle of rounding
    on 82/yr; tolerance is now max(1e-4, 1/fleet)).
  - **Unreachable observed shares (cost-input problem, not calibration):** gasoline buses 24.2% and
    LPG buses 3.6% observed but modelled cost per mile is a $240/mile placeholder; natural gas
    freight trucks 1.96% at $355/mile; LDV freight natural gas 0.74% at $20,415/mile. With TTLE −3
    to −8 no finite weight gives these a share. Their weights are written as 0 and the miss is
    reported; the realised diesel bus share is 0.887 vs 0.640 observed until the costs are fixed.
  - Mandate correction for passenger LDVs: target the pre-overlay share = observed × (pure/realised)
    from the current run. Pass 1 (from base3) landed BEV at 5.29% vs 5.05% observed (more states bind
    as the pure share falls); pass 2 solved from `runs/verify3.tab`, verify3b pending.
  - Trajectory re-anchoring on apply: for t > IT, new(t) = E_new + (old(t) − E_old)(F − E_new)/(F − E_old),
    exact for the workbook's E + (F − E)·s(t) family; count basis in the workbook is t − IT.
- **Step 3b (trajectory fitter) built**, dry-tested on a synthetic BEV target (2030 25%, 2040 60%,
  2050 85%): hits the targets from one export (K_j = sales/weight predictor), and flags that the
  fitted weight exceeds 1 (7.9 in 2050) — the target needs more preference than cost parity gives.
  No US targets supplied yet; `benchmarks/vehicle-technology-share-targets.csv` is the input.
- **Step 3a verification, passes 1–3** (`runs/verify3.tab`, `verify3b.tab`, `verify3c.tab`): freight LDVs,
  buses and freight trucks reproduce their reachable observed shares to ≤1e-4 on the first run.
  Passenger LDVs (mandate binding in 15 subregions) converged geometrically: BEV 5.29% → 5.16% →
  5.10% vs 5.05% observed; the remaining 0.05 pp is state-level top-up granularity. Rule for the
  skill: mandate-bound groups take 2–3 solve/run passes; all others one.
- **Step 4 layer 1 (`check_conventions.py`) built and run on the US inputs:** V1–V3, V6 pass;
  V4 WARN: hard coal and lignite are banned only through 2025 while nuclear/SMR/CCS/H2 are banned
  through 2030–31 — a coal merchant build is possible from 2026 if trailing prices spike; V8: BAU
  CES non-zero in 29 subregions (state CES laws, expected for the US); V9: nuclear and biomass
  mandated retirements stop in 2034, geothermal 2026 (economic retirement then governs). RAF derates
  coal 0.63 / lignite 0.60 / gas 0.9 / peakers 0.8 and reaches reliability credit and retirement too.
- **Step 5 (BFPIaE) built, dry-run on `runs/base4.tab`** (steps 1–3 applied): eps-us carries a live
  distortion — coal mining 05 percent change 9.8% (2025) rising to 28% (mid-2030s), pipelines
  352T353 −0.9% → −23.4% (2050), oil & gas 06 to −11%, refining 19 to −10%. FPIEBP puts production at
  priority 1 for most fuels (China-lineage pattern), so seven production rows qualify under the
  two-filter rule (hard coal, lignite, natural gas, gasoline, diesel, jet fuel, LPG); crude oil,
  heavy fuel oil and NG imports/exports pass through unchanged. The fixed-point loop is deferred
  until the step 4 comparison is settled (run order 4 → 5).
- **Step 4 layer 3 (`rebase_vre_cf.py`) built**: implied curve CF vs model CF at IT — solar PV 0.232
  curve / 0.208 model (HYECFCA 1.067), onshore wind 0.343 / 0.333, offshore 0.420 / 0.449, solar
  thermal 0.250 / 0.234. Benchmark CF column fills once `benchmarks/elec-*.csv` exist (EIA 2025 pull
  in progress).
- **Step 4 layer 2/4 (`compare_benchmarks.py`) built**; awaiting the same benchmark files.
- **Step 4 layer 2 result, US 2025 vs EIA (EPM Table 1.1/1.1A generation, 6.2 June-2025 capacity;
  `benchmarks/sources.md`):** generation ratios model/EIA — coal 1.00, gas 0.97, nuclear 1.00, hydro
  0.97, wind 1.00, solar (utility + small-scale) 1.01, geothermal 1.00, petroleum 0.94, total 0.98.
  Capacity within 2% except solar 1.12 (model 214 GW vs EIA 191 GW AC net summer — a capacity-basis
  difference, since generation matches; CF 0.208 vs 0.231 follows from it) and biomass 0.34 (model
  3.8 GW / 16.9 TWh vs EIA 11.4 GW / 40.9 TWh — EIA's category includes wood and landfill-gas
  cogeneration the model books elsewhere; data-scope question, not dispatch). **Decision: no RAF /
  BGDPbES / SYSHECF change for the US anchor year; the dispatch emulator is not needed here** (it
  earns its keep where several historical years disagree, as in Korea). No national wholesale
  price benchmark exists (EIA publishes hub prices only); model 2025 = $42/MWh.
- Layer 3 (VRE rebase, report only): solar factor 1.109 is the capacity-basis artefact above — not
  applied; onshore wind 1.027 (CF 0.333 vs 0.342) left alone at this precision; offshore has no 2025
  benchmark.

- **Step 5 loop (`run_loop.py`) converged in two model runs**: max |percent change| 28.0% (base4) →
  4.3% (after pass 1) → 1.2% (after pass 2, ≤ 2% tolerance). Seven production rows replaced (hard
  coal, lignite, natural gas, gasoline, diesel, jet fuel, LPG). Final confirming run `runs/final.tab`
  also serves the power ↔ BFPIaE interaction check against `runs/base4.tab`.

- **Final confirmation (`runs/final.tab`, all five steps applied):** BFPIaE max |percent change| 1.2%
  (refining, the slowest row, as in China); steps 1–2 still step-free (0.0% at every in-horizon
  handoff; aircraft ±1 airframe); power ↔ BFPIaE interaction: 2025 generation and price unchanged to
  four decimals, forward years drift ≤0.3% total / ≤1.2% on small sources — no second 4 → 5 pass.

- **AEO case convention (Robbie, 2026-09-21):** the US model uses the AEO Alternative Electricity and
  Transportation case; benchmarks and comparisons use that case, not the central/"Counterfactual
  Baseline" case. `vehicle-sales-projection.csv` rebuilt accordingly (same 2025 value).
- **Official-statistics check:** MarkLines light vehicles vs BEA (FRED ALTSALES, class 1-3) within 0.5%
  every year 2004-2025; MarkLines medium+heavy vs BEA heavy trucks (HTRUCKSSA) 0.416 vs 0.417 M in 2025.
  AEO Table 38 is 1.1-1.2 M below BEA because it stops at 8,500 lb. AEO's own VMT/stock gives
  10,518 mi/veh in 2025 = BAADTbVT exactly; AEO falls to 9,500 by 2050, the input to 9,092 (AEO 2025
  side case). AEO stock +24%, VMT +12%, sales flat -> implied vehicle life 18 -> 22 yr; EPS matches the
  stock growth but with a fixed life sells +24%. The divergence is lifetime, not mileage.
- **AVL provenance (workbook):** BTS NTS 2015 Table 1-20 lifetimes 13 (cars) / 14 (light trucks),
  weighted 13.4; then "calibrated" to 17 so that SYVbT/L matched ~15 M passenger LDV sales. That is
  the share's job now, so AVL can revert to a lifetime estimate - but 13.4 is 2000s-era median life;
  current median light-vehicle life is ~16-18 yr, so 17 stands as a lifetime, not as a sales fit.

### Pending after this session
- **Workbook sync.** The steps write CSVs only. `eps-input-data-checks` will flag CSV/xlsx drift for
  `Share of Cargo Dist Transported that is New This Year.xlsx`, `Share of Cpnt E Use that is New This
  Year.xlsx`, `Transportation Technology Shareweights.xlsx` (Data sheet anchors D:E for LDVs/HDVs),
  `Additional New Vehicles Calibration Variable.xlsx` (About note: sum-to-zero convention dropped,
  reason), and `BAU Fuel Production Imports and Exports.xlsx` (production tab, after convergence).
  Paste values in Excel or via COM — not openpyxl (sparklines are dropped on save). Add a dated
  About-tab note in each.
- **Placeholder vehicle prices — awaiting colleague (Robbie shared 2026-09-21).** NBPoNVP rows for
  gasoline/LPG buses, natural gas/gasoline/LPG freight trucks, and natural gas/LPG light commercial
  were set to 999,999,999 in commit 7dc6f64e (mkmahajan, 2026-01-28, "Vehicle price updates for
  latest data sources"; ATB + AEO Table 38 do not price them), replacing real values (gasoline bus
  ~$342k, LPG bus ~$574k) with no workbook note. Effect: hard zero sales for those technologies.
  Conflicts with the observed shares (gasoline buses 24%, LPG buses 3.6%, NG trucks 2%). If the
  intent was to retire them: drop them from `benchmarks/vehicle-technology-shares.csv`. If not:
  restore the pre-7dc6f64e rows (`git show 7dc6f64e^:InputData/trans/NBPoNVP/...`) and re-run 3a.
- **Vehicle sales benchmark** (`benchmarks/vehicle-sales.csv`) from MarkLines, then re-run step 1 so
  ANVCV is populated.
- **Step 1 re-run with MarkLines sales (`benchmarks/vehicle-sales.csv`, US LDVs 2004–2025; HDVs
  uncovered → step-free).** Point-cohort ANVCV rejected after the dry run (2026 sales 12.7 M, share
  +19% persisting to 2050). Adopted: ±3-year triangular kernel on the cohort, history extended past IT
  with the model's own sales, last pre-handoff year pinned to year-IT sales. Applied; verified in
  `runs/verify1k.tab`: step at handoff 0.0% for LDVs (both cargo types), 2025 sales 15.18 M =
  observed, retirements 12.7 M → 11.7 M (2027) → 14.2 M (2030); shares 0.0586 → 0.0680 (psgr),
  0.0667 → 0.0814 (frgt). Residual: +1.9% sales step in the handoff year when ANVCV ends.
  **Finding for the transport lead:** modelled LDV sales run 1.12× AEO 2026 in 2025 (MarkLines 16.7 M
  vs AEO 15.0 M — the sources disagree on 2025 itself) and 1.65× by 2050, because the constant share
  rides cargo-distance growth while BAADTbVT miles per passenger LDV fall 14%; AEO holds sales flat.
  Not a share issue (`benchmarks/vehicle-sales-projection.csv`, diagnostic printed by the step).
- **Sales-scope reconciliation (Robbie, 2026-09-21 PM: "MarkLines and AEO should match").** They do
  once classes align. MarkLines US 2025 = 16.31 M cars + light trucks (class 1-2b, incl. Transit /
  Express / ProMaster / E-Series vans and HD pickups) + 0.21 M medium (class 4-7) + 0.21 M heavy
  (class 8). AEO Table 38 = 15.0 M under 8,501 lb; class 2b is AEO's "commercial light trucks" (no
  sales series); Table 49 light-medium = class 3 (312 k), medium = class 4-6 (156 k), heavy = 7-8
  (288 k). EPS scope (SYVbT About): freight LDVs = commercial LT + light-medium + medium; freight
  HDVs = heavy only (model 278 k vs AEO 288 k). Benchmark rebuilt on that scope; the earlier 16.7 M
  LDV anchor included class 4-8 trucks. My earlier "AEO reference" label was the Alternative
  Electricity & Transportation side case from the NBPoNVP workbook; the central case gives the same
  15.0 M for 2025.
- **Step 1 re-applied on the rebuilt benchmark, verified in `runs/verify1m.tab`:** shares 0.06769
  (psgr) / 0.08250 (frgt); handoff steps 0.0%. LDV sales vs the AEO-equivalent scope (Table 38 +
  class 3-6; class 2b missing, so AEO is ~0.5-1 M low): 1.07 / 1.06 / 1.04 for 2025-27 = parity
  within the 2b gap; then 1.16 (2029), 1.22 (2030), 1.34 (2035), 1.59 (2050). The interim
  divergence from 2028 is structural: the constant share rides cargo-distance growth (+8%) and
  falling miles per vehicle (-14%) while ANVCV climbs back from the recession cohorts. Retirements
  13.7 M (2025) → 13.0 M (2027) → 15.7 M (2030). Open decision: time-varying share (model change).
- **LAUNCH STATE for step 1 (Robbie's call, 2026-09-21 evening): pinned mode applied and verified
  (`runs/verify1p.tab`).** Shares 0.05261 (psgr, −10% vs original) / 0.06635 (frgt); ANVCV non-zero in
  every year 2025–2050 (sales-only lever after the 2040/2042 handoffs). Verified: LDV sales on the
  benchmark path in every year (1.07× the AEO-equivalent, which is the class-2b scope gap), handoff
  step 0.0% both groups. Residual, as designed: early retirements 18.1 M vs ~14.1 M real (BTS scrappage
  12–15 M), so the fleet holds ~282–291 M through 2050 instead of growing to ~355 M (AEO scope-adjusted):
  about −19% in 2050. Cohort mode kept as `--mode cohort` for a future time-varying share.
- **Stock-size test (2026-09-21, runs `stocktest_original` / `stocktest_pinned`, same model, only
  SoCDTtiNTY + ANVCV differ):** LDV stock 343 M vs 288 M in 2050 (−16%); LDV fuel use 1.189e16 vs
  1.184e16 BTU (−0.5%); transport energy CO2 −0.5%; BEV share of the LDV stock 0.307 vs 0.310. Confirms
  the equations at EPS.mdl:3750 and :14650: fuel = exogenous cargo distance × technology share of the
  stock ÷ fleet fuel economy, so the stock LEVEL does not reach energy or emissions; only its
  technology composition and the sales/stock turnover rate do. Vehicle count matters for
  vehicle-count outputs (spending, EV units, per-vehicle costs) and for internal consistency
  (implied miles per vehicle = cargo distance / stock).
- **Implied miles per vehicle (2026-09-22, runs `stocktest2_original` / `stocktest2_pinned`, export adds
  `BAU Fleet Avg Fuel Economy` and `BAU Cargo Dist Transported by Vehicle Technology`).** Robbie asked what
  compensates for the fleet size if distance, fuel economy and emissions are all unchanged. Answer: nothing
  in the model does; the identity vehicles × miles/vehicle = cargo distance is not written anywhere. Cargo
  distance is exogenous (EPS.mdl:3730), sales = share × distance / BAADTbVT + ANVCV (:10873), fuel = distance
  / fleet fuel economy (:14652); the stock is bookkeeping downstream of fuel. The quantity that absorbs the
  fleet size is the IMPLIED miles per vehicle = distance / stock / loading, which the model never checks
  against BAADTbVT (itself AEO VMT / stock, Alternative Transportation case). 2050 fleet fuel economy for
  gasoline passenger LDVs: 3.975e-4 vs 3.956e-4 pass-mi/BTU (pinned 0.5% worse), same 3.1e12 passenger-miles
  on 196 M vs 161 M cars. Implied miles per passenger LDV vs the file: original 1.00 (2025) → 1.09 (2035–40)
  → 1.04 (2050); pinned 1.01 → 1.17 → 1.27. Freight LDVs: original 1.01 → 1.18 (2050); pinned 1.00 → 1.14.
  The original inputs therefore also break the identity (freight by 18%) — a standing input-consistency
  finding independent of the launch choice. New diagnostic `steps/01-trans-turnover/miles_per_vehicle.py`
  reports the ratio; `export-vars.lst` now carries the distance variable. Pinned inputs restored after the
  test (SoCDTtiNTY psgr 0.05261).
- **Workbook sync (2026-09-22, `calibration/sync_workbooks.py`, Excel COM).** Robbie asked where the data-only
  update lives and whether the xlsx files were updated per the build-input-xlsx skill; they were not. Fixed: each
  of the five workbooks (SoCDTtiNTY, ANVCV, SoCEUtiNTY, TTS, BFPIaE) now carries a `Calibration` tab holding the
  calibrated values with provenance (step, run, method), pre-calibration values alongside, and the output tabs
  reference it, so the original 1/lifetime, s-curve and AEO-scaling derivations stay visible. Dry run compared
  every output cell to its CSV before saving; all five matched. Two things changed on the CSV side: (1) the four
  on-road TTS CSVs were re-exported from the workbook, because the step's re-anchoring formula reproduces the
  workbook s-curve only to ~1e-4 (the workbook is the source of record; the change is immaterial to the model
  and below any rerun threshold, verify3c stands); (2) nothing else - SoCEUtiNTY values were taken from the
  applied CSV because `steps/02/out/results.json` held a later dry-run solve, not the applied one. ANVCV About
  text "The sum of each row should be zero" replaced with the new convention (Robbie's 2026-09-21 decision).
  TTS Data tab: HDV passenger gasoline/LPG, HDV freight natural gas/gasoline, LDV freight natural gas/LPG anchors
  are 0 (unreachable at placeholder costs) and are flagged provisional in the About record pending the colleague's
  cost-input fix. BFPIaE workbook internals (one drawing, no sparklines in this version) preserved.
- **Round 2 on the updated model (2026-09-22, eps-us develop_4.0.6 @ bcd444b3; `run_all.py`, runs `base5`,
  `r2_verify1..3c`, `bfpiae1/2`, `r2_final`, ~11 min).** Upstream brought fdab3be0 (real prices for alternative
  bus/truck technologies, replacing the 999,999,999 placeholders) and bcd444b3 (BEEEfEPS lever setting); no .mdl
  change. Tracked inputs were reset to HEAD and the whole chain re-run from a fresh export.
  Results: step 1 identical to round 1 (psgr LDVs 0.05261, frgt 0.06635; ANVCV differs by <0.1%); every handoff
  step 0.0% in the confirming run (aircraft passenger +0.4%, 285 planes). Step 2 identical, all 15 groups 0.0%.
  Step 3 converged in three passes (passenger LDV BEV 5.05% target reached); with real prices the formerly
  unreachable groups (gasoline/LPG buses, NG/LPG freight LDVs, NG/gasoline trucks) invert to exactly the committed
  weights (k-test ≤ 2e-5), so no TTS row is zeroed any more. Step 4: V1–V3, V6 pass, V4 WARN (coal/lignite bans end
  2025), US 2025 within 3% of EIA for every major source, no dispatch change. Step 5 converged in two passes
  (28% → 4.2% → 1.2%); interaction check: no power-sector movement above tolerance. Implied miles per vehicle vs
  BAADTbVT unchanged from round 1 (passenger LDVs 1.27 in 2050, freight LDVs 1.14; committed inputs 1.04 / 1.18).
  Workbooks synced with `sync_workbooks.py --tab runs/r2_final.tab` (all five tabs match their CSVs).
  Tooling fixes this round: verify mode in steps 1–2 no longer re-solves against the applied CSV (it reports the
  apply's record); `sync_workbooks.py` reads calibrated values from the applied CSVs and the ANVCV demand term from
  the final export; `run_all.py` added; old round-1 exports and scratch files removed (stock-size test kept under
  `diagnostics/`).
- **Code moved into the skill (2026-09-22, Robbie's decision).** The Python now lives in agentic-age
  `skills/eps-calibrate/scripts/` (mirrored to `~/.claude/skills/eps-calibrate/`); this folder keeps only the
  region's data and results: benchmarks/, this log, export-vars.lst, out/<step>/ (results.json, charts) and
  git-ignored runs/. Scripts resolve the model from the working directory. Verified from this repo root:
  init_repo (nothing to create), check_conventions, steps 1–2 verify-only, step 3 and 5 dry solves, step 4
  comparison, miles-per-vehicle diagnostic and the workbook sync dry run (0 mismatches) all reproduce round 2.
