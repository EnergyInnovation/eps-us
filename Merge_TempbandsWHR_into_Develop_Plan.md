# Merge plan: `develop_tempbands+whr` → `develop`

> **AS-EXECUTED STATUS (2026-07-31 evening): COMPLETE — all gates pass.** Merge resolved in `4c116bd8`; one runtime blocker root-caused and fixed in `464c0c65`. See §7 (appended) for what the plan didn't predict. Awaiting Dan's review + push; WebAppData/docs (Phase F) still out of scope.

**Written 2026-07-31, pending Dan's sign-off.** Merge-base `2c873fcf` (2026-07-16). Target: `origin/develop` at `650a7f6f` (12 commits ahead of local `develop`, which sits at the merge-base). Companion doc: `PEaWHRP_Change_Summary_for_Merge.md` (§7 merge guidance — directionally all confirmed; several counts corrected below).

---

## 0. What recon found (evidence, not guesses)

Three read-only agents ran against `git merge-tree --write-tree origin/develop develop_tempbands+whr` (tree `6abdb1d0`), plus main-loop verification of their claims. No working-tree changes were made.

### 0.1 The collision surface is far smaller than §7 feared

- **Only one content-conflicted file: `EPS.mdl`.** The only other files changed on both branches are the 20 FoPITY CSVs, and those auto-merge (see 0.3).
- **Robbie never touched the heating-dimensioned input CSVs** (`IEMUEF` etc.) on develop. §7.4's "re-apply Robbie's values at 11-element shape" step is unnecessary — our temp-band CSVs carry over cleanly.
- Corrected subscript counts (summary doc §7.1 had 64/30/31; actuals verified by direct extraction, comments stripped):

| Family | origin/develop | branch | Resolution |
|---|---|---|---|
| `ISIC Code` | **52** (disaggregated `ISIC 01`,`02`,`03`,`07`,`08`…) | 42 (aggregated) | develop's |
| `Industry Category ISIC Code` | **25** | **25** | Same count both sides; only element *names* differ. develop's names, then verify `Waste Heat Availability Index` chain (name check, not structural rebuild) |
| `Industrial Process` | 10 | **11** (temp bands) | ours |
| `Govt Cash Flow Type` | 14 | **15** (`indst efficiency subsidy`; `remainder` still last) | ours |
| `Industry Category` | 25 | 25 (byte-identical) | either |

### 0.2 EPS.mdl: 65 conflict hunks, but 57 are cosmetic

- **57/65 hunks (4,044 lines)** are sketch-layout-only: the variable/arrow sequence on both sides was extracted and diffed programmatically — byte-identical; only x/y coordinates and item IDs differ. Zero model-logic risk; resolvable by script.
- **8/65 hunks are genuine**, all one theme — our WHR→"Measure" restructure vs develop's Material Efficiency / carbon-tax-rebate industry work landing in the same neighborhoods:
  - **#1, #2** (equations): adjacent alphabetical insertions from both sides — keep both, reorder. Trivial.
  - **#3** (equations, Industry): develop keeps `This Year Change in Industrial Energy Consumption for Heat Generation Due to Waste Heat Recovery` (a variable we deleted in the restructure) and adds `This Year Change in Industry Unit Costs as Share of BAU Output with Hold at Minimum Production` (Material-Efficiency-related). Needs a consumer trace before deciding (keep develop's ME equation, drop the dead WHR one — but verify nothing on develop still consumes the WHR variable's outputs through paths we replaced).
  - **#4, #5** (sketch: Policy Control Center, Policy Implementation Schedule): our lever removals/additions vs develop's box set that still shows retired lever names. Take ours + graft any develop-only new boxes (e.g. material efficiency lever).
  - **#9** (sketch: Industry Main, 2,043 lines): ours adds ~55 measure-structure boxes; develop retains ~14 boxes we lack (Material Efficiency, carbon-tax passthrough). Union: our layout as base + place develop's boxes.
  - **#19** (sketch: Industry Cash Flow, 797 lines): same shape — our generalized Measure financing chain + develop's ME/CCS-rebate cash-flow boxes.
  - **#21** (sketch: Input-Output Model, 1,727 lines): develop's side carries the whole TIOT/Material-Efficiency IO rework; our side is the pre-rework IO view. Take develop's side wholesale (our branch added no measure content to the IO view — assert this during resolution; the census agent's "which naming is newer" labels here were muddled, so re-verify box sets before discarding ours).

### 0.3 FoPITY: auto-merge is structurally sound — with one wart and one hard gate

- Auto-merged `FoPITY-policy-elements.csv` = **3,726 rows** = 3,757 (base) + 25 (develop's sole change: the `indst material efficiency` block) − 56 (our net). Verified: no duplicate elements, every block contiguous, and all parallel FoPITY files row-aligned with each other (spot-checked at the insertion boundary).
- **Wart:** git relocated `indst material efficiency` to a semantically arbitrary slot (between `indst reduce nonenergy product demand` and a LULUCF lever) because our rewrite consumed its original anchor. Functionally harmless — `VECTOR ELM MAP` anchors on each block's first element by name, and blocks are contiguous — but ugly.
- **Hard gate:** the `Policy Element` subscript family in EPS.mdl auto-merged *separately* from the CSVs. Its element order MUST match the CSV row order exactly, and git made both placement decisions independently. This must be verified programmatically before any simulation (Phase 2, step 2e). If they disagree, conform the .mdl family to the CSV order (or move both to the semantically sensible spot in one coordinated edit).
- Robbie's `indst material efficiency` lever is `[Industry Category]`-dimensioned, **not** process-dimensioned — §7.2's conditional ("add it band-dimensioned if process-dimensioned") resolves to: keep as-is.

**Recommendation: accept the auto-merge ordering** (verify-and-accept) rather than hand-rebuilding the industry region. The doc's rebuild advice predated evidence that the auto-merge is sound. Optional cosmetic relocation of the ME block in both .mdl and all 20 CSVs can be done later as an isolated commit if the ordering offends.

### 0.4 Residual semantic risk git can't flag

Where develop rewrote an equation we did NOT touch (or vice versa), git silently takes the newer side — fine. The danger case is an equation both sides edited on *different lines* (multi-line equations), which merges silently but wrongly. The §7.3 list (industry cash-flow consumers like `Change in Miscellaneous Expenditures by Industry`, `Change in Government Cash Flow by Cash Flow Type`, `GRA Weights…`, `Industrial Clean Heat Production Subsidy Amount Paid`, the three §3.6 application points) is exactly this set. Phase 2, step 2d audits every one of them in the merged file against both parents.

---

## 1. Pre-merge hygiene (main loop, ~10 min) — needs Dan's call on two items

1. **Revert** the uncommitted FoPITY-9 / FoPITY-9-WebApp edits (hand-tweaked industry carbon-tax ramp; pairs with untracked `IndustryCarbonTax.cin` / `DanTaxVars.lst` from sweep testing). *Default: revert. Say so if it was meant to be kept.*
2. **Commit `PEaWHRP_Change_Summary_for_Merge.md` to `develop_tempbands+whr`** first, so the handoff doc travels with the branch. *Needs approval (commit rule).*
3. Leave the other untracked files (`*.bak`, `*.lst`, `*.cin`) — untracked files don't interfere with a merge.
4. Fast-forward local `develop` to `origin/develop`.
5. Create working branch **`merge/tempbands-whr-into-develop`** from `develop_tempbands+whr`; merge `origin/develop` *into it*. Final delivery = PR/merge of this branch into `develop` after validation. All resolution commits stay on this branch; **Dan reviews and pushes** — nothing leaves the machine without his approval.
6. Back up nothing manually — git is the backup; abort path is `git merge --abort` / delete the branch.

## 2. Merge + resolution

**Step 2a — mechanical sketch hunks (script + Haiku-tier agent, ~30 min).**
`git merge origin/develop` on the working branch → EPS.mdl gets the 65 marker hunks. A Python script resolves the 57 layout-only hunks by taking the **branch (ours)** side, *asserting first* on each hunk that the two sides' variable-name sequences are identical (re-verifying the census claim hunk-by-hunk — a census flag is a lead, not a finding). Ours is preferred because the branch's sketch passed `sketch_lint.py` and was hand-corrected by Dan. Agent writes/runs the script; main loop spot-checks 3 random hunks.

**Step 2b — trivial equation hunks #1, #2 (main loop, minutes).** Keep both sides' variables, alphabetical order.

**Step 2c — the 6 real reconciliations.**
- **#3**: Sonnet agent traces consumers of both disputed variables on both parents; main loop decides (expected outcome: keep develop's ME unit-cost equation, delete the dead WHR variable, confirm no orphaned references).
- **#21 (IO view)**: verify our side has no boxes develop's lacks that we need (measure content should all live on Industry views); then take develop's side wholesale.
- **#4, #5, #9, #19 (sketch unions)**: our side as base; develop-only boxes (Material Efficiency, carbon-tax passthrough, CCS rebate) placed via the `eps-mdl-sketch-edit` skill. One Sonnet agent per view pair, main-loop review of the sketch lint output. These four resolve together — same underlying collision.

**Step 2d — silent-merge equation audit (Sonnet agent, verify escalation to Opus only if discrepancies).** For every §7.3 equation plus the three §3.6 application points: diff merged definition vs each parent's. Confirm (i) our additive Measure terms survived, (ii) develop's rewrites survived, (iii) no equation silently lost either side. Output: table of variable → status → fix needed. Main loop applies any fixes.

**Step 2e — Policy Element order gate (script).** Extract `Policy Element` family order from merged EPS.mdl; compare 1:1 against merged `FoPITY-policy-elements.csv` and one FoPITY-N.csv. Must be exact. Also assert `Govt Cash Flow Type` merged with `remainder` last and `indst efficiency subsidy` present, and that `GRA-indsteffmeasures.csv` + its `GRA Weights` row survived.

**Step 2f — commit checkpoint** on the working branch (approval covered by sign-off below).

## 3. Verification gates (sequential; stop at first failure)

| # | Gate | How | Pass criterion |
|---|---|---|---|
| 1 | Input shapes | `CheckGetDirectShapes.py` | 0 mismatches/missing (heating-dim CSVs are ours untouched, so genuinely expect 0) |
| 2 | Inputs exist | `eps-validate-inputs` skill | 0 missing files |
| 3 | Model loads | headless `LOADMODEL`, clean `vensimdp.err` | banner only |
| 4 | **Zero-policy exact-zero invariant** | run, extract measure deployment / multipliers / cash flows | deployment ≡ 0, multipliers ≡ 1, flows ≡ 0 (fastest detector of a broken merge) |
| 5 | Zero-policy regression vs both parents | compare headline outputs (emissions, GDP, elec gen) vs branch's `Pac*` baseline and vs a fresh origin/develop baseline run | diffs explainable: vs branch → only Robbie's IO/ISIC changes; vs develop → only temp-band accounting |
| 6 | Lever smoke test | SETVAL each of: 4 measure levers, `indst material efficiency`, 2 sample temp-band-dimensioned levers, 1 lever *after* the relocated ME block in row order | each produces a nonzero delta in its own domain and nothing fires the wrong domain (VECTOR ELM MAP anchor check) |
| 7 | WHAI sanity | extract `Waste Heat Availability Index` from gates 4/6 runs | all values in (0,1], =1 at start year |
| 8 | Carbon-tax $100 spot check | compare summed deployed fractions vs branch's ~65 | same ballpark, monotone deployment |

Gate runs are ~2 min each (US national); agents parse the `.tab`s, main loop judges. Still deferred, as before the merge: formal Vensim units check, WebAppData.xlsx, docs repo (Phase F).

## 4. Wrap

- Update `PEaWHRP_Change_Summary_for_Merge.md` §7 with as-executed notes (or a short `decisions.md`), including the corrected subscript counts and the FoPITY verify-and-accept decision.
- Dan reviews the branch diff, approves final merge to `develop` and pushes. KB write-up per `session-wrap` if findings warrant.

## 5. Agent/model assignments (per the tiering table)

| Work | Tier |
|---|---|
| Sketch-hunk resolver script run + assertions; Policy Element order gate; `.tab` series extraction | haiku |
| Hunk #3 consumer trace; sketch unions (#4/5/9/19) via sketch-edit skill; step 2d equation audit; gate-run analysis | sonnet |
| Adversarial verification only if 2d finds discrepancies or a gate fails unexplained | opus |
| Resolution decisions, spot checks, final judgment | main loop |

Estimated wall-clock: ~half a day including all gate runs, most of it Phase 2c/2d and simulation time.

## 6. Known caveats going in

- The census agent's hunk-#21 "which naming is newer" description was internally muddled — re-verify box sets before discarding our IO view side (step 2c bakes this in).
- Hunk #3's `This Year Change in Industry Unit Costs…` equation may reference Material Efficiency variables — its fate is a decision, not a mechanical rule.
- The capacity-market overshoot (documented pre-existing issue) will distort any high-carbon-tax electricity results in gate 8 — judge deployment behavior, not electricity-price-linked outputs.

---

## 7. As-executed appendix (what actually happened, 2026-07-31)

**Executed as planned:** Phases 0–2 ran essentially as written. 56/65 hunks script-resolved (one extra hunk was GUI run-state, resolved to develop's side); equation audit found all 18 risk equations clean; FoPITY auto-merge accepted (Dan's call); `Policy Element` turned out to load via `GET DIRECT SUBSCRIPT` from the CSV, making the §2e order gate structurally unfailable; all 82 VECTOR ELM MAP anchors verified. Five ghost sketch boxes (variables develop's passthrough rework deleted, still drawn in our Industry-Main view) were removed — the sketch agent initially misattributed them; they were merge artifacts.

**What the plan didn't predict — the gate-4 blocker (fixed in `464c0c65`):**
1. **A semantic conflict git cannot see.** Develop's `126ceb8d` added `Normalized Change in Industrial Capital Expenditures` referencing `New Waste Heat Recovery Equipment Capital Expenditures That Are Not Financed` — a variable this branch renamed. The union had one dangling reference. **Vensim loads such a model cleanly and hangs mute at initial-value computation** (generic "Problems encountered in the simulation", no error text anywhere, no .vdfx created; `NOINTERACTION` makes it a silent CPU-freeze). Root-caused by commit bisection in a worktree after all dialog/log probing failed. Fix: substitute `New Measure Capital Expenditures That Are Not Financed` (the successor, mirroring the branch's substitution in the level-dollar twin). *Review note for the ME owner: confirm that term is intended in the normalized per-unit-output equation.*
2. **Embedded changes-file record.** The branch model (since `2c43ee22`) carried GUI-state line `10:IndustryCarbonTax.cin` — with the local cin present, every default headless run silently applied a $300/t industry tax. Removed. Verified the branch's committed Pac* validation runs were NOT contaminated (PacBase2 measure fractions exactly 0).
3. 1,189 stale subscript-control selection lines (union of both parents' GUI state) stripped from the model file.

**Lesson worth institutionalizing:** after any EPS merge, scan for dangling references (variables with 0 definitions but >0 references) before attempting a simulation — it is a one-minute script and would have caught the blocker instantly. Neither LOADMODEL, CheckGetDirectShapes, nor sketch lint detects this class.

**Gate results (final EPS.mdl, commit `464c0c65`):**
| Gate | Result |
|---|---|
| GET DIRECT shapes (1,343 calls) | 0 issues |
| LOADMODEL / sketch lint | clean / clean |
| Zero-policy exact-zero invariant | fractions ≡ 0, multipliers ≡ 1, cash flows ≡ 0 (exact) |
| Zero-policy vs parents (Total CO2e 2050, g) | merged 5.187e15; branch 5.067e15 (+2.4% = Robbie's data fixes); develop 5.854e15 (−11.4% = temp-band industry recalibration). Dan to eyeball magnitudes. |
| WHAI | [0.286, 1.0], =1 at start year |
| Lever smoke (6 runs, READCIN) | each lever fires its own domain/industry only, incl. develop's `indst material efficiency` at its relocated FoPITY block; standards pay no subsidy; $100/t industry tax → broad deployment, 2050 CO2e −10.5% |

**Artifacts left in repo root** (gitignored or untracked): `MergeZeroPol.*`, `Smoke*.{cin,tab,vdfx}`, `MergeGate*.{cmd,lst}`, `MergeSmokeVars.lst`, `SuspectVars.lst` — reusable gate battery; various `Bisect*`/`Retest*`/`InitOnly*` diagnostics deletable. Worktree `..\eps-us-develop-baseline` holds the develop baseline + the independently-fixed verification run (`RealFix.*`); safe to `git worktree remove --force` when done. Still deferred, unchanged from pre-merge: formal units check, WebAppData.xlsx, documentation repo (Phase F).
