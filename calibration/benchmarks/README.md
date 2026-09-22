# Benchmarks

Observed data the calibration steps compare against or solve toward. Each file is a plain CSV so
any region can drop in its own; the steps never query a subscription service directly.

| file | used by | columns | notes |
|---|---|---|---|
| `vehicle-sales.csv` | step 1 | `country,year,vehicle_type,cargo_type,units` | `vehicle_type` / `cargo_type` use the model's subscript element names (`LDVs`, `HDVs`, `aircraft`, `rail`, `ships`, `motorbikes`; `passenger`, `freight`). Needed back to IT−L per group for the ANVCV cohorts (e.g. 2008 for passenger LDVs at L=17). Source for LDV/HDV: EI's MarkLines export (values pasted, source noted in `sources.md`). |
| `vehicle-technology-shares.csv` | step 3 | `country,year,vehicle_type,cargo_type,technology,share` | Observed share of new sales by technology within each vehicle type × cargo type, per year; shares in a group-year should sum to 1 (they are renormalised if not). Years ≥ IT are solved with that year's modelled costs; years before IT copy the IT weights. |

Missing rows are allowed: a group with no sales history takes the step-free share only, and the
step prints a prompt to research a source before accepting that.

Record the provenance of every file in `sources.md` next to it (dataset, edition, date pulled).
