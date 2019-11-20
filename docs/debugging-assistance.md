---
layout: page
title:  "Debugging Assistance"
---

The debugging assistance sheet is a tool for developers who edit the Energy Policy Simulator (EPS) model file, EPS.mdl.  This requires a copy of Vensim DSS or Vensim Pro, the editor tiers that support subscripts.  Unless you plan on editing the structure or subscripts of the model (not just swapping the input data), you can likely disregard the debugging assistance sheet.

The sheet essentially tests for two conditions that should be true, irrespective of any edits to the model structure:

* When all policy levers are disabled, the change in emissions (of all pollutants, in all sectors) should be zero.  That is, when there are no policies enabled, the policy case should equal the BAU case.
* No matter which policies are enabled (if any), the sum of all changes in cash flows should equal zero.  This is true because whenever an actor pays money, someone else must receive that money.  Hence, all negative cash flows for one actor are balanced by positive cash flows for other actor(s).

## Testing Change in Pollutants

To test that the change in pollutant emissions is zero when policies are disabled, simply [run the model](running-the-model.html), then examine the contents of the "Change in Total CO2e Emissions" variable in the upper left, as shown in the following screenshot:

![debugging change in total CO2e emissions](debugging-assistance-ChngTotEmis.png)

In the event that this variable has any non-zero values, first check to make sure that all policies are disabled.  (This is the default, if you run the model without adjusting any policy levers.)  If all policies are disabled and there is still a non-zero result for this variable, you can check the sector-specific totals below to determine which sector(s) are the source of the difference between the policy and BAU cases.  Once you have identified the problematic sector(s), you must then examine their "Main" and "BAU" sheets to track down the problem.  Problems with inequality of the policy and BAU cases when all policy levers are disabled usually stem from a change made to a "Main" sheet that was accidentally omitted from a corresponding "BAU" sheet.

Note that by default, changes in electricity price affect demand in all three demand sectors, and changing demand in the demand sectors affects electricity price.  Therefore, an inequality in one sector can cause inequalities to appear in other sectors, even if those other sectors are structurally sound.  There are a few options you may consider to prevent this effect from interfering with your ability to find the bug.  First, the change in the problematic sector is often of a larger magnitude than the change in other sectors, which are just feeling the effects of slight differences in electricity prices.  Second, there is a one-year delay in the adjustment of electricity price in response to policy effects or changes in demand, so sometimes the problematic sector will show a deviation that starts one year earlier than the deviation in other sectors.  Finally, you can enable the "Boolean Prevent Policies from Affecting Electricity Prices" lever on the "Policy Control Center" page (and ensure that policy is scheduled to take effect during all years of the model run- see the help doc on [Adjusting Policy Implementation Schedules](adjusting-plcy-impl-schd.htm) for details).  If that is the only policy that is enabled, it should not introduce differences between the policy and BAU cases in a structurally sound model.

## Testing Sums of Cash Flow Changes

To test that the sum of all cash flows total zero, simply run the model.  The sum of Changes in Cash Flows should be approximately zero, irrespective of which policies are enabled and their settings.

Due to rounding error in Vensim, when policies are enabled, the sum will not quite equal zero.  It will tend to bounce around chaotically, usually within +/- $1 million of zero.  For example, here is the relevant structure, shown with a policy package that contains many enabled policies:

![debugging change in total cash flows](debugging-assistance-ChngTotCash.png)

Below, you can see a graph of the "Sum of Changes in Cash Flows" variable (for this example policy package):

![graph of sum of changes in total cash flows](debugging-assistance-CashGraph.png)

This is a good result.  Variance is chaotic and stays within +/- $60,000 of zero.  This is an indication that the variance is due to rounding error, rather than to bugs in the model's cash flow calculations.

A result that indicates the presence of a bug will tend to be a trend (where the sum of changes in cash flows only grows or only shrinks during the whole model run) and will generally exceed +/- $1 million (often by a large margin- sometimes in the billions of dollars).  This usually means that a new policy cost relationship was introduced into one of the "cash flow" sheets, but the inverse cash flow was not applied to the recipient of the dollars spent due to this new policy cost relationship (or the would-be recipient, in the case of dollars that are _not_ spent due to the policy).

In the event there is a bug, you can examine the sector-specific cash flow totals below, and the cash flow totals for specific industries to the right, to determine where the problem(s) may lie.  All of these totals should equal zero, accounting for chaotic variance due to rounding error.  (When a cash flow is generated in any sector, the recipient of that cash flow is also assigned within that sector.  This is why the same actor, such as "government," has cash flows generated by tax receipts separately from every sector that involves taxes.  This is what allows us to test each sector independently for a total cash flow summing to zero.)  The total for specific industries on the right refers not to calculations done within a sector, but to the mapping of cash flow impacts from the various sectors onto more meaningful industry categories that is done on the [Cumulators sheet](cumulators.html).