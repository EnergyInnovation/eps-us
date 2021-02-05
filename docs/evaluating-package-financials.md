---
layout: page
title:  "Evaluating the Financial Costs or Benefits of a Policy Package"
---

## Policy-Driven Costs and Savings are Not "Good" or "Bad"

There is not just one correct way to calculate the financial cost or savings of a set of policies, and even the same type of cost (or savings) may be seen either in a positive or negative light.

Policies can increase or decrease spending on:

- Capital equipment (e.g. power plants, appliances in buildings, industrial equipment, etc.)
- Labor
- Fuel/energy
- Other O&M (apart from labor and fuel/energy)
- Tax and subsidy payments

All of these changes in spending are calculated in the Energy Policy Simulator.

However, the simulator can't tell you whether a change is "good" or not.  For example, a policy that improves the lifetime reliability of industrial equipment would reduce capital spending (because factories need to replace their equipment less often).  This "saves" the business money, which sounds good.  But it reduces economic activity (reduces GDP), by reducing the sales of the companies that manufacture the equipment, and the companies that make the materials (like steel) of which the equipment is made.

GDP is itself not a clear "good."  This is because not all spending is equal.  Spending on food, entertainment, and leisure travel are often considered good, but higher spending on disaster recovery or medical expenses is often considered bad.  A policy that worsens air quality and sickens people, so they must visit the doctor more often and buy expensive medicines, will tend to increase GDP (even after accounting for lost workdays).  This is especially true if the policy primarily sickens retirees, who are not working.  But no reasonable person would argue that making retirees sicker is a good policy outcome, even if it boosts GDP.

Similarly, spending **more** on labor can be seen as a positive thing (job creation), and spending **less** on labor can be seen as a positive thing (automation increases domestic businesses' productivity and competitiveness).

A wise policymaker thinks not only about whether a policy increases or decreases certain types of costs, but what underlying dynamic drives those changes, and whether that dynamic makes the country (and the world) a better or a worse place to live.

## Cost Metrics in the Energy Policy Simulator

The Energy Policy Simulator includes a number of cost metrics:

1. The first important cost metric is "Change in Capital and Operational Expenditures."  This is a useful total that expresses how much the policy package saves money or increases spending.  It respects the user's settings for how government raises or spends revenue (discussed on the documentation page for the EPS's [input-output model](io-model.html)), so it correctly reflects user choices such as making carbon taxes revenue-neutral.  It roughly expresses both the cost to domestic firms and the amount of economic stimulus the policy will provide.  The simulator subdivides the metric into components (fuel and O&M, capital equipment, taxes and subsidies) to help users see what cost changes went into the metric.  This is critical for evaluating if the type of spending driven by the policies is "good" or "bad" spending (or savings), with spending on fuel often considered bad and spending on capital equipment often considered good, or at least neutral.

2. Another important set of metrics concerns the impact of the policy package on the government's financial situation.  Details are  provided by the "Government Cash Flow Accounting" graph and the two national debt-related graphs in the web interface, which show the following effects of the policy package:

    * Change in government spending
    * Change in budget deficit
    * Change in household taxes
    * Change in payroll taxes
    * Change in corporate income taxes
    * Cumulative change in the national debt
    * Change in interest paid on the national debt

    Reviewing these metrics helps the model user understand some of the financial implications of the policy package for government.  For example, a policy package that increases the budget deficit may provide short-term stimulus to the economy, but it will also increase interest payments on the national debt.

3. The third key metric are the macroeconomic results of the EPS's [input-output model](io-model.html).  These results include the policy package's effects on:

    * Number of jobs
    * GDP / value added
    * Employee compensation

    These quantities can each be viewed via several different breakouts:

    * By industry (e.g. which industries are gaining/losing jobs, value added, etc.)
    * By effect type: direct, indirect, or induced.  For definitions of these terms, see the doc page on the [input-output model](io-model.html).

    And a few additional details are available:

    * Jobs by union representation status
    * Average compensation per employee

    These metrics are often of particular interest to policymakers, who may want to understand (for example) which policies will boost employment and in which industries.

4. The last important cost metric is a breakout of "Direct Cash Flow Changes."  This shows how much money each of the following nine entities directly spend or save due to the policy package:

    1. Government
    2. Labor and consumers
    3. Non-energy industries
    4. Foreign entities
    5. Electricity suppliers
    6. Coal suppliers
    7. Natural gas and petroleum suppliers
    8. Biomass and biofuel suppliers
    9. Other energy suppliers (e.g. hydrogen, uranium, etc.)

    The simulator breaks out the cash flow changes for each of the nine entities above into four components:

    * Change in domestic revenues
    * Change in export revenues
    * Change in energy expenditures
    * Change in non-energy expenditures

    Seeing the component parts of the cash flow changes can help the user to understand whether a change is a "good" or "bad" thing, from that user's perspective, and can give the user an idea of which policies to change in order to achieve a desired financial effect.

## First-Order Cash Flows and Higher-Order Economic Effects

The Energy Policy Simulator first calculates direct (or "first-order") financial effects of a policy package within each sector: Who gives how much more (or less) money to whom?  Then, using its built-in [input-output model](io-model.html), the EPS calculates higher-order (indirect and induced) effects.  These come from the industries that supply industries affected by the policy package, and from the respending of money received by households or by government (or if less money is received due to the policy package, then how households or government make up for the reduction).

How money is used by households and government can have a large impact on the policy's outcome.  A carbon price that raises government revenue will go farther if the government wisely spends the money (for example, on support for research and development, which can accelerate technological progress, or improving public transit systems, as public transit [generates economic value](https://www.ebp-us.com/sites/default/files/project/uploads/timeismoney.pdf) far greater than its costs).  If the revenue is spent unwisely, the policy will not do nearly so much good.  In the EPS, how government uses or raises revenue for/from specific policies can be set using Government Revenue Accounting levers, discussed on the [input-output model](io-model.html) documentation page.

Therefore, the graphs that show "Financial: Direct Cash Flow Changes" should not be interpreted as which entities "win" and which entities "lose" due to a policy package.  First-order cash flows aren't where the money ultimately lands.

The proper simulation of policy effects on GDP (or jobs) requires accounting for higher-order effects.  For example, a model must account for the re-integration of displaced workers into the economy and the long-term effects of efficiency gains on the economy.  This is easiest to visualize in the context of an intervention (such as automation) that displaces workers and reduces spending while increasing productivity.  In the short term, this sort of intervention looks bad, as it reduces jobs and GDP.  But in the longer term, displaced workers find new places in the economy where they can work, and the entire economy produces more goods with fewer people.  Many of the best policies to mitigate climate change, such as policies that improve products' energy efficiency, improve material efficiency in industry, and promote renewable electricity generation, have disruptive short-term effects because they save money (reduce GDP).  In the longer term, the economy will be better off for these reductions, just as the economy is better off today because of all the labor-saving and energy-saving devices and techniques invented since the Middle Ages.

The Energy Policy Simulator uses induced jobs, induced value added (GDP contribution), and induced employee compensation to capture how savings (for example, from reduced energy expenditures) can create jobs in other parts of the economy (when the money is spent on other things).

## Non-Financial Metrics

Fortunately, non-financial metrics are not as equivocal as financial metrics.  For example, the Energy Policy Simulator includes an estimate of avoided premature mortality (human lives saved) due to reduced pollution.  This is an unqualified good.

Similarly, avoiding greenhouse gas (GHG) emissions is an unqualified good, as it reduces both human suffering and huge financial costs in later years.  There is widespread scientific agreement that the types of technological and policy interventions necessary to transition to a sustainable society are vastly cheaper than the damage that unchecked global warming would do to our economy.

## Rules of Thumb for Policymakers

If the guidelines above regarding financial metrics make them seem too multifaceted to be used for policy guidance, a few rules of thumb might help:

* Energy and material efficiency will have long-term positive financial effects, even if the near-term, direct effects show negative GDP impacts.  In the EPS, the positive induced effects will generally outweigh the negative direct effects for efficiency policies.

* Carbon pricing can result in considerable economic growth, if the revenues are spent well.  If not, carbon pricing is an economic headwind.  (However, it could be used to offset other taxes that are worse economic headwinds, like sales or payroll taxes.)

* Utilize a mix of supply-side interventions (new energy technologies, etc.) and demand-side interventions (material or energy efficiency, etc.).  In the short term, supply-side interventions may increase capital spending and (hence) employment, while reducing demand for industrial products and materials may reduce spending.  Balancing the two types of policy may help to maintain a stable and growing job market, avoiding a boom-and-bust cycle.

* Focus on objective goods.  Nobody can argue with saving human lives.  Don't let the debate about the effects of a policy package exclusively center on financial outcomes.
