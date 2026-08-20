# Steel breakout — research notes (2026-08-20)

*Condensed from three research syntheses (web-search based). **Every value here is snippet-sourced and must be verified against its primary source before entering a release input workbook.** These notes exist so the Phase 4 workbook builds can trace each DRAFT placeholder. Known fetch failures: USGS MCS PDFs (403), EIA AEO2025 Table 30 (table browser), DOE Liftoff industrial-decarb PDF, IEA Iron & Steel Roadmap, MPP strategy, GEI Steel Climate Impact 2025 — all identified as the right primary sources but not read directly; pull manually.*

## 1. US production / capacity / trade / scrap (→ BSD, SYSPbP, MASSfS)

| Parameter | Central value | Source anchor |
|---|---|---|
| Crude steel production 2023–25 | ~80 Mt (metric) ≈ 88–90 M net tons/yr | AISI ASR 2023/2024/2025 (steel.org); worldsteel WSIF 2025; USGS MCS |
| Route split | EAF ~70% / BF-BOF ~30% (2024) | Recycling Today (71.8% EAF); Global Energy Monitor |
| Ore-based EAF feed | ~4.4 Mt/yr nameplate DRI/HBI (Cliffs Toledo 1.9 + Nucor Louisiana 2.5) | company pages/SEC filings; pig-iron imports not yet sourced |
| Capability / utilization | 117.8 M net tons (AISI, Jul 2025); 75–77% utilization 2024–25 | AISI weekly AIS-7 via Steel Market Update |
| Trade | imports ~28, exports ~8–9, net ~19–20 M net tons/yr (2024) | AISI/Census IMP2412; trade.gov exports report |
| Scrap | apparent consumption 63 Mt (2024): ~58% obsolete / 24% prompt / 18% home; exports 14.9 Mt (world's largest exporter, declining ~8%/yr) | USGS MCS iron-and-steel-scrap (PDF 403'd — verify); MEPS |
| Scrap to 2050 | global EOL scrap ~doubles to ~900 Mt; US-specific forward estimate NOT found — flagged gap | JISF/worldsteel via gmk.center, AIST |
| BAU production to 2050 | no authoritative figure retrieved; placeholder flat 80 Mt. AEO2025 added H2-DRI to its steel module — anchor BSD to AEO Table 30 when pulled | EIA AEO2025 narrative/IDM assumptions |

Known snippet error caught: AISI 2021/2022 figures (94.6/94.7 M net tons) contradict AISI's own −6.2% claim — verify in the ASR PDFs.

## 2. Pathway techno-economics (→ SEIbPaF, SPCC, SPPL, SPSW gating)

| Pathway | Capex $/(t/yr) | Energy (per t crude steel) | Direct CO2 t/t | Life | Readiness |
|---|---|---|---|---|---|
| BF-BOF | ~1,200 (700–2,000, boundary-sensitive) | coke 13–18 GJ (300–600 kg coke/t HM); NG ~1–2 GJ; elec 300–400 kWh | 2.1–2.2 (coke ovens alone ~0.71) | BF campaign 15–20 yr (median 1st 19, reline ~10.5) | mature |
| BF-BOF + CCS | +150–600 (my back-calc from $100–300/tCO2 × 1.5–2 t captured — weak) | + capture parasitic load (UNQUANTIFIED — real gap) | ~0.9–1.1 residual at 50–60% plant-wide capture | as BF-BOF | zero commercial plants; BF-integration TRL 6–7 |
| NG DRI + EAF | ~700 (600–800) | NG 10–11 GJ/t DRI (Midrex 258–270 Nm³); elec ~600–800 kWh total | 0.7–1.2 | ~20–25 yr | mature (Midrex/HYL) |
| H2 DRI + EAF | ~1,000–1,100 (DIW DP2082: €600–1,000 DRI+EAF + €250 electrolysis — fetch failed) | H2 52–58 kg/t (Vogl et al. 2018 JCP 203 — READ THE PAPER: their 3.48 MWh/t elec figure may or may not include EAF melt, a 2× ambiguity); elec ~600–800 kWh ex-electrolyzer | <0.1–0.4 | ~25 yr | Stegra Boden startup mid-2026 (2.5 Mtpa); HYBRIT pilot; **Cliffs Middletown DOE award cancelled 2025, plant continues on coal** |
| Scrap EAF | ~500 (400–600) | elec 400–500 kWh; NG ~0.3–0.5 GJ | ~0.06–0.1 direct | ~20–25 yr | mature |
| MOE (Boston Metal) | ~1,000 (single 2019 company estimate) | ~4 MWh/t | ~0 direct | unknown | TRL ~4–6; 2026 10kt/y plant is critical-metals, NOT steel; commercial steel = analyst-speculated early/mid-2030s |
| Aqueous electrolysis (Electra) | unknown (generic electrowinning ~3,000 — NOT Electra-specific) | ~3 MWh/t (110 °C process) | ~0 direct | unknown | TRL ~5–6; 500 t/y demo mid-2026; company targets commercial 2029 |

Coke: met-coal-to-coke ratio 1.3:1 vs 1.6:1 across sources — unresolved. Grid-dependence caveat: pathways 4–7's near-zero CO2 is direct-only; indirect follows the model's electricity treatment automatically once wired.

## 3. GEM plant-level BF fleet (→ SPRS)

Access: GIST bulk file registration-gated (contact Astrid Grigsby-Schulte, GEM; June 2026 V1 release; CC BY 4.0). Country-aggregate JSON at gist-dashboard-*.herokuapp.com is fetchable but has no plant rows. Furnace-level detail is public on gem.wiki per plant — Gary Works page spot-verified 2026-08-20.

Operating fleet ≈24.6 Mt/yr hot metal (8 plants, 13 operating BFs) + ~9.5 Mt mothballed (Granite City A, Indiana Harbor #3/#4, Dearborn C3):

| Plant | Operating BFs (Mt) | Retirement/reline intelligence |
|---|---|---|
| Gary Works | 14/4/6/8 (6.5) | BF14 $350M full reline Dec 2025 (+~20 yr); others relined 2016–2020 |
| Edgar Thomson | 1, 3 (2.8) | Nippon 10-yr full-capacity pledge; BF3 relined 2001 — overdue, unannounced |
| Granite City | B (1.3) | restarted Mar 2026; closure protection expires June 2027 |
| Indiana Harbor | 7 (4.2) | relined 2021; H2-injection trial done, pipeline underway |
| Burns Harbor | C, D (5.0) | relined 2007/2008 — both at decision point; CCS feasibility Phase 1 done |
| Cleveland | 5, 6 (2.8) | BF5 relined 2022; BF6 (2013) flagged end-of-life, plans unannounced |
| Middletown | 3 (2.1) | DOE H2-DRI award cancelled; coal BF refurb + ~70 MW BF-gas cogen (Ohio EPA permit Feb 2026) |

DRAFT SPRS judgment (documented in `make_steel_csvs.py`): retire Granite City B (2028), Edgar Thomson BF3 (2029), Cleveland BF6 (2030), Burns Harbor C (2032), Gary BF14 (2046), Burns Harbor D (2049) ≈ 11.4 Mt by 2050; committed/recently-relined units continue. NG DRI: Nucor Louisiana share out 2043–44. All assumption-laden — replace with GIST bulk data.
