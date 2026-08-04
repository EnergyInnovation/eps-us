# Prompt for Claude in Excel — add the BAU-deployment column to the PEaWHRP workbook

Open `InputData/indst/PEaWHRP/Process Efficiency and Waste Heat Recovery Parameters.xlsx`
and paste everything below the line into Claude in Excel.

Context for Dan (not part of the prompt): the two CSVs already carry this column with US
zeros, and `EPS.mdl` already reads it. This task makes the workbook — the traceable source —
match. After it's done, re-exporting the two tabs through `InputData/CSV Export Tool.xlsm`
should reproduce the committed CSVs bit-for-bit; if it doesn't, don't overwrite them, tell me.

---

I need to add one new column to two export tabs in this workbook, plus a documentation
entry on the About tab. Please make only these changes and nothing else.

## 1. Tab `PEaWHRP-WMD` (waste heat measures)

Data currently occupies A1:K176 — row 1 is the header, rows 2–176 are the 175 measure rows.

- In **L1**, enter the header text exactly: `BAU deployed share of potential by end year`
- In **L2:L176**, enter the value `0` in every cell.
- Set the number format of **L2:L176** to `0.000E+00`, matching columns E through H.
- Match L1's font/fill/border styling to the existing header cells A1:K1.

## 2. Tab `PEaWHRP-PMD` (process efficiency measures)

Same change. Data occupies A1:K426 — row 1 header, rows 2–426 are the 425 measure rows.

- **L1**: `BAU deployed share of potential by end year`
- **L2:L426**: `0`, formatted `0.000E+00`, header styled to match A1:K1.

## 3. Critical formatting constraints

- **Do not add anything below the last data row** on either tab (no totals, no notes, no
  stray formatting). The model reads these tabs as exported CSVs, and any populated cell
  below the data block makes Vensim read a `-3.5697E+35` sentinel value.
- **Do not use a percent number format** on the new column. It must export as `0.000E+00`,
  not as a `%` string.
- Leave columns A–K completely untouched, including the formulas in column K.

## 4. Tab `About` — document the new column

Add a new entry in the existing house style (bold title line, then the description; match
the formatting of the entries already there). Suggested wording:

> **BAU deployed share of potential by end year (column L of PEaWHRP-WMD and PEaWHRP-PMD)**
>
> The share of each measure's potential — as loaded in this file — that the business-as-usual
> case is assumed to reach by the final year of the model run, without any new policy. The
> model ramps this linearly from zero in the start year to the value given here in the final
> year, using the model's own start and end years, so the ramp adapts to each geography's run
> period. It caps both the economic and the standards deployment channels, so policy is only
> credited with deployment beyond what the baseline delivers on its own.
>
> Set to zero for every row in the United States, where no current policy is expected to
> drive material deployment of these measures.
>
> This column is intended for geographies whose baseline includes efficiency policy — for
> example the EU, where the Energy Efficiency Directive and related measures drive adoption
> in the reference case. Note that it should capture only the **non-price** share of baseline
> policy. Price-based baseline policy such as the EU Emissions Trading System is already
> reflected in the BAU energy prices the model uses to compute each measure's business-as-usual
> payback, so including it here as well would count it twice.
>
> The values are not available from Kermeli et al. (2022). That paper's implementation rates
> describe how far adoption goes under an ambitious efficiency scenario, and its reference
> case does not model measures individually. Values for a non-US geography therefore need to
> come from that region's own baseline projection (for example the EU Reference Scenario or
> PRIMES) or from a documented judgment, and the source should be recorded here when set.

## 5. When finished

Save the workbook as .xlsx in place. Tell me which cells you changed and confirm that
nothing was added below row 176 on PEaWHRP-WMD or below row 426 on PEaWHRP-PMD.
