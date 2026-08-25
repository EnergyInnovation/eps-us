"""DRAFT-input generator for the cement pathway module (Phase 1a).

Adapted from CreateSteelDraftInputsScript.py, following the naming map and
DRAFT-value table in Cement_1a_Spec.md. Emits all 10 new input CSVs under
InputData/indst/<ACRONYM>/<ACRONYM>.csv, relative to this script's own
location (portable - no hard-coded user paths). Every DRAFT value below
carries an inline source comment; primary-source verification is still
required before release (see cement_1a_notes.md for open reconciliation
items, e.g. the BCtCR vs. WRI clinker-ratio discrepancy).

Unlike the steel generator, this script does NOT calibrate against the
existing generic industrial structure (no BIFU/BPFUbIP level-calibration
step) - Phase 1a cement inputs are independent DRAFT placeholders, and the
Cement Module Energy as Share of Generic Energy by Fuel diagnostic (in
cement_1a_equations.txt) is left to report the resulting gap for review
ahead of the Phase 1b wiring step, rather than being solved for here.
"""
import csv
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "InputData", "indst")

# Match the steel generator's year range for time-series inputs so all
# industry-breakout modules' CSVs line up column-for-column.
YEARS = list(range(2021, 2051))

PATHWAYS = ["dry kiln with precalciner", "dry kiln with CCS", "electric kiln",
            "alternative chemistry cement"]

# Must match the model's Industrial Fuel subscript family order exactly
# (verified by grep against EPS.mdl - see cement_1a_notes.md).
FUELS = ["electricity if", "hard coal if", "natural gas if", "biomass if",
         "petroleum diesel if", "heat if", "crude oil if", "heavy or residual fuel oil if",
         "LPG propane or butane if", "hydrogen if", "green hydrogen if", "low carbon hydrogen if"]


def write(folder, name, rows):
    d = os.path.join(ROOT, folder)
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, name)
    with open(p, "w", newline="") as f:
        # csv.writer quotes any cell containing a comma. Unquoted commas in
        # the unit-string header shift GET DIRECT DATA's year row relative to
        # the data rows (adversarial-review finding 1, 2026-08-24): the time
        # axis silently lands 1-2 years early and the tail years read blank.
        w = csv.writer(f, lineterminator="\n")
        for r in rows:
            w.writerow(r)
    print("wrote", p)


# ---------------- BCD: BAU Cement Demand ----------------
# Phase 4 verification (2026-08-25): 84.0 Mt CONFIRMED (USGS MCS2026:
# portland+blended 82.0 + masonry 2.1; 2021-25 series 91.0/91.2/89.7/85.0/
# 84.0). No physical tonnage forecast exists: AEO2026 Table 29 (cement AND
# lime, suptab_29.xlsx, "Counterfactual Baseline") implies ~+0.5-0.6%/yr in
# shipments-$ and process-CO2 proxies to 2050. Held FLAT as the deliberate
# simplification (the proxies bundle lime and are not tonnage); the AEO-
# consistent alternative (~97 Mt by 2050) is documented for team choice.
rows = [["Unit: metric tons/year (VERIFIED 84 MMT 2025, USGS MCS2026; held flat - AEO2026 Table 29 proxies imply ~+0.5%/yr, team choice documented)"] + YEARS,
        ["BAU Cement Demand"] + [84_000_000] * len(YEARS)]
write("BCD", "BCD.csv", rows)

# ---------------- BCtCR: BAU Clinker to Cement Ratio ----------------
# VERIFIED 2026-08-25 (Phase 4): 0.8214 = USGS MCS2026 2025 domestic clinker
# production (69 Mt) over cement production (84 Mt). Imported clinker
# (~0.66 Mt) deliberately EXCLUDED (module demand basis = domestically
# produced clinker; including imports made the module build capacity to
# "replace" imports). The WRI-cited 0.88 is RECONCILED: same USGS series,
# older vintage - the domestic ratio fell 0.8749/0.8716/0.8560/0.8471/0.8214
# over 2021-2025 (PLC/Type IL adoption; USGS: blended cement = 63% of 2025
# shipments, 95% of it Type IL). A flat ratio therefore overstates future
# clinker: DRAFT BAU trajectory declines linearly 0.8214 (2025) -> 0.78
# (2035), flat after (judgment: the market-driven PLC transition largely
# completes; PCA's 0.75-by-2050 roadmap figure is a target, not BAU - team
# review item). 2025 value unchanged so the start year stays balanced.
def bctcr(y):
    if y <= 2025:
        return 0.8214
    if y >= 2035:
        return 0.78
    return round(0.8214 + (0.78 - 0.8214) * (y - 2025) / 10, 5)
rows = [["Unit: dimensionless (VERIFIED 2025 = USGS 69/84 domestic basis; declining to 0.78 by 2035 per 2021-25 PLC trend, judgment - see generator comments)"] + YEARS,
        ["BAU Clinker to Cement Ratio"] + [bctcr(y) for y in YEARS]]
write("BCtCR", "BCtCR.csv", rows)

# ---------------- MASCM: Maximum Annual SCM Supply for Cement ----------------
# Phase 4 build-up (2026-08-25, sources per verification dossier): fly ash
# used in concrete 14.6 Mt (ACAA 2024 survey, DIRECT) + CCPs to blended
# cement/clinker feed 5.3 Mt (ACAA - possible overlap with the concrete
# figure, flagged) + GGBFS <~4.8 Mt (USGS slag MCS: 16 Mt total slag sales,
# GGBFS <30% of tonnage, heavily import-dependent) + natural pozzolans ~1-2
# Mt (capacity ~2 Mt, NPA via secondary) = ~22 Mt current. Structurally
# DECLINING: fly ash falls with coal retirements (partially offset by pond
# harvesting), GGBFS falls with BF closures and rides imports. DRAFT
# trajectory: 22 Mt (2025) declining linearly to 15 Mt (2050). Non-binding
# at default blending levels; binds only under aggressive SCM policies.
def mascm(y):
    return round(22_000_000 + (15_000_000 - 22_000_000) * max(0, y - 2025) / 25)
rows = [["Unit: metric tons/year (Phase 4 build-up: ~22 MMT current from ACAA fly ash + USGS GGBFS + pozzolans, declining to 15 by 2050 - see generator comments)"] + YEARS,
        ["Maximum Annual SCM Supply for Cement"] + [mascm(y) for y in YEARS]]
write("MASCM", "MASCM.csv", rows)

# ---------------- SYCPbP: Start Year Clinker Production by Pathway ----------------
# DRAFT: all start-year (2025) clinker production attributed to the dry
# kiln with precalciner pathway (69 Mt, USGS 2025 clinker), since dry
# kiln with precalciner is essentially the entire existing US clinker
# fleet; CCS, electric kiln, and alternative chemistry cement are all
# pre-commercial in the US today.
prod = {"dry kiln with precalciner": 69_000_000, "dry kiln with CCS": 0,
        "electric kiln": 0, "alternative chemistry cement": 0}
rows = [["Unit: metric tons/year in start year (DRAFT; USGS 2025 clinker production, all attributed to dry kiln with precalciner - verify)", "Start Year Production"]]
for pw in PATHWAYS:
    rows.append([pw, prod[pw]])
write("SYCPbP", "SYCPbP.csv", rows)

# ---------------- SYCCU: Start Year Cement Capacity Utilization ----------------
# DRAFT: 0.69, i.e. 69 Mt clinker production over ~100 Mt reported US
# clinker nameplate capacity (USGS).
rows = [["Unit: dimensionless (DRAFT 69/100 Mt; USGS 2025 production over reported nameplate capacity - verify against USGS/PCA before release)", "Utilization"],
        ["Start Year Cement Capacity Utilization", 0.69]]
write("SYCCU", "SYCCU.csv", rows)

# ---------------- CPRS: Cement Preexisting Capacity Overhaul Decision Schedule ----------------
# Phase 2b DECISION SCHEDULE semantics: CPRS[Y] = NAMEPLATE capacity whose
# kiln campaign ends in year Y (overhaul-vs-replace decided endogenously by
# the CRSW-weighted two-option logit; retire-branch capacity exits
# production same-year and leaves the stock from Y+1). Built from fleet age
# cohorts (Princeton NZA Annex K: ~92 pre-2000 kilns ~49.6 Mt/yr nameplate
# + 38 post-2000 kilns ~46.7 Mt/yr; 35-yr campaign convention) because
# GEM's cement tracker records no kiln vintages. DRAFT: pre-2000 cohort
# decides 5.0 Mt/yr over 2026-2035; post-2000 cohort 4.7 Mt/yr over
# 2036-2045 (install years + ~35). Upgrade with PCA Plant Information
# Summary kiln-level data if access is granted.
# Phase 4 verification (2026-08-25): the cohort totals are CONFIRMED EXACTLY
# against NZA Annex K sec 6.3 (92 pre-2000 kilns = 49.6 Mt/yr; 38 post-2000
# = 46.7 Mt/yr). Schedule shape revised to match NZA's own convention: the
# pre-2000 cohort turns over at 7%/yr of its 49.6 Mt from 2026 (3.47 Mt/yr,
# exhausting ~2040 - NZA's post-2025 rate; its 3%/yr 2018-25 retirements are
# already embedded in the USGS 2025 capacity our stock initializes from);
# the post-2000 cohort reaches its 35-yr campaign end individually staggered
# over installs ~2000-2010, approximated as 4.7 Mt/yr over 2036-2045.
# Decision OUTCOME stays endogenous. Upgrade path: PCA Plant Information
# Summary kiln-level data (proprietary - EI access needed).
def cprs(pw, y):
    if pw != "dry kiln with precalciner":
        return 0
    total = 0
    # pre-2000 cohort: 7%/yr of 49.6 Mt from 2026 until the 49.6 exhausts
    # (14 x 3.47 = 48.58; remainder 1.02 in 2040)
    if 2026 <= y <= 2039:
        total += 3_470_000
    elif y == 2040:
        total += 1_020_000
    # post-2000 cohort: 35-yr staggered campaign ends, approximated flat
    if 2036 <= y <= 2045:
        total += 4_700_000
    return total
rows = [["Unit: metric tons/year nameplate reaching campaign-end decision (NZA Annex K cohorts confirmed exact; pre-2000 at NZA 7%/yr from 2026, post-2000 35-yr staggered 2036-45)"] + YEARS]
for pw in PATHWAYS:
    rows.append([pw] + [cprs(pw, y) for y in YEARS])
write("CPRS", "CPRS.csv", rows)

# ---------------- CPPL: Cement Pathway Campaign Length ----------------
# DRAFT: 35 years between kiln shell/drive overhaul decisions (Princeton NZA
# kiln-life convention; no public authoritative campaign source - the
# weakest-sourced parameter set, see Cement_Breakout_Research_Notes.md).
# Alternative chemistry 30 (matches its shorter CPAL). DISTINCT from CPAL
# asset life per the steel P23 lesson.
cppl = {"dry kiln with precalciner": 35, "dry kiln with CCS": 35,
        "electric kiln": 35, "alternative chemistry cement": 30}
rows = [["Unit: years between kiln overhaul decisions (DRAFT NZA 35-yr convention; weakest-sourced parameter - verify before release)", "Campaign Length"]]
for pw in PATHWAYS:
    rows.append([pw, cppl[pw]])
write("CPPL", "CPPL.csv", rows)

# ---------------- CRCC: Cement Overhaul Capital Cost per Unit Annual Capacity ----------------
# Phase 4 verification (2026-08-25): NO authoritative kiln overhaul/shell-
# replacement cost exists in public literature (targeted search: GCCA,
# IEEE-IAS/PCA Cement Conference, company disclosures - nothing citable;
# 1990s-era long-dry-to-precalciner CONVERSION studies ran $9-29/(t/yr) in
# then-year dollars). Generic manufacturing brownfield-modernization runs
# 40-70% of greenfield, but that describes full modernization - our ~10%
# represents a NARROW kiln shell/drive/controls overhaul buying one more
# campaign, between the refractory-only trivial case and full rebuild.
# Explicitly an EI engineering judgment (dry kiln updated to track the
# raised greenfield: 10% of 375); resolving data likely lives in PCA
# Cement Conference or member-only ECRA reports.
crcc = {"dry kiln with precalciner": 38, "dry kiln with CCS": 93,
        "electric kiln": 45, "alternative chemistry cement": 60}
rows = [["Unit: $/(metric ton/yr) overhaul (EI judgment ~10% of greenfield; no public source exists - see generator comments)", "Overhaul Capital Cost"]]
for pw in PATHWAYS:
    rows.append([pw, crcc[pw]])
write("CRCC", "CRCC.csv", rows)

# ---------------- CRSW: Cement Overhaul Shareweight ----------------
# DRAFT: 25 flat (steel's SRSW draft value) - calibration weight on the
# overhaul branch capturing unmodeled stickiness (site integration, quarry
# co-location, permitting); set so overhauling wins at default costs,
# reproducing observed multi-decade kiln longevity.
rows = [["Unit: dimensionless (DRAFT 25 flat, steel SRSW draft value - calibrate to observed fleet longevity)"] + YEARS,
        ["Cement Overhaul Shareweight"] + [25] * len(YEARS)]
write("CRSW", "CRSW.csv", rows)

# ---------------- CPCC: Cement Pathway Capital Cost per Unit Annual Capacity ----------------
# Phase 4 verification (2026-08-25): dry kiln with CCS $933 CONFIRMED
# EXACTLY (Princeton NZA Annex K Table 3, $3.5B / 3.75 Mt/yr, no learning;
# note the CCS increment it implies, ~$560/t, sits above CEMCAP European
# estimates and the Brevik retrofit ~$333/t - open uncertainty, likely
# transport/no-learning inclusions). Dry kiln with precalciner raised 300 ->
# 375: ECRA 2009 gives $180-350/t (2009$, size-dependent) and an IEA-cited
# ~EUR 263/t (2010, 1 Mt/yr); inflating ~$235/t (2009$) by construction-cost
# indices to 2026$ lands ~$370-400 [SNIPPET tier - primary ECRA/IEA PDFs not
# directly readable]. Electric kiln $450: NO cost data exists at any scale
# (pilot-only) - pure judgment. Alternative chemistry $600: an Nth-plant
# assumption; first-of-kind actuals are 5-8x higher (Brimstone ~$2,700/t,
# Sublime Holyoke ~$5,000/t at demo scale) with no published learning curve -
# strong caveat, team review item.
capex = {"dry kiln with precalciner": 375, "dry kiln with CCS": 933,
         "electric kiln": 450, "alternative chemistry cement": 600}
rows = [["Unit: $/(metric ton/yr) greenfield (CCS=NZA confirmed; dry kiln 375 = ECRA-inflated SNIPPET tier; electric/alt-chem judgment, FOAK actuals 5-8x higher - see generator comments)", "Capital Cost"]]
for pw in PATHWAYS:
    rows.append([pw, capex[pw]])
write("CPCC", "CPCC.csv", rows)

# ---------------- CPAL: Cement Pathway Asset Life ----------------
# Phase 4 verification (2026-08-25): the only public anchor is 35 years -
# Princeton NZA Annex K's kiln retirement age (EIA IDM's 30-yr assumption
# "extended by 5", matching the observed ~36-yr fleet age); NO source exists
# for 40-yr or vintage-differentiated lives. CPAL aligned to the anchor:
# 35/35/35/30. Note CPAL (asset life) and CPPL (campaign length) currently
# COINCIDE at these values - they remain separate inputs (steel P23 lesson)
# because for cement the overhaul campaign plausibly IS the economic life;
# revisit if kiln-level campaign data ever arrives.
life = {"dry kiln with precalciner": 35, "dry kiln with CCS": 35,
        "electric kiln": 35, "alternative chemistry cement": 30}
rows = [["Unit: years economic asset life (35 = NZA Annex K / EIA-IDM+5 anchor, the only public source; alt chem 30 judgment)", "Asset Life"]]
for pw in PATHWAYS:
    rows.append([pw, life[pw]])
write("CPAL", "CPAL.csv", rows)

# ---------------- CPSW: Cement Pathway Shareweight ----------------
# DRAFT placeholder entry-gate ramps (TBS convention): dry kiln with
# precalciner always eligible (incumbent); dry kiln with CCS ramps in from
# 2028; electric kiln from 2032; alternative chemistry cement from 2030.
# Ramp years are judgment calls pending team review, mirroring the
# structure (not calibration) of steel's SPSW.
# Gates revised in Phase 4 verification (2026-08-25): the May 30, 2025 DOE/
# OCED cancellation wave killed the Heidelberg Mitchell CCS ($500M),
# Brimstone ($189M), and Sublime ($87M) awards; Brevik (Norway) proves CCS
# at commercial scale but no US project has a live path; electric kilns are
# pilot-only (Heidelberg ELECTRA plasma first test Feb 2025, Coolbrook/
# Adani in development). Gates: CCS 2030 (was 2028), alternative chemistry
# 2033 (was 2030; Sublime Holyoke is 30 kt/yr demo scale), electric kiln
# 2035 (was 2032). Judgment ramp years, team review item.
def sw(pw, y):
    if pw == "dry kiln with precalciner":
        return 1
    if pw == "dry kiln with CCS":
        return 1 if y >= 2030 else 0
    if pw == "electric kiln":
        return 1 if y >= 2035 else 0
    if pw == "alternative chemistry cement":
        return 1 if y >= 2033 else 0
rows = [["Unit: dimensionless (entry gates revised per post-2025 DOE-cancellation project landscape: CCS 2030 / alt chem 2033 / electric 2035; team review)"] + YEARS]
for pw in PATHWAYS:
    rows.append([pw] + [sw(pw, y) for y in YEARS])
write("CPSW", "CPSW.csv", rows)

# ---------------- CEIbPaF: Cement Energy Intensity by Pathway and Fuel ----------------
# Phase 4 verification (2026-08-25): thermal 3.43 MMBtu/METRIC ton CONFIRMED
# = DOE Bandwidth Study 2017 Table 3-2 "current typical" dry pyroprocessing
# 1,554 Btu/lb x 2,204.6 lb/metric ton (a verification agent flagged a
# "discrepancy" using 2,000 lb/short ton - the metric conversion is correct);
# nothing newer supersedes it (GNR global ~3.3-3.5 MJ-basis is consistent).
# PCA 2023 fuel-mix totals CONFIRMED via PCA press release (NG 31% record,
# alt fuels 16%); the 33/20 coal-vs-petcoke split within the remaining 53%
# stays a documented judgment - no 2023 primary split exists, but MECS 2018
# (coal 41% : petcoke 24% of onsite fuel = ~63:37) is directionally
# consistent with our ~62:38. Electricity 142 kWh/t cement is within the
# MECS-2018-derived 132-142 range (re-derive from MECS Table 3.2 + USGS for
# release precision). CCS adders CORROBORATED: 2.1 MMBtu/t at ~0.72 tCO2/t
# captured = ~2.9 GJ/tCO2, inside IEAGHG 2018-TR03's with-heat-recovery band
# (3.1-3.3) and Brevik's reported 2.7-3.0 GJ/tCO2. Electric kiln 4.0 and
# alt-chem 2.5 MMBtu/t remain INTERNAL ENGINEERING ESTIMATES - neither
# Coolbrook nor Sublime has published an energy intensity.
# Apportionment (adversarial-review finding 3, 2026-08-24; the earlier
# draft's coal+petcoke+alt-fuel lump made module coal 1.58x the generic 239
# coal total - structurally impossible for a subset):
#   coal        33% -> hard coal if                 1.13e6 BTU/t
#   natural gas 31% -> natural gas if               1.06e6 BTU/t
#   petcoke     20% -> heavy or residual fuel oil if 0.69e6 BTU/t
#   alt fuels   16% -> biomass if                   0.55e6 BTU/t
# Petcoke booking hypothesis: the generic structure's odd 47.15 TBtu of
# heavy/residual-oil FEEDSTOCK for 239 (BIFUaF) matches module petcoke
# (0.686 MMBtu/t x 69 Mt ~= 47.4 TBtu) within ~1% - petcoke appears to be
# booked as resid feedstock in BIFU, making it cement's analog of steel's
# coking-coal feedstock (verify against the BIFU workbook at Phase 1b; the
# 33/20 coal/petcoke split within PCA's combined 53% is itself a DRAFT
# judgment). Alt fuels (tires/waste) ride the biomass element as nearest
# physical fit; generic 239 biomass is zero, so the share diagnostic reads
# 0 for biomass by ZIDZ - a known boundary item for the 1b calibration.
# Electricity 5.9e5 BTU/t: 142 kWh/t cement (PCA 2008 survey) / 0.8214
# clinker ratio = 173 kWh/t clinker x 3412 BTU/kWh. Dry kiln with CCS adds
# an amine-capture energy penalty (DRAFT): +2.1e6 BTU/t natural gas
# (capture steam) and +1.5e5 BTU/t electricity (capture auxiliaries).
# Electric kiln and alternative chemistry cement are electricity-only
# placeholders (4.0e6 and 2.5e6 BTU/t) pending literature verification.
lit = {
    "dry kiln with precalciner":    {"electricity if": 590_000, "hard coal if": 1_130_000, "natural gas if": 1_060_000,
                                     "heavy or residual fuel oil if": 690_000, "biomass if": 550_000},
    "dry kiln with CCS":            {"electricity if": 590_000 + 150_000, "hard coal if": 1_130_000, "natural gas if": 1_060_000 + 2_100_000,
                                     "heavy or residual fuel oil if": 690_000, "biomass if": 550_000},
    "electric kiln":                {"electricity if": 4_000_000},
    "alternative chemistry cement": {"electricity if": 2_500_000},
}
rows = [["Unit: BTU/metric ton clinker (DRAFT: DOE Bandwidth 2017 thermal x PCA 2023 fuel mix; coal 33%/NG 31%/petcoke->resid 20%/alt fuels->biomass 16%; CCS adds amine energy; electric kiln/alt chem placeholders - verify before release)"] + FUELS]
for pw in PATHWAYS:
    rows.append([pw] + [lit[pw].get(f, 0) for f in FUELS])
write("CEIbPaF", "CEIbPaF.csv", rows)

# ---------------- CCF: Calcination CO2 Factor by Pathway ----------------
# Net process CO2 per t clinker (g CO2/t), Phase 2a. Dry precalciner and
# electric kiln: 510,000 g/t - CONFIRMED Phase 4 (2026-08-25): EPA GHGI
# Eq. 4-1, EF = 0.650 CaO x (44.01/56.08) = 0.510, identical in the
# 1990-2023 edition (NOTE: that edition was never officially posted by EPA;
# the public copy is EDF's FOIA release - cite the official 1990-2022
# edition for the factor). Updated anchors: cement process CO2 40.6 MMT
# (2023) / 41.9 (2022, official); lime 11.5 (2023) / 12.2 (2022). Dry kiln
# with CCS: 51,000 (90% capture DRAFT judgment - capture energy is in
# CEIbPaF; captured-tons ledger/45Q integration deferred to the CCS-
# framework reconciliation). Alternative chemistry cement: 0 (non-carbonate
# binder).
ccf = {"dry kiln with precalciner": 510_000, "dry kiln with CCS": 51_000,
       "electric kiln": 510_000, "alternative chemistry cement": 0}
rows = [["Unit: g CO2/metric ton clinker net of pathway-integral capture (DRAFT: EPA GHGI 0.510 t/t calcination factor; CCS 90% capture judgment; verify before release)", "Calcination CO2 Factor"]]
for pw in PATHWAYS:
    rows.append([pw, ccf[pw]])
write("CCF", "CCF.csv", rows)

print("\nDone. 14 input CSVs written under", ROOT)
