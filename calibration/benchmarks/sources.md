# Benchmark provenance

- `vehicle-technology-shares.csv` (2026-09-21): seeded from the legacy
  `InputData/trans/TTS/calibration/calibration_parameters.csv` (`share_obs`, 2024 and 2025, LDVs and
  HDVs × passenger/freight). Original sources are documented in the legacy
  `calibration_parameters.xlsx`; carry them here when that folder is retired.
- `vehicle-sales.csv`: not yet present. Planned source: EI MarkLines export (LDVs, HDVs by year).

## Electricity benchmarks (EIA), pulled 2026-09-21

All figures below were pulled directly from EIA-published Excel/HTML tables (not
secondary summaries) on 2026-09-21. Every number in `elec-generation.csv` and
`elec-capacity.csv` traces to one of the tables listed here; the `table` column
in each CSV repeats the specific table used per row. Verify against the live
EIA pages before use in any deliverable — table contents can be revised on a
rolling basis (EIA flags 2025 as preliminary throughout).

**Note on edition:** as of the pull date, EIA's *current* Electric Power Monthly
edition is dated August 26, 2026 (carries data through June 2026). This edition's
Table 1.1 / 1.1.A already contain a full calendar-year-2025 annual row (marked
preliminary by EIA), so the originally-suggested "Feb 2026 edition" was not
needed for generation data — the live edition is more current and already has
full-year 2025. A February 20, 2026 edition PDF archive does exist
(`https://www.eia.gov/electricity/monthly/archive/february2026.pdf`, 18 MB) if
a colleague wants to cross-check the earlier-vintage December 2025 estimates,
but it was not parsed here (PDF table extraction, not the primary route used).

### Generation — `elec-generation.csv`

- **EPM Table 1.1**, "Net Generation by Energy Source: Total (All Sectors),
  2016–June 2026" — `https://www.eia.gov/electricity/monthly/xls/table_1_01.xlsx`
  — edition Aug 26, 2026. Coal, natural gas, nuclear, hydro (conventional),
  petroleum (liquids + coke), pumped storage, and both utility-scale and
  small-scale-solar-augmented totals. **2025 annual values are preliminary**
  per EIA's note on the table; 2024 and prior are final.
- **EPM Table 1.1.A**, "Net Generation from Renewable Sources: Total (All
  Sectors), 2016–June 2026" — `https://www.eia.gov/electricity/monthly/xls/table_1_01_a.xlsx`
  — edition Aug 26, 2026. Wind, solar PV (utility + small-scale estimate),
  solar thermal, wood, landfill gas, biogenic MSW, other waste biomass,
  geothermal. **2025 preliminary.**
- **EPM Table 5.1**, "Sales of Electricity to Ultimate Customers: Total by
  End-Use Sector, 2016–June 2026" — `https://www.eia.gov/electricity/monthly/xls/table_5_01.xlsx`
  — edition Aug 26, 2026. All-sectors retail sales annual total. **2025
  preliminary.**
- **EPM Table 7.1**, "Electric Power Industry – U.S. Electricity Imports from
  and Electricity Exports to Canada and Mexico (Megawatthours)" —
  `https://www.eia.gov/electricity/monthly/xls/table_7_01.xlsx` — edition
  Aug 26, 2026. Net imports = imports − exports, annual. Values in the raw
  table are MWh; converted to GWh (÷1000) for the CSV. **2025 preliminary.**
- **Wholesale price:** EIA does not publish a single national annual-average
  wholesale electricity price. Its "Wholesale Electricity Market Data" / Grid
  Monitor resources (`https://www.eia.gov/electricity/wholesalemarkets/`)
  report day-ahead prices per regional trading hub, not a national annual
  average comparable to the retail-price table. Recorded as `NA` in the CSV
  with that explanation in `eia_category`. If a wholesale figure is genuinely
  needed, the next-best primary route is averaging EIA's published hub series
  yourself and documenting the weighting — not done here.

### Capacity — `elec-capacity.csv`

- **EPM Table 6.2.A**, "Net Summer Capacity of Utility Scale Units by
  Technology and by State, June 2026 and 2025" —
  `https://www.eia.gov/electricity/monthly/xls/table_6_02_a.xlsx` — edition
  Aug 26, 2026, U.S. Total row. Renewable/fossil/pumped-storage/nuclear/
  all-sources aggregates, **June 2025** snapshot (point-in-time, sourced by
  EIA from Form EIA-860 + EIA-860M; EIA labels values preliminary).
- **EPM Table 6.2.B**, "Net Summer Capacity Using Primarily Renewable Energy
  Sources and by State, June 2026 and 2025" —
  `https://www.eia.gov/electricity/monthly/xls/table_6_02_b.xlsx` — same
  edition, U.S. Total row. Wind, solar PV (utility + small-scale), solar
  thermal, hydro, biomass, geothermal, **June 2025**.
- **EPM Table 6.2.C**, "Net Summer Capacity of Utility Scale Units Using
  Primarily Fossil Fuels and by State, June 2026 and 2025" —
  `https://www.eia.gov/electricity/monthly/xls/table_6_02_c.xlsx` — same
  edition, U.S. Total row. Splits natural gas into Combined Cycle,
  Combustion Turbine (peaker), and "Other Natural Gas" (steam turbine +
  internal combustion combined — EIA does not split these two further in
  this table); also coal, petroleum coke, petroleum liquids. **June 2025**.
- **Electric Power Annual (EPA) Table 4.3**, "Existing Capacity by Energy
  Source, 2024" — `https://www.eia.gov/electricity/annual/html/epa_04_03.html`
  — **final, year-end December 31, 2024** figures (EIA-860 annual survey, not
  preliminary). Used for all 2024 capacity rows. Does not split natural gas
  by prime mover.

**Important caveat on capacity vintage mismatch:** 2025 capacity comes from a
mid-year (June 2025) EPM snapshot because EIA has not yet published final
year-end-2025 capacity — that will appear in Electric Power Annual 2025,
expected roughly October 2026. 2024 capacity comes from the already-final,
year-end (Dec 31, 2024) Electric Power Annual Table 4.3. The two years are
therefore not perfectly apples-to-apples in timing (mid-year 2025 vs.
year-end 2024), though both are "net summer capacity" in MW. Note this before
using the 2024→2025 capacity columns for a growth-rate calculation — the
implied change spans about 18 months, not 12.

**Natural gas prime-mover split for generation:** not attempted. EIA's
published Electric Power Monthly tables report U.S. total natural gas
generation as a single series (Table 1.1); a generation-by-prime-mover split
would require aggregating unit-level EIA-923 generator data, which was out of
scope for this pull. The capacity tables (6.2.C) do split by prime mover and
are used for `elec-capacity.csv`.

## Vehicle sales (MarkLines), rebuilt 2026-09-21 PM (scope per the SYVbT workbook)
- EPS scope (SYVbT About tab): freight LDVs = AEO commercial light trucks + light-medium + medium duty;
  freight HDVs = AEO heavy duty only. So the LDV benchmark = MarkLines Cars + Light Trucks (class 1-2b)
  + Medium Trucks (class 4-7); Heavy Trucks (class 8) are the HDV scope and are NOT in this file because
  no cohort history exists before 2020 (AEO 2026 heavy-truck sales 288k in 2025 vs model 278k - close).
- `vehicle-sales.csv`, US: 2020-2025 from the model-level files (`raw\`, rolling file wins on overlap,
  12 months each). 2004-2019 from the Customized Aggregation pivot (`history\history_long.csv`, no Type
  field): total minus the class-8 share of the "Unclassified" segment (measured 2020-25), medium trucks
  estimated at 1.35% of the remainder (2020-25 ratio). Pre-2020 values are therefore estimates.
- **Passenger/freight split is an assumption:** MarkLines has no cargo-type dimension, so LDV totals
  are split by the model's start-year freight share (9.3%, `runs/base4.tab`), constant across years.
- Scope check vs AEO 2026 (Alternative Electricity & Transportation case, in the model's NBPoNVP
  workbook): AEO Table 38 = cars + light trucks under 8,500 lb (15.0 M in 2025); MarkLines light
  vehicles 16.3 M; the ~1.3 M difference is class 2b, which AEO carries as commercial light trucks.
- `vehicle-sales-projection.csv` (rebuilt 2026-09-21, final): **AEO 2026 Alternative Electricity and
  Transportation case** - the case the US model is built on (Robbie, 2026-09-21: use it, not the central
  case, going forward) - from the Table 38 tab in the NBPoNVP workbook and the Table 49 tab in the
  BAADTbVT workbook. Value = Table 38 Total Vehicles Sales (< 8,501 lb) + Table 49 light-medium (class 3)
  + medium (class 4-6) new-truck sales. Class 2b commercial light trucks have no AEO sales series, so the
  benchmark is ~0.4 M below the EPS LDV scope. `aeo2026-reference-ldv.csv` (central case, pulled from
  EIA supplemental tables) is kept only for the cross-check; central and side case agree on 2025 sales.

## Official-statistics cross-check (FRED / BEA), 2026-09-21
- `fred_ALTSALES.csv` (light-weight vehicle sales, class 1-3, millions SAAR, monthly), `fred_HTRUCKSSA.csv`
  (heavy-weight trucks, class 4-8, thousands/month SA), `fred_LAUTOSA.csv`, `fred_LTRUCKSA.csv` - pulled
  from https://fred.stlouisfed.org/graph/fredgraph.csv?id=<series> on 2026-09-21 (BEA source data).
- MarkLines (EPS LDV scope) vs BEA light vehicles: +1.0% to +2.6% every year 2004-2025 (the excess is
  the medium trucks we add for the EPS scope). MarkLines medium+heavy vs BEA heavy trucks: within
  ~5% 2020-25. AEO Table 38 sits ~1.1 M below BEA in 2024-25 because it stops at 8,500 lb.
