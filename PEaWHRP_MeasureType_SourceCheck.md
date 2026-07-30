# Are any efficiency measures really "buy a newer machine"? — source check

**2026-07-28. Conclusion: my earlier removal list was mostly wrong. Do not act on it.** At most 2 of 13 measures are supported as equipment purchases, and even those are judgment calls. A separate data-provenance problem surfaced (see §3).

## 1. Why this check happened

I proposed removing ~13 "equipment replacement" measures from `PEaWHRP-PMD` (≈33% of that set's savings potential), on the theory that buying a better machine happens anyway at equipment turnover, which `BIEEI` autonomous improvement already carries. **That classification came from a keyword script matching measure *names*, not from reading any source.** Dan challenged it on "efficient screening" — screening is a process step, so the name can't tell you whether the measure is a new screen or a reconfigured screening loop. He was right.

The proper test isn't "unit vs system" but: **does this happen anyway when equipment wears out** (→ BIEEI covers it, and keeping it here double-counts), **or is it a deliberate retrofit decision** (→ belongs in the measure list)?

## 2. What the sources actually say

Sources: [ENERGY STAR cement guide (Worrell, Kermeli, Galitsky 2013)](https://www.energystar.gov/sites/default/files/tools/ENERGY%20STAR%20Guide%20for%20the%20Cement%20Industry%2027_08_2013_Rev%20js%20reformat%2011192014.pdf) · [iron & steel guide LBNL-4779E](https://www.energystar.gov/sites/default/files/buildings/tools/Iron_Steel_Guide.pdf) · [pulp & paper guide LBNL-2268E](https://www.energystar.gov/sites/default/files/buildings/tools/Pulp_and_Paper_Energy_Guide.pdf) · [petrochemical guide LBNL-964E](https://eta-publications.lbl.gov/) (downloaded copy)

| Measure | My call | Source verdict | Evidence |
|---|---|---|---|
| High-pressure roller presses (cement) | remove | **KEEP — retrofit** | "most often used to expand the capacity of **existing** grinding mills… the **addition** of high-pressure roller presses"; retrofit $6.5/ton vs $16/ton standalone |
| Replace ball mills with VRMs (cement) | remove | **Remove candidate — equipment** | "CalPortland… **replaced several ball mills** with a state-of-the-art vertical roller mill system"; economics framed for "a new cement grinding line" |
| Variable speed drives (steel) | remove | **KEEP — retrofit** | "large fans are used to control air quality… the **installment** of variable speed drives"; fans stay, drive is added |
| Ultra-high power EAF (steel) | remove | **Likely keep — unclear** | "Converting the furnace operation to… UHP… by installing new transformers **or paralleling existing transformers**… **retrofit** of its transformer system"; forces added panel cooling |
| Efficient refiners (pulp & paper) | remove | **KEEP — process change** | Closest source measure "Refiner improvements": "implemented a refiner **control strategy**" / "**switch to conical refiners** rather than disk refiners" |
| Efficient refiner + pretreatment, TMP | remove | **KEEP — process change** | Closest: thermopulping / RTS pulping — "can be **turned on and off as desired** by mill personnel"; "**increasing the rotational speed** of the primary refiner" |
| Shoe press (pulp & paper) | remove | **Remove candidate — equipment** | "Extended nip presses use a large concave shoe **instead of one of the rotating cylinders**" — discrete substitution in the same functional role |
| Efficient screening (pulp & paper) | remove | **Cannot classify** | Phrase absent from the guide; nearest are distinct named measures ("Automatic chip handling and thickness screening", "Bar-type chip screening") |
| Steam box (pulp & paper) | remove | **Cannot classify** | Absent from the guide entirely (line-break-tolerant search, zero hits) |
| Improved compressors (chemicals) | remove | **Unclear** | Appears only inside a list of ethylene "utility systems" options as "Improved compressor/driver efficiencies" — no standalone description |
| Advanced furnace materials (chemicals) | remove | **Not found** | Phrase absent; the guide's nearest content is furnace **coil design** improvement incl. "ceramic coils or ceramic coated coils" — a material upgrade to an existing furnace, i.e. retrofit-shaped |
| PFPB (aluminum) | remove | **Unclear — leans remove** | "all **new** aluminum smelters use pre-baked anodes"; PFPB is named best-practice for new build. Notably the same LBNL report calls inert anodes and wetted cathodes "easily installed **retrofits** in existing cells" and says no such thing about PFPB — weak evidence it's a new-cell/rebuild technology ([LBNL-62806 Rev.2 World Best Practice](https://eta-publications.lbl.gov/sites/default/files/industrial_best_practice_en.pdf)) |
| New decoating equipment (aluminum) | remove | **Remove candidate — equipment** | Vertical Floatation Melter "used **in place of a gas reverberatory furnace**… decoats, preheats and melts in one operation"; IDEX decoater described as a standalone kiln ([DOE Aluminum Report 2016](https://www.energy.gov/sites/prod/files/2016/04/f30/Aluminum%20Report.pdf)) |

**Score: 4 clear reversals, 2 probable reversals, 3 unverifiable, 4 supported or leaning-supported.**

**There is no LBNL/ENERGY STAR aluminum guide.** That series covers iron & steel, cement, refining, pulp & paper, glass, breweries, corn wet milling, pharmaceuticals, vehicle assembly and metal casting — but not aluminum. The two aluminum measures trace instead to an LBNL best-practice benchmarking report and a DOE bandwidth study, neither authored by Kermeli. That is a fourth document family the workbook's "Kermeli" attribution doesn't cover.

Note the two clearest reversals — roller presses and variable speed drives — carry the **largest electricity savings in the whole efficiency set** (0.051 and 0.059), so the "≈33% of potential" figure was wrong in both magnitude and direction.

## 3. Two findings that outlast the classification question

**(a) The double-count worry is largely self-answering.** `BIEEI` captures what firms do *at* turnover. The premise of this whole structure is that these measures sit in an audited backlog precisely because firms *don't* do them. Retrofits and add-ons are therefore not in BIEEI by construction — the overlap only bites where "the old machine wore out and we bought the better one." Only the VRM row clearly fits that, with the shoe press arguable.

**(b) The `Source` column says "Kermeli" for measures Kermeli didn't author, and several labels don't exist in the guides.** Confirmed across four documents:

| Measure origin | Actual guide authors | Kermeli an author? |
|---|---|---|
| Cement (roller presses, VRMs) | Worrell, **Kermeli**, Galitsky 2013 | yes |
| Iron & steel (VSDs, UHP) | Worrell, Blinde, Neelis, Blomen, Masanet — LBNL-4779E | no |
| Pulp & paper (refiners, shoe press, …) | Kramer, Masanet, Xu, Worrell — LBNL-2268E | no |
| Petrochemical (compressors, furnace materials) | Neelis, Worrell, Masanet — LBNL-961E | no |

And five labels are absent from the corresponding guide entirely: "efficient screening", "efficient refiners", "steam box", "advanced furnace materials", plus "improved compressors" having no standalone description. The likeliest explanation is that the workbook cites a **Kermeli compilation** (a journal paper or inventory that itself draws on these ENERGY STAR guides) rather than the guides directly, with labels paraphrased in the process. The footnote letters (a/b/c/d/e/f) that would disambiguate have no legend anywhere in the workbook.

**Recommend adding a source legend mapping each footnote letter to a specific document + table**, independent of anything else here — otherwise every future question like this one costs the same effort, and right now the potentials cannot be traced to a citable page.

## 3b. Dan's sharper criterion (2026-07-28) — supersedes the BIEEI framing

Dan's point: EPS 4.1 doesn't just have an autonomous-improvement trend, it has **actual machinery for "replace old equipment with more efficient equipment"** — vintaged equipment stock accounting, an early-retirement lever to speed turnover, and an equipment-efficiency-standards lever that sets how good the new units are. So a measure like "replace a boiler with a more efficient boiler" is *already a modeled channel with its own levers*. Keeping such a measure in the measure list represents the same abatement twice, and lets two different levers each claim it.

**Revised test for removal:** would this measure's saving be *embodied in a replacement unit of the same equipment*? If yes, it belongs to the stock/standards/early-retirement channel, not the measure list. If it's an add-on, an auxiliary system, a control strategy, or an operating practice applied to equipment you keep, it belongs here.

This test cuts differently from my original name-based list — and it does *not* reinstate it. The two big reversals stand: high-pressure roller presses are explicitly an **addition to an existing ball mill** (the mill stays), and variable speed drives leave the fans in place. Neither is a replacement unit.

**Name-level shortlist for source-checking (NOT a decision — this is the same kind of keyword pass that failed before):**

| Set | Rows flagged by name | Share of that set's potential |
|---|---|---|
| Waste heat | 1 of 41 — "Conversion to Grate Cooler" | 0.5% |
| Efficiency | 17 of 63 | 33.4% |

Within the efficiency set the shortlist is dominated by two rows: **Replace ball mills with VRMs (13.3%)** and **Use of High-Pressure Roller Presses (11.6%)** — and source text says the second one is an add-on and should stay. So the genuinely-flagged share is likely nearer 20% than 33%, and the shortlist also surfaces three rows my original list missed entirely: Endless Hot Rolling of Steel Sheets, Optimization cell design, and Vertical shaft kiln.

**Two questions this raises before anything is removed:**

1. **Can the destination channel actually carry the abatement?** Relocating a measure only works if the stock/standards machinery can represent it. The efficiency-standards lever moves unit energy factors toward `IEMUEF` (the best-available floor). If `IEMUEF` was calibrated *without* assuming VRM-grade grinding or UHP-grade EAFs, then deleting those measures loses the abatement rather than relocating it — the standard would hit its floor before delivering it. Worth checking `IEMUEF` against the technologies being removed.
2. **Where is the boundary for component swaps?** UHP is new *transformers* on a furnace you keep; PFPB is new *cells* in a potline you keep. Both change the equipment's energy intensity without replacing "the equipment" as EPS defines it (process × fuel). These need Dan's call — the model's unit of equipment is coarser than the measure list's.

## 3c. THE PRUNING LIST (2026-07-28, tiered by what's blocking each)

Shares are % of the efficiency set's savings potential unless noted. Two tests must both pass to justify removal: **(i)** the measure is a like-for-like replacement of original equipment (Dan's criterion), and **(ii)** the destination channel — standards + turnover, floored at `IEMUEF` — can actually carry the abatement.

### Tier 1 — remove now (both tests pass)

| Measure | Share | Why |
|---|---|---|
| **Shoepress** (3 rows) | 0.34% | Source: "extended nip presses use a large concave shoe **instead of one of the rotating cylinders**" — replaces a press cylinder. Saves drying steam; destination is the <200 °C gas bands, 14–16% headroom, never binds before 2050. |
| **New decoating equipment** | 0.49% | Source: VFM "used **in place of a gas reverberatory furnace**". Destination is 200–500 °C gas, 17% headroom, never binds. |

Combined ≈ **0.8%**. Small, but unambiguous on both tests.

### Tier 2 — your boundary call on component swaps

| Measure | Share | The question |
|---|---|---|
| **Ultra-high power (UHP)** | 0.90% | New transformers on a furnace you keep. Is a component upgrade inside retained equipment "replacing original equipment"? Destination (>1000 °C, 36% headroom) can carry it either way. **Also a data question:** this row records *fuel* savings (0.00398) and zero electricity, yet UHP is fundamentally about electrical power input to an EAF — is the intended saving reduced burner gas from shorter tap-to-tap times, or is the fuel/elec assignment wrong? |

### Tier 3 — blocked on IEMUEF question C

| Measure | Share | The blocker |
|---|---|---|
| **Replace ball mills with VRMs** | **13.3%** | Verified equipment swap, so test (i) passes. Test (ii) fails as things stand: machine-drive electricity has 13.0% total headroom, BAU eats 6.8 points by 2050, leaving ~6.2 against the 7.8 needed. **Resolution depends on whether `IEMUEF`'s machine-drive floor already assumes VRM-grade grinding** (question C in the Excel investigation). If it does → genuine double count → remove, and accept that the standards lever under-delivers. If it doesn't → no double count with the standards channel, only a partial overlap with BIEEI's 0.28%/yr → keep. |

### Tier 4 — need a source check before deciding

| Measure | Share | Note |
|---|---|---|
| Endless Hot Rolling of Steel Sheets | 1.36% | Name suggests a new rolling line; unverified |
| Optimization cell design | 1.20% | Aluminum cell redesign — could be new cells or retrofit |
| **Efficient refiners** (3 rows) | 1.44% | Reopened: the source gives *both* "implemented a refiner **control strategy**" and "**switch to conical refiners** rather than disk refiners". The second half is an equipment swap. Needs a call on which the 1.44% represents |
| Vertical shaft kiln | 0.07% | New kiln; unverified |
| Conversion to Grate Cooler | 0.46% *of waste-heat set* | Only equipment-swap candidate in the WHR set; unverified |

### Never remove — verified add-ons to retained equipment

High-pressure roller presses (11.6%), variable speed drives, efficient refiner + pretreatment/TMP (thermopulping and RTS are operating-parameter changes).

### One structural note on relocation

Our measures are **industry-level** — they carry no process dimension. The standards channel is **process × fuel**. So relocating any measure means someone must decide which heat band or process bucket receives it. That's an extra modeling judgment per measure, not an automatic transfer, and it's why the Tier 1 entries above required me to reason about destination bands by hand.

## 3d. RESOLUTION — exclusions applied 2026-07-28

**Removed (10 slot rows, ≈17% of the efficiency set's pre-pruning potential):** Replace ball mills with VRMs (Dan's ruling: within IEMUEF technology scope → double count with standards channel) · Efficient refiners ×3 (Rutten 2017: "technology replacement option") · Endless Hot Rolling (Worrell 2010: "construction of an ESP plant" — new-build) · New decoating equipment (DOE 2016: "in place of a gas reverberatory furnace") · Shoepress ×3 (LBNL-2268E: replaces a press cylinder) · Vertical shaft kiln (Boulamanti & Moya 2017: "choice of vertical shaft kiln, instead of the other types").

**Kept (Dan's component-swap ruling — retrofit projects on retained equipment):** UHP, PFPB (Söderberg→PFPB cell conversion), Conversion to Grate Cooler ("converting a planetary cooler into an efficient reciprocating grate cooler"), Optimization cell design (Rutten: "renovation of PFPB cells" — flagged: Rutten also calls it "substitution").

**Kept (verified process changes/add-ons):** High-pressure roller presses, VSDs, Efficient screening (Fleiter 2012: "increasing the slurry consistency from 1.5 to 2.5%… optimization of the screening process" — settled by Dan's supplied full text), Steambox (Rutten: "an add-on technology"), Advanced furnace materials (Ren 2006: ceramic coatings on existing tubes), Improved compressors (Neelis 2008: controls/repairs).

**Flagged, not removed:** TMP refiner + pretreatment (Fleiter measure 5: RTS refiner "compared to conventional disc refiners" + pre-compression add-on — mixed; awaiting Dan's veto either way). UHP's fuel-vs-elec savings assignment still odd (faithful to Kermeli's table, but physically surprising).

**Mechanics:** exclusions ride the workbook's own bucket chain (`Kermeli Data` col P → `X equip-replace`) with dated rationale notes in new col W; the 10 statically-wired export slot rows converted to literal "(empty slot)" pattern (same convention as the pre-existing X-bucket exclusions). Export script now reads the parameters workbook directly — during verification this surfaced 23 WMD rows whose values had drifted between Dan's 08:13 export file and his 12:31 workbook save (Bianchi fill ~−2.5%, gap-fill band redistribution); confirmed against the pre-edit backup that all 23 pre-date these edits. Single-source-of-truth export eliminates that drift class. Incident note: programmatic saves strip Excel's cached formula values — the export script now fails loudly on a cache-less workbook; recalc requires an Excel open+save (COM automation nonfunctional on this machine).

## 4. Recommendation

1. **Remove nothing on my original 13-measure list.** That Excel prompt is withdrawn.
2. **Source-supported removal candidates under Dan's criterion** (§3b), with their share of the efficiency set's potential:

| Measure | Share | Evidence strength |
|---|---|---|
| Replace ball mills with VRMs | 13.3% | strong — explicit unit-for-unit replacement |
| Ultra-high power (UHP) | 0.9% | boundary call — new transformers on a furnace you keep |
| New decoating equipment | 0.5% | moderate — "in place of a gas reverberatory furnace" |
| Shoepress | 0.3% | strong — replaces one of the two press cylinders |
| PFPB | 0.3% | weak/leaning — new-build technology, retrofit status unstated |
| **Total** | **~15%** | (vs the ~33% I originally claimed) |

Plus three name-level candidates never source-checked: Endless Hot Rolling, Optimization cell design, Vertical shaft kiln (~2.6% combined), and one in the waste-heat set: Conversion to Grate Cooler (0.5% of that set).

3. **Verified keeps** — do not remove: high-pressure roller presses (11.6%), variable speed drives, efficient refiners, efficient refiner + pretreatment (TMP).
4. **Before removing anything, check `IEMUEF`** can actually carry the relocated abatement (§3b question 1). Otherwise the saving disappears instead of moving.
5. **Add the footnote-letter → source legend** to the workbook (§3b). Four different document families are involved and the attribution column names the wrong authors for three of them.
6. The remaining unverifiable measures ("efficient screening", "steam box", "advanced furnace materials", "improved compressors") need whoever assembled the list to name the actual source before anyone can classify them.

*Verify the quoted passages and page references against the source PDFs before any of this reaches a work product.*
