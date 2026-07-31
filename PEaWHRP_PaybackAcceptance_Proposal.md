# Proposal: replace PSUS with a payback-acceptance curve

**2026-07-31 · Status: PROPOSAL — not implemented.** Responds to Dan's challenge that PSUS is too simplistic and its implied thresholds are absurd (full unlock at 14× the value of saved energy ≈ $40/gal diesel).

## 1. What's wrong with the current mechanism

The barrier regime's ceiling is `MIN(1, PSUS × (Value/BAU Value − 1))` with PSUS = 0.075 (WHR) / 0.10 (PEM). Three defects:

1. **Absurd implied thresholds.** Full unlock requires Value = (1 + 1/PSUS) × BAU value ≈ 14×. No plausible policy delivers that on gas-fired heat; the mechanism is effectively dead below ~$200/t and does all its work in a range no scenario visits.
2. **Perverse ordering.** Measures *not* cost-effective at BAU (regime A) jump to a ceiling of 1 the moment policy flips them, while the *cheapest* measures — the audited backlog the whole structure exists to represent — creep behind PSUS. The model deploys expensive measures faster than cheap ones. The adoption literature says the opposite of neither: adoption falls smoothly with payback, with no discontinuity at the BAU-cost-effectiveness boundary.
3. **One hand-set parameter carries the result.** 183 of 196 active WHR tranches under a $300/t tax are ceiling-limited by PSUS; measure-level economics — the thing we spent the whole restructure quantifying — barely matters for them.

## 2. Reframe: barriers as a distribution of payback thresholds

Dan's suggestion — a shadow cost / implicit discount rate perceived by factory owners — is what the audit-adoption literature actually measures, and the three framings are mathematically interchangeable:

> a payback threshold τ ≡ an implicit discount rate ≈ 1/τ (for long-lived assets) ≡ a shadow capital-cost multiplier (true payback ÷ τ)

The empirical anchors, from the sources already in hand (downloaded for the PSUS calibration; quotes verbatim from the local copies — verify against the PDFs before publication):

- **Anderson & Newell (2004, IAC audit data, ~10k projects):** "most require a payback of **15 months or less** as their investment threshold, corresponding to an **80% or greater hurdle rate**"; "the implicit investment threshold… was about a **1.25- to 1.5-year payback**, which corresponds to about a **65% to 80% hurdle rate** for projects lasting 10 years or more"; "**Plants reject about half** of recommended projects."
- **IAC/OSTI VFD study:** "<20% adoption" for motor-system VFDs at ~15.5-month payback; ~40% for cheaper compressed-air recommendations — even sub-2-year paybacks leave most of the distribution unmoved.
- Dan's framing confirmed: firms behave as if energy savings 2–3 years out barely count, so capital costs loom enormous. That is a *distribution* of thresholds across firms — not a single cliff, and not a value-ratio multiplier.

## 3. The mechanism

One exogenous curve **S(p)** = share of firms whose threshold accepts a simple payback of p years (survivor function, decreasing; S(∞) = 0). Then per tranche:

```
Payback p          = (MCLM × capex) / MAX(ε, Value − MCLM × opex)        { years; p = ∞ if denominator ≤ 0 }
p_BAU              = same at BAU prices (no subsidy)
Deployment ceiling = MAX(0, (S(p) − S(p_BAU)) / (1 − S(p_BAU)))
```

The denominator renormalizes to *remaining* potential: firms below the BAU threshold already adopted, and that adoption is embedded in the base-year energy data and Kermeli's diffusion netting — which is precisely the counterfactual-screen logic, now continuous.

**Properties:**
- **Exact zero-policy invariant, no screen needed.** At zero policy p = p_BAU → ceiling = 0 identically. Measures not cost-effective at BAU have S(p_BAU) = S(∞) = 0, so they use the same formula — regimes A and B unify into one continuous rule, killing the perverse ordering (an expensive measure flipped cost-effective at a 2.5-yr payback gets ceiling S(2.5) ≈ 0.2, not 1.0).
- **The stubborn tail stays stubborn.** Fat-tailed S means the last tranche of the backlog never unlocks at any price — matching the literature — while the responsive middle moves at realistic policy strength.
- **Dynamics unchanged.** The 20%/yr start rate, retirement backfill (fix 1), standards floor (still bypasses everything), cost-level spread, and availability index all stay as-is; only the ceiling formula changes.

## 4. Proposed default curve (adjustable CSV)

Anchored on: ~50% rejection at the 1.25–1.5-yr typical threshold; <20–40% adoption near 15-month paybacks for costlier categories; steep decline beyond 2 years; small persistent tail. Approximately lognormal (median ≈ 1 yr, σ ≈ 0.9):

| p (yr) | 0 | 0.25 | 0.5 | 1.0 | 1.5 | 2 | 3 | 4 | 6 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| S(p) | 0.85 | 0.75 | 0.65 | 0.50 | 0.38 | 0.27 | 0.13 | 0.06 | 0.02 | 0.005 |

S(0) = 0.85, not 1: even instant-payback measures see incomplete adoption (hidden costs, attention). Settable to 1 if Dan prefers full unlock at extreme signals.

## 5. Worked numbers vs PSUS ($4/MMBtu gas heat, measure with 1.2-yr BAU payback, S(1.2) ≈ 0.45)

| Policy | Value multiple | Payback | **New ceiling** | PSUS ceiling |
|---|---|---|---|---|
| $50/t CO₂ | 1.7× | 0.72 yr | **(0.58−0.45)/0.55 ≈ 0.24** | 0.05 |
| $100/t | 2.3× | 0.52 yr | **≈ 0.35** | 0.10 |
| $300/t | 5.0× | 0.24 yr | **≈ 0.55** | 0.30 |

Responsive at realistic carbon prices, saturating sensibly, never requiring $40/gal-equivalents — and the residual non-adoption at even $300/t is a documented empirical fact rather than an artifact.

## 6. What changes, what's decided by Dan

**Implementation (small):** one new CSV (the S curve, ~10 points) + Vensim LOOKUP; per-tranche payback variables (all inputs exist); replace the two `Tranche Economically Deployable` equations; delete PSUS. Re-run full battery.

**Decisions:**
1. **MHRP must shrink or go.** Barriers can't live in both the hurdle premium *and* the acceptance curve — that double-counts. Propose MHRP → 0 (LCOS reverts to pure WACC financial cost; the curve carries all behavior). LCOS then only defines cost-effectiveness for the standards-channel cost accounting and cash flows.
2. **One shared curve or per-set?** PSUS distinguished WHR (0.075) from PEM (0.10). Simplest: one curve + optional per-set payback scale factor (e.g., WHR paybacks perceived 1.3× longer — integration projects have more hidden cost). Recommend starting shared.
3. **Curve values** — the table above is a first pass from A&N/IAC; Dan adjusts.
4. **Caveat to accept:** A&N/IAC data are audited plants (information barrier already removed) and 1981–2000 small/medium manufacturers. The curve is an optimistic envelope for un-audited plants; a coverage-style downscale is possible later.

## 7. Alternative considered and not recommended

A single implicit discount rate (e.g., 70%) in the LCOS, keeping the binary screen: simpler, but restores the cliff (all-or-nothing per tranche), loses the empirically observed smooth adoption gradient, and reintroduces the regime discontinuity. The distribution *is* the phenomenon.
