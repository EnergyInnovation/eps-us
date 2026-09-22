# Stock-size test (2026-09-22)

Two BAU runs identical except SoCDTtiNTY/ANVCV (committed vs pinned-mode inputs), exporting fleet fuel
economy, cargo distance by technology, fuel use, vehicles and sales. Result: LDV stock -16% in 2050, fuel
and CO2 -0.5%, fleet fuel economy within 0.5% - the stock level does not reach energy or emissions because
cargo distance is exogenous and vehicles x miles/vehicle = distance is not enforced anywhere. Details in
calibration-log.md (2026-09-21/22 entries) and the team KB, eps/transportation/vehicle-sales-logit.md.
`_stocktest2.py` swaps the inputs and runs both cases; `_stocktest2_report.py` tabulates 2050 fuel economy.
