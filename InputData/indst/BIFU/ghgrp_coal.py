"""Coal burned at industrial facilities reporting to EPA's Greenhouse Gas Reporting Program
(subpart C, stationary combustion), by NAICS code - an independent check on MECS and AEO.

Usage: <python> -I ghgrp_coal.py <download dir> <year> [<year> ...]
The download dir holds, per year, coal_<year>_<fueltype>.json from
  https://data.epa.gov/efservice/C_FUEL_LEVEL_INFORMATION/REPORTING_YEAR/=/<year>/FUEL_TYPE/CONTAINING/<type>/JSON
(types Bituminous, Subbituminous, Lignite, Anthracite, Mixed) and fac_<year>.json from
  https://data.epa.gov/efservice/PUB_DIM_FACILITY/YEAR/=/<year>/JSON

Energy per unit and fuel is recovered from the reported CH4 (CO2e): subpart C computes CH4 as heat
input x 1.1e-2 kg CH4/MMBtu for coal (40 CFR 98 Table C-2) for every tier, CEMS units included,
and the program used GWP 25 for CH4 through reporting year 2023. So MMBtu = CH4 CO2e (t) x 1000 /
(0.011 x 25). Where CO2 is reported by fuel (tiers 1-3) the script also converts CO2 with Table C-1
factors as a cross-check. Coal coke and petroleum coke are not counted.
Limits: covers only facilities above the reporting threshold (25,000 t CO2e/yr); coal burned in
units reported under subpart D (electric generating units with a utility NAICS) is not here.
"""
import json, os, sys, glob, collections

CO2_EF = {"Bituminous": 93.28, "Subbituminous": 97.17, "Lignite": 97.72, "Anthracite": 103.69,
          "Mixed (Industrial sector)": 94.67, "Mixed (Electric Power sector)": 95.52,
          "Mixed (Commercial sector)": 94.27}  # kg CO2/MMBtu, Table C-1
CH4_PER_MMBTU_CO2E = 0.011 * 25 / 1000.0          # t CO2e per MMBtu

def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0

def main():
    d = sys.argv[1]
    for year in sys.argv[2:]:
        fac = {r["facility_id"]: r for r in json.load(open(os.path.join(d, f"fac_{year}.json")))}
        rows = []
        for p in glob.glob(os.path.join(d, f"coal_{year}_*.json")):
            rows += json.load(open(p))
        seen = set(); by = collections.defaultdict(lambda: [0.0, 0.0, set()])
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
            co2 = sum(f(r.get(k)) for k in ("tier1_co2_combustion_emissions", "tier2_co2_combustion_emissions",
                                             "tier3_co2_combustion_emissions"))
            naics = str(fac.get(r["facility_id"], {}).get("naics_code") or "?")
            b = by[naics]
            b[0] += ch4 / CH4_PER_MMBTU_CO2E / 1e6            # trillion Btu, from CH4
            b[1] += co2 * 1000 / CO2_EF[ft] / 1e6              # trillion Btu, from CO2 (tiers 1-3 only)
            b[2].add(r["facility_id"])
        out = sorted(((n, v[0], v[1], len(v[2])) for n, v in by.items()), key=lambda x: -x[1])
        print(f"== {year}: coal at subpart C units, trillion Btu (from CH4; from CO2 where reported), facilities")
        groups = collections.defaultdict(float)
        for n, e, e2, nf in out:
            if e >= 0.5:
                print(f"  {n:8s} {e:8.1f} {e2:8.1f} {nf:4d}  {fac_name(fac, by, n)}")
            g = ("311221 wet corn milling" if n == "311221" else "325193 ethanol" if n == "325193" else
                 "325 other chemicals" if n.startswith("325") else "311-312 other food" if n[:3] in ("311", "312") else
                 "322 paper" if n.startswith("322") else "327 nonmetallic minerals" if n.startswith("327") else
                 "324 petroleum and coal products" if n.startswith("324") else "331 primary metals" if n.startswith("331") else
                 "22 utilities" if n.startswith("22") else "other " + n[:3])
            groups[g] += e
        for g, e in sorted(groups.items(), key=lambda x: -x[1]):
            print(f"  [group] {g:32s} {e:8.1f}")

def fac_name(fac, by, naics):
    ids = list(by[naics][2])[:2]
    return "; ".join(str(fac.get(i, {}).get("facility_name"))[:30] for i in ids)

if __name__ == "__main__":
    main()
