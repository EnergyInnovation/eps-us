# Calibration

Region-specific calibration data and results for this EPS model. The code that produces them is the
team's `eps-calibrate` skill (agentic-age `skills/eps-calibrate/scripts/`, mirrored to
`~/.claude/skills/eps-calibrate/` on every machine); nothing in this folder is executable.

```
calibration/
  README.md            this file
  calibration-log.md   dated record of every calibration performed on this model
  export-vars.lst      the SAVELIST the steps' BAU export draws from (edit if a step needs more variables)
  benchmarks/          observed data the steps read: vehicle sales, technology shares, electricity
                       generation/capacity/price (see benchmarks/README.md; provenance in sources.md)
  out/<step>/          each step's results: results.json, charts, verification overlays
  runs/                headless run exports (*.tab, git-ignored)
```

Run from this folder's parent (the model root):

```
py "%USERPROFILE%\.claude\skills\eps-calibrate\scripts\run_bau_export.py" --name base
py "%USERPROFILE%\.claude\skills\eps-calibrate\scripts\run_all.py" --base calibration/runs/base.tab --tag r1
py "%USERPROFILE%\.claude\skills\eps-calibrate\scripts\sync_workbooks.py" --dry --tab calibration/runs/r1_final.tab
```
