# EPS 4.1 Industry Flow — Architectural Assessment

Draft for staff review, 2026-07-17 (Checkpoint 2 of the review plan in
`Industry41_Structure_Review_Plan.md`). Based on a full equation-level read of the
working-tree `EPS.mdl` (post temp-band restructure, model side). Line numbers drift —
re-locate variables by name. Everything here is review input, not a sign-off; verify
equations in Vensim and data claims against sources before relying on them.

## 1. The flow in one page

Demand → stock → choice → energy, all one-year-lagged, no within-year circularity:

1. **Demand**: `Last Year Output by ISIC Code with Fuels Based on Energy Content` (lagged
   industry $ output, IO-feedback-adjusted unless `BDMFL` disables) is allocated to the
   11 processes by **BAU-frozen** energy shares (from BIFU × BPFUbIP input data).
2. **Stock**: three tranches serve that demand — preexisting equipment (INTEG decaying by
   IESD natural-retirement curves / site profiles, plus the early-retirement lever),
   model-run vintages (write-once "flash" INTEGs per `Model Run Vintage`, retiring by
   age-based IESD lookups), and **new equipment = the residual gap** (MAX(0, share-scaled
   demand − surviving capacity)).
3. **Choice**: new equipment's fuel mix comes from a GCAM-style logit —
   `10000 × IES shareweights × exp(IELC × PV cost per unit output)` — where the PV cost
   stacks annualized capital (net of clean-heat ITC, RnD, cost-of-capital lever, over the
   RPfFISCC repayment window) plus fuel + fuel tax + carbon tax − clean-heat PTC (over the
   IESD lifetime window), all on an electricity-equivalent service basis (1/(1−PIFURfE)).
   Electrification and alt-fuel-shift levers then override the logit output by
   conservative share transfer. Fuel shares and intensity freeze into the vintage at
   install year.
4. **Energy**: Σ(vintage output × frozen share × frozen intensity) + new + preexisting
   (start-year shares, single scalar intensity) → WHR multiplier (heat bands) → process-
   efficiency multiplier → + CCS fuel − captured methane → `Industrial Fuel Use` →
   emissions/cash flows. The vintage dimension is summed away here; nothing downstream
   carries it.
5. **Feedbacks**: cash flows → IO model → next-year output (macro loop); utilization loop
   via lagged output; carbon tax and fuel tax get true FoPITY schedule foresight in the
   PV costs; everything else is myopic or trailing.

Feedstocks/non-energy use, process emissions (MAC curves), and the process *mix* remain
top-down — the stock model covers energy use only.

## 2. What the architecture gets right

- **The right fix for 4.0.5's real weaknesses.** Policy effects now respect stock
  turnover (electrification can't teleport the fleet), costs move fuel choice
  endogenously (carbon tax, ITC/PTC, and cost-of-capital levers work through one
  consistent economic channel instead of nothing), and vintage-tagged PTC duration
  (BCHPD) reproduces 45Q/48C-style mechanics faithfully.
- **Policy stacking is genuinely well-engineered.** Explicit anti-double-count guards
  everywhere the channels could collide: MIN (stronger-of) for standards vs
  price-induced efficiency; residual netting for MAC levers vs carbon-tax abatement; MAX
  for forced vs economic CCS and for early vs natural retirement (with a monotone
  ratchet); conservative share transfers for the forced-share levers. This is better
  discipline than most IAMs manage.
- **Consistent with the rest of EPS.** Same logit family as transportation, same vintage
  pattern as power plants, per-cell FoPITY scheduling via VECTOR ELM MAP. Maintainers
  learn one idiom.
- **Engineered for cheap simulation.** Write-once vintage INTEGs, one-year-lag loop
  breaking (no SIMULTANEOUS blocks, no iteration — unlike the electricity capacity
  market), and the July perf pass already hoisted the hot logit/PV work.
- **Deliberately minimal foresight.** Only carbon tax and fuel tax — the two streams
  firms can actually read out of legislation — get schedule foresight; that's defensible
  economics and it's what made the FoPITY future-year isolation cheap.

## 3. Structural findings and design questions (ranked)

### 3.1 The utilization factor never binds (verify intent — likely a scaling bug)

`Industrial Equipment Utilization Factor[IC,IP] = MIN(1, ZIDZ(Last Year Output by ISIC
Code with Fuels Based on Energy Content[IC], Σ potential[IC,IP]))`. The numerator is
**whole-industry output**; the denominator is potential for **one process**, which is
built (initialization and additions alike) as output × process-share. So the ratio is
≈ 1/process-share ≥ 1 for every process, and the MIN pins at 1 unless total industry
output falls below a single process's potential — essentially never. By contrast,
`Output from New Industrial Equipment` and `Initial Output by Industry Category and
Process` both correctly share-scale the same numerator, which strongly suggests the
utilization numerator was meant to be share-scaled too.

**Consequence if unintended:** existing equipment always runs at full potential. When an
industry's output declines (BAU decline, material-efficiency lever, macro-feedback
contraction), energy use does not fall with it — the only demand response is zeroed new
additions, with energy decaying only as fast as retirement. Demand-side policies
under-deliver emissions cuts on the existing stock, symmetrically in BAU and policy
branches (so BAU validation won't catch it; "Change in" outputs for demand-reduction
levers are biased toward zero). **Verification recipe:** plot
`Industrial Equipment Utilization Factor` for a BAU-declining industry (e.g. coal
mining 05) — pinned at exactly 1 across the run supports the diagnosis; the fix is
multiplying the numerator by the same ZIDZ process-share used in the additions equation
(and mirroring in the BAU twin and the inlined copy in `Output from Preexisting
Industrial Equipment`).

### 3.2 The process mix is frozen at BAU shares

Output is allocated to the 11 processes by start-year BAU energy shares forever; no
lever, price, or trend moves it. Structural change *within* an industry — EAF
displacing BF-BOF, clinker substitution, low-temp process innovation — is out of scope
except via exogenous BAU data. This makes the new temperature-band detail static: bands
can't grow or shrink relative to each other. That's a defensible first-cut
simplification, but worth an explicit decision, because the band restructure invites
exactly these questions ("what if high-heat demand shrinks?"). Cheapest upgrade:
time-varying process shares as input data (BPFUbIP is already per-year-capable);
expensive upgrade: endogenous process choice (probably not worth it).

### 3.3 Preexisting stock is a gray box

The pre-2025 fleet — which dominates energy use for the first decade — has: one scalar
energy intensity per industry (no fuel or process differentiation), start-year fuel
shares (only early retirement changes them), and **no efficiency improvement over time**
(BIEEI applies to new equipment only). All fleet efficiency gains come from turnover
plus the fleet-wide process-efficiency lever. If historical in-place improvement
(retrofits, housekeeping) is real, BAU calibration must absorb it through turnover
speed or the BIEEI path, which distorts the vintage structure it's calibrating. Decide:
either accept and document, or give preexisting stock a simple exogenous intensity
decay.

### 3.4 No retrofit pathway

The model offers exactly two routes to change existing equipment's fuel: wait for
retirement, or the early-retirement lever (full capital write-off + new build). There is
no convert-in-place option (e.g. boiler electrification retrofit at a fraction of
replacement capex), even though that's a major real-world channel for the <200 °C bands
and the likely subject of clean-heat policy analysis. WHR is the only retrofit-shaped
measure and it's an energy multiplier, not a fuel switch. A minimal version — a
lever-driven transfer of preexisting/vintage fuel shares with an associated capex — is a
mid-size addition that would substantially widen the policy questions 4.1 can answer.

### 3.5 Logit calibration and IES semantics

- `IELC = −6` is one uniform cost-sensitivity for all 25 industries × 11 processes ×
  12 fuels. GCAM's own sectoral logits vary exponents by nest. With a single exponent,
  the IES shareweights do all the heterogeneity work — document how they were calibrated
  (fit to observed shares at observed prices?) or the fuel-choice response to a carbon
  tax is essentially one assumed elasticity economy-wide.
- **Data-governance trap:** the IES CSV headers say "Max Fraction of Production" but the
  equation uses them as multiplicative logit priors, not caps — a 0.03 entry does *not*
  cap the share at 3% (only 0 is a hard exclusion). Whoever populates the band data next
  will reasonably assume cap semantics. Rename the header/xlsx label or add cap logic;
  don't leave the mismatch.
- Flat logit over 12 fuels includes near-substitutes (three hydrogen variants, two heavy
  oils) — classic IIA share-splitting. A two-level nest (electric vs combustion, then
  fuel) is the standard fix if hydrogen-vs-electrification results start looking odd.

### 3.6 Foresight heterogeneity — mostly defensible, one flag

Carbon/fuel tax: schedule foresight (good). Fuel prices: BAU-path data foresight with
myopic policy perturbations (fine). But **electricity price enters as a trailing 5-year
average with no forward component** — in fast grid-decarbonization scenarios,
electrification decisions lag real electricity cost declines by ~5 years, a structural
thumb on the scale against electrification, compounding with 3.4. If intentional
(conservatism, stability), document it; if not, using the BAU electricity price path the
way fuel prices are handled would be more symmetric. Also note capital is discounted
over the repayment window while fuels use the lifetime window — defensible
(loan-payment vs operating-horizon framing) but nonstandard vs LCOE convention;
it interacts with IELC calibration and should be stated in the docs.

### 3.7 No endogenous learning on industrial equipment

`IECCpUAEU` is static; only the RnD lever and the standards elasticity move equipment
capex, while other EPS sectors have endogenous learning. And industrial **CCS learning
is decoupled from adoption**: CCS capex learns by doing, but the retrofit-adoption
decision uses a static cost lookup vs `Value of CCS` — learning never accelerates
uptake, it only re-prices cash flows. Both are scope decisions worth making explicitly,
since heat-pump and electrolyzer cost declines are central to industrial-heat debates.

### 3.8 Cash-flow landings shape the jobs story

Financed capex and the clean-heat **ITC** revenue land on ISIC 64T66 (finance); the
**PTC** lands on the producing industry's own ISIC. So the IO/jobs model stimulates
different industries depending on subsidy *form*, not just size. Possibly intended
(financed purchases flow through lenders), but the ITC-to-finance choice in particular
deserves a second look before distributional results are published.

## 4. Better choices — recommendations ranked

1. **Resolve 3.1 now** (utilization numerator share-scaling): one-line fix × 3 sites if
   confirmed; it changes demand-decline behavior everywhere. Do before any calibration.
2. **Decide and document 3.3 and 3.6** (preexisting-stock improvement; electricity price
   basis): cheap to change, easy to defend either way, but must be deliberate.
3. **Fix the IES header/semantics mismatch (3.5)** before the band data is populated —
   after that it's a live data-entry hazard.
4. **Consider a minimal retrofit lever (3.4)** for the next structural iteration; it is
   the biggest capability gap relative to the policy questions the temp bands exist to
   answer.
5. **Time-varying process shares (3.2)**: low-cost input-data generalization; decide
   whether bands should be able to drift before geographies build band datasets.
6. Housekeeping (non-headline, from the code reviews): duplicate inlined utilization
   expression in `(BAU) Output from Preexisting Industrial Equipment`; hoistable logit
   denominator; stale 10-process `{boilr}…` comments on the lever matrices; reversed
   subscript order on the cost-of-capital lever ([IP,IC] vs everyone else's [IC,IP]);
   missing MAX(0,·) on the BAU clean-heat capex netting; restore the FoPITY
   "REGENERATE" maintenance note without the literal `~`; `Reqayments` typo family.

## 5. Runtime implications

The architecture *is* the runtime cost, and it's spent deliberately:

- **State growth**: the vintage layer's big arrays are `…Fuel Type Shares…by Vintage`
  (25×11×12×26 ≈ 85,800 el. × 2 twins) and the potential-output family (7,150 el. × ~8).
  The intensity-by-vintage array already drops the process dimension (7,800 el.) — an
  economization that shows the designers were watching size. Total industry state is
  roughly two orders of magnitude above 4.0.5's pipeline, but vintage stocks are
  write-once INTEGs (cheap per step), and the expensive per-step work — logit exp() and
  the PV sums over 75 Future Years — was just cut ~90% by the July hoists.
- **No iteration**: unlike the electricity capacity market's 20-pass optimization,
  industry solves in one pass with one-year lags. Per-timestep, industry should remain
  well behind electricity as the dominant cost. The FoPITY lookup/INITIAL work moved the
  remaining schedule cost to initialization.
- **Would the "better choices" above cost runtime?** 3.1 (fix), 3.3, 3.5, 3.6 —
  negligible. A retrofit pathway (3.4) adds one lever-driven share-transfer stage on
  existing tranches — small (3,300-element scale, no new vintage arrays) *if* retrofits
  are tagged onto existing vintages rather than tracked as their own stock. Time-varying
  process shares (3.2) — free (data read). Nested logit (3.5) — a second normalization
  layer, minor. None threaten the vintage layer, which is the one expensive commitment
  already made.
- **What to measure** (Workstream D, once the band data lands and the tree is
  committable): init vs run wall-time split, develop vs `dev_4.0.5_aeo26`, and the same
  runs through SDEverywhere for the web build, where subscript count inflates generated
  code — the 10→11 process growth is ~10% on process arrays and likely invisible, but
  the vintage layer's compile-size effect on the web bundle is worth one measurement
  before the core release.

## 6. Suggested validation probes (behavioral, once data lands)

1. Utilization pin test (3.1): extract `Industrial Equipment Utilization Factor` for
   coal mining / declining industries, BAU.
2. Demand-shock test: material-efficiency lever at 20% on one industry — does energy
   fall ~proportionally or only via halted additions?
3. Turnover-rate sanity: BAU share of 2050 energy from preexisting stock per industry vs
   expectation from IESD curves (catches both retirement calibration and the 3.3
   gray-box effect).
4. Electrification-vs-hydrogen logit response: carbon-tax sweep; check hydrogen variants
   don't take implausible joint share (IIA symptom).
5. PTC vintage window: single-year clean-heat PTC pulse; confirm payments persist
   exactly BCHPD years for the tagged vintages and decision costs saw only the window.
