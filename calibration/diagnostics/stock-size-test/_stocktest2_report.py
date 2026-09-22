import sys, json
from pathlib import Path
sys.path.insert(0, str(Path.home() / '.claude/skills/eps-calibrate/scripts'))  # lib lives in the skill
from lib.tab import Tab
O = Tab('calibration/runs/stocktest2_original.tab'); P = Tab('calibration/runs/stocktest2_pinned.tab')
FE='BAU Fleet Avg Fuel Economy'; V='BAU Vehicles'; D='BAU Cargo Dist Transported by Vehicle Technology'; F='BAU Transportation Sector Fuel Used'
techs=['gasoline vehicle','diesel vehicle','battery electric vehicle','plugin hybrid vehicle','natural gas vehicle','LPG vehicle','hydrogen vehicle']
for cargo in ('passenger','freight'):
    print(f"\n=== LDVs {cargo}, 2050")
    print(f"{'tech':26}{'FE orig':>12}{'FE pinned':>12}{'ratio':>8}{'veh orig':>12}{'veh pinned':>12}{'dist orig':>12}{'dist pinned':>12}")
    for t in techs:
        k=('LDVs',cargo,t)
        if k not in O.data[FE]: continue
        fo,fp=O.value(FE,2050,*k),P.value(FE,2050,*k)
        vo,vp=O.value(V,2050,*k),P.value(V,2050,*k)
        do,dp=O.value(D,2050,*k),P.value(D,2050,*k)
        print(f"{t:26}{fo:12.4g}{fp:12.4g}{fp/fo if fo else float('nan'):8.3f}{vo/1e6:11.1f}M{vp/1e6:11.1f}M{do:12.3g}{dp:12.3g}")
# series for chart
out={'years':O.years}
for cargo in ('passenger','freight'):
    for t in ('gasoline vehicle','battery electric vehicle'):
        k=('LDVs',cargo,t)
        out[f'{cargo}|{t}|orig']=O.series(FE,*k); out[f'{cargo}|{t}|pinned']=P.series(FE,*k)
json.dump(out, open('calibration/runs/stocktest2_fe.json','w'))
