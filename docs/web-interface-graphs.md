---
layout: page
title:  "Output Graphs Available in the Web Interface"
---

The web interface allows the user to visualize Energy Policy Simulator (EPS) results through a variety of output graphs.  As of EPS 3.2.0, there are 154 different output graphs available in the web interface.  However, which graphs are shown in the web interface may be customized for different EPS country or regional adaptations.  Many graphs include more than one data series, such as a graph of power plant capacity by plant type (coal, nuclear, hydro, etc.).  Therefore, over 600 different data series are available in the web interface.  (Thousands more are available in the [downloadable version](download.html) of the EPS.)

## List of Output Graphs

Here is a list of the graphs that are available for the EPS web interface as of version 3.2.0:

* Emissions: CO<sub>2</sub>e
  * Total (includes land use)
  
  Economy-wide CO<sub>2</sub>e emissions, including Land Use, Land Use Change, and Forestry (LULUCF)
  
  * Total (excludes land use)
  
  Economy-wide CO<sub>2</sub>e emissions, excluding Land Use, Land Use Change, and Forestry (LULUCF)
  
  * By Sector
  
  Economy-wide CO<sub>2</sub>e emissions broken out by sector (District Heat & Hydrogen, Water & Waste, Agriculture, Buildings, Transportation, Electricity, Industry, Geoengineering, Land Use)
  
  * By Source Type
 
 Economy-wide CO<sub>2</sub>e emissions broken out by source type (Process Emissions, Energy, Geoengineering, Land Use)
 
 * By Pollutant
  
  Economy-wide CO<sub>2</sub>e emissions broken out by pollutant (N<sub>2</sub>O, F-gases in CO<sub>2</sub>e, CH<sub>4</sub>, CO<sub>2</sub>)
  
  * Per Unit GDP
  
  CO<sub>2</sub>e emissions per unit Gross Domestic Product
  
  * Agriculture
  
  Agriculture sector CO<sub>2</sub>e emissions
  
  * Buildings
  
  Buildings sector CO<sub>2</sub>e emissions
  
  * District Heat & Hydrogen
  
  District Heat & Hydrogen sector CO<sub>2</sub>e emissions
  
  * Electricity
  
  Electricity sector CO<sub>2</sub>e emissions
  
  * Industry
  
  Industry sector CO<sub>2</sub>e emissions
  
  * Land Use
  
  Land Use, Land Use Change, and Forestry sector CO<sub>2</sub>e emissions
  
  * Transportation
  
  Transportation sector CO<sub>2</sub>e emissions
  
  * Water & Waste
  
  Water & Waste sector CO<sub>2</sub>e emissions

* Emissions (by Pollutant)

Economy-wide emissions (in metric tons) broken out by the following 12 pollutants
  
  * CO<sub>2</sub>
  * CH<sub>4</sub>
  * N<sub>2</sub>O
  * F-gases (in CO<sub>2</sub>e)
  * PM<sub>2.5</sub>
  * PM<sub>10</sub>
  * BC
  * OC
  * NO<sub>x</sub>
  * VOC
  * SO<sub>x</sub>
  * CO

* Emissions: Energy-Related CO<sub>2</sub>
  
  * By Sector
  
  Economy-wide CO<sub>2</sub>e emissions from combustion of fuels for energy purposes broken out by sector (District Heat & Hydrogen, Water & Waste, Agriculture, Buildings, Transportation, Electricity, Industry, Geoengineering)
  
  * By Sector (reallocated energy carriers)
  
  Economy-wide CO<sub>2</sub>e emissions from combustion of fuels for energy purposes broken out by sector, with Electricity and District Heat and Hydrogen sector emissions reallocated to demand sectors (Water & Waste, Agriculture, Buildings, Transportation, Industry, Geoengineering)
  
  * By Fuel Type
  
  Economy-wide CO<sub>2</sub>e emissions from combustion of fuels for energy purposes broken out by fuel type
  
  * Per Unit GDP
  
  Economy-wide CO<sub>2</sub>e emissions from combustion of fuels for energy purposes per unit Gross Domestic Product

* Effects by Policy: CO<sub>2</sub>e Wedge Diagrams

This graph presents the relative impact of each enabled policy in a scenario in terms of the change in CO<sub>2</sub>e emissions.
  
  * Total
  
  * Agriculture
  
  * Buildings
  
  * District Heat & Hydrogen
  
  * Electricity
  
  * Industry
  
  * Transportation

* Effects by Policy: CO<sub>2</sub>e Abatement Cost Curve
  
  * NPV through 2050
  
  This graph presents the relative cost of each enabled policy in a scenario in terms of the average cost per ton CO<sub>2</sub>e abated. This version of the abatement cost curve is calculated by dividing the cumulative CO<sub>2</sub>e emissions reductions attributed to a given policy through 2050 by the net present value of the policy-induced change in capital, operational, and fuel expenditures through 2050.
  
  * NPV through 2030
  
  This graph presents the relative cost of each enabled policy in a scenario in terms of the average cost per ton CO<sub>2</sub>e abated. This version of the abatement cost curve is calculated by dividing the cumulative CO<sub>2</sub>e emissions reductions attributed to a given policy through 2030 by the net present value of the policy-induced change in capital, operational, and fuel expenditures through 2030.

* Financial: Policy Package Cost/Savings
  
  * Change in CapEx + OpEx
  
  Change in capital expenditures, fuel and operational expenditures (including labor), and additional carbon tax on process emissions. This metric does not include subsidy payments, as these are considered cash transfers rather than capital or operational expenditures. This graph displays each of these components in addition to their sum, which is one way to represent the overall costs or savings of a policy package. The "Change in CapEx and OpEx" reports only changes in amounts paid and excludes changes in amounts received. The changes in amounts paid can be positive or negative. For example, if a policy causes consumers to buy less fuel, then consumers have a positive cash flow change (because they have saved money on fuel), and the “Change in CapEx and OpEx” will be negative (because less money is being spent as a result of the policy package). It does not matter that the fuel industry is receiving less money, because changes in receipts are excluded from this cost metric.
  
  * ^ Total Only
  
  This output graph reports only the Total Change in CapEx + OpEx from the metric above
  
  * Government Cash Flow Accounting
  
  This graph presents how the government handles added or lost revenue. This metric is broken out into spending increases or decreases in each of the following five categories: Corporate Income Taxes, Payroll Taxes, Household Taxes, Budget Deficit, and Government Spending (i.e., increases or decreases in spending proportional to how the existing government budget is spent). Positive values denote increased government spending and negative values denote decreased government spending. Users can control how the government allocates changes in spending across these five categories with the Government Revenue Accounting levers in the lefthand policy selector pane.
  
  * Cumulative Change in National Debt
  
  Change in national debt as a result of the selected policies. Changes to the budget deficit are cumulated across each year of the model run to find the cumulative change in the national debt (or surplus) as of each modeled year.
  
  * Change in Interest Paid on National Debt
 
 Change in national debt interest payments as a result of the selected policies in each year
  
  * Change in Government Cash Flow by Source
  
  This graph presents the net effects of the selected policies on government cash flow prior to government decisions about how to handle its changes in cash flow (which can be controlled with the Government Revenue Accounting levers in the lefthand policy selector pane). This metric is broken out by sources of cash flow changes (Carbon Tax Revenue, Fuel Tax Revenue, EV Subsidy, Electric Generation Subsidy, Electricity Capacity Construction Subsidy, Distributed Solar Subsidy, Fuel Subsidy, National Debt Interest, Remaining Government Cash Flows).

* Financial: Jobs, GDP, and Earnings
  
  * Change in Jobs
  
  Policy-induced changes in jobs in each year (i.e., increase or decrease in number of employed individuals in a given year, relative to business-as-usual). Note that some jobs (e.g., construction) may be short-term, meaning this metric can be thought of in terms of job-years (one job that lasts for one year equates to one job-year). This graph reports the total change in jobs and also breaks out jobs by Fossil Fuel and Utility Jobs, Manufacturing and Construction Jobs, and Other Jobs.
  
  * Change in Union and Non-Union Jobs
  
  Policy-induced changes in jobs in each year (i.e., increase or decrease in number of employed individuals in a given year, relative to business-as-usual). Note that some jobs (e.g., construction) may be short-term, meaning this metric can be thought of in terms of job-years (one job that lasts for one year equates to one job-year). This graph reports the total change in jobs and also breaks out jobs by Union and Non-Union. Note that we currently use time-invariant union representation shares by industry to calculate this metric.
  
  * Direct/Indirect/Induced Change in Jobs
  
  Policy-induced changes in jobs in each year (i.e., increase or decrease in number of employed individuals in a given year, relative to business-as-usual). Note that some jobs (e.g., construction) may be short-term, meaning this metric can be thought of in terms of job-years (one job that lasts for one year equates to one job-year). This graph reports the total change in jobs and also breaks out jobs by Direct, Indirect, and Induced impacts. For an explanation of these terms, see the [Input-Output Model](io-model.html) sheet.
  
  * Direct Plus Indirect Change in Jobs
  
  Policy-induced changes in jobs in each year, excluding induced changes in jobs (i.e., increase or decrease in number of employed individuals in a given year, relative to business-as-usual). Note that some jobs (e.g., construction) may be short-term, meaning this metric can be thought of in terms of job-years (one job that lasts for one year equates to one job-year). This graph reports the Direct and Indirect changes in jobs but excludes the Induced changes in jobs. For an explanation of these terms, see the [Input-Output Model](io-model.html) sheet.
  
  * Change in GDP
  
  Policy-induced changes in Gross Domestic Product in each year, relative to business-as-usual. This graph reports the total change in GDP and also breaks out changes in GDP by Fossil Fuel and Utilities, Manufacturing and Construction, and Other Contributors.
  
  * Percent Change in GDP
  
  Percent change in Gross Domestic Product (relative to business-as-usual) in each year. This graph reports the total percent change in GDP and also breaks out changes in GDP by Fossil Fuel and Utilities, Manufacturing and Construction, and Other Contributors.
  
  * Direct/Indirect/Induced Change in GDP
  
  Policy-induced changes in Gross Domestic Product in each year, relative to business-as-usual. This graph reports the total change in GDP and also breaks out changes in GDP by Direct, Indirect, and Induced impacts. For an explanation of these terms, see the [Input-Output Model](io-model.html) sheet.
  
  * Change in Employee Compensation
  
  Policy-induced change in total employee compensation in each year, further broken out by compensation for Fossil Fuels and Utilities, Manufacturing and Construction, and Others.
  
  * Change in Compensation per Employee
  
  Policy-induced change in compensation per employed person in each year.
  
  * Direct/Indirect/Induced Change in Compensation
  
  Policy-induced change in total employee compensation in each year, further broken out by Direct, Indirect, and Induced changes in compensation. For an explanation of these terms, see the [Input-Output Model](io-model.html) sheet.

* Financial: Direct Cash Flow Changes

Direct (first-order) change in capital expenditures, fuel and operational expenditures (including labor), and additional carbon tax on process emissions. This metric does not include subsidy payments, as these are considered cash transfers rather than capital or operational expenditures. This graph displays each of these components in addition to their sum, which is one way to represent the overall costs or savings of a policy package. The "Change in CapEx and OpEx" reports 
  
  * Cash Flow Change (by Entity)
  
  Direct (first-order) policy-induced change in cash flow by each of the nine entities tracked in the Energy Policy Simulator (Government, Non-Energy Industries, Labor and Consumers, Foreign Entities, Electricity Suppliers, Coal Suppliers, Natural Gas and Petroleum Suppliers, Biomass and Biofuel Suppliers, and Other Energy Suppliers). This metric is upstream of the macroeconomic input-output model and therefore do not include how government and households respend money. Since any money that is spent by one entity is received by another, the total of these cash flow changes sums to zero.
  
  * Government Cash Flow Components
  
  Direct (first-order) policy-induced change in government cash flow, broken out by Change in Revenue, Change in Energy Expenditures, and Change in Non-Energy Expenditures. 
  
  * Non-Energy Industries Cash Flow Components
  
  Direct (first-order) policy-induced change in non-energy industries cash flow, broken out by Change in Revenue, Change in Energy Expenditures, and Change in Non-Energy Expenditures.
  
  * Labor and Consumers Cash Flow Components
  
  Direct (first-order) policy-induced change in labor and consumers cash flow, broken out by Change in Revenue, Change in Energy Expenditures, and Change in Non-Energy Expenditures.
  
  * Foreign Entities Cash Flow Components
  
  Direct (first-order) policy-induced change in foreign entities cash flow, broken out by Change in Revenue, Change in Energy Expenditures, and Change in Non-Energy Expenditures.
  
  * Electricity Supplier Cash Flow Components
  
  Direct (first-order) policy-induced change in electricity supplier cash flow, broken out by Change in Revenue, Change in Energy Expenditures, and Change in Non-Energy Expenditures.
  
  * Coal Supplier Cash Flow Components
  
  Direct (first-order) policy-induced change in coal supplier cash flow, broken out by Change in Revenue, Change in Energy Expenditures, and Change in Non-Energy Expenditures.
  
  * Natural Gas and Petroleum Supplier Cash Flow Components
  
  Direct (first-order) policy-induced change in natural gas and petroleum supplier cash flow, broken out by Change in Revenue, Change in Energy Expenditures, and Change in Non-Energy Expenditures.
  
  * Biomass and Biofuel Supplier Cash Flow Components
  
  Direct (first-order) policy-induced change in biomass and biofuel supplier cash flow, broken out by Change in Revenue, Change in Energy Expenditures, and Change in Non-Energy Expenditures.
  
  * Other Energy Supplier Cash Flow Components
  
  Direct (first-order) policy-induced change in other energy supplier cash flow, broken out by Change in Revenue, Change in Energy Expenditures, and Change in Non-Energy Expenditures.

* Human Health & Social Benefits
  
  * Avoided Deaths Wedge Diagram
  
  This graph presents the relative impact of each enabled policy in a scenario in terms of the number of avoided premature deaths
  
  * Avoided Premature Deaths
  
  Annual avoided premature deaths as a result of a policy package
  
  * Monetized Avoided Deaths & Climate Benefits
  
  Monetized annual avoided premature deaths (according to the Value of a Statistical Life) and climate benefits (according to the Social Cost of Carbon) as a result of a policy package
  
  * Avoided Lost Workdays
  
  Annual avoided lost workdays as a result of a policy package
  
  * Avoided Respiratory Symptoms and Bronchitis
  
  Annual avoided respiratory symptoms and bronchitis as a result of a policy package
  
  * Avoided Asthma Attacks
  
  Annual avoided asthma attacks as a result of a policy package
  
  * Avoided Nonfatal Heart Attacks
  
  Annual avoided nonfatal heart attacks as a result of a policy package
  
  * Avoided Hospital Admissions
  
  Annual avoided hospital admissions as a result of a policy package
  
  * Avoided Respiratory ER Visits
  
  Annual avoided respiratory emergency room visits as a result of a policy package
  
  * Avoided Minor Restricted Activity Days
  
  Annual avoided minor restricted activity days as a result of a policy package

* Electricity Generation, Capacity, and Demand
  
  * Generation
  
  Annual electricity generation by power plant type
  
  * Policy-Driven Change in Generation
  
  Changes in electricity generation by power plant type due to enabled policies
  
  * Capacity
  
  Annual electricity generation capacity by power plant type
  
  * Policy-Driven Change in Capacity
  
  Changes in electricity generation capacity by power plant type due to enabled policies
  
  * Electricity Demand by Sector
  
  Electricity demand broken out by sector (District Heat & Hydrogen, Water & Waste, Agriculture, Transportation, Industry, Buildings)

* Electricity: Levelized Costs, Curtailment and Water Use
  
  * Levelized Cost of Electricity (after subsidies)
  
  Levelized Cost of Electricity by power plant type in 2020, 2030, 2040, and 2050 (after any subsidies for generation or power plant construction)
  
  * Curtailed Electricity from Renewables
  
  Annual curtailed electricity broken out by renewable power plant type
  
  * CO<sub>2</sub>e Emissions by Plant Type
  
  Annual Electricity sector CO<sub>2</sub>e emissions broken out by power plant type  
  
  * Water Withdrawals by Power Plants
  
  Annual water withdrawals (water taken to use for cooling) by power plant type 
  
  * Water Consumption by Power Plants
  
  Annual water withdrawals (water taken and not returned to the water body, i.e. evaporated) by power plant type 

* Transport: Vehicles by Technology

Sales by vehicle technology for the following classes of vehicles:
  
  * Sales: Cars and SUVs
  
  * Sales: Buses
  
  * Sales: Light Freight Trucks
  
  * Sales: Med & Heavy Freight Trucks
  
  * Sales: Motorbikes

Stock by vehicle technology for the following classes of vehicles:
  
  * Fleet Composition: Cars and SUVs
  
  * Fleet Composition: Buses
  
  * Fleet Composition: Light Freight Trucks
  
  * Fleet Composition: Med & Heavy Freight Trucks
  
  * Fleet Composition: Motorbikes

* Transport: Travel Demand, Fuel Use, and Emissions
  
  * CO2 Emissions by Vehicle Type
  
  Annual Transportation sector CO<sub>2</sub> emissions by vehicle type
  
  * Fuel Use by Fuel Type
  
  Annual Transportation sector fuel use by fuel type
  
  * Fuel Use by Vehicle Type
  
  Annual Transportation sector fuel use by vehicle type
  
  * Travel Demand (Passenger Modes)
  
  Annual cargo distance traveled by passenger vehicles, by vehicle type
  
  * Travel Demand (Freight Modes)
  
  Annual cargo distance traveled by freight vehicles, by vehicle type

* Industry: Fuel Use
  
  * By Industry (Including Feedstocks)
  
  Annual Industry sector fuel use by subindustry, including feedstocks
  
  * By Fuel (Including Feedstocks)
  
  Annual Industry sector fuel use by fuel type, including feedstocks
  
  * By Industry (Excluding Feedstocks)
  
  Annual Industry sector fuel use by subindustry, excluding feedstocks and only including fuels used for energy purposes
  
  * By Fuel (Excluding Feedstocks)
  
  Annual Industry sector fuel use by fuel type, excluding feedstocks and only including fuels used for energy purposes

* Industry: CO<sub>2</sub>e Emissions
  
  * Total by Industry
  
  Annual Industry sector CO<sub>2</sub>e emissions by subindustry
  
  * Total by Pollutant
  
  Annual Industry sector CO<sub>2</sub>e emissions by pollutant (N<sub>2</sub>O, F-gases in CO<sub>2</sub>e, CH<sub>4</sub>, CO<sub>2</sub>)
  
  * Process Emissions by Industry
  
  Annual Industry sector process emissions by subindustry; process emissions refer to pollutants that occur as a result of industry operations and which were not related to the combustion of fuel for energy
  
  * Process Emissions by Pollutant
  
  Annual Industry sector process emissions by pollutant (N<sub>2</sub>O, F-gases in CO<sub>2</sub>e, CH<sub>4</sub>, CO<sub>2</sub>); process emissions refer to pollutants that occur as a result of industry operations and which were not related to the combustion of fuel for energy
  
  * Energy-Related Emissions by Industry
  
  Annual Industry sector energy-related emissions by subindustry
  
  * Energy-Related Emissions by Pollutant
   
  Annual Industry sector energy-related emissions by pollutant

* Buildings: Energy Use
  
  * By Building Component
  
  Annual Buildings sector energy consumption by building component
  
  * By Building Type
  
  Annual Buildings sector energy consumption by building type (commercial, rural residential, urban residential)
  
  * By Energy Source
  
  Annual Buildings sector energy consumption by fuel type

* Energy Consumption
  
  * Primary Energy by Source
  
  Annual economy-wide primary energy consumption by fuel type
  
  * Primary Energy by End Use Sector
  
  Annual economy-wide primary energy consumption by end use sector (District Heat & Hydrogen, Water & Waste, Agriculture, Buildings, Transportation, Electricity, Industry, Geoengineering)
  
  * Per Unit GDP
  
  Annual economy-wide primary energy consumption per unit Gross Domestic Product 
  
  * Electricity Consumption
  
  Annual electricity consumption
  
  * Hard Coal Consumption
  
  Annual hard coal consumption
  
  * Lignite Consumption
  
  Annual lignite consumption
  
  * Natural Gas Consumption
  
  Annual natural gas consumption
  
  * Petroleum Fuels Consumption
  
  Annual petroleum fuels consumption
  
  * Liquid Biofuels Consumption
  
  Annual liquid biofuels consumption
  
  * Biomass Consumption
  
  Annual biomass consumption
  
  * LPG Propane & Butane Consumption
  
  Annual liquefied petroleum gas and butane consumption
  
  * Municipal Solid Waste Consumption
  
  Annual municipal solid waste consumption
  
  * Hydrogen Consumption
  
  Annual hydrogen consumption

* Energy Exports, Imports and Production
  
  * Energy Exports
  
  Annual energy exports by fuel type
  
  * Change in Energy Exports
  
  Annual policy-induced changes in energy exports by fuel type
  
  * Energy Export Revenue
  
  Annual energy export revenue by fuel type
  
  * Change in Energy Export Revenue
  
  Annual policy-induced changes in energy export revenue by fuel type
  
  * Embedded CO<sub>2</sub> in Exported Fuels
  
  Annual embedded CO<sub>2</sub> emissions in exported fuels by fuel type (fuel exports times the carbon intensities of the respective fuels)
  
  * Change in Embedded CO<sub>2</sub> in Exported Fuels
  
  Annual policy-induced changes in embedded CO<sub>2</sub> emissions in exported fuels by fuel type (fuel exports times the carbon intensities of the respective fuels)
  
  * Energy Imports
  
  Annual energy imports by fuel type
  
  * Change in Energy Imports
  
  Annual policy-induced changes in energy imports by fuel type
  
  * Energy Import Expenditures
  
  Annual energy import expenditures by fuel type
  
  * Change in Energy Import Expenditures
  
  Annual policy-induced changes in import expenditures by fuel type
  
  * Energy Production
  
  Annual domestic energy production by fuel type
  
  * Change in Energy Production
  
  Annual policy-induced changes in domestic energy production by fuel type

* Fuel Costs (by Fuel, by Sector)

Fuel costs in 2020, 2030, 2040, and 2050 by fuel type, by sector (Commercial Buildings, Residential Buildings, Electricity, Transportation, Industry, District Heat and Hydrogen)
  
  * Electricity
  * Hard Coal
  * Lignite
  * Natural Gas
  * Petroleum Gasoline
  * Petroleum Diesel
  * Biomass
  * Heavy or Residual Fuel Oil
  * LPG Propane or Butane
  * Hydrogen

* Technology Costs
  
  * Batteries
  
  Battery cost per kilowatt-hour, including the upfront battery cost and the balance of system costs (e.g., labor)
  
  * CCS Capital Equipment
  
  Capital cost of carbon capture and sequestration equipment to capture one metric ton of CO<sub>2</sub>e per year, broken out by sector (Electricity and Industry)
  
  * Onshore Wind Turbines
  
  Construction cost per unit capacity of onshore wind turbines, before construction subsidies
  
  * Offshore Wind Turbines
  
  Construction cost per unit capacity of offshore wind turbines, before construction subsidies
  
  * Solar PV (Utility-Scale)
  
  Construction cost per unit capacity of utility-scale solar photovoltaic systems, before construction subsidies
  
  * Hydrogen Electrolyzers
  
  Capital cost of hydrogen production equipment to produce one kilogram H<sub>2</sub> per year
