---
layout: page
title:  "How the EPS Avoids Double Counting Policy Effects"
---

## About Double Counting and Policy Types

The EPS has been designed to avoid double-counting the effects of policies on model results, such as emissions reductions or cash flow changes.  This means that if Policy A abates two tons of CO<sub>2</sub>e, and Policy B abates two tons of CO<sub>2</sub>e, then when the user enables Policies A and B together, the total abatement will only be four tons if the policies are completely non-interacting.  If one of the tons abated by each policy is the "same" ton, then the model will count that abatement only once, so that the total abatement of Policies A and B together will be three tons.  It is crucial that the model be able to avoid double-counting policy effects in its results in order to accurately assess the effects of packages consisting of many interacting policies.

This can pose a challenge for pricing policies (especially a carbon tax), which may incentivize a wide variety of actions to reduce emissions.  For example, a carbon tax applied to the Transportation sector may make driving fossil fuel-powered vehicles more expensive, reducing demand for travel.  It may also increase the attractiveness of electric vehicles (EVs) relative to fossil fuel-powered vehicles, leading to a change in the market shares of these types of vehicles.  In other words, it may lead both to a shift in demand for transportation services and to technology switching.

In the Energy Policy Simulator, some actions that may be undertaken to lower emissions are either price-driven or are governed by a separate policy lever particular to that action, not both.  For example, changes in demand for building services (such as how often occupants choose to use their lights, air conditioning, or cooking appliances) are price-driven; there is no policy lever that allows the user to explicitly set a reduction in demand for building services.  In contrast, industries converting their manufacturing processes that run on natural gas to run on electricity is governed by a separate policy lever (an industrial electrification policy), and this conversion will not be undertaken solely due to changes in the cost of natural gas or electricity.

## Combining Multiple Policies

Multiple pricing policies combine together without difficulty: they each influence the final price, and the final price determines the action undertaken.  Multiple non-pricing policies usually also combine together without difficulty, as each policy typically specifies the point at which it influences action, and each policy can be modeled at that point in the calculation flow, "seeing" effects of upstream policies as having already happened in the current model year.

It can be more challenging to combine pricing effects and non-pricing policies without double counting.  There are essentially two ways to achieve this: either the separate policy lever is specifically defined to be additive to any price-induced shifting, or the separate lever is a floor (or ceiling) that only takes effect after price-induced shifting.  (Throughout the rest of this documentation page, a "floor" refers to either a ceiling or to a floor, which are not meaningfully different for purposes of this discussion.)  Unfortunately, there are downsides to each of these approaches:

Additive policies are dissimilar from real-world policies, because policymakers can't foresee the amount of price-induced shifting that will occur in the future and then enact a policy that specifies a strictly additive change, perhaps to hit a desired target.  (Even with hindsight, it can be tough or impossible to determine how much of an action was undertaken due to differences between actual historical costs and counter-factual possible historical costs, so calculating the "base" to which an additive policy must be applied may not be possible.  This means that in the real world, it may not be clear whether or not an actor has complied with an additive policy, even in retrospect.)  Therefore, while additive policies are comparatively easy to model, they have drawbacks when seeking to represent policies that a real policymaker could plausibly enact.

In contrast, floor policies are straightforward to enact in the real world, but on the modeling side, they can reduce the EPS's ability to ascribe emissions reductions or other impacts to a particular policy (e.g. in wedge diagrams or cost curve diagrams) while capturing all policy interactions.  In the web app interface, the EPS tests for policy contributions to an interacting package by sequentially disabling each policy in turn, noting the resulting change in emissions (or costs, or other metric of interest), then re-enabling the disabled policy and moving on to the next policy.  At the end, it scales the results of each policy's contribution such that the total equals the package's total effect.  The reason this presents a difficulty with floor and pricing policy interactions can be hard to visualize, so here is a helpful example:

The EPS adjusts EV market share based on policies that affect fuel price, reflecting the way fuel prices influence buyers' vehicle choices.  The EPS also includes an EV sales mandate, which can require that at least a certain percentage of vehicle sales consist of EVs.  The EV sales mandate is implemented as a floor, so the mandate has no effect if EV sales would be high enough to comply based on pricing policies alone.  Suppose you design a policy package that features a carbon tax policy and also an EV sales mandate that would require an increase in EV market share equal to the increase obtained from the carbon tax.  When the EPS breaks that policy package into its component parts, the model will tell you that the EV sales mandate is responsible for no increase in EV deployment, because when it relaxes the EV sales mandate, the EV market share does not drop, as that higher market share is being fully supported by the pricing policy.  The EPS will also find that the carbon tax policy results in no increase in EV market share, because when the carbon tax is relaxed, there is no drop in EV market share, as the EV market share is fully supported by the EV sales mandate policy.  Thus, even though the change in EV market share from the policy package as a whole is calculated correctly, no policy receives "credit" for that increase.

It is possible to get around this problem by performing an analysis of policy contributions to your metric of interest by enabling each policy within the policy package in turn, noting the effect, then disabling it and repeating for the next policy.  At the end, it scales the components so they sum to the policy package's total effect.  This "policy-enabling" procedure would correctly ascribe 50% of the effect on EV deployment in our example above to the sales mandate and 50% to the carbon tax.  Unfortunately, because only one policy is ever enabled at a given time, it fails to capture policy interactions.  Thus, there are pluses and minuses to each approach.

Both methods provide valuable insight and researchers studying these topics should consider evaluating policies from both perspectives.  The [ContributionTest Python script](testing-policy-contributions.html) included with the Energy Policy Simulator can be configured to use either policy-disabling (the default) or policy-enabling calculation modes.  The wedge diagrams and cost curves available through the web interface use only policy-disabling analysis, as as this approach minimizes inaccuracy for most use cases.

## Selecting the Best Approach for Each Modeled Action

As model developers, we must carefully balance upsides and downsides of handling each potential mitigation action in a solely price-driven way, solely driven by a separate policy lever, or as a combination of the two (with the separate lever either specifying an additive amount or serving as a floor):
* Treating an action as solely price-driven properly captures the price-behavior feedbacks.  This approach is often the preference of classical economists.  However, it is poor at capturing [non-price barriers](https://energyinnovation.org/wp-content/uploads/2018/01/2016-08-18-Broad-Spectrum-Published-Article.pdf), and by definition, it disallows the possibility of mandating more of that action via a separate policy, something that is often done and can achieve good results in the real world.
* Treating an action as solely driven by a separate policy lever allows for granular control over that action and allows us to easily account for non-price barriers that limit the extent to which the action may be undertaken due to market forces alone.  Unfortunately, it makes that action completely insensitive to pricing policies.  Even in the presence of severe non-price barriers, in the real world, there is often at least a small sensitivity to price changes.
* Using a combined approach requires us to treat the policy lever as additive or as a floor.  Additive policies may be dissimilar from plausibly enactable real-world policies in the way the desired quantity of action is specified.  Policies that are a floor often have no effect until above a certain threshold and lead the EPS to incorrectly under-estimate the contribution of both the pricing policy and the floor policy to the total policy package's effect when using a policy-disabling analysis mode (which can cause wedge diagrams and policy cost curve diagrams generated by the web app to be inaccurate).

As developers of the EPS, we resolve these trade-offs by using an approach for each action that best reflects the way policies regarding that action are usually implemented in the real world, while looking to minimize error in the most common use cases.  The correct approach necessarily varies by action.  As a result, the EPS does not have a consistent treatment of how policies drive mitigation actions, and we believe it to be more accurate as a result.

The following table lists which approach is used to govern which types of action in the EPS.  This table may not include all effects that exist in the EPS, but it aims to include the major types of modeled actions that contribute to emissions abatement.  A key to the acronyms used in the table appears below the table.

| Sector | Action | Price-Driven? | Separate Lever(s)? | Non-Pricing Policies |
| ------ | ------ | :-----------: | :----------------: | -------------------- |
| Transportation | Change in demand for travel | yes | yes | additive: TDM |
| Transportation | Technology choice (e.g. electric vs. combustion engine LDVs) | yes | yes | floor: EV mandate; additive: reduce EV range anxiety, EV charger deployment |
| Transportation | Fuel supply blending | no | yes | LCFS |
| Transportation | Efficiency of new vehicles of a given technology | yes | yes | additive: standards, parameterized feebate<sup>A</sup> |
| Transportation | Mode shifting (e.g. shifting trips from LDVs to buses) | no | yes | TDM |
| Transportation | Conventional pollutant reduction | no | yes | standards |
| Electricity<sup>B</sup> | Technology choice for new power plants | yes | yes | floors: RPS, ban new plant types, mandated capacity construction |
| Electricity | Flexibility provision | no | yes | DR, transmission, batteries |
| Electricity | Transmission loss reduction | no | yes | reduce T&D losses |
| Electricity | Early retirement of fossil plants | yes | yes | additive: early retirement |
| Electricity | Change in electricity imports & exports | no | yes | electricity imports, electricity exports |
| Buildings | Change in demand for building services | yes | no | none |
| Buildings | Technology choice (e.g. natural gas vs. electric appliances) | no | yes | building component electrification |
| Buildings | Change in efficiency of new building components | yes | yes | additive: building codes, rebate, labeling |
| Buildings | Accelerated retrofitting | no | yes | commercial retrofitting |
| Buildings | Distributed solar PV deployment | no | yes | RPS tranche, parameterized subsidy<sup>C</sup> |
| Industry | Change in demand for industrial products | yes | yes | additive: material efficiency / longevity / re-use, shift to non-animal products |
| Industry | Technology choice (e.g. natural gas vs. electric production processes) | no | yes | fuel switching |
| Industry | Change in energy efficiency of production | no | yes | standards, waste heat recovery, system integration |
| Industry | Early retirement of industrial facilities | no | yes | early retirement |
| Industry | Process emissions abatement | yes | yes | additive: 8 levers (including agriculture) |
| District Heat<sup>B</sup> | Technology choice (fuel switching) | no | yes | fuel switching |
| District Heat | Efficiency | no | yes | CHP |
| LULUCF | All actions | no | yes | each action has its own lever |
| CCS | Amount of deployment | no | yes | CCS deployment |
| Hydrogen Supply<sup>B</sup> | Technology choice (e.g. methane reforming, electrolysis, etc.) | no | yes | production pathway switching |
| Geoengineering | Amount of deployment | no | yes | direct air capture |
| R&D | Amount of progress achieved | no | yes | separate levers for each technology |
| Fuel Trade | Quantities of fuels imported/exported | yes | yes | reduce exports |

<sup>A</sup> The feebate is a pricing policy, but it is converted into a percentage increase in efficiency via a parameter from a study, then applied additively following pricing effects.

<sup>B</sup> Note that change in demand for electricity, district heat, and hydrogen is handled in each energy-demanding sector, not in the Electricity, District Heat, or Hydrogen Supply sectors.

<sup>C</sup> The subsidy for distributed solar PV is a pricing policy, but it is converted into a percentage increase in deployment via a parameter from a study.  There is no purely price-driven mechanism for distributed PV deployment that responds to, say, changes in the price of electricity from the grid.

Key to acronyms used in this table:
* CCS = carbon capture and sequestration
* CHP = combined heat and power
* DR = demand response
* EV = electric vehicle
* LCFS = low carbon fuel standard
* LDVs = light duty [on-road] vehicles
* LULUCF = land use, land use change, and forestry
* R&D = research and development
* T&D = transmission and distribution
* TDM = transportation demand management