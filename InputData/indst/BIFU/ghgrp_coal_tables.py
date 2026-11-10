"""Write GHGRP subpart C coal tables for the BIFU workbook.

Usage: <python> -I ghgrp_coal_tables.py <download dir> <out dir>
Outputs:
  ghgrp_coal_facilities_2023.csv  one row per facility: id, name, state, NAICS, EPS industry, coal (MMBtu)
  ghgrp_coal_by_naics.csv         coal (trillion Btu) by NAICS and year, 2011-2023, with EPS industry
Energy is backed out of reported CH4 (see ghgrp_coal.py). Facilities outside industry (utilities,
universities, government, etc.) get EPS industry "(not industry)".
"""
import csv, glob, json, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ghgrp_coal import CO2_EF, CH4_PER_MMBTU_CO2E, f

GLASS = ("327211", "327212", "327213", "327215", "327993")
STEEL = ("331110", "331111", "331112", "331221", "331222", "331210", "3312", "331511")

def eps_industry(n):
    n = str(n)
    if n.startswith("111") or n.startswith("112") or n.startswith("113") or n.startswith("114") or n.startswith("115"):
        return "agriculture and forestry 01T03"
    if n.startswith("2121") or n.startswith("213113"): return "coal mining 05"
    if n.startswith("211") or n.startswith("213"): return "oil and gas extraction 06"
    if n.startswith("212"): return "other mining and quarrying 07T08"
    if n.startswith("311") or n.startswith("312"): return "food beverage and tobacco 10T12"
    if n[:3] in ("313", "314", "315", "316"): return "textiles apparel and leather 13T15"
    if n.startswith("321"): return "wood products 16"
    if n[:3] in ("322", "323"): return "pulp paper and printing 17T18"
    if n == "325193": return "refined petroleum and coke 19"   # EPS counts ethanol plants in refining
    if n.startswith("324199"): return "iron and steel 241"         # BPFUbIP mapping convention (coke)
    if n.startswith("324"): return "refined petroleum and coke 19"
    if n.startswith("325"): return "chemicals 20"
    if n.startswith("326"): return "rubber and plastic products 22"
    if n.startswith(GLASS): return "glass and glass products 231"
    if n.startswith("327"): return "cement and other nonmetallic minerals 239"
    if n.startswith(STEEL) or n.startswith("3312"): return "iron and steel 241"
    if n.startswith("331"): return "other metals 242"
    if n.startswith("332"): return "metal products except machinery and vehicles 25"
    if n.startswith("333"): return "other machinery 28"
    if n.startswith("334"): return "computers and electronics 26"
    if n.startswith("335"): return "appliances and electrical equipment 27"
    if n.startswith("3364"): return "nonroad vehicles 30"
    if n.startswith("336"): return "road vehicles 29"
    if n[:3] in ("337", "339"): return "other manufacturing 31T33"
    if n.startswith("486"): return "energy pipelines and gas processing 352T353"
    if n.startswith("562") or n.startswith("22131") or n.startswith("22132"): return "water and waste 36T39"
    if n[:2] == "23": return "construction 41T43"
    return "(not industry)"

def coal_by_facility(d, year):
    fac = {r["facility_id"]: r for r in json.load(open(os.path.join(d, f"fac_{year}.json")))}
    rows = []
    for p in glob.glob(os.path.join(d, f"coal_{year}_*.json")):
        rows += json.load(open(p))
    seen = set(); out = collections.defaultdict(float)
    for r in rows:
        ft = r.get("fuel_type")
        if ft not in CO2_EF:
            continue
        key = (r["facility_id"], r.get("unit_name"), ft)
        if key in seen:
            continue
        seen.add(key)
        ch4 = sum(f(r.get(k)) for k in ("tier1_ch4_emissions_co2e", "tier2_ch4_emissions_co2e",
                                         "tier3_ch4_emissions_co2e", "tier4_ch4_emissions_co2e",
                                         "part_75_ch4_emissions_co2e"))
        out[r["facility_id"]] += ch4 / CH4_PER_MMBTU_CO2E
    return fac, out

def main():
    d, o = sys.argv[1], sys.argv[2]
    fac, mm = coal_by_facility(d, 2023)
    with open(os.path.join(o, "ghgrp_coal_facilities_2023.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["facility_id", "facility_name", "state", "naics_code", "EPS industry", "coal_MMBtu_2023"])
        for fid, v in sorted(mm.items(), key=lambda x: -x[1]):
            r = fac.get(fid, {})
            n = r.get("naics_code") or ""
            w.writerow([fid, r.get("facility_name"), r.get("state"), n, eps_industry(n), round(v, 1)])
    years = [2011, 2014, 2018, 2022, 2023]
    tab = collections.defaultdict(dict)
    for y in years:
        fac_y, mm_y = coal_by_facility(d, y)
        for fid, v in mm_y.items():
            n = str(fac_y.get(fid, {}).get("naics_code") or "?")
            tab[n][y] = tab[n].get(y, 0.0) + v / 1e6
    with open(os.path.join(o, "ghgrp_coal_by_naics.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["naics_code", "EPS industry"] + [f"coal_TBtu_{y}" for y in years])
        for n in sorted(tab, key=lambda k: -max(tab[k].values())):
            w.writerow([n, eps_industry(n)] + [round(tab[n].get(y, 0.0), 2) for y in years])

if __name__ == "__main__":
    main()
