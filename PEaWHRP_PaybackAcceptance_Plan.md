# Implementation plan: payback-acceptance curve for measure deployment

**2026-07-31 · Status: PLAN — awaiting Dan's approval to implement.**
Approved direction (Dan): replace PSUS with an empirically anchored payback-acceptance curve; **delete the MHRP hurdle premium** (barriers move wholly into the curve; keeping both double-counts).
Companion: `PEaWHRP_PaybackAcceptance_Proposal.md` (rationale, literature anchors). Literature corroboration in §8 (two research agents in flight at time of writing; results to be appended).

## 1. Design in one paragraph

One exogenous survivor curve per measure set, S(p) = share of firms that accept a simple payback of p years. Each tranche computes its payback at policy prices and at BAU prices; the deployment ceiling is the newly-unlocked share of the remaining (non-adopting-at-BAU) firms: `MAX(0, (S(p_policy) − S(p_BAU)) / (1 − S(p_BAU)))`. Measures not cost-effective at BAU have p_BAU beyond the curve (S≈0), so both current regimes collapse into this one continuous rule. Everything downstream — 20%/yr start rate, retirement backfill, standards floor, cost levels, availability index — is untouched.

## 2. New input file

`InputData/indst/PEaWHRP/PEaWHRP-PAC.csv` — read via `GET DIRECT LOOKUPS` (CECRCbI precedent), one row per `Measure Set`, columns = payback grid (years):

```
share of firms accepting simple payback (yr),0,0.25,0.5,0.75,1,1.25,1.5,2,2.5,3,4,5,6,8,10
waste heat measures,0.85,0.75,0.65,0.57,0.50,0.44,0.38,0.27,0.19,0.13,0.06,0.035,0.02,0.008,0.003
process efficiency measures,0.85,0.75,0.65,0.57,0.50,0.44,0.38,0.27,0.19,0.13,0.06,0.035,0.02,0.008,0.003
```

- Rows identical at launch (one behavioral curve); the Measure Set dimension gives per-set adjustment for free if evidence later argues WHR integration projects face higher hidden costs.
- Anchors: S(1.25–1.5) ≈ 0.38–0.44 and ~50% overall rejection (Anderson & Newell 2004: threshold "15 months or less… 80% or greater hurdle rate"; "plants reject about half"); S(1.3) consistent with IAC VFD adoption 20–40% at ~15-month paybacks; shape ≈ lognormal(median 1 yr, σ 0.9); S(0)=0.85 (even instant payback sees incomplete adoption). **All values Dan-adjustable; §8 may tighten them.**
- Vensim lookups clamp flat beyond both endpoints (S(>10) = 0.003, S(<0) n/a).

## 3. EPS.mdl changes

**ADD (5 + lookup):**

```
PAC Payback Acceptance Curve[Measure Set](            GET DIRECT LOOKUPS('InputData/indst/PEaWHRP/PEaWHRP-PAC.csv', ',', '1', 'B2') )
    ~ Dmnl ~ Share of firms whose investment threshold accepts a given simple
    payback (years, dimensionless in the lookup).  Anchored on audited-plant
    adoption data; see PEaWHRP_PaybackAcceptance_Plan.md. |

Waste Heat Measure Simple Payback Period[Industry Category, Waste Heat Measure, Measure Cost Level] =
    IF THEN ELSE( Value of WHM Energy Savings − MCLM[cl] × WHMOC <= 0, 10,
      MIN(10, ZIDZ( MCLM[cl] × WHMCC, Value of WHM Energy Savings − MCLM[cl] × WHMOC )))
    ~ Dmnl ~ Simple payback in years at policy-inclusive value (subsidy shortens
    payback).  Capped at the curve's 10-year endpoint, where acceptance ≈ 0. |

Waste Heat Measure Simple Payback Period at BAU Prices[...] = (same with WHM Value at BAU Prices, no subsidy)
    + the two PEM twins
```

Zero-capex measures: payback = 0 when opex leaves positive value → S(0) = 0.85 ceiling; if opex alone exceeds value → 10 yr → ~0. Both sensible.

**MODIFY (4):**

```
{Waste Heat, Process Efficiency} Measure Tranche Economically Deployable[i,m,cl] =
    IF THEN ELSE( potential <= 0, 0,
      MAX(0,
        ( PAC[set]( p_policy ) − PAC[set]( p_BAU ) )
        / MAX(1e-6, 1 − PAC[set]( p_BAU )) ))
    { keeps its name (it is still the deployment ceiling) — no sketch churn }

{Waste Heat, Process Efficiency} Measure Capital Recovery Factor:  drop MHRP; rate = WACC only.
    { financial LCOS reverts to true cost of capital; LCOS now serves only the
      cost-accounting side — the adoption decision no longer references it }
```

Note: after this change **LCOS no longer gates deployment at all** — payback does. LCOS remains for cash-flow/levelized reporting. The `Levelized Cost of … Energy Savings` variables stay (used in outputs), now MHRP-free.

**DELETE (2 + 2 CSVs):** `MHRP Measure Hurdle Rate Premium` (+ `PEaWHRP-MHRP.csv`), `PSUS Price Signal Unlock Sensitivity` (+ `PEaWHRP-PSUS.csv`). Both CSVs parked as `.retired` until validation passes, then removed.

## 4. Invariant proof obligations

1. **Zero-policy:** with all levers 0, policy prices ≡ BAU prices and subsidy = 0 ⇒ p_policy ≡ p_BAU ⇒ ceiling ≡ 0. Exact, by construction.
2. **Monotone response:** ceiling is nondecreasing in the value of saved energy (S decreasing in p, p decreasing in value).
3. **No regime cliff:** ceiling is continuous through the BAU-cost-effectiveness boundary (p_BAU crossing 10 yr moves S(p_BAU) smoothly to ~0).
4. **Standards unaffected:** floor still composes by MAX in the deployment equation.

## 5. Test plan

**T-py (before any Vensim run):** Python harness replicating payback + ceiling formulas; cases: regime-A measure (p_BAU=10), super-cheap measure (p_BAU=0.3), zero-capex both signs of opex, denominator ≤ 0, subsidy-only unlock, S-endpoint clamps, zero-policy identity.

**Battery (after):**
| Run | Expectation |
|---|---|
| Zero-policy | all invariants (deployment 0, multipliers 1, cash flows 0) — unchanged from MeasBase3 |
| $50/t, $100/t, $300/t industry carbon tax | monotone 3-point response curve; gas-heat tranches now respond visibly at $50 (PSUS gave ~0.05 ceilings); no tranche exceeds ceiling; unjustified-dip count stays 0 |
| 100% standards (iron & steel) | identical to MeasStd3 (standards bypass the ceiling) |
| Comparison table | 2050 deployed fractions and savings vs MeasCTax3 (PSUS) at $300 — expect moderate increase, concentrated in cheap gas-heat tranches; coal-heat tranches roughly unchanged (they unlocked under PSUS too) |

**Acceptance:** all invariants pass; response curve monotone with no cliffs; results explainable tranche-by-tranche via the S curve.

## 6. Rollout sequence

1. Write PEaWHRP-PAC.csv + T-py harness → green.
2. EPS.mdl edits (add/modify/delete per §3) → LOADMODEL-clean.
3. Battery + comparison → report to Dan.
4. Update `PEaWHRP_Sketch_Update_Checklist.md`: remove MHRP + PSUS objects, add PAC + 4 payback variables (suggest placing next to the value/LCOS cluster in the new measures view).
5. Mark `PEaWHRP_ShockRamp_Implementation_Plan.md` superseded (pointer to this doc).
6. Memory + plan-doc status updates. Commit only on Dan's instruction.

## 7. Open defaults for Dan (none blocking)

- Curve values (§2 table) — adjust any time; they're the whole behavioral content.
- S(0) = 0.85 vs 1.0.
- Whether the WHR row should start below the PEM row (PSUS had 0.075 vs 0.10); launched identical.

## 8. Literature corroboration

### 8a. Peer-model precedent (research agent, 2026-07-31 — verify quotes against primary PDFs before citing)

Three major models use a mechanism **functionally identical** to the proposed curve:

| Model | Mechanism | Note |
|---|---|---|
| **FORECAST** (Fraunhofer ISI; Fleiter et al. 2018, Energy Strategy Reviews 22) | "a distribution of payback time expectations is used: With increasing payback time, the share of companies investing decreases" — logistic S-curve of adoption share vs payback, bounded by min/max diffusion | Calibration: ~55% implementation at 3-yr payback (current policy) → ~85% (transformation scenario) |
| **NEMS Industrial Demand Module** (EIA, AEO2025 doc, p.26) | "an assumption about the distribution of required investment payback periods called the **payback acceptance curve**" — `AcceptFrac` lookup, paybacks 0–12 yr, small vs large plants, linearly interpolated | EIA literally names it "payback acceptance curve"; used for CHP economic-potential conversion |
| **PRIMES** (E3Modelling 2018 doc, §V.2 p.203) | "calculates a payback period, which combines with frequency distribution of threshold values reflecting heterogeneity of consumers and installations, to determine likelihood of investment" | Applied to industrial control systems + buildings renovation |

Adjacent precedent (behavioral heterogeneity via logit market share, not threshold distributions): **CIMS** (Rivers & Jaccard 2006 — revealed industrial discount rate example 34.7%), **Invert/EE-Lab**. Contrast case: **UK N-ZIP** uses single deterministic hurdle rates (12/11/10% by tech maturity) — some peers do it the simple way; the distribution approach is the better-established one for adoption realism.

**The actual NEMS AcceptFrac values** (supplied by Dan 2026-07-31, from the NEMS industrial cogeneration input file; small- and large-plant columns identical): 100% at 0–1 yr, 86.2% at 2, 72.9% at 3, 60.1% at 4, 48.1% at 5, 37.1% at 6, 27.2% at 7, 18.7% at 8, 11.6% at 9, 6.2% at 10, 2.4% at 11, 0.3% at 12. **Deliberately NOT adopted here:** it sits far above all revealed-behavior evidence (100% acceptance at 1-yr payback vs the ~50% adoption observed across 89k audited recommendations), because it is an EIA engineering-judgment assumption for CHP — large strategic energy-supply projects — not an estimate of retrofit-measure adoption. Loading it would erase the sub-2-year backlog that constitutes the efficiency gap. Kept as the optimistic bound for sensitivity runs; its fat 4–8-yr tail mildly supports lifting our S(4)/S(6) (0.06/0.02 → ~0.10/0.04) if Dan wants a hedge toward strategic-investor behavior.

**Calibration divergence to resolve (Dan):** FORECAST's ~55% at 3-yr payback is far above the drafted S(3) = 0.13 (from A&N audit data). Plausible reconciliation: FORECAST's number is cumulative implementation over multi-year windows in EU policy context; A&N measures adoption within ~2 years of a US audit. NEMS's actual `AcceptFrac` values (published in the IDM documentation) would be a useful third anchor — worth pulling before finalizing defaults. Drafted curve sits at the conservative/empirical end.

### 8b. Empirical adoption-vs-payback studies (research agent, 2026-07-31 — verify against primary PDFs before citing)

| Source | Population | Key number | Verdict on drafted curve |
|---|---|---|---|
| Anderson & Newell 2004 | ~10k IAC recs | threshold "15 months or less… ≥80% hurdle rate"; half rejected | supports |
| **Muthulingam et al. 2013** (M&SOM) | **89,299 IAC recs, 13k+ US SME plants** | **mean payback 1.06 yr, mean adoption 50.16%**; adoption falls monotonically & convexly in ln(payback) | **near-exact hit on S(1)=0.50** |
| Gerarden, Newell & Stavins 2017 (JEL survey) | literature | reaffirms A&N; industrial hurdle multipliers 1.76–3.6× cost of capital (Diederen NL; Löfgren et al. SE) | supports steep decline past 1–2 yr |
| Fleiter et al. 2012 | German pulp & paper | "a payback time of 2 years is often used as a threshold… while equipment lifetime exceeds 10 years" | supports ~2-yr cutoff, non-US |
| Rohdin, Thollander & Solding 2007 | Swedish foundries | formal criteria 1–3 yr; **>50% of private firms use no formal criterion** | supports shape; hints fatter tail |
| Blass et al. 2013 | 5.8k IAC recs | top-management attention shifts implementation ±13 pp | curve is an average over attention states |
| DOE ITAC official stats (itac.university) | full database 1981–2024 | overall implementation ~45–50% | aggregate anchor confirmed |
| Qiu, Wang & Wang 2015 | IAC 2002–11 (**paywalled, unverified**) | implied discount 40–45%, threshold ~9 months | would steepen the front — chase via EI subscription |
| DeCanio 1993/98 | (**paywalled, unverified**) | reported 50–100% hurdle rates | consistent; unconfirmed |

**Net calibration verdict:** the S(1) = 0.50 anchor is now triple-confirmed (A&N, Muthulingam, ITAC aggregate) and the 1–3-yr steep decline is corroborated on three continents' industrial surveys. Two opposing adjustment candidates roughly offset: Qiu et al. (unverified) argues a steeper front; Rohdin's no-formal-criterion firms argue a fatter tail. **Recommend launching with the drafted curve unchanged**, revisiting front/tail if EI can retrieve the two paywalled papers. FORECAST's much higher 55%-at-3-yr is best read as cumulative multi-year implementation under EU policy support, vs these cohort-level adoption rates — i.e., our 20%/yr start rate supplies the cumulative dimension separately, so the curves are not directly comparable and should NOT be averaged.
