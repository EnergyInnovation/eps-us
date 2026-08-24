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
# DRAFT: flat 84 MMT/yr. Source: USGS Mineral Commodity Summaries 2026,
# reported 2025 US cement production ~84 Mt. Held flat pending an AEO- or
# PCA-anchored growth trajectory.
rows = [["Unit: metric tons/year (DRAFT flat 84 MMT; USGS MCS2026 2025 production - anchor to AEO/PCA before release)"] + YEARS,
        ["BAU Cement Demand"] + [84_000_000] * len(YEARS)]
write("BCD", "BCD.csv", rows)

# ---------------- BCtCR: BAU Clinker to Cement Ratio ----------------
# DRAFT: 0.8214 flat = USGS 2025 DOMESTIC clinker production (69 Mt) over
# BCD (84 Mt). Imported clinker (~0.66 Mt) is deliberately EXCLUDED
# (adversarial-review finding 4, 2026-08-24): the module's demand basis is
# domestically produced clinker, so including imports made the module build
# 1.04 Mt of greenfield capacity in the start year to "replace" imports.
# With 0.8214, start-year clinker demand equals SYCPbP exactly and the
# start year opens balanced. Clinker trade stays dollar-side via IESE.
# WRI's commonly cited US clinker ratio is 0.88 - flagged for team
# reconciliation (likely an apparent-consumption basis difference).
rows = [["Unit: dimensionless (DRAFT 0.8214 flat; USGS 2025 domestic clinker 69/84 - imported clinker excluded so start year opens balanced; WRI cites 0.88, reconciliation flagged)"] + YEARS,
        ["BAU Clinker to Cement Ratio"] + [0.8214] * len(YEARS)]
write("BCtCR", "BCtCR.csv", rows)

# ---------------- MASCM: Maximum Annual SCM Supply for Cement ----------------
# DRAFT: 25 MMT/yr flat, judgment placeholder. Fly ash + slag + pozzolan
# supply build-up (coal-plant retirements shrinking fly ash supply over the
# horizon, offset by growing slag/pozzolan/limestone-calcined-clay supply)
# is not yet modeled; this is a static judgment call pending that build-up.
rows = [["Unit: metric tons/year (DRAFT 25 MMT flat; judgment placeholder - fly ash/slag/pozzolan supply build-up pending, verify before release)"] + YEARS,
        ["Maximum Annual SCM Supply for Cement"] + [25_000_000] * len(YEARS)]
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

# ---------------- CPRS: Cement Preexisting Capacity Retirement Schedule ----------------
# DRAFT: conservative age-based placeholder - 1.0 Mt/yr of dry kiln with
# precalciner NAMEPLATE (the schedule subtracts from a nameplate stock)
# retiring 2027-2036 (~10 Mt over the decade, roughly 10% of the start-year
# fleet), all other pathways/years zero. TIMING CONVENTION (adversarial-
# review finding 2, 2026-08-24): CPRS[Y] is the retirement FLOW during year
# Y; with Euler INTEG the stock reflects it from Y+1, so scheduled tons
# disappear from the capacity stock in 2028-2037. Author real schedules
# with that one-year lag in mind (or move to steel's same-year-decision
# form, which arrives anyway when this is recast to a decision schedule in
# Phase 2b).
def cprs(pw, y):
    if pw == "dry kiln with precalciner" and 2027 <= y <= 2036:
        return 1_000_000
    return 0
rows = [["Unit: metric tons/year (DRAFT ~10 Mt conservative age-based retirement of dry kiln with precalciner 2027-2036; recast to decision schedule in Phase 2b, verify before release)"] + YEARS]
for pw in PATHWAYS:
    rows.append([pw] + [cprs(pw, y) for y in YEARS])
write("CPRS", "CPRS.csv", rows)

# ---------------- CPCC: Cement Pathway Capital Cost per Unit Annual Capacity ----------------
# DRAFT: dry kiln with precalciner ($300/(t/yr)) and electric kiln/
# alternative chemistry cement ($450 / $600) are judgment placeholders;
# dry kiln with CCS ($933/(t/yr)) is scaled from the Princeton Net-Zero
# America study's cited cement CCS retrofit cost of ~$3.5B for a 3.75 Mt/yr
# clinker line (3.5e9 / 3.75e6 ~= 933).
capex = {"dry kiln with precalciner": 300, "dry kiln with CCS": 933,
         "electric kiln": 450, "alternative chemistry cement": 600}
rows = [["Unit: $/(metric ton/yr) greenfield (DRAFT; dry kiln/electric kiln/alt chem judgment placeholder, CCS = Princeton NZA $3.5B/3.75Mt - verify before release)", "Capital Cost"]]
for pw in PATHWAYS:
    rows.append([pw, capex[pw]])
write("CPCC", "CPCC.csv", rows)

# ---------------- CPAL: Cement Pathway Asset Life ----------------
# DRAFT placeholders: dry kiln with precalciner and dry kiln with CCS 40
# years (typical cement plant/kiln life), electric kiln 35 years (newer,
# less field experience), alternative chemistry cement 30 years (novel
# process, conservative shorter assumed life pending data).
life = {"dry kiln with precalciner": 40, "dry kiln with CCS": 40,
        "electric kiln": 35, "alternative chemistry cement": 30}
rows = [["Unit: years economic asset life (DRAFT placeholder - verify before release)", "Asset Life"]]
for pw in PATHWAYS:
    rows.append([pw, life[pw]])
write("CPAL", "CPAL.csv", rows)

# ---------------- CPSW: Cement Pathway Shareweight ----------------
# DRAFT placeholder entry-gate ramps (TBS convention): dry kiln with
# precalciner always eligible (incumbent); dry kiln with CCS ramps in from
# 2028; electric kiln from 2032; alternative chemistry cement from 2030.
# Ramp years are judgment calls pending team review, mirroring the
# structure (not calibration) of steel's SPSW.
def sw(pw, y):
    if pw == "dry kiln with precalciner":
        return 1
    if pw == "dry kiln with CCS":
        return 1 if y >= 2028 else 0
    if pw == "electric kiln":
        return 1 if y >= 2032 else 0
    if pw == "alternative chemistry cement":
        return 1 if y >= 2030 else 0
rows = [["Unit: dimensionless (DRAFT placeholder entry gates; ramp shapes pending team review)"] + YEARS]
for pw in PATHWAYS:
    rows.append([pw] + [sw(pw, y) for y in YEARS])
write("CPSW", "CPSW.csv", rows)

# ---------------- CEIbPaF: Cement Energy Intensity by Pathway and Fuel ----------------
# DRAFT: dry kiln with precalciner intensities from DOE Bandwidth Study
# 2017 (3.43 MMBtu/t clinker thermal) apportioned by PCA's 2023 reported
# fuel mix, RE-BOOKED per adversarial-review finding 3 (2026-08-24; the
# earlier draft's coal+petcoke+alt-fuel lump made module coal 1.58x the
# generic 239 coal total - structurally impossible for a subset):
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
# electric kiln: 510,000 g/t (EPA GHGI calcination emission factor 0.510
# tCO2/t clinker; electrification changes combustion, not chemistry). Dry
# kiln with CCS: 51,000 (90% capture DRAFT judgment - capture energy is in
# CEIbPaF; captured-tons ledger/45Q integration deferred to the CCS-framework
# reconciliation). Alternative chemistry cement: 0 (non-carbonate binder).
ccf = {"dry kiln with precalciner": 510_000, "dry kiln with CCS": 51_000,
       "electric kiln": 510_000, "alternative chemistry cement": 0}
rows = [["Unit: g CO2/metric ton clinker net of pathway-integral capture (DRAFT: EPA GHGI 0.510 t/t calcination factor; CCS 90% capture judgment; verify before release)", "Calcination CO2 Factor"]]
for pw in PATHWAYS:
    rows.append([pw, ccf[pw]])
write("CCF", "CCF.csv", rows)

print("\nDone. 11 input CSVs written under", ROOT)
