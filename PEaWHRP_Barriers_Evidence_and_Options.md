# Why cheap efficiency upgrades don't deploy — evidence and design options

**Draft for staff review — 2026-07-27.** Written after testing the new waste-heat / process-efficiency measure structure in the US EPS. Citations were checked against sources in this session, but several items still need a direct primary-source read before anything here goes into published material (flagged below).

## 1. What the model does today, and what we saw

The new measure structure uses a "flip" rule: an upgrade deploys on its own economics only if a policy changes it from unprofitable to profitable at the firm's decision rate (WACC + 7 points, ~11–13%). Upgrades that are *already* profitable at baseline prices are treated as blocked by non-price barriers, reachable only through the standards lever.

Testing with a $300/ton carbon tax on industry:

- The tax is a big signal — it raises the value of saved fuel roughly **3.7–3.8× by 2050** (median across industries).
- But most measures are already a good deal without it: the median measure costs ~$1.7 per MMBtu saved against baseline fuel worth $4–6.
- So **87% of waste-heat potential (178 of 205 tranches) and 70% of efficiency potential (222 of 315) is "already profitable → blocked"**; the tax recruits only the ~13–30% sitting near the profitability line.
- The subsidy lever hits the same wall: it can only reach the same near-the-line band.

Question: is that the right behavior, and if not, what should replace it?

## 2. What the evidence says

**Factories really do leave ~half of short-payback upgrades on the table.** Anderson & Newell analyzed the DOE Industrial Assessment Center audit database: plants adopted **53% (mean) of recommended projects**, the projects they did adopt had an average payback of **1.29 years**, and the adoption pattern implies firms act as if they need **50–100% annual returns** ([Anderson & Newell 2004, *Resource and Energy Economics*](https://doi.org/10.1016/S0928-7655(03)00048-4); [free RFF version](https://media.rff.org/documents/RFF-DP-02-58.pdf)). The program's own current statistics agree: **49.8% implementation across 169,430 recommendations, 1985–2024** ([DOE ITAC implementation rates](https://itac.university/implementation-rates)).

**Engineering estimates overstate what shows up on the meter.** The randomized evaluation of the federal Weatherization Assistance Program found **projected savings were ~2.5× realized savings** ([Fowlie, Greenstone & Wolfram 2018, *QJE*](https://academic.oup.com/qje/article-abstract/133/3/1597/4828342); [NBER WP 21331](https://www.nber.org/papers/w21331)). Residential context, but it's the cleanest test of engineering-model bias — and our measure data are engineering estimates.

**Subsidizing already-profitable upgrades pays a lot of people who would have acted anyway.** In a large Mexican appliance-replacement program, **43–54% of participants were non-additional** program-wide, roughly doubling the cost per unit of energy actually saved; at some subsidy thresholds the share was 69–84% ([Boomhower & Davis 2014, *J. Public Economics*](https://doi.org/10.1016/j.jpubeco.2014.04.002); [free copy](https://faculty.haas.berkeley.edu/ldavis/Boomhower%20and%20Davis%20JPubEc%202014.pdf)). *Correction to earlier drafts: "about half" is the right program-wide framing, not "most."*

**Waste heat specifically has been a known, stable, unharvested resource for decades.** DOE's assessment: **20–50% of industrial energy input is lost as waste heat; 5–13 quadrillion BTU/yr unrecovered** out of ~32 quads of industrial use ([DOE/BCS 2008](https://www1.eere.energy.gov/manufacturing/intensiveprocesses/pdfs/waste_heat_recovery.pdf)). Meanwhile US industrial gas prices swung from ~$4.45/Mcf (2000) to **$9.65 (2008)** down to $3.32 (2020) and back to $7.69 (2022) ([EIA industrial gas price series](https://www.eia.gov/dnav/ng/hist/n3035us3A.htm)) — price roughly doubled and halved twice without clearing the backlog. Europe's 2022 shock was far larger (the IEA put 2022 average TTF at several times the pre-crisis norm; single-day peaks ~15× — *exact multiple still to be confirmed against the [IEA Gas Market Report Q3-2022](https://www.iea.org/reports/gas-market-report-q3-2022)*) and still produced acceleration, not clearance.

The umbrella literature for all of this is the "energy-efficiency gap" ([Gerarden, Newell & Stavins 2017, *JEL*](https://www.aeaweb.org/articles?id=10.1257/jel.20161360); [Jaffe & Stavins 1994, *Energy Policy*](https://doi.org/10.1016/0301-4215(94)90138-4)).

**Bottom line:** the model's *level* — most of this stock doesn't move on price — is what history shows. The model's *shape* — literally zero price response for the blocked stock — is a simplification; reality shows small-but-nonzero movement when prices jump.

**Data caveat that matters as much as the mechanism:** the 87% blocked share leans on assumed costs. Most waste-heat rows are "Bianchi fill" potentials at an assumed ~$10/MMBtu-yr capital cost (≈$1.5/MMBtu levelized — always under fuel value, hence always blocked). If real costs are 3–4× higher, a meaningful chunk migrates into the price-responsive band. A sensitivity run with fill costs doubled should precede any strong conclusion.

## 3. Design options

The binding constraint on all options: **with no policies set, the model must deploy nothing**, because baseline efficiency progress is already in the BIEEI input data. Double-counting is the failure mode.

| Option | Idea | Price/subsidy response | Verdict |
|---|---|---|---|
| **A. Flip rule (current)** | Barriers absolute for profitable measures | Zero for blocked stock; thin band only | Right level, crude shape; subsidy lever nearly inert |
| **B. Very high hurdle rate (50–100%)** | Firms act as if money is very expensive | Small after calibration — the rate high enough to explain non-adoption also mutes policy response | **Rejected.** Two problems: the calibration trap, and — decisively — *no hurdle rate can block a free measure*. Our data has 25 zero/negative-cost tranches; a pure-hurdle design deploys them in the baseline, which double-counts. It still needs a screen. |
| **C. Shock-size ramp (recommended)** | Wall stays at baseline prices, but erodes in proportion to the price signal: value X% above baseline unlocks ~0.2·X% of the blocked stock (dial adjustable) | Continuous; zero at baseline by construction; subsidy lever becomes active | One new input constant + edits to two equations. Dial anchored on the 2005–08 gas doubling (modest observed acceleration → sensitivity ~0.1–0.3). With sensitivity = 0 it reproduces today's screen exactly. |
| **D. Barrier-removal lever** | Model audits/energy-management programs (Better Plants, ISO 50001, EU mandatory audits) as a lever that unlocks blocked stock at a program cost | Unchanged; adds a third instrument between standards and prices | Conceptually most honest — non-price barrier, non-price instrument. Filed as v2: another lever, another FoPITY block, needs program-cost data. |
| **E. Diffusion / S-curve dynamics** | Adoption spreads by imitation | Rich but parameter-heavy | Too heavy for EPS's industry resolution. |

## 4. Recommendation

Keep the wall at baseline prices; add option C's ramp with a default sensitivity of zero (behavior identical to today until the dial is turned). Then:

1. Turn the dial in test runs and re-examine the $300/ton picture before choosing a default.
2. Run the Bianchi-fill cost sensitivity (double the assumed capex) to see how much of "87% blocked" is assumption.
3. Add the two transparency outputs (share of potential that is price-addressable vs. standards-only, per industry) regardless of the mechanism chosen.
4. Keep option D on the shelf as a possible future lever.

Open items before publication: confirm the Houde & Aldy free-rider figure (not verified), the exact IEA TTF multiple, and pre-2000 EIA gas prices; decide which of the two 1994 Jaffe & Stavins papers to cite. All staff-review, per usual practice.
