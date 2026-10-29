"""DRAFT-input generator for the steel pathway module (Phases 1a-1b).
Regenerates the shipped CSVs from the calibration logic documented in
Steel_1b_Carveout_Memo.md. The per-variable xlsx workbooks are the canonical
source going forward; this script is kept for traceability of the 2026-08-20
draft values and to rerun the BIFU/BPFUbIP level calibration if the underlying
data change. Portable: paths are repo-relative. BF BOF with CCS shareweight is
deliberately zero until the Phase 2 CCS block wires its capture economics
(45Q-style credits, retrofit capex) - without them the pathway would compete
on incomplete costs.

Original notes: SEIbPaF is
level-calibrated so start-year pathway-weighted energy by fuel reproduces the
model's BIFU-based iron-and-steel process-end-use energy plus feedstock
(D13; AEO2026 Table 30 cross-checks within a few percent). Literature sets
pathway DIFFERENCES; a common per-ton adder per fuel carries downstream/
finishing energy shared by all routes. Data updates from primary verification:
MASSfS 70 Mt flat (USGS 2025e consumption 57 + exports 13); H2-DRI electricity
1,160 kWh/t ex-electrolyzer (Vogl et al. 2018 derived); SPRS GEM-conservative
(only units with expiring campaigns and no planned reline retire).
"""
import csv, os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "InputData", "indst")
YEARS = list(range(2021, 2051))
PATHWAYS = ["traditional BF BOF", "BF BOF with CCS", "natural gas DRI",
            "hydrogen DRI", "molten oxide electrolysis", "aqueous electrolysis", "scrap EAF"]
FUELS = ["electricity if", "hard coal if", "natural gas if", "biomass if",
         "petroleum diesel if", "heat if", "crude oil if", "heavy or residual fuel oil if",
         "LPG propane or butane if", "hydrogen if", "green hydrogen if", "low carbon hydrogen if"]

BIFU_FILE = {"electricity if": "electricity", "hard coal if": "coal", "natural gas if": "natural-gas",
             "biomass if": "biomass", "petroleum diesel if": "petroleum-diesel", "heat if": "heat",
             "crude oil if": "crude-oil", "heavy or residual fuel oil if": "heavy-or-residual-oil",
             "LPG propane or butane if": "LPG-propane-or-butane", "hydrogen if": "hydrogen",
             "green hydrogen if": "green-hydrogen", "low carbon hydrogen if": "lowcarbon-hydrogen"}
BPF_FILE = {"electricity if": "electricity", "hard coal if": "hard-coal", "natural gas if": "natural-gas",
            "biomass if": "biomass", "petroleum diesel if": "petroleum-diesel", "heat if": "heat",
            "crude oil if": "crude-oil", "heavy or residual fuel oil if": "hvy-resid-fuel-oil",
            "LPG propane or butane if": "LPG", "hydrogen if": "hydrogen",
            "green hydrogen if": "green-hydrogen", "low carbon hydrogen if": "lowcarbon-hydrogen"}

def write(folder, name, rows):
    d = os.path.join(ROOT, folder)
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, name)
    with open(p, "w", newline="") as f:
        for r in rows:
            f.write(",".join(str(x) for x in r) + "\n")
    print("wrote", p)

def read_csv(path):
    with open(path, newline="") as f:
        return list(csv.reader(f))

def bifu_2025(kind, fuel):
    """kind: 'fE' or 'aF'; returns iron-and-steel 2025 value in BTU."""
    rows = read_csv(os.path.join(ROOT, "BIFU", f"BIFU{kind}-{BIFU_FILE[fuel]}.csv"))
    hdr = rows[0]
    col = next(i for i, h in enumerate(hdr) if h.strip() == "2025")
    for r in rows[1:]:
        if r and r[0].strip().lower().startswith("iron and steel"):
            v = r[col].strip()
            return float(v) if v else 0.0
    return 0.0

def process_endues_share(fuel):
    """Sum of the first 8 process columns (process end uses) for iron & steel;
    falls back to the fallback file when the 241 row is absent or all-zero."""
    def row_share(rows, key):
        for r in rows[1:]:
            if r and r[0].strip().lower().startswith(key):
                vals = [float(x) if x.strip() else 0.0 for x in r[1:12]]
                return sum(vals[:8]), sum(vals)
        return None
    rows = read_csv(os.path.join(ROOT, "BPFUbIP", f"BPFUbIP-{BPF_FILE[fuel]}.csv"))
    got = row_share(rows, "iron and steel")
    if got and got[1] > 0:
        return got[0] / got[1]
    fb = read_csv(os.path.join(ROOT, "BPFUbIP", "BPFUbIP-fallback.csv"))
    got = row_share(fb, fuel.replace(" if", "").lower())
    if got and got[1] > 0:
        return got[0] / got[1]
    return 1.0  # no data: treat all as process

# ---------------- BSD ----------------
rows = [["Unit: metric tons/year (DRAFT flat 80 MMT; USGS MCS 2026 shows 79.5-85.8 range 2021-25 with 82 in 2025e - anchor to AEO before release)"] + YEARS,
        ["BAU Steel Demand"] + [80_000_000] * len(YEARS)]
write("BSD", "BSD.csv", rows)

# ---------------- SYSPbP ----------------
prod = {"traditional BF BOF": 24_000_000, "BF BOF with CCS": 0, "natural gas DRI": 4_000_000,
        "hydrogen DRI": 0, "molten oxide electrolysis": 0, "aqueous electrolysis": 0,
        "scrap EAF": 52_000_000}
rows = [["Unit: metric tons/year in start year (DRAFT; GEM GIST 2024 partial-coverage production and AISI shares - verify)", "Start Year Production"]]
for pw in PATHWAYS:
    rows.append([pw, prod[pw]])
write("SYSPbP", "SYSPbP.csv", rows)

# ---------------- SYSCU ----------------
write("SYSCU", "SYSCU.csv", [["Unit: dimensionless (AISI 2024-2025 avg utilization; USGS 2026 capacity 105 Mt corroborates - verify)", "Utilization"],
                             ["Start Year Steel Capacity Utilization", 0.76]])

# ---------------- SPSW ----------------
def sw(pw, y):
    if pw in ("traditional BF BOF", "natural gas DRI", "scrap EAF"): return 1
    if pw == "BF BOF with CCS": return 0
    if pw == "hydrogen DRI": return 0.25 if y >= 2028 else 0
    if pw == "molten oxide electrolysis": return 0.05 if y >= 2032 else 0
    if pw == "aqueous electrolysis": return 0.05 if y >= 2031 else 0
rows = [["Unit: dimensionless (DRAFT placeholder entry gates; ramp shapes pending team review)"] + YEARS]
for pw in PATHWAYS:
    rows.append([pw] + [sw(pw, y) for y in YEARS])
write("SPSW", "SPSW.csv", rows)

# ---------------- MASSfS ----------------
rows = [["Unit: metric tons/year (DRAFT - USGS MCS 2026: 2025e consumption 57 + exports 13 = ~70 Mt domestic availability; held flat pending US-specific forward estimate)"] + YEARS,
        ["Maximum Annual Scrap Supply"] + [70_000_000] * len(YEARS)]
write("MASSfS", "MASSfS.csv", rows)

# ---------------- SPRS (GEM GIST June 2026 V1 informed) ----------------
# Conservative BAU: only operating units whose campaign is expiring with NO
# planned reline in GIST retire on schedule. Units with planned relines
# (Gary BF14 2026, Burns Harbor C/D 2027, Middletown BF3 2027, Edgar Thomson
# BF3/BF1 2030) are assumed to continue; cost-based/policy retirement takes
# over in Phase 2/3. Question flagged for team: how aggressive should
# scheduled BAU BF retirements be?
# P2-B recast (Dan 2026-08-20): SPRS is no longer a retirement schedule but
# tons of nameplate capacity reaching a reline-or-replace DECISION each year
# (GEM GIST June 2026 V1 reline data: announced planned-reline years where
# present, last completed reline + 20 yr campaign otherwise). The outcome is
# chosen endogenously in the model. GEM iron capacities (ttpa) are scaled to
# module nameplate (production / SYSCU) so the whole start-year stock decides.
SCALE_BF = (24_000_000 / 0.76) / 24_595_000
bf_decisions = {2026: 2_540_000,                          # Gary BF14 (reline announced 2026)
                2027: 2_480_000 + 2_480_000 + 2_090_000,  # Burns Harbor C+D, Middletown BF3 (planned 2027)
                2028: 1_270_000,                          # Granite City B (campaign end, none planned)
                2030: 1_270_000 + 1_500_000,              # Edgar Thomson BF3+BF1 (planned 2030)
                2033: 1_370_000,                          # Cleveland BF6 (2013+20)
                2036: 1_361_000,                          # Gary BF8 (2016+20)
                2038: 1_234_000,                          # Gary BF6 (2018+20)
                2040: 1_360_000,                          # Gary BF4 (2020+20)
                2041: 4_200_000,                          # Indiana Harbor BF7 (2021+20)
                2042: 1_440_000}                          # Cleveland BF5 (2022+20)
ngdri_decisions = {2040: 2_440_000,                       # Cliffs Toledo HBI (2020+20, scaled)
                   2043: 1_300_000, 2044: 1_300_000}      # Nucor Louisiana (~30 yr from 2013, scaled)
def sprs(pw, y):
    if pw == "traditional BF BOF": return round(bf_decisions.get(y, 0) * SCALE_BF)
    if pw == "natural gas DRI": return ngdri_decisions.get(y, 0)
    if pw == "scrap EAF":
        # 68.4 Mt nameplate fleet / ~25 yr rebuild cycle, spread over exactly one
        # campaign (2025-2049) so the whole start-year fleet decides once; from
        # 2050 the DELAY FIXED recurrence carries the relined 2025 cohort back,
        # so a nonzero 2050 schedule row would double-decide ~2.7 Mt (review
        # finding, 2026-09-25). Years before the start year are irrelevant to
        # the model and zeroed for consistency.
        return 2_740_000 if 2025 <= y <= 2049 else 0
    return 0
rows = [["Unit: metric tons/year of nameplate capacity reaching a reline-or-replace decision (DRAFT from GEM GIST June 2026 V1; decision outcome is endogenous)"] + YEARS]
for pw in PATHWAYS:
    rows.append([pw] + [sprs(pw, y) for y in YEARS])
write("SPRS", "SPRS.csv", rows)

# ---------------- SRCC: reline capital cost ----------------
# Anchor: Gary BF14 full reline $350M / 2,540 ttpa ~= $138/(t/yr). Other
# pathways: ~15% of greenfield as placeholder (no public data found).
rcc = {"traditional BF BOF": 138, "BF BOF with CCS": 138, "natural gas DRI": 105,
       "hydrogen DRI": 158, "molten oxide electrolysis": 150, "aqueous electrolysis": 225,
       "scrap EAF": 75}
rows = [["Unit: $/(metric ton/yr) reline or rebuild (DRAFT - Gary BF14 $350M/2.54Mt anchor; others ~15% of greenfield placeholder)", "Reline Capital Cost"]]
for pw in PATHWAYS:
    rows.append([pw, rcc[pw]])
write("SRCC", "SRCC.csv", rows)

# ---------------- SRSW: reline shareweight ----------------
# Calibration weight on the reline branch capturing unmodeled stickiness
# (product-mix/quality requirements, site integration, switching costs), set
# so relining wins at default costs - reproducing the fleet-wide reline
# behavior GEM documents - while a strong carbon tax still flips the
# decision. DRAFT pending calibration review.
rows = [["Unit: dimensionless (DRAFT calibration weight for the reline branch; verify against observed reline behavior)"] + YEARS,
        ["Reline Shareweight"] + [25] * len(YEARS)]
write("SRSW", "SRSW.csv", rows)

# ---------------- SEIbPaF: literature route values, then D13 level calibration ----------------
lit = {
    "traditional BF BOF":        {"electricity if": 1_194_000, "hard coal if": 15_170_000, "natural gas if": 1_422_000},
    "BF BOF with CCS":           {"electricity if": 2_047_000, "hard coal if": 15_170_000, "natural gas if": 1_422_000},
    "natural gas DRI":           {"electricity if": 2_389_000, "natural gas if": 9_952_000},
    "hydrogen DRI":              {"electricity if": 3_956_000, "natural gas if": 474_000, "hydrogen if": 6_255_000},
    "molten oxide electrolysis": {"electricity if": 13_650_000},
    "aqueous electrolysis":      {"electricity if": 10_240_000},
    "scrap EAF":                 {"electricity if": 1_536_000, "natural gas if": 474_000},
}
total_prod = sum(prod.values())
report = []
cal = {pw: {} for pw in PATHWAYS}
for f in FUELS:
    fe, af = bifu_2025("fE", f), bifu_2025("aF", f)
    pe_share = process_endues_share(f)
    target = fe * pe_share + af
    module_sy = sum(prod[pw] * lit[pw].get(f, 0) for pw in PATHWAYS)
    if target <= 0 and module_sy == 0:
        for pw in PATHWAYS:
            cal[pw][f] = lit[pw].get(f, 0)
        continue
    # hard coal is route-specific (coking coal for the BF route), not common
    # downstream energy: scale it on coal-using pathways rather than spreading
    # an adder onto routes that burn no coal.
    if f == "hard coal if" and module_sy > 0:
        scale = target / module_sy
        for pw in PATHWAYS:
            cal[pw][f] = lit[pw].get(f, 0) * scale
        report.append(f"{f}: target {target/1e12:,.1f} TBtu (fE {fe/1e12:.1f} x pe {pe_share:.3f} + aF {af/1e12:.1f}), lit-module {module_sy/1e12:,.1f} TBtu -> route-specific scale {scale:.3f}")
        continue
    adder = (target - module_sy) / total_prod
    if adder >= 0:
        for pw in PATHWAYS:
            cal[pw][f] = lit[pw].get(f, 0) + adder
        mode = f"additive adder {adder:,.0f} BTU/t"
    else:
        scale = target / module_sy if module_sy > 0 else 0
        for pw in PATHWAYS:
            cal[pw][f] = lit[pw].get(f, 0) * scale
        mode = f"multiplicative scale {scale:.3f}"
    report.append(f"{f}: target {target/1e12:,.1f} TBtu (fE {fe/1e12:.1f} x pe {pe_share:.3f} + aF {af/1e12:.1f}), lit-module {module_sy/1e12:,.1f} TBtu -> {mode}")

rows = [["Unit: BTU/metric ton crude steel (DRAFT: literature route values plus common per-ton adder calibrated to BIFU-based 2025 process-end-use + feedstock energy by fuel; see Steel_1b_Carveout_Memo.md)"] + FUELS]
for pw in PATHWAYS:
    rows.append([pw] + [round(cal[pw].get(f, 0)) for f in FUELS])
write("SEIbPaF", "SEIbPaF.csv", rows)
print("\nCALIBRATION REPORT:")
for r in report:
    print(" ", r)

# ---------------- SPCC / SPPL ----------------
capex = {"traditional BF BOF": 1200, "BF BOF with CCS": 1600, "natural gas DRI": 700,
         "hydrogen DRI": 1050, "molten oxide electrolysis": 1000, "aqueous electrolysis": 1500,
         "scrap EAF": 500}
rows = [["Unit: $/(metric ton/yr) greenfield (DRAFT placeholder; verify vs IEA/MPP/DOE Liftoff)", "Capital Cost"]]
for pw in PATHWAYS:
    rows.append([pw, capex[pw]])
write("SPCC", "SPCC.csv", rows)

life = {"traditional BF BOF": 20, "BF BOF with CCS": 20, "natural gas DRI": 25,
        "hydrogen DRI": 25, "molten oxide electrolysis": 20, "aqueous electrolysis": 20,
        "scrap EAF": 25}
rows = [["Unit: years (DRAFT placeholder - BF campaign/reline vs EAF life; GEM shows capacity-weighted 11.7 yr since last reline; verify)", "Lifetime"]]
for pw in PATHWAYS:
    rows.append([pw, life[pw]])
write("SPPL", "SPPL.csv", rows)

# ---------------- SPAL: asset life (split from SPPL campaign length, review F6) ----------------
al = {"traditional BF BOF": 40, "BF BOF with CCS": 40, "natural gas DRI": 40,
      "hydrogen DRI": 40, "molten oxide electrolysis": 30, "aqueous electrolysis": 30,
      "scrap EAF": 40}
rows = [["Unit: years economic asset life (DRAFT - site lives through several reline campaigns; verify)", "Asset Life"]]
for pw in PATHWAYS:
    rows.append([pw, al[pw]])
write("SPAL", "SPAL.csv", rows)
