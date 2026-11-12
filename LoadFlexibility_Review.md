# Industrial and data-center load flexibility: review notes

**Branch:** `load-flexibility`, cut from develop at 41b7c541 (2026-11-12).
**Status:** built and tested; ready for review.
**About this file:** it is a review aid. Remove it before the branch merges into develop, because eps-us does not keep memos in the repo.

## What the branch adds

A policy that makes part of an industry's (or data centers') electricity use move out of the tightest hours of each day and into the other hours of the same day. It stands for policies that pay or require large loads to be flexible:
- time-of-use or real-time pricing;
- interruptible service;
- flexible-interconnection deals for data centers;
- on-site storage.

Daily electricity use does not change; only its timing does. Dispatch, the storage and demand-response peak shaving, the reliability (reserve-margin) requirement, capacity builds, electricity prices and emissions all respond through the existing electricity chain.

A second policy pays for the peak reduction this delivers, per megawatt per year. Ratepayers fund it through electricity rates, the same way the existing demand-response program is paid.

### New policy levers (all default to zero)

| Lever | Units | Schedule element |
|---|---|---|
| `Flexible Share of Industrial Electricity Load[Industry Category]` | share of the load in the tightest hours that moves | `indst load flexibility X <industry>` (25) |
| `Flexible Share of Data Center Electricity Load` | same | `bldgs data center load flexibility X` |
| `Load Flexibility Payment per Unit Peak Reduction` | $/MW-year | `elec load flexibility payment X` |

### New inputs

| Input | Default | Meaning |
|---|---|---|
| `LFAH Load Flexibility Avoided Hours per Day` (`InputData/elec/LFAH`) | 4 | How many of each day's tightest hours flexible load stays out of. Matches the 4-hour demand-response event length. |
| `LFDT Load Flexibility Day Types[Electricity Timeslice]` (`InputData/elec/LFDT`) | 1 for all six day types | Which day types load shifts on. All 1 = every day (time-of-use style). Representative days set to 0 = peak days only (interruptible or demand-response style). |

## How it works (Electricity Supply – Main, band "Flexible Industrial and Data Center Load")

1. **Pick the tightest hours.**
   - `Last Year Spare Potential Output from Surviving Capacity by Hour` lags the existing spare-capacity measure by one year, to avoid a same-year loop.
   - `Load Flexibility Hour Tightness Rank` ranks the hours of each day type by that spare capacity.
   - `Load Flexibility Avoided Hour Flag` marks the LFAH tightest hours on the day types LFDT allows.
2. **Why spare capacity and not price.** The thermal-battery charging window ranks hours by marginal dispatch cost, but that cost is nearly flat in this model: a $1–3/MWh spread across a day through 2040. On the two net-peak day types its most expensive hours are overnight. Spare capacity is tightest at hours 18–21 in every day type and year, which are the hours that set the reliability requirement.
3. **Move the load.**
   - `Industrial Electricity Shifted by Hour from Load Flexibility[Electricity Timeslice, Hour, Industry Category]` removes the flexible share of the load in the avoided hours.
   - It returns that energy to the other hours of the same day, in proportion to the industry's own load × last year's spare capacity (`Load Flexibility Refill Weight`). The returned load therefore leans toward hours with surplus wind and solar.
   - The variable is a net change by hour that sums to zero over each day. `Data Center Electricity Shifted by Hour from Load Flexibility` does the same for data centers, using the new `Data Center Electricity Demand by Hour`.
4. **Hook-in points.**
   - Both shifted variables are added inside `Total Electricity Demand by Hour before Distributed Generation and Thermal Battery Charging`.
   - The industrial one is also added to `Output Industrial Electricity Demand by Hour and Industry Category`, so the existing hourly graphs show the shift.
   - Carbon-capture electricity is not shifted.
5. **Payments** (Electricity Supply – Cash Flow, section "Paying for Peak-Hour Load Reduction").
   - `Industrial Load Flexibility Peak Reduction` (MW) is the average load removed in the avoided hours of the two net-peak day types. It is multiplied by the payment rate to give `Industrial Load Flexibility Payments`; data centers work the same way.
   - `Total Load Flexibility Payments` is added to:
     - `Electricity Supplier Other Expenditures` (and from there into rates);
     - `Electricity Sector Change in Nonenergy Expenditures by Entity[electricity suppliers]`;
     - `Electricity Sector Change in Revenue by Entity[nonenergy industries]`;
     - `Electricity Subtotal Change in OM Expenditures`.
   - `Load Flexibility Payments by Recipient ISIC Code` books each industry's payment to its own industry code. Data centers go to ISIC 62T63, IT and information services. The existing demand-response program instead spreads its payment by electricity spending.
   - Like the demand-response payment, it is treated as payment for a service, so it stays in industry revenue at the input-output handoff.

## Files changed

- `EPS.mdl`:
  - 21 new equation blocks and 7 edited equations;
  - diagram additions on Electricity Supply – Main, Electricity Supply – Cash Flow, Policy Control Center (levers), Policy Implementation Schedule ("This Year" values), Cost Outputs and Web Application Support Variables (consumer shadows).
- `InputData/elec/LFAH/`, `InputData/elec/LFDT/`: CSVs plus workbooks with About tabs.
- `InputData/plcy-schd/FoPITY/`: the 19 schedule files gain 27 elements at the end, and the generator script gains the matching entries. The regenerated files keep the old content as a byte-identical prefix.
- `WebAppData.xlsx`: 3 Policy Characteristics rows and 27 PolicyLevers rows. The ID chain is contiguous to 3182.
- `InputData/acronym-key.xlsx`: LFAH and LFDT.

## Checks done

- **Zero policy:** all 14,270 exported series are bit-identical to develop 41b7c541, before and after the diagram edits. The error log is banner-only.
- **Energy conservation:** each industry's daily electricity per day type is conserved to within 2e-6.
- **Diagram checker:** no new problems on any touched view. The three new levers count as unconnected, as every lever on Policy Control Center does.

## Test results (US, zero-policy base)

Test setting: 25% flexible share for all industries and data centers, payment $50,000/MW-year, default schedule (ramping to the full value by 2050).

| | 2030 | 2040 | 2045 | 2050 |
|---|---|---|---|---|
| Load moved out of the tightest hours on peak days, GW | 8 | 34 | 48 | 63 |
| Fossil and nuclear capacity, GW | 0 | −20 | −30 | −24 |
| Grid batteries, GW | 0 | −7 | −10 | −8 |
| Solar / wind, GW | 0 / 0 | +2 / −30 | +102 / −40 | +104 / −43 |
| Industry electricity price | +0.03% | −1.5% | −1.0% | −0.4% |
| Total CO2e, Mt (daily shifting) | +0.1 | +8 | −22 | −43 |
| Total CO2e, Mt (peak days only) | +0.1 | +10 | +2 | −9 |

- **Payments:** $25.5B in total over 2025–2050.
- **Industry only at a 10% share:** 6 GW less fossil capacity, 3 GW fewer batteries and 8–9 Mt less CO2e by 2045–2050, with $6.1B in payments.
- **Avoided-window test, 4 vs 5 vs 6 hours:** about the same avoided firm-plus-battery capacity (21–41 GW). A wider window trades firm capacity for batteries, and 4 hours gave the largest emissions cut. The default stays at 4.

**How to read these:**
- **Avoided capacity is about half the load moved.** About 200 GW of grid batteries already flatten the evening peak in the base run, and the reliability step re-sizes the fleet around the lower need. Flexible load mainly substitutes for battery duty and the last firm plants.
- **Nothing happens to capacity before about 2037,** because the system has surplus capacity until then. Early years show only the payment cost on rates.
- **Daily shifting raises the value of solar and lowers the value of wind.** Moving load into high-spare midday hours causes more solar and less wind to be built. 2040 emissions rise because wind falls before the extra solar arrives.
- **Do not use capacity-market dollars as the benefit measure.** With flexibility, the system sits at the point where the capacity market switches on, and it flips between $0 and about $85–90B from year to year. The cumulative savings swing from $108B to $334B depending on the window. This is the known lumpy capacity-market behavior; report avoided capacity instead.

## What the model does not capture

- **Customer-level price signals.** Industry pays one annual average rate, so the flexible customer's own savings are not modeled: time-of-use, demand and coincident-peak charges, and interruptible discounts. System savings reach everyone through the pooled rate.
- **Energy-price value of shifting.** It is understated, because hourly prices in the model are nearly flat (no scarcity pricing).
- **Behavior and costs.** The flexible share is set by policy, not chosen by producers. There is no cost of being flexible (oversized equipment, storage, labor scheduling). There is no plant-level scheduling, location, or interconnection queue.

## Questions for the reviewer

1. Is a payment basis of average megawatts removed in the avoided hours of peak days sensible, or should it be the reduction at the single tightest hour?
2. Should the payment be treated as a service, like demand response (kept in industry revenue at the input-output handoff), or as a transfer?
3. Is ISIC 62T63 the right recipient code for data centers?
4. Refill weighting (the industry's own load × spare capacity): does that represent how flexible plants would reschedule?
5. Plausible default ranges for the industrial share by industry: roughly 5–15% overall, higher for electrolysis, arc-furnace steel, chlor-alkali, cement grinding, air separation and pulp. These ranges are not yet sourced.
6. Follow-ups worth doing:
   - a government-funded payment option, which needs a new government cash-flow type;
   - letting flexible load see a cheaper electricity price in the electrification choice;
   - a fix for the capacity market's on/off behavior.
