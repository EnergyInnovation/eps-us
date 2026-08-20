# Phase 1b carve-out: wiring design (2026-08-20 evening block)

*How the steel pathway module takes ownership of iron & steel 241's process energy. Implements D4/D9/D13/D14. For Dan's review — implementation proceeds in this block; flag anything wrong and it reverts cheaply.*

## The two splice points

The generic industry structure computes energy in `[Industry Category, Industrial Fuel, Industrial Process]` space, then applies WHR and process-efficiency multipliers, then sums over processes into fuel use:

```
(policy)  Industrial Equipment Energy Use by Fuel Type and Process before Waste Heat Recovery   ← SPLICE 1
             × WHR Measure Energy Use Multiplier            (heating bands)
             × Efficiency Measure Energy Use Multiplier     (process improvements)
          → Industrial Fuel Use for Energy before CCS...  → for Energy Purposes → emissions, costs, elec demand

(BAU)     BAU Industrial Energy Use by Fuel Type and Process (BIFUfE data × BPFUbIP shares)      ← SPLICE 2
          → BAU Industrial Fuel Use for Energy...
```

**Splice 1 (policy):** replace `...before Waste Heat Recovery[iron and steel 241, Industrial Fuel, industrial process end use]` with module energy mapped into processes. Because the splice sits *upstream* of the WHR and efficiency-measure multipliers, **WHR and process-efficiency levers keep acting on steel automatically** — D14's porting requirement is satisfied by the choice of splice point, no re-plumbing. Nonprocess end uses keep the generic equation (the D4 subrange boundary). Mechanically: the existing equation's two `:EXCEPT:` branches each get a steel exclusion, plus one new steel branch.

**Splice 2 (BAU):** the BAU side is *data-driven* (BIFUfE), not stock-computed — so the module's BAU twin chain replaces `BAU Industrial Energy Use by Fuel Type and Process[241, *, process end use]` the same way. This is exactly D13's inventory refresh: steel's BAU energy stops being the (stale) BIFU series for process end uses and becomes tonnage × calibrated intensities. At defaults the policy and BAU module chains see identical inputs, so Change-in variables for steel stay ≈ 0 by construction.

## Fuel→process mapping (no new input needed)

`Steel Energy Use Process Shares[Industrial Fuel, industrial process end use]` = INITIAL share of each fuel across process end uses from the existing BAU apportionment (`BAU Industrial Energy Use by Fuel Type and Process`, which embeds BPFUbIP). The module's energy-by-fuel is spread across process bands exactly as the model already believes steel's fuel use is distributed — so WHR (heating bands) and any band-specific logic see sensible energy. Phase 2's coke chain can later assign coke/coal physically to `heat above 1000 C`.

## Feedstock (D9)

Coking coal sits in `BIFUaF` (feedstock), not energy. 1b treatment: the module's coal intensity represents *total* coal (energy + feedstock); a computed start-year ratio (`INITIAL` of BIFUaF/(BIFUfE+BIFUaF) for 241 coal) splits module coal between the energy chain and the nonenergy/feedstock chain, both spliced. Accounting-neutral at start year; Phase 2's coke chain replaces the ratio with physical coke/PCI flows and endogenizes the process CO2.

## Calibration (D13)

`SEIbPaF` keeps its literature-based *pathway ratios* but gets level-scaled per fuel so that start-year pathway-weighted intensity × start-year production reproduces the calibration target for 241's process-end-use energy by fuel (energy + feedstock for coal). Target hierarchy: MECS/GHGRP-refreshed inventory numbers (agent pull in flight) where they arrive in time; otherwise the model's BIFU-based 2025 values as interim with the inventory swap flagged. Implied intensity changes vs literature (esp. NG, which carries finishing/reheat energy under full ownership) get documented in the SEIbPaF workbook.

## Deliberate lever dispositions at 1b (per D14 — dispositions to confirm)

| Lever | 1b behavior on steel process end uses | Note |
|---|---|---|
| WHR measures | **live** (splice upstream of multiplier) | D14: port in ✓ |
| Process-efficiency measures | **live** (same) | D14 ✓ |
| Electrification policy (PIFURfE) | off | pathway choice is the electrification mechanism now |
| Fuel shifting (IFSR incl. IFSR-ironsteel) | off | ditto; `IFSR-ironsteel.csv` retires with steel's generic fuel choice |
| Thermal batteries | off for steel process uses | would double-count vs pathway electrification; revisit if team wants TBs inside steel |
| Clean heat ITC/PTC | off for steel process uses | pathway subsidies arrive in Phase 3 |
| Early retirement of industrial equipment (incl. BIISRP) | off for steel process uses | replaced by SPRS + Phase 2 steel early-retirement lever |
| Energy-intensity standards (BIEEI trajectory) | off | Dan: boiler-style standards don't map onto steel |
| Material efficiency / demand reduction | **live** (acts via `Percent Change in Production due to Policies` → tonnage) | unchanged |
| Carbon tax on fuels | **live** (prices flow into pathway logit fuel costs; direct tax booking via fuel use as today) | Phase 2 adds process-CO2 exposure |
| CCS | unchanged in 1b (existing % capture framework) | Phase 2 reconciles with the BF-BOF+CCS pathway |

Nonprocess end uses (HVAC, lighting, other nonprocess) keep ALL generic levers.

## Known interim inconsistency (documented, resolved in Phase 3)

The generic equipment stock for 241's process end uses keeps computing (its energy is simply no longer consumed), and its **new-equipment capex still books into cash flows**. Until Phase 3 replaces it with pathway capex, steel's equipment spending in the cash-flow layer reflects the vestigial generic structure — roughly the right magnitude, wrong composition. Flagged rather than zeroed, because zeroing now would leave steel with no equipment capex at all.

## Gates for 1b — RESULTS (2026-08-20 evening, implemented and run)

1. **No structural leakage — PASS (reframed).** Strict "only 241 changes" is unattainable with feedbacks live: 344 non-steel fuel-use rows move. But **zero** non-steel changes exist at initialization; max relative delta thereafter is 4.9% (coal mining NG — the energy-industry production feedback responding to steel's lower coal demand), and the channels are all legitimate (electricity demand → dispatch → prices; energy-industry output coupling; macro feedbacks). The carve-out touches only steel cells structurally.
2. **Start-year calibration — PASS.** BAU 2025 fuel use for 241 within ~1.5% of pre-splice values (elec 290.9→294.6 TBtu; coal 37.1→37.7; NG 450.5→457.9; feedstock analogous). The additive/route-specific calibration hit its targets (adders: elec +1.84, NG +4.63 MMBtu/t; coking coal ×1.229 → BF-BOF 18.6 MMBtu/t, corroborated by GEM met-coal ratios).
3. **Defaults twin identity — PASS exactly** (max |policy−BAU|/BAU = 0.000% across steel fuels).
4. **Mechanics run — PASS, with an instructive result.** (US_ClimateAmbition.cin turned out to be broken repo-wide — 286 stale pre-temp-band subscript references, flagged as its own fix task — so the test ran a $300/t industry carbon tax instead.) Costs respond correctly and strongly: BF-BOF $227→$675/t (the coal carbon charge; arithmetic checks against 18.6 MMBtu/t coal), H2-DRI +$56, scrap EAF +$58. Steel demand falls 2.9% through the production chain; H2-DRI production doubles; NG-DRI new builds lose share to scrap EAF. **But 2050 BF-BOF production barely moves (22.4→22.0 Mt)** — with the conservative GEM retirement schedule, almost no BF capacity retires by 2050, and the draft has uniform-ration production with no merit-order dispatch, no cost-based stranding, no CCS pathway economics, and no process-CO2 tax exposure in the choice. A $300 carbon tax therefore strands nothing yet. That is precisely the Phase 2 machinery's job (see `Steel_Phase2_Design_Memo.md` §2, §4, §5) — the draft behaves as designed, and the gap is the designed gap.

**The D13 trajectory refresh, quantified:** the old data-driven steel BAU *grew* NG use 43% by 2050 (451→642 TBtu) and coal energy 35% — while AEO2026 Table 30 shows steel NG roughly flat (+3%) and met coal falling ~2%/yr. The module's BAU lands at NG +6% (458→484) and coal declining (37.7→36.1 energy; feedstock tracks BF-BOF retirement) — far closer to EIA's own outlook. **Consequence: 2050 BAU steel energy and emissions are materially lower than the pre-breakout model**, which will shift headline BAU CO2e. This is the intended inventory/outlook refresh, but it needs team awareness before merging.
