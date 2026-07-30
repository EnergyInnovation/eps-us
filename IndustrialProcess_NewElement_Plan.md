# Restructuring the `Industrial Process` Heating Elements into Temperature Bands

Working plan — draft for staff review, revised 2026-07-16. Verify all inventories against
the repo and all new input data against primary sources before use.

## STATUS (code implementation executed 2026-07-16 — all changes uncommitted, revertible via git)

Done (by Claude, structural/code only — no data values invented):
- **EPS.mdl**: subscript definitions rewritten (5 bands at positions 1–5, family now 11
  elements); all element renames (18+18+18+27 occurrences); 12 new IES equation blocks for
  `heat above 1000 C`; 9 lever matrices expanded with zeros; 9 VECTOR ELM MAP anchors
  renamed; sketch subscript entries updated. Backup: `EPS.mdl.bak`.
- **GraphDefinitions.vgd**: 8 series renamed, 2 new `heat above 1000 C` series added.
- **FoPITY (19 files)**: renamed 656 heating rows and inserted 164 new-band rows per file
  (ramp values copied verbatim from the adjacent `heat 500 to 1000 C` rows); every
  schedule file's row sequence verified identical to FoPITY-policy-elements.csv
  (3,756 → 3,920 elements).
- **IES**: 48 heating CSVs `git mv`-renamed (`IES-heatbelow100-*`, `IES-heat100to200-*`,
  `IES-heat200to500-*`, `IES-heat500to1000-*`); 12 new `IES-heatabove1000-*.csv` created
  as **zero-shareweight placeholders** (replace with real data).
- **BCHSR**: labels renamed + fifth zero row added (both files were all-zero already).
- Transform scripts kept at repo root for reuse in other geographies:
  `TempBandRestructure_MDL.js`, `TempBandRestructure_FoPITY.js`.

Remaining — Dan (data):
- Repopulate the heating rows/columns (4 → 5 entries, bands in subscript order) in:
  BIEEI (2), BPFUbIP (13), EoIEPwEEI, IECCpUAEU, IEMUEF, IESD (3), PIFURfE, RPfFISCC,
  SYIEUEFbIPaF, SHELF-indstproc (6) — per the layout table in §2 — and the paired
  .xlsx/.xlsm sources. Until these have 11 process entries, simulation will fail on
  GET DIRECT dimension mismatches (LOADMODEL may already flag constants files).
- Replace the 48 renamed IES files' contents + 12 placeholder files with real
  shareweight data.
- Remap the 294 old-element SETVAL lines in US_ClimateAmbition.cin / hydgn.cin /
  procemiss.cin (judgment call — see §2).

Remaining — coordination: web app (WebAppData.xlsx, FoPITY-*-WebApp already restructured),
EPS docs, other geographies (rerun the two scripts there).

## 0. The change

Replace the four current heating elements (which mix equipment type and temperature):

| Old (positions 1–4) | New (positions 1–5) |
|---|---|
| boilers | heat below 100 C |
| nonboiler low temp | heat 100 to 200 C |
| nonboiler med temp | heat 200 to 500 C |
| nonboiler high temp | heat 500 to 1000 C |
| — | heat above 1000 C |

Boiler energy is folded into the bands (steam mostly serves the <200 °C bands). The six
non-heating elements (`cooling` … `other nonprocess`) are unchanged but shift from family
positions 5–10 to 6–11. `Industrial Process` goes 10 → 11 elements; the
`industrial heating process` subrange is redefined as the five bands and stays contiguous
at positions 1–5, which keeps the clean-heat `VECTOR ELM MAP (industrial heating
process-1)` arithmetic valid.

**Naming (decided 2026-07-16):** `heat below 100 C`, `heat 100 to 200 C`,
`heat 200 to 500 C`, `heat 500 to 1000 C`, `heat above 1000 C` — spelled-out ASCII
(Vensim element names and FoPITY CSV rows can't safely carry `<`, `>`, `°`, or commas).

**Division of labor (decided 2026-07-16):** Dan supplies and populates all input-data
values (he has the temperature-band data); Claude's implementation scope is code only —
EPS.mdl edits, the FoPITY policy-element regeneration script, and CSV *restructuring
scripts* if useful, but no data values. Implementation starts only after staff review of
this plan.

**Ordering invariant (unchanged from before):** subscript definition order = row/column
order in every GET DIRECT CSV = FoPITY policy-element cycle order = inline matrix order.

## 1. The data problem (gates everything)

Every per-process input currently keyed to boilers/nonboiler-temp must be re-expressed by
temperature band. Note the old nonboiler splits are MECS °F ranges (low <300 °F, med
300–1000 °F, high >1000 °F), which do NOT align with the new °C bands — this is a genuine
re-disaggregation, not a relabel.

Needed by industry (× fuel where applicable):
- **Heat demand by temperature band** → BPFUbIP shares. Candidate sources: NREL/DOE
  industrial process-heat demand datasets (McMillan et al.), MECS Table 5.2 for fuel/boiler
  splits, sector studies (steel/cement >1000 °C, food/paper <200 °C). Boiler fuel gets
  allocated to bands via steam-temperature assumptions. **Each industry's shares must
  still sum to 100%** so Start Year energy is preserved.
- **Equipment characteristics by band**: capital cost (IECCpUAEU), efficiency-standard
  elasticity (EoIEPwEEI), minimum/start-year unit energy factors (IEMUEF, SYIEUEFbIPaF),
  survival/retirement (IESD ×3), repayment period (RPfFISCC), BAU efficiency improvement
  (BIEEI), electrification potential (PIFURfE), hourly load shapes (SHELF ×6),
  shareweights (IES).
- **Scaffold option** for a first mechanical pass: build band values as energy-weighted
  combinations of the old boiler/nonboiler values so BAU totals are preserved, validate
  the plumbing, then refine band-specific data in a second pass.

## 2. Input files affected

All paired `.xlsx`/`.xlsm` sources must be updated alongside the CSVs.

### Restructure heating rows/columns (4 → 5 entries), positions of non-heating entries shift by one
- `InputData/indst/BIEEI/` — BIEEI-elec.csv, BIEEI-other.csv (rows = process)
- `InputData/indst/BPFUbIP/` — 12 per-fuel CSVs + fallback (process = columns; verify) — re-derive shares, keep row sums at 100%
- `InputData/indst/BCHSR/` — BCHSR-investment.csv, BCHSR-production.csv (rows = heating process; all zeros today, so mechanical)
- `InputData/indst/EoIEPwEEI/EoIEPwEEI.csv` (cols = process)
- `InputData/indst/IECCpUAEU/IECCpUAEU.csv` (rows = process, transposed read `B2*`)
- `InputData/indst/IEMUEF/IEMUEF.csv` (cols = process)
- `InputData/indst/IESD/` — IESD-AAaWER.csv, IESD-FoIERbA.csv, IESD-FoPERNbA.csv (rows = process)
- `InputData/indst/PIFURfE/PIFURfE.csv` (cols = process)
- `InputData/indst/RPfFISCC/RPfFISCC.csv` (rows = process)
- `InputData/indst/SYIEUEFbIPaF/SYIEUEFbIPaF.csv` (cols = process)
- `InputData/elec/SHELF/SHELF-indstproc-{winter,spring,summer,fall,winterpeak,summerpeak}.csv` (rows = process)

### IES (per-(process,fuel) files)
- Delete/retire the 48 heating files (`IES-boilers-*`, `IES-nonboilerlow-*`,
  `IES-nonboilermed-*`, `IES-nonboilerhigh-*`); create 60 new per-band files
  (`IES-heat1-elec.csv`, … naming TBD) × 12 fuels. 72 non-heating files unchanged.
- Update `Industrial Equipment Shareweights.xlsx/.xlsm`.

### FoPITY (19 files: FoPITY-policy-elements.csv + FoPITY-1..9.csv + FoPITY-1..9-WebApp.csv)
- `FoPITY-policy-elements.csv` **defines the `Policy Element` subscript** (GET DIRECT
  SUBSCRIPT) — rebuild every process-crossed block with the new 11-element cycle:
  - 6 policies × 25 industries × process: 250 → **275 rows each** (`indst shift to
    electricity`, `indst shift to alt fuel`, `indst eqpt early retirement`, `indst eqpt
    cost of capital`, `indst fuel efficiency stds`, `indst elec efficiency stds`)
  - `RnD industry capital cost reduction` × 12 fuels: 120 → **132 rows**
  - `indst clean heat ITC` / `PTC`: 4 → **5 rows each**
- Ordering per block must match the VECTOR ELM MAP flattening: industry-major for the six
  industry×process policies **except** `indst eqpt cost of capital` (process-major);
  RnD is process×fuel; clean heat follows subrange order.
- Same edits mirrored in all 18 schedule CSVs. **Generate these with a script** (pattern:
  the repo's Create*Script.py helpers); hand-editing ~1,700 rows across 19 files is
  error-prone.

### Scenario files — WILL break until updated
294 SETVAL lines reference the old element names and will error on load:
- `US_ClimateAmbition.cin` (286 lines), `hydgn.cin` (4), `procemiss.cin` (4)
- Remapping old settings to bands needs judgment (a boilers electrification fraction
  doesn't map 1:1 to a temperature band). Sweep **all** `.cin` in the repo before running.

### Not affected
`BAU_Lever_Settings.txt`; `RPfFHSCC` (hydgn — separate subscript family despite shared
names; decide separately whether to align it); savelists; acronym-key (unless names
change acronyms).

## 3. EPS.mdl edits

1. **Subscript definitions** — rewrite `Industrial Process:` (11 elements, bands first)
   and `industrial heating process:` (the 5 bands).
2. **IES equation blocks** — rename the 48 heating blocks' subscript elements and CSV
   paths; add 12 new blocks for the fifth band (60 heating blocks total). Mirror each
   fuel's `:INTERPOLATE:`/`:=` pattern.
3. **VECTOR ELM MAP anchors** — 9 references use `... X boilers` as the block's first
   element (e.g. `Selected Policy Implementation Schedule[indst clean heat ITC X
   boilers]`); rename to the new first band in: indst shift to alt fuel, indst shift to
   electricity, indst eqpt early retirement, indst eqpt cost of capital, indst fuel/elec
   efficiency stds, RnD industry capital cost reduction, indst clean heat ITC, indst
   clean heat PTC.
4. **Inline constant lever matrices** — restructure the process dimension (10 → 11,
   heating entries first) with zeros; update the `{...}` comment labels:
   - `Fraction of Eligible Industrial Energy Use Shifted to Electricity` [25×10 → 25×11]
   - `Fraction of Eligible Industrial Energy Use Shifted to Alternate Fuel` [25×11]
   - `Minimum Share of Start Year Industrial Equipment Retired` [25×11]
   - `Perc Improvement in Eqpt Efficiency Stds Above BAU for Combustible Fuels` [25×11]
   - `Perc Improvement in Eqpt Efficiency Stds Above BAU for Electricity` [25×11]
   - `Perc Decrease in Cost of Capital for Clean Industrial Equipment` [10×25 → 11×25]
   - `RnD Industry Capital Cost Perc Reduction` [10×12 → 11×12]
   - `Perc Subsidy for Clean Industrial Heat Equipment` [4 → 5 entries]
   - `Subsidy for Clean Industrial Heat Production` [4 → 5 entries]
5. **Review, likely no change**: `:EXCEPT: [..., other nonprocess]` mobile-equipment
   blocks; `RPfFISCC ...[other processes]` proxy references (~3 sites); the ~187
   process-dimensioned equations inherit the new elements automatically.
6. **Comments/labels**: `{boilr}` style comments in RnD matrix; the model-notes text
   mentioning "coal-powered boilers" (Debugging section); sketch-section `6:<element>`
   entries (cosmetic — Vensim regenerates on GUI save).

## 4. Suggested sequence

1. Staff review of this plan; freeze band data methodology (Dan has the data in hand).
2. Script the FoPITY policy-element regeneration (deterministic, testable) — code task.
3. EPS.mdl edits (subscript, IES blocks, anchors, matrices) — code task.
4. Dan restructures/populates the input CSVs + xlsx sources with the band data
   (per the inventory in §2; ordering invariant in §0 applies to every file).
5. Headless BAU run: fix GET DIRECT dimension errors from `vensimdp.err` iteratively.
6. Validate (below), then remap `.cin` scenarios.

## 5. Validation

Bit-identical regression is **not** achievable here (the heating stock is re-partitioned,
so logit fuel choice and vintage tracking arithmetic all change). Instead:
1. **Start Year conservation**: with scaffold shares, Start Year `Industrial Fuel Use`
   by industry × fuel must match the old model exactly (BPFUbIP rows sum to 100%).
2. **BAU trajectory drift**: compare headline outputs (Total CO2e, Industrial Fuel Use,
   GDP, electricity demand) old vs. new BAU; drift should be small and explainable by
   the re-partition; investigate anything structural.
3. **Policy response smoke tests**: electrification lever on one band; clean heat ITC/PTC
   (now 5 bands); efficiency stds — confirm sensible signs/magnitudes and that FoPITY
   schedules land on the right elements (spot-check `Selected Policy Implementation
   Schedule` rows in a VDF2TAB extract — the classic symptom of a mis-ordered
   FoPITY file is a policy silently ramping the wrong process).
4. Re-run an updated `US_ClimateAmbition.cin` and sanity-check against published results.

## 6. Downstream coordination

- **EPS.mdl is shared across all geographies** — every geography's InputData needs the
  same restructure; sequence with the core-version release (model team).
- Web app: FoPITY-*-WebApp files, WebAppData.xlsx, lever surface and labels.
- EPS online documentation (industry sector pages, lever descriptions).
