---
layout: page
title:  "Assumptions and Limitations"
---

In order to create a computer model that is less complex than the real world, it is necessary to make a number of assumptions and simplifications.  Similarly, model capabilities and results may be affected by limitations in the available data.  This page documents some of the more important assumptions and limitations in the Energy Policy Simulator (EPS), to provide context when working with the model or interpreting its results.

If you are seeking an explanation for a difference between EPS results and either historical data or the outputs of a different model, see the [Comparing Results to Reality or Other Models](comparing-results.md) page.

## Uncertainty is Greater with More or Stronger Policies

Many policies in the EPS have effects that are numerically defined in the model based on scientific studies and others' modeling results.  For example, the effect of improved appliance labeling on the energy efficiency of newly sold appliances is drawn from a study and used as input data in the EPS.  Other policies specify their effects by definition (for example, a tax applied to coal increases the price of coal by the amount specified by the user), but the elasticity of demand for coal with respect to coal price in a given sector must be drawn from a suitable study or model.

Studies investigating individual policies or economic relationships typically did so under a particular set of real-world conditions, which cannot reflect all possible combinations of policy settings that a user might select in the EPS.  In the real world, the coefficients or elasticities that relate certain policies to the quantities they affect would likely change depending on the social and economic environment in which those policies were enacted.  For example, the effect of a feebate of a given magnitude on the efficiency of newly sold cars would likely be lower in a scenario with a high carbon tax, as the higher gasoline costs caused by the carbon tax already cause many price-conscious consumers to opt for more efficient vehicles.  The remaining car buyers may be price-insensitive and would therefore be less influenced by the feebate, so the feebate has less effect than it would in a scenario without a carbon tax.  (You could also think of this effect as a carbon tax having less influence on car buyers in a world with a feebate.  There is no "implementation ordering" of policies in the EPS: they are all simulated at once.)

Generally, the model's business-as-usual (BAU) case is likely to be closest to the conditions under which the various policies were analyzed in the original studies used as input data for the EPS.  Therefore, the uncertainty of policy effects is likely smallest when few policies are used and enabled policies are set at low values.  Uncertainty increases as the policy package includes a greater number of policies and the settings of those policies become more extreme.

## Characterizing Uncertainty Numerically is Not Possible

Almost all of the input data used in the EPS lack numerical uncertainty bounds.  Even if such bounds had been available, it would have been difficult to carry them through the complex model calculations to establish uncertainty bounds on the final result.

As an alternative, the Policy Solutions model supports Monte Carlo analysis, which can highlight the sensitivity of the model results to changes in any particular input or set of inputs.  A user who lacks confidence in a particular value may run a Monte Carlo simulation, varying the suspect value within the range that he/she believes is reasonable, to obtain a probability distribution for whichever outputs in which he/she is interested.

## EPS Policies Imply Actions, Not Targets

The EPS contains policy levers that imply specific actions (with one exception: the Renewable Portfolio Standard).  Examples include taxing carbon emissions, setting a fuel economy standard for trucks, retiring industrial facilities early, afforesting or reforesting a specific amount of land, and so forth.  However, some things that are "policies" in the real world do not imply specific actions, but rather, set a target to be met via unknown actions.  For example, a carbon cap (as in a cap-and-trade system) specifies a total allowable quantity of emissions but does not specify which actions will be undertaken to meet that target.

The model is designed to predict the outcomes of specific combinations of policy actions, not to seek an "optimal" set of policy actions to meet a specific target within Vensim.  Therefore, policies that consist of setting targets to be met via unknown actions are not included in the set of policy control levers offered by the EPS.  (The Renewable Portfolio Standard is met via the same decision logic that the EPS uses to determine what electricity sources to build in other circumstances, but limiting the selection to RPS-qualifying sources.)

This does not mean that the EPS cannot help a user understand the effect of a policy that sets a target.  The truth is that there are many (likely infinitely many) different combinations of actions that would result in compliance with the target.  The [Testing Policy Permutations Python script](testing-policy-permutations.html) developed for use with the model enables users to search across many of combinations of policy settings to find ones that optimize particular outputs.  For example, if a user has a maximum allowable carbon emissions in mind (a carbon cap), he/she can perform thousands of runs of the model while varying policies of interest, discard all of the results with carbon emissions in excess of the cap, and sort the remaining scenarios by another metric of interest (such as least cost).  The result will be a set of policies that imply specific actions that, when taken together, achieve the emissions target at least cost.
