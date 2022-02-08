---
layout: page
title:  "Output Graphs Available in the Web Interface"
---

The web interface allows the user to visualize Energy Policy Simulator (EPS) results through a variety of output graphs.  As of EPS 3.3.1, there are 174 different output graphs available in the web interface.  However, which graphs are shown in the web interface may be customized for different EPS country or regional adaptations.  Many graphs include more than one data series, such as a graph of power plant capacity by plant type (coal, nuclear, hydro, etc.).  Therefore, over 600 different data series are available in the web interface.  (Thousands more are available in the [downloadable version](download.html) of the EPS.)

## List of Output Graphs

* ### Emissions: CO<sub>2</sub>e
  * **Total (includes land use)**
  
    _Economy-wide CO<sub>2</sub>e emissions, including Land Use, Land Use Change, and Forestry (LULUCF)_
  
  * **Total (excludes land use)**
  
    _Economy-wide CO<sub>2</sub>e emissions, excluding Land Use, Land Use Change, and Forestry (LULUCF)_
  
  * **By Sector**
  
    _Economy-wide CO<sub>2</sub>e emissions or sequestration broken out by sector (District Heat & Hydrogen, Water & Waste, Agriculture, Buildings, Transportation, Electricity, Industry, Geoengineering, Land Use)_
  
  * **By Source Type**
 
    _Economy-wide CO<sub>2</sub>e emissions or sequestration broken out by source type (Process Emissions, Energy, Geoengineering, Land Use)_
 
  * **By Pollutant**
  
    _Economy-wide CO<sub>2</sub>e emissions broken out by pollutant (N<sub>2</sub>O, F-gases in CO<sub>2</sub>e, CH<sub>4</sub>, CO<sub>2</sub>)_
  
  * **Per Unit GDP**
  
    _CO<sub>2</sub>e emissions per unit Gross Domestic Product_
  
  * **Agriculture**
  
    _Agriculture sector CO<sub>2</sub>e emissions_
  
  * **Buildings**
  
    _Buildings sector CO<sub>2</sub>e emissions_
  
  * **District Heat & Hydrogen**
  
    _District Heat & Hydrogen sector CO<sub>2</sub>e emissions_
  
  * **Electricity**
  
    _Electricity sector CO<sub>2</sub>e emissions_
  
  * **Industry**
  
    _Industry sector CO<sub>2</sub>e emissions_
  
  * **Land Use**
  
    _Land Use, Land Use Change, and Forestry sector CO<sub>2</sub>e emissions_
  
  * **Transportation**
  
    _Transportation sector CO<sub>2</sub>e emissions_
  
  * **Water & Waste**
  
    _Water & Waste sector CO<sub>2</sub>e emissions_

* ### Emissions (by Pollutant)

  _Economy-wide emissions (in metric tons) of each of the following 12 pollutants:_
  
  * **CO<sub>2</sub>**

  * **CH<sub>4</sub>**

  * **N<sub>2</sub>O**

  * **F-gases (in CO<sub>2</sub>e)**
  
  * **PM<sub>2.5</sub>**

  * **PM<sub>10</sub>**

  * **BC**

  * **OC**

  * **NO<sub>x</sub>**

  * **VOC**

  * **SO<sub>x</sub>**

  * **CO**

* ### Emissions: Energy-Related CO<sub>2</sub>
  
  * **By Sector**
  
    _Economy-wide CO<sub>2</sub>e emissions from combustion of fuels for energy purposes broken out by sector (District Heat & Hydrogen, Water & Waste, Agriculture, Buildings, Transportation, Electricity, Industry, Geoengineering)_
  
  * **By Sector (reallocated energy carriers)**
  
    _Economy-wide CO<sub>2</sub>e emissions from combustion of fuels for energy purposes broken out by sector, with emissions from Electricity, District Heat, and Hydrogen production reallocated to demand sectors (Water & Waste, Agriculture, Buildings, Transportation, Industry, Geoengineering)_
  
  * **By Fuel Type**
  
    _Economy-wide CO<sub>2</sub>e emissions from combustion of fuels for energy purposes broken out by fuel type_
  
  * **Per Unit GDP**
  
    _Economy-wide CO<sub>2</sub>e emissions from combustion of fuels for energy purposes per unit Gross Domestic Product_

* ### Effects by Policy: CO<sub>2</sub>e Wedge Diagrams

  _These graphs present the relative impact of each enabled policy in a scenario in terms of the change in CO<sub>2</sub>e emissions. The "Total" wedge diagram includes all emission from the modeled region, while the sector-specific wedge diagrams only include direct emissions from those sectors.  Note that policies affectiong one sector may impact emissions in other sectors.  For example, electrification of industry (an Industry Sector policy) may affect emissions from the Electricity Sector.  Therefore, viewing a sector-specific wedge diagram may not show the full emissions impacts of that sector's policies.  For a detailed description of how wedge thicknesses are calculated, see [Calculating Wedge Diagrams and Cost Curves](calculating-wedge-diagrams-and-cost-curves.html)._
  
  * **Total**
  
  * **Agriculture**
  
  * **Buildings**
  
  * **District Heat & Hydrogen**
  
  * **Electricity**
  
  * **Industry**
  
  * **Transportation**

* ### Effects by Policy: CO<sub>2</sub>e Abatement Cost Curve
  
  _These graphs show the abatement and cost-effectiveness of each policy. Each policy is displayed as a box whose horizontal width is based on the average annual abatement attributed to that policy (with abatement atributions made using the same procedure as in the wedge diagrams above) through 2050 or 2030. The height of each box, above or below the X-axis, is the average cost per ton CO<sub>2</sub>e abated. This is calculated by dividing the cumulative CO<sub>2</sub>e emissions reductions attributed to a given policy through 2050 or 2030 by the net present value of the policy-induced change in capital, operational, and fuel expenditures caused by that policy through 2050 or 2030._

  * **NPV through 2050**
  
  * **NPV through 2030**

* ### Financial: Policy Package Cost/Savings
  
  * **Change in CapEx + OpEx**
  
    _This graph shows one way to represent the overall costs of a policy package: the change in capital expenditures, fuel and operational expenditures (including labor), and additional carbon tax on process emissions. This graph displays each of these components in addition to their sum. Revenue-neutral taxes (i.e. taxes that are fully rebated to businesses and consumers, according to the policy package's [Government Revenue Accounting settings](io-model.html), controlled by levers in the policy selector pane) and revenue-neutral subsidies (similarly controlled by Government Revenue Accounting settings) are considered cash transfers rather than capital and operational expenditures and are therefore added to or subtracted from the metric such that the total excludes these cash transfers. The "Change in CapEx and OpEx" reports only changes in amounts paid and excludes changes in amounts received (which always equal the changes in amounts paid). The changes in amounts paid can be positive or negative. For example, if a policy causes consumers to buy less fuel, then the “Change in CapEx and OpEx” will be negative (because consumers are spending less money on fuel as a result of the policy package). It does not matter that the fuel industry is receiving less money, because changes in receipts are excluded from this cost metric._
  
  * **^ Total Only**
  
    _This output graph reports only the Total Change in CapEx + OpEx from the metric above, to allow for multiple scenarios to be compared on the same graph._
  
  * **Government Cash Flow Accounting**
  
    _This graph presents how the government handles added or reduced revenue. This metric is broken out into increases or decreases in each of the following five categories: Corporate Income Taxes, Payroll Taxes, Household Taxes, Budget Deficit, and Government Spending (i.e., increases or decreases in spending proportional to how the existing government budget is spent). Values on this graph should be read literally. For instance, a positive value for "budget deficit" indicates the government is running a higher budget deficit in order to make up for a reduction in its cash flow (rather than decreasing total amount spent or raising taxes), whereas a negative value for "budget deficit" indicates the government is using policy-driven increases in its cash flow to reduce the budget deficit (rather than increasing government spending or reducing taxes). Similarly, a positive value for "Change in Household Taxes" means tax receipts have increased, while a negative value indicates tax receipts have decreased. Thus, a policy package that increases government cash flow may be handled via accounting modes with a mixture of positive and negative values (such as increased spending combined with decreased household taxes). Users can control how the government handles changes in its revenues across these five categories by using the Government Revenue Accounting levers in the policy selector pane._
  
  * **Cumulative Change in National Debt**
  
    _Change in national debt as a result of the selected policies. Changes to the budget deficit are cumulated across each year of the model run to find the change in the national debt (or surplus) relative to business-as-usual as of each modeled year._
  
  * **Change in Interest Paid on National Debt**
 
    _Change in national debt interest payments as a result of the selected policies in each year_
  
  * **Change in Government Cash Flow by Source**
  
    _This graph presents the net effects of the selected policies on government cash flow prior to government decisions about how to handle its changes in cash flow (which can be controlled with the Government Revenue Accounting levers in the policy selector pane). This metric is broken out by sources of cash flow changes (Carbon Tax Revenue, Fuel Tax Revenue, EV Subsidy, Electric Generation Subsidy, Electricity Capacity Construction Subsidy, Distributed Solar Subsidy, Fuel Subsidy, National Debt Interest, Remaining Government Cash Flows). "Remaining Government Cash Flows" is often dominated by changes in tax receipts due to overall growth or shrinkage of the economy (GDP and Employee Compensation) but also includes changes in costs paid by government, such as spending on energy to power government buildings._

* ### Financial: Jobs, GDP, and Earnings
  
  * **Change in Jobs**
  
    _Policy-induced changes in jobs in each year (i.e., increase or decrease in number of employed individuals in a given year, relative to business-as-usual). Note that some jobs (e.g., construction) may be short-term, meaning this metric can be thought of in terms of job-years (one job that lasts for one year equates to one job-year). This graph reports the total change in jobs and also breaks out jobs by Fossil Fuel and Utility Jobs, Manufacturing and Construction Jobs, and Other Jobs._

  * **Change in Jobs by Sex**
  
    _Policy-induced changes in jobs in each year (i.e., increase or decrease in number of employed individuals in a given year, relative to business-as-usual), disaggregated into categories by sex. Note that some jobs (e.g., construction) may be short-term, meaning this metric can be thought of in terms of job-years (one job that lasts for one year equates to one job-year).  In the U.S. version of the EPS, the available sex categories are based on those categories for which U.S. government data are available (in particular, from the Bureau of Labor Statistics) and should not be interpreted as a reflection Energy Innovation's views of which sex categories exist or are worthy of being reported separately._

  * **Percent Change in Jobs by Sex**
  
    _The same metric as above, graphed as a percent change in the number of jobs held by people of each sex (relative to the BAU case in that same year)._

  * **Change in Jobs by Race**
  
    _Policy-induced changes in jobs in each year (i.e., increase or decrease in number of employed individuals in a given year, relative to business-as-usual), disaggregated into categories by race. Note that some jobs (e.g., construction) may be short-term, meaning this metric can be thought of in terms of job-years (one job that lasts for one year equates to one job-year).  In the U.S. version of the EPS, the available race categories are based on those categories for which U.S. government data are available (in particular, from the Bureau of Labor Statistics) and should not be interpreted as a reflection Energy Innovation's views of which race categories exist or are worthy of being reported separately._

  * **Percent Change in Jobs by Race**
  
    _The same metric as above, graphed as a percent change in the number of jobs held by people of each race (relative to the BAU case in that same year)._

  * **Change in Jobs by Hispanic or Latino Status**
  
    _Policy-induced changes in jobs in each year (i.e., increase or decrease in number of employed individuals in a given year, relative to business-as-usual), disaggregated into categories by Hispanic or Latino status. Note that some jobs (e.g., construction) may be short-term, meaning this metric can be thought of in terms of job-years (one job that lasts for one year equates to one job-year).  In the U.S. version of the EPS, the available Hispanic or Latino status categories are based on those categories for which U.S. government data are available (in particular, from the Bureau of Labor Statistics) and should not be interpreted as a reflection Energy Innovation's views of which Hispanic or Latino status categories exist or are worthy of being reported separately._

  * **Perc Change in Jobs by Hispanic or Latino Status**
  
    _The same metric as above, graphed as a percent change in the number of jobs held by people of each Hispanic or Latino status (relative to the BAU case in that same year)._

  * **Change in Jobs by Age Bracket**
  
    _Policy-induced changes in jobs in each year (i.e., increase or decrease in number of employed individuals in a given year, relative to business-as-usual), disaggregated into categories by age bracket. Note that some jobs (e.g., construction) may be short-term, meaning this metric can be thought of in terms of job-years (one job that lasts for one year equates to one job-year)._

  * **Percent Change in Jobs by Age Bracket**
  
    _The same metric as above, graphed as a percent change in the number of jobs held by people of each age bracket (relative to the BAU case in that same year)._
  
  * **Change in Jobs by Union Status**
  
    _Policy-induced changes in jobs in each year (i.e., increase or decrease in number of employed individuals in a given year, relative to business-as-usual), disaggregated into categories by union representation status. Note that some jobs (e.g., construction) may be short-term, meaning this metric can be thought of in terms of job-years (one job that lasts for one year equates to one job-year)._

  * **Percent Change in Jobs by Union Status**
  
    _The same metric as above, graphed as a percent change in the number of jobs held by people of each union status (relative to the BAU case in that same year)._

  * **Direct/Indirect/Induced Change in Jobs**
  
    _Policy-induced changes in jobs in each year (i.e., increase or decrease in number of employed individuals in a given year, relative to business-as-usual). Note that some jobs (e.g., construction) may be short-term, meaning this metric can be thought of in terms of job-years (one job that lasts for one year equates to one job-year). This graph reports the total change in jobs and also breaks out jobs by Direct, Indirect, and Induced impacts. For an explanation of these terms, see the [Input-Output Model](io-model.html) sheet._
  
  * **Direct Plus Indirect Change in Jobs**
  
    _Policy-induced changes in jobs in each year, excluding induced changes in jobs (i.e., increase or decrease in number of employed individuals in a given year, relative to business-as-usual). Note that some jobs (e.g., construction) may be short-term, meaning this metric can be thought of in terms of job-years (one job that lasts for one year equates to one job-year). This graph reports the Direct and Indirect changes in jobs but excludes the Induced changes in jobs. For an explanation of these terms, see the [Input-Output Model](io-model.html) sheet._
  
  * **Change in GDP**
  
    _Policy-induced changes in Gross Domestic Product in each year, relative to business-as-usual. This graph reports the total change in GDP and also breaks out changes in GDP by Fossil Fuel and Utilities, Manufacturing and Construction, and Other Contributors._
  
  * **Percent Change in GDP**
  
    _Percent change in Gross Domestic Product (relative to business-as-usual) in each year. This graph reports the total percent change in GDP and also breaks out changes in GDP by Fossil Fuel and Utilities, Manufacturing and Construction, and Other Contributors._
  
  * **Direct/Indirect/Induced Change in GDP**
  
    _Policy-induced changes in Gross Domestic Product in each year, relative to business-as-usual. This graph reports the total change in GDP and also breaks out changes in GDP by Direct, Indirect, and Induced impacts. For an explanation of these terms, see the [Input-Output Model](io-model.html) sheet._
  
  * **Change in Employee Compensation**
  
    _Policy-induced change in total employee compensation in each year, further broken out by compensation for Fossil Fuels and Utilities, Manufacturing and Construction, and Others._
  
  * **Change in Compensation per Employee**
  
    _Policy-induced change in compensation per employed person in each year._
  
  * **Direct/Indirect/Induced Change in Compensation**
  
    _Policy-induced change in total employee compensation in each year, further broken out by Direct, Indirect, and Induced changes in compensation. For an explanation of these terms, see the [Input-Output Model](io-model.html) sheet._

* ### Financial: Direct Cash Flow Changes
  
  * **Cash Flow Change (by Entity)**
  
    _Direct (first-order) policy-induced change in cash flow for each of nine entities tracked in the Energy Policy Simulator (Government, Non-Energy Industries, Labor and Consumers, Foreign Entities, Electricity Suppliers, Coal Suppliers, Natural Gas and Petroleum Suppliers, Biomass and Biofuel Suppliers, and Other Energy Suppliers). This metric is upstream of the macroeconomic input-output model and therefore does not include how government, households, and industries respend additional money (or how they compensate for reductions in money), so it does not capture economy-wide growth or shrinkage caused by the modeled policies. (See the graphs in the "Financial: Jobs, GDP, and Earnings" section for financial outputs that include policy-driven changes in economy size.) Since any money that is spent by one entity is received by another, direct cash flow changes sum to zero._
  
  * **Government Cash Flow Components**
  
    _Direct (first-order) policy-induced change in government cash flow, broken out by Change in Revenue, Change in Energy Expenditures, and Change in Non-Energy Expenditures._
  
  * **Non-Energy Industries Cash Flow Components**
  
    _Direct (first-order) policy-induced change in non-energy industries cash flow, broken out by Change in Domestic Revenue, Change in Export Revenue, Change in Energy Expenditures, and Change in Non-Energy Expenditures._
  
  * **Labor and Consumers Cash Flow Components**
  
    _Direct (first-order) policy-induced change in labor and consumers cash flow, broken out by Change in Revenue, Change in Energy Expenditures, and Change in Non-Energy Expenditures._
  
  * **Foreign Entities Cash Flow Components**
  
    _Direct (first-order) policy-induced change in foreign entities cash flow, broken out by Change in Revenue, Change in Energy Expenditures, and Change in Non-Energy Expenditures._
  
  * **Electricity Supplier Cash Flow Components**
  
    _Direct (first-order) policy-induced change in electricity supplier cash flow, broken out by Change in Domestic Revenue, Change in Export Revenue, Change in Energy Expenditures, and Change in Non-Energy Expenditures._
  
  * **Coal Supplier Cash Flow Components**
  
    _Direct (first-order) policy-induced change in coal supplier cash flow, broken out by Change in Domestic Revenue, Change in Export Revenue, Change in Energy Expenditures, and Change in Non-Energy Expenditures._
  
  * **Natural Gas and Petroleum Supplier Cash Flow Components**
  
    _Direct (first-order) policy-induced change in natural gas and petroleum supplier cash flow, broken out by Change in Domestic Revenue, Change in Export Revenue, Change in Energy Expenditures, and Change in Non-Energy Expenditures._
  
  * **Biomass and Biofuel Supplier Cash Flow Components**
  
    _Direct (first-order) policy-induced change in biomass and biofuel supplier cash flow, broken out by Change in Domestic Revenue, Change in Export Revenue, Change in Energy Expenditures, and Change in Non-Energy Expenditures._
  
  * **Other Energy Supplier Cash Flow Components**
  
    _Direct (first-order) policy-induced change in other energy supplier cash flow, broken out by Change in Domestic Revenue, Change in Export Revenue, Change in Energy Expenditures, and Change in Non-Energy Expenditures._

* ### Human Health & Social Benefits
  
  * **Avoided Deaths Wedge Diagram**
  
    _This graph presents the relative impact of each enabled policy in a scenario in terms of the number of avoided premature deaths_

  * **Percent Change in Deaths**
  
    _This graph shows the percentage change in the number of deaths occurring each year (relative to the BAU case in that same year)._
  
  * **Avoided Deaths by Sex**

    _Annual avoided premature deaths as a result of a policy package disaggregated by sex.  In the U.S. version of the EPS, the available sex categories are based on those categories for which U.S. government data are available (in particular, from the Bureau of Labor Statistics, since we use these categories for job impacts as well as health impacts) and should not be interpreted as a reflection Energy Innovation's views of which sex categories exist or are worthy of being reported separately._

  * **Percent Change in Deaths by Sex**

    _The same metric as above, graphed as a percent change in the number of deaths of people of each sex (relative to the BAU case in that same year)._
  
  * **Avoided Deaths by Race**

    _Annual avoided premature deaths as a result of a policy package disaggregated by race.  In the U.S. version of the EPS, the available race categories are based on those categories for which U.S. government data are available (in particular, from the Bureau of Labor Statistics, since we use these categories for job impacts as well as health impacts) and should not be interpreted as a reflection Energy Innovation's views of which race categories exist or are worthy of being reported separately._

  * **Percent Change in Deaths by Race**

    _The same metric as above, graphed as a percent change in the number of deaths of people of each race (relative to the BAU case in that same year)._
  
  * **Avoided Deaths by Hispanic or Latino Status**

    _Annual avoided premature deaths as a result of a policy package disaggregated by Hispanic or Latino status.  In the U.S. version of the EPS, the available Hispanic or Latino status categories are based on those categories for which U.S. government data are available (in particular, from the Bureau of Labor Statistics, since we use these categories for job impacts as well as health impacts) and should not be interpreted as a reflection Energy Innovation's views of which Hispanic or Latino status categories exist or are worthy of being reported separately._

  * **Percent Change in Deaths by Hispanic or Latino Status**

    _The same metric as above, graphed as a percent change in the number of deaths of people of each Hispanic or Latino status (relative to the BAU case in that same year)._
  
  * **Avoided Premature Deaths**
  
    _Annual avoided premature deaths as a result of a policy package_
  
  * **Monetized Avoided Deaths & Climate Benefits**
  
    _Monetized annual avoided premature deaths (according to the Value of a Statistical Life) and climate benefits (according to the Social Cost of Carbon) as a result of a policy package_
  
  * **Avoided Lost Workdays**
  
    _Annual avoided lost workdays as a result of a policy package_
  
  * **Avoided Respiratory Symptoms and Bronchitis**
  
    _Annual avoided respiratory symptoms and bronchitis as a result of a policy package_
  
  * **Avoided Asthma Attacks**
  
    _Annual avoided asthma attacks as a result of a policy package_
  
  * **Avoided Nonfatal Heart Attacks**
  
    _Annual avoided nonfatal heart attacks as a result of a policy package_
  
  * **Avoided Hospital Admissions**
  
    _Annual avoided hospital admissions as a result of a policy package_
  
  * **Avoided Respiratory ER Visits**
  
    _Annual avoided respiratory emergency room visits as a result of a policy package_
  
  * **Avoided Minor Restricted Activity Days**
  
    _Annual avoided minor restricted activity days as a result of a policy package_

* ### Electricity Generation, Capacity, and Demand
  
  * **Generation**
  
    _Annual electricity generation by power plant type_
  
  * **Policy-Driven Change in Generation**
  
    _Changes in electricity generation by power plant type due to enabled policies_
  
  * **Capacity**
  
    _Annual electricity generation capacity by power plant type_
  
  * **Policy-Driven Change in Capacity**
  
    _Changes in electricity generation capacity by power plant type due to enabled policies_
  
  * **Electricity Demand by Sector**
  
    _Electricity demand broken out by sector (District Heat & Hydrogen, Water & Waste, Agriculture, Transportation, Industry, Buildings)_

* ### Electricity: Levelized Costs, Curtailment, Emissions and Water Use
  
  * **Levelized Cost of Electricity (after subsidies)**
  
    _Levelized Cost of Electricity by power plant type in 2020, 2030, 2040, and 2050 (after any subsidies for generation or power plant construction)_
  
  * **Curtailed Electricity from Renewables**
  
    _Annual curtailed electricity broken out by renewable power plant type_
  
  * **CO<sub>2</sub>e Emissions by Plant Type**
  
    _Annual Electricity sector CO<sub>2</sub>e emissions broken out by power plant type_
  
  * **Water Withdrawals by Power Plants**
  
    _Annual water withdrawals (water taken to use for cooling) by power plant type_
  
  * **Water Consumption by Power Plants**
  
    _Annual water withdrawals (water taken and not returned to the water body, i.e. evaporated) by power plant type_

* ### Transport: Vehicles by Technology

  _Sales by vehicle technology for the following classes of vehicles:_
  
  * **Sales: Cars and SUVs**
  
  * **Sales: Buses**
  
  * **Sales: Light Freight Trucks**
  
  * **Sales: Med & Heavy Freight Trucks**
  
  * **Sales: Motorbikes**

  _Stock by vehicle technology for the following classes of vehicles:_
  
  * **Fleet Composition: Cars and SUVs**
  
  * **Fleet Composition: Buses**
  
  * **Fleet Composition: Light Freight Trucks**
  
  * **Fleet Composition: Med & Heavy Freight Trucks**
  
  * **Fleet Composition: Motorbikes**

* ### Transport: Travel Demand, Fuel Use, and Emissions
  
  * **CO2 Emissions by Vehicle Type**
  
    _Annual Transportation sector CO<sub>2</sub> emissions by vehicle type_
  
  * **Fuel Use by Fuel Type**
  
    _Annual Transportation sector fuel use by fuel type_
  
  * **Fuel Use by Vehicle Type**
  
    _Annual Transportation sector fuel use by vehicle type_

  * **Fuel Use (Total)**

    _Annual Transportation sector fuel use (total)_
  
  * **Travel Demand (Passenger Modes)**
  
    _Annual cargo distance traveled by passenger vehicles, by vehicle type_
  
  * **Travel Demand (Freight Modes)**
  
    _Annual cargo distance traveled by freight vehicles, by vehicle type_

* ### Industry: Fuel Use
  
  * **By Industry (Excluding Feedstocks)**
  
    _Annual Industry sector fuel use by subindustry, excluding feedstocks and only including fuels used for energy purposes_
  
  * **By Fuel (Excluding Feedstocks)**
  
    _Annual Industry sector fuel use by fuel type, excluding feedstocks and only including fuels used for energy purposes_

  * **Total (Excluding Feedstocks)**
  
    _Annual Industry sector fuel use (total), excluding feedstocks and only including fuels used for energy purposes_

  * **By Industry (Including Feedstocks)**
  
    _Annual Industry sector fuel use by subindustry, including feedstocks_
  
  * **By Fuel (Including Feedstocks)**
  
    _Annual Industry sector fuel use by fuel type, including feedstocks_

  * **Total (Including Feedstocks)**
  
    _Annual Industry sector fuel use (total), including feedstocks_

* ### Industry: CO<sub>2</sub>e Emissions
  
  * **Total by Industry**
  
    _Annual Industry sector CO<sub>2</sub>e emissions by subindustry_
  
  * **Total by Pollutant**
  
    _Annual Industry sector CO<sub>2</sub>e emissions by pollutant (N<sub>2</sub>O, F-gases in CO<sub>2</sub>e, CH<sub>4</sub>, CO<sub>2</sub>)_
  
  * **Process Emissions by Industry**
  
    _Annual Industry sector process emissions by subindustry; process emissions refer to pollutants that occur as a result of industry operations and which were not related to the combustion of fuel for energy_
  
  * **Process Emissions by Pollutant**
  
    _Annual Industry sector process emissions by pollutant (N<sub>2</sub>O, F-gases in CO<sub>2</sub>e, CH<sub>4</sub>, CO<sub>2</sub>); process emissions refer to pollutants that occur as a result of industry operations and which were not related to the combustion of fuel for energy_
  
  * **Energy-Related Emissions by Industry**
  
    _Annual Industry sector energy-related emissions by subindustry_
  
  * **Energy-Related Emissions by Pollutant**
   
    _Annual Industry sector energy-related emissions by pollutant_

* ### Buildings: Energy Use
  
  * **By Building Component**
  
    _Annual Buildings sector energy consumption by building component_
  
  * **By Building Type**
  
    _Annual Buildings sector energy consumption by building type (commercial, rural residential, urban residential)_
  
  * **By Energy Source**
  
    _Annual Buildings sector energy consumption by fuel type_

  * **Total**
  
    _Annual Buildings sector energy consumption (total)_

* ### Energy Consumption
  
  * **Primary Energy by Source**
  
    _Annual economy-wide primary energy consumption by fuel type_
  
  * **Primary Energy by End Use Sector**
  
    _Annual economy-wide primary energy consumption by end use sector (District Heat & Hydrogen, Water & Waste, Agriculture, Buildings, Transportation, Electricity, Industry, Geoengineering)_
  
  * **Per Unit GDP**
  
    _Annual economy-wide primary energy consumption per unit Gross Domestic Product_
  
  * **Electricity Consumption**
  
    _Annual electricity consumption_
  
  * **Hard Coal Consumption**
  
    _Annual hard coal consumption_
  
  * **Lignite Consumption**
  
    _Annual lignite consumption_
  
  * **Natural Gas Consumption**
  
    _Annual natural gas consumption_
  
  * **Petroleum Fuels Consumption**
  
    _Annual petroleum fuels consumption_
  
  * **Liquid Biofuels Consumption**
  
    _Annual liquid biofuels consumption_
  
  * **Biomass Consumption**
  
    _Annual biomass consumption_
  
  * **LPG Propane & Butane Consumption**
  
    _Annual liquefied petroleum gas, propane, and butane consumption_
  
  * **Municipal Solid Waste Consumption**
  
    _Annual municipal solid waste consumption_
  
  * **Hydrogen Consumption**
  
    _Annual hydrogen consumption_

* ### Energy Exports, Imports and Production
  
  * **Energy Exports**
  
    _Annual energy exports by fuel type_
  
  * **Change in Energy Exports**
  
    _Annual policy-induced changes in energy exports by fuel type_
  
  * **Energy Export Revenue**
  
    _Annual energy export revenue by fuel type_
  
  * **Change in Energy Export Revenue**
  
    _Annual policy-induced changes in energy export revenue by fuel type_
  
  * **Embedded CO<sub>2</sub> in Exported Fuels**
  
    _Annual fuel exports in terms of the quantity of CO<sub>2</sub> that would be emitted if the fuels are combusted._
  
  * **Change in Embedded CO<sub>2</sub> in Exported Fuels**
  
    _Annual policy-induced changes in fuel exports in terms of the quantity of CO<sub>2</sub> that would be emitted if the fuels are combusted._
  
  * **Energy Imports**
  
    _Annual energy imports by fuel type_
  
  * **Change in Energy Imports**
  
    _Annual policy-induced changes in energy imports by fuel type_
  
  * **Energy Import Expenditures**
  
    _Annual energy import expenditures by fuel type_
  
  * **Change in Energy Import Expenditures**
  
    _Annual policy-induced changes in import expenditures by fuel type_
  
  * **Energy Production**
  
    _Annual domestic energy production by fuel type_
  
  * **Change in Energy Production**
  
    _Annual policy-induced changes in domestic energy production by fuel type_

* ### Fuel Costs (by Fuel, by Sector)

  _Fuel costs in 2020, 2030, 2040, and 2050 by fuel type, by sector (Commercial Buildings, Residential Buildings, Electricity, Transportation, Industry, District Heat and Hydrogen)_
  
  * **Electricity**

  * **Hard Coal**

  * **Lignite**

  * **Natural Gas**

  * **Petroleum Gasoline**

  * **Petroleum Diesel**

  * **Biomass**

  * **Heavy or Residual Fuel Oil**

  * **LPG Propane or Butane**

  * **Hydrogen**

* ### Technology Costs
  
  * **Batteries**
  
    _Battery cost per kilowatt-hour, including the battery cost and the balance of system costs (e.g., labor for its installation)_
  
  * **CCS Capital Equipment**
  
    _Capital cost of carbon capture and sequestration equipment to capture one metric ton of CO<sub>2</sub>e per year, broken out by sector (Electricity and Industry)_
  
  * **Onshore Wind Turbines**
  
    _Construction cost per unit capacity of onshore wind turbines, before construction subsidies_
  
  * **Offshore Wind Turbines**
  
    _Construction cost per unit capacity of offshore wind turbines, before construction subsidies_
  
  * **Solar PV (Utility-Scale)**
  
    _Construction cost per unit capacity of utility-scale solar photovoltaic systems, before construction subsidies_
  
  * **Hydrogen Electrolyzers**
  
    _Capital cost of hydrogen production equipment to produce one kilogram H<sub>2</sub> per year via electrolysis_
