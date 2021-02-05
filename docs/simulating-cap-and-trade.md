---
layout: page
title:  "Simulating a Cap-and-Trade Policy"
---

## Background

The Energy Policy Simulator (EPS) includes a policy lever that allows you to specify a carbon tax rate.  It does not include an explicit lever for a carbon cap (in a cap-and-trade system).

It is possible to convert a carbon cap to an equivalent carbon tax rate, enter this rate in the EPS, and obtain all the outputs of interest that the EPS typically provides.  Perhaps the simplest way to make this conversion is to look up the quantity of emissions abatement demanded by the cap in a published marginal abatement cost (MAC) curve, which contains data on the cost to abate a ton of CO<sub>2</sub> as a function of how many tons of CO<sub>2</sub> have already been abated.  A MAC curve must be particular to the modeled country or region, and if the cap-and-trade policy enforces different caps on different sectors, each covered sector must have its own MAC curve.

We do not wish to use this approach in the EPS.  This is for two reasons.  First, it can be difficult or impossible to locate reliable MAC curves for all regions that we wish to simulate.  Second, in the real world, a MAC curve is not static, but dynamic.  The curve shifts depending on what other, complementary policies are in place alongside the carbon cap.  Also, a published MAC curve likely involves assumptions or data choices different from those in the EPS's input dataset, so a particular emissions level reported by the EPS may not correspond precisely to the equivalent number on the published MAC curve.  Therefore, a static MAC curve from a third-party source is not the best method of converting a carbon cap into an equivalent tax rate.

Fortunately, it is possible to use the EPS itself to identify the carbon tax rate that is equivalent to the permit price under a cap-and-trade system.  This allows you to use any combination of policies (or no other policies) alongside the carbon cap, does not require additional data sources, and it works for any region for which an EPS has been built, even if no published MAC curves exist.

## Using the Cap-and-Trade Python Script

To model a cap-and-trade policy, you will need to know five things about the policy you wish to model:
* Which sectors does it cover?  (The EPS supports: transportation, electricity generation, residential buildings, commercial buildings, and industry.)
* What is the permitted quantity of emissions under the cap?  This may be particular to each covered sector, or it may be a sum of emissions from all covered sectors.
* If the cap has a price floor, what is it?
* If the cap has a price ceiling, what is it?
* What complementary policies (non-carbon-pricing, non-BAU policies) will be in effect alongside the carbon cap, if any?

The permitted quantity of emissions, price floor, and price ceiling typically change each year under a cap-and-trade policy.  You need these values for **each year** for which you wish to use the EPS to determine the emissions permit price.

The `CreateCarbonCapToTaxScript.py` Python script is designed to facilitate determining the emissions permit price under a cap.  A single run of the script is sufficient to find the permit prices in each modeled year.  Detailed instructions on how to set up the script are included in comments within the script itself, but briefly, you set up the script by specifying:

* The complementary policies `.cin` file, if you wish to use complementary policies alongside the carbon cap
* The number of the policy implementation schedule you wish to use**<sup>[1]</sup>**
* The price floor (the lowest floor among the years for which you want to determine permit prices)**<sup>[2]</sup>**
* The price ceiling (the highest ceiling among the years for which you want to determine permit prices)**<sup>[2]</sup>**
* Which sectors are covered under the cap

**[1]** You may use any sensible carbon pricing implementation schedule at this point, such as a linear ramp-in from the first year the policy takes effect until the last year that the cap gets stricter.  If you know the cap quantities in each year, the best approach may be to design a schedule that phases in (approaches 1) in proportion to the rate at which the cap declines (approaches the lowest cap value among all simulated years).  For example, if the model run goes from 2018-2050, and the cap begins at 5000 MMT/yr in 2020, declines linearly to 1000 MMT/yr in 2040, then stays constant thereafter, your schedule would be: (2018, 0), (2020, 0), (2040, 1), (2050, 1).  The schedule you create now will not be the final schedule you will use to represent the cap-and-trade policy.  You will set the final schedule based on modeled permit prices (described below).  You simply need a reasonable schedule here (i.e. instead of setting the implementation percentage to 100% in every year) because carbon pricing has temporal path-dependent effects, due to stock turnover of various types of capital equipment, and we want to account for this path dependency when identifying permit prices.

**[2]** Remember to adjust the floor and cap in the script to account for your chosen policy implementation schedule.  The script specifies the carbon tax lever setting that will be used, which is fully in effect only in years with an implementation value of 1.  Therefore, you must INCREASE the floor and ceiling values in the script if you are testing a year where the implementation schedule is less than one.  For example, if you are interested in the emissions permit price in 2030, and the policy schedule for the carbon tax in 2030 is 0.5 (i.e. 50% implemented), then the 2030 floor and 2030 ceiling prices (from the carbon cap legal text) must be doubled to obtain the lever settings to enter in the script.  If interested in permit prices in multiple years, FIRST adjust all the floor and ceiling prices to reflect the carbon tax policy implementation schedule, THEN enter the lowest floor and the highest ceiling prices in the script.

Pay special attention to the control levers and policy levers that alter the carbon tax's coverage scope.  The control levers `BEPEfCT Boolean Exempt Process Emissions from Carbon Tax` and `BENCEfCT Boolean Exempt Non CO2 Emissions from Carbon Tax` determine whether certain types of emissions are covered by carbon pricing, and the policy levers `Toggle Whether Carbon Tax Affects Process Emissions` and `Toggle Whether Carbon Tax Affects Non CO2 Emissions` reverse the behaviors specified in these control levers.  The control levers were set when the EPS for the region you are simulating was built, and you should not need to adjust them.  If your carbon cap policy behaves differently (for example, if the control lever does not exempt non-CO<sub>2</sub> gases, but the cap-and-trade policy you wish to model does exempt non-CO<sub>2</sub> gases), then you must enable the `Toggle Whether Carbon Tax Affects Non CO2 Emissions` in your ComplementaryPolicies `.cin` file.

The file `OutputVarsForCarbonCapToTaxScript.lst` already includes the variables you are most likely to need, but if the carbon cap you are simulating considers emissions from a different part of the energy system, you can add more emissions output variables to the list.  (Note that although the default emissions output variables in this file are in CO<sub>2</sub>e, not CO<sub>2</sub>, you do not need CO<sub>2</sub>-specific output variables to simulate a carbon cap that exempts non-CO<sub>2</sub> gases.  You simply need to ensure the control and policy levers correctly describe your policy, as described in the prior paragraph.)

## Interpreting the Script's Output

Run the Python script to generate a Vensim command script, then run the Vensim command script.  It produces an output file containing the policy implementation schedule for the carbon tax, as well as emissions levels for each sector (and total across the economy, with and without LULUCF emissions) at each carbon price tier.  (The sectors do not add up to the total, as they exclude emissions from certain activities that are not within any sector subject to carbon pricing in the EPS, such as agriculture, water + waste, hydrogen supply, etc.)

First, sum the rows containing emissions from the covered sectors (or refer to the appropriate economy-wide total, if the cap you are simulating is applied economy-wide).  For example, if you are simulating a carbon cap on the buildings sector, you should sum the "residential buildings sector" and "commercial buildings sector" rows.  It is often convenient to use Excel's "filter" to hide rows that contain emissions data for parts of the economy not relevant to the simulated carbon cap policy.

Then, in each year of interest:

1. The tested carbon tax lever settings appear in column C.  Multiply these lever settings by the carbon tax implementation schedule value in the year you are testing.  For example, if in year 2030, the carbon tax implementation schedule says 0.5, then multiply all values in column C by 0.5, to obtain the carbon tax rate that the EPS actually tested in year 2030.

2. Look up that year's emissions cap quantity from among the displayed rows.

	* If the emissions from the run at that year's price floor are below that year's cap quantity, the price floor is the permit price.

	* If the emissions from the run at that year's price ceiling are above that year's cap quantity, the price ceiling is the permit price.

	* If the emissions at that year's cap quantity fall in between that year's price floor and price ceiling, find the price whose emissions are closest to that year's cap quantity.  This is the permit price.

3. Repeat these steps for each year of interest, remembering to reset the tested carbon tax settings in column C each time, so they can be updated for each tested year's carbon tax implementation schedule value.  An Excel sheet can be set up to do this analysis quickly by making one tested carbon prices column for each simulated year and using `VLOOKUP()` to compare the cap quantity to the range of modeled quantities.

## Simulating Independent Caps on Different Sectors

If the carbon cap policy you are simulating imposes independent caps on different sectors, you must run the Python script and perform the analysis described above for each sector or set of sectors that has its own, independent cap.  For example, suppose the industry sector is capped at X tons, the electricity generation sector is capped at Y tons, and they can’t trade permits with each other.  In this case, you need to run the script twice, once per sector, as you are finding permit prices in two independent markets.

## Using Discovered Permit Prices in a Scenario

Once you know the emissions permit price in each year, you may simulate the carbon cap alongside its complementary policies (if any), to obtain a rich and detailed set of EPS outputs.

First, open the policy implementation schedule file you used when running the Python script.  In the year of highest permit price, enter "1" in the `cross carbon tax` schedule.  For all other years, enter the fraction of that year's permit price divided by the highest year's permit price.  For example, if the highest permit price was found to be $40/ton in 2040, and the price was found to be $30/ton in 2030, enter ordered pairs (2040, 1) and (2030, 0.75).

Depending on whether your permit prices fit a neat trend, you may not need to enter an ordered pair for every modeled year.  You may be able to approximate the carbon price trend using the linear interpolation capabilities of FoPITY.  However, if you want to simulate the discovered permit prices exactly, you likely will need to enter an ordered pair for every year of the model run when carbon pricing is in effect (plus zero in the first year, and zero in the last year before carbon pricing comes into effect).

Update the schedule number in the blue tabs, save a copy of FoPITY under a new name and export the blue tabs as `.csv` files, using filenames based on the updated tab names.

In Vensim, open the EPS model, enter SyntheSim mode, and load your `ComplementaryPolicies.cin` file.  Set the Policy Implementation Schedule Selector to the schedule number you just assigned to your new FoPITY file.  Set the carbon tax lever on each covered sector to the value of the permit price in the highest year ($40 in our example above).  Finally, save a new `.cin` file, using a descriptive name.  This `.cin` file saves your complete policy package, including the cap-and-trade policy and complementary policies.  You may now perform analysis using this scenario as you would any other policy scenario.  Remember that it can be recreated in the web interface and shared with others, if you prefer to use the web interface rather than Vensim to analyze your policy package.