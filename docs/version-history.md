---
layout: page
title:	"Version History"
---
This page tracks updates that have been made with each version of the Energy Policy Simulator.

### **3.0.0 - Oct 19, 2020**

* New Input-Output Model
  * An economic input/output (I/O) model has been added as a component of the Energy Policy Simulator.
  * New output metrics include the change in gross domestic product (GDP), employment (jobs), total employee compensation, average compensation per employee, number of union and non-union jobs, government spending, budget deficit/surplus, household tax revenue, payroll tax revenue, corporate income tax revenue, size of the national debt, and interest paid on the national debt.
  * Changes in GDP, jobs, and compensation can also be visualized disaggregated by economic sector or by their direct, indirect, and induced components.
  * Respending of changes in cash flow for government, households, and industries is now accounted for, providing a holistic look at policy impacts on economic activity.
  * New Government Revenue Accounting (GRA) settings allows the user to specify how government raises or spends changes in revenue caused by the policy package.  Options include changes in regular spending, deficit spending, household taxes, payroll taxes, and corporate income taxes.
  * Feedback loops from the I/O model to the Transportation, Buildings, and Industry sectors capture the energy demand and emissions associated with indirect and induced economic activity.
  * A new [documentation page](io-model.html) explains the I/O model in detail.
  * We gratefully acknowledge the invaluable contributions of the [American Council for an Energy-Efficient Economy](https://www.aceee.org/) (ACEEE), [Jim Barrett](https://www.barretteconomics.com/), and [Skip Laitner](https://www.linkedin.com/in/skip-laitner-746b124/) for their guidance and advice in implementing this feature, and for allowing us to learn from the [DEEPER I/O model](https://www.aceee.org/files/pdf/fact-sheet/DEEPER_Methodology.pdf), originally created by Skip Laitner.
* Improved Public Health Calculations
  * In addition to the policy package's effects on premature mortality (introduced in version 1.0.3), the EPS now calculates impacts on 10 additional health outcomes, including lost workdays, hospital admissions, non-fatal heart attacks, asthma attacks, respiratory symptoms and bronchitis.
* Data Updates
  * First simulated year advanced from 2018 to 2019
  * Data in input variables based on EIA Annual Energy Outlook updated to use AEO 2020 values
  * Various other input data updates 
* Other Improvements
  * Industry Sector
    * Industrial process emissions multipliers (used in indst/BPEiC and indst/PERAC) are now disaggregated by gas.  These multipliers now allow for replacement of BPEiC data with arbitary, user-specified data while keeping abatement potentials and costs in PERAC in sync with BPEiC.
    * Added revenue data for "water & waste" industry (water treatment, wastewater, solid waste collection, landfilling, recycling, etc.)
    * Use of the material efficiency policy on the chemicals industry and on the other industries category is now disallowed because these industry categories are aggregates in our new I/O data (chemicals includes pharmaceuticals), and the material efficiency cannot target only the relevant parts of these aggregates to obtain accurate financial outcomes
    * Industry now can pass on a share of its policy-driven changes in expenditures to buyers of its products (specified in indst/SoCiIEPTtB).  Removed embedded carbon and associated cost calculations for vehicles, power plants, and building components, to avoid double-counting.  (The new approach covers all products in the economy and all sources of expenditure changes, not just a carbon tax.)
    * The model now accounts for more different types of costs that are passed through to buyers when calculating the policy-driven change in industrial production, such as the costs of capital equipment purchased in response to energy efficiency standards and the costs of implementing process emissions abatement policies.
  * Electricity Sector
    * Peak power demand calculations now calculate summer and winter peaks separately
    * Peak power demand calculations use equipment load factors (elec/ELF) to more accurately determine peak demand, which is particularly important in scenarios with substantial electrification
    * Users may now override endogenous learning for electricity generation capacity by specifying time series capital costs in elec/CCaMC
    * Imported electricity price and BAU exported electricity price may now be customized
    * Balance of system is now included in grid battery costs (and is unaffected by endogenous learning)
    * Soft costs for onshore wind, offshore wind, and solar PV power plants (and distributed solar PV) now accept time-series BAU data
    * Power plant fuel type shifting (such as coal-to-gas retrofits) will now only occur if the target power plant type is economic (not subject to economically-driven early retirement) or if the target fuel is a drop-in replacement (i.e. no retrofitting required).
    * Grid battery policy is now set as a fraction of potential capacity achieved rather than as a percentage growth rate, allowing for finer control over timing and quantity of grid battery deployment
  * Fuels
	  * Added output graphs of Embedded CO2 in Exported Fuels and Change in Embedded CO2 in Exported Fuels
    * The carbon tax rate may now be explicitly set for District Heat and Hydrogen sector instead of inheriting the Industry sector rate
    * Fuels cost input data and Vensim sheet reorganized for clarity and ease of adaptation to other regions
    * Change in carbon tax revenue and change in fuel tax revenue are now calculated explicitly, to support new government revenue handling options
    * Reduced domestic demand for domestically-produced fuels is now partially compensated for by increased exports (fuels/PoFDCtAE)
  * Buildings Sector
    * Implemented cash flows for efficient building component rebate policy
    * Building fuel shifting policy now accounts for incremental capital costs of electrified (i.e. heat pump) building heating systems and water heaters
  * Other
    * WebAppData now detects duplicate and missing policy ID numbers
    * The model no longer uses GET DIRECT DATA to access data from outside of the model run timeframe
    * Model structure diagram updated to show new economic and public health outputs
    * Fraction of technology outside modeled region that affects endogenous learning can now be customized (endo-learn/FoTOMRAEL)
    * All Python scripts now include the capability to limit the time range of data written to output files
    * Policy package CapEx + OpEx and Cost Curve output graphs now respond to user's government revenue handling selections to determine revenue neutrality
* Bug Fixes
  * Fixed off-by-one-year error in cement process CO2 multipliers (indst/BPEiC) and two missing formulas for cement (indst/PERAC)
  * Do not exclude heat as a fuel type that can power industry CCS
  * Added geoengineering sector to energy-related CO2 output graphs
  * Limited effect of building component labeling policy to affected market share (bldgs/PPEIdtIL)
  * Fixed formula error in "Change in Amount Spent on Vehicle Maintenance"
  * Fixed double-counting of certain cash flow changes due to changes in industrial production
  * Very high carbon tax rates applied to industrial process (non-energy) emissions can no longer cause oscillating production changes
  * Fixed bug in "Subsidy Paid on Distributed Solar Capacity" formula
  * Capital costs for new CCS equipment are now allocated amongst power plant types and amongst industries proportionally to year-over-year increase in CCS usage instead of total current-year CCS usage by each plant type and industry
  * Power plant decommissioning costs are no longer charged if a power plant type has retired to zero and there is no capacity left to retire
	* The industrial fuel shifting policy's capital equipment costs now account for increases in usage of all industrial fuel types

### **2.1.2 - July 9, 2020**

* Fixed minor formula error in variable "Potential RPS Qualifying Electricity Output" and its BAU equivalent

### **2.1.1-us-v2 - May 12, 2020**

* Updated COVID-19 recession's GDP impact and elasticities of sectoral-energy-use-to-GDP using latest data from EIA Short-Term Energy Outlook (ctrl-settings/GDPGR, ctrl-settings/EoSEUwGDPiR, plcy-schd/FoPITY)

### **2.1.1 - May 12, 2020**

* Major Improvements
	* Added capability to simulate COVID-19 recession impacts, adjustable in the web interface via a policy-like slider and implementation schedule.  This simulates effects of exogenous GDP changes on demand for energy, energy-using services, and products.  It can be adapted for different countries or reconfigured to represent other economic recessions (or booms) via updated input data.
	* The CCS policy lever has been overhauled.  It now is set in terms of a percentage of CO<sub>2</sub> captured, is subscripted by sector (electricity and industry sectors), and can be used to capture industrial process CO<sub>2</sub> and CO<sub>2</sub> from fuel burned to power the CCS process itself.
* Minor Improvements
	* Added graphs of industry sector energy-related CO<sub>2</sub>e emissions by industry and by pollutant to web interface
	* Vehicle maintenance costs are now included and are considered in vehicle technology selection
	* When new peaker plants are built to meet peak electricity demand, cost-based allocation is used instead of allocating proportinally to existing peaker capacity
	* Output graph definitions in WebAppData now have an include/exclude flag, and localizing units is easier thanks to a new unit selection tab
	* Added three *X*-per-unit-BAU-GDP output graphs to WebAppData (unflagged for U.S.) to support regions where this metric is commonly used, such as India
	* Non-country multipliers for industrial process emissions (indst/BPEiC and indst/PERAC) now accept time series values
	* Updated input data in elec/ARpUIiRC, elec/BCRbQ, elec/BECF, elec/BRPSPTY, elec/DRC, elec/DRCo, elec/CCaMC, elec/MCGLT, fuels/BCFpUEbS, and trans/BVTStL
	* The relationship between increases in transmission capacity and the usable fraction of flexibility points is now governed by an input variable (elec/EoTCCwTC) rather than a hard-coded relationship, giving the EPS the flexibility to better represent renewables deployment and curtailment in power systems facing varying degrees of transmission constraints
	* In the District Heat sector, heat pumps can be represented using the electricity fuel type.  dist-heat/EoCtUH now includes heat pump efficiency data.
	* Metallurgical (feedstock) coal is now included in industrial coal use (indst/BIFUbC and indst/BPoIFUfE)
* Bug Fixes
	* Added missing non-country multiplier for cement process emissions (in indst/BPEiC and indst/PERAC)
	* Nuclear lifetime extension policy is no longer shown in U.S. web app because BAU data already incorporate extensions (to 80-year operating lifetimes) except where a plant is known to be closing sooner
	* Labor now correctly receives a share of revenues from building retrofitting and from distributed solar deployment
	* Fixed overly-high costs for utility demand response (DR) programs caused by outliers in input dataset

### **2.1.0 - Jan 21, 2020**

Note that starting with this release, Vensim 8 or later (64-bit) is required to run the Energy Policy Simulator. Update your copy of Vensim Model Reader for free from [Ventana Systems' website](https://vensim.com/free-download/).

* New Features
	* New Sector: Geoengineering.  Currently, the geoengineering sector includes one technology, direct air capture (DAC), and its associated policy.
	* Implemented cost-driven power plant retrofitting (such as coal-to-gas) and fuel type shifting (for instance, between crude oil, heavy fuel oil, and diesel)
	* New Policy: Subsidize electricity capacity construction
	* CSV Export Tool now can build its own file list, removing the need for manual updates to this tool (except for changes in number or names of custom policy schedules)
* Data Updates
	* Data on BAU industrial process emissions, abatement potentials, and costs (indst/BPEiC, indst/PERAC) has been updated to the latest sources, greatly streamlined, and can be toggled to select any country, facilitating EPS adaptations.  Industrial process emissions policy levers updated accordingly.
	* Updated to latest data in elec/CCAMC (from EIA, LBNL, and NREL)
	* Updated to latest GREET model data in fuels/BFPIaE, fuels/PEI, web-app/BCF
	* Updated data in endo-learn/BGSaWC, elec/EoPPFTSwFP, elec/ARpUIiRC, elec/BDSBaPCF, and fuels/BS
* Bug Fixes and Minor Improvements
	* Added graphs of GHG emissions, energy-related CO2 emissions, and energy use per unit BAU GDP.  These graphs not shown in the U.S. web interface by default but are available in Vensim and can be exposed in the web interface in regional EPS adaptations.
	* The model now tracks fuel-cost-driven changes in cargo distance transported down to the vehicle technology (engine type) level
	* Certain multi-line graphs changed to stacked area, to take advantage of new support for mixed-sign data series in stacked area charts
	* Fixed R&D levers to refer to LPG and hydrogen vehicles instead of nonroad vehicles
	* Improve subscript usage in energy use total variables
	* Improve accuracy of assignment of process emissions abatement to correct pollutants
	* Corrections to hydrogen production efficiencies in hydgn/HPEbP
	* The policy to change electricity imports is now subscripted by electricity source (power plant type) in the foreign country

### **2.0.0 - Oct 7, 2019**

* New Hydrogen Supply Sector
	* There now exists a new sector in the EPS that calculates hydrogen production (in response to hydrogen demand from other sectors) and associated energy use, emissions, costs/savings, electricity demand response potential, etc.
	* New Policy: Shift Hydrogen Production Pathway (e.g. in the U.S., from steam reforming of natural gas to electrolysis)
	* District Heating Sector renamed District Heat and Hydrogen Sector, grouping these energy carriers in various totals and output graphs
* Fuels
	* Five new fuel types have been added: (1) crude oil, (2) heavy or residual fuel oil, (3) LPG / propane / butane, (4) municipal solid waste, and (5) hydrogen.  Each of these fuels has been added to each sector that can use it.
	* "jet fuel" renamed "jet fuel or kerosene" and extended to the buildings sector
	* Different pollutions emissions intensities may now be specified (in fuels/PEI) for different industries
	* Fuels' pollutant emissions intensities may now improve (or worsen) over the model run in the BAU case by specifying values in new input variable fuels/PEIIR
	* Policy-driven changes in imports and exports of fuels are now calculated
	* Corrected omission of biomass and diesel burned in district heat plants, and diesel burned in power plants, from fuel use totals
	* Total fuel use disaggregated by fuel and by sector is now provided on the "Cross-Sector Totals" sheet in Vensim
	* Thermal fuel production subsidies now account for fuel imports and exports, improving accuracy
	* Retail prices of district heat and hydrogen are now by default influenced by changes in costs for district heat producers and hydrogen producers, with control lever plcy-ctrl-ctr/BAEPAbCiPC governing default behavior.  A subscripted policy lever toggles this behavior in the policy case.
* Transportation Sector
	* Two new vehicle technologies have been added: LPG vehicle and hydrogen vehicle
	* New Policy: Reduce EV Range Anxiety and Charging Time (with support variable trans/BRAaCTSC)
	* New Policy: EV Charger Deployment (with support variable trans/EoCSoEVMS)
	* New Policy: Hydrogen Vehicle Sales Minimum
	* Removed EV Perks policy
	* Added calculation of cost of policy-driven EV charger deployment and corresponding changes in cash flows to government, industry, and labor
	* Non-road vehicle types (aircraft, rail, ships) now have associated vehicle technology types, and the EV and Hydrogen Vehicle mandate policy levers can be applied to these vehicle types.  The "nonroad vehicle" placeholder technology type has been removed.
	* trans/AVL Average Vehicle Lifetime is now subscripted by cargo type
	* Fuel economy standards are now subscripted by cargo type and vehicle type.  Applicable vehicle technologies are specified in a new input variable, trans/VTStFES.
	* Conventional pollutant standards for separately-regulated pollutants are now subscripted by pollutant type
	* Improved handling of retirements of integer numbers of vehicles in the early years of a model run for vehicle types with relatively small numbers of vehicles (such as aircraft or freight ships)
	* Improved methodology for passenger ships and freight ships, including adjustment to account for the EIA data source provides distance traveled only for domestic shipping, not international shipping
* Electricity Sector
	* Decommissioning costs for retiring power plants have been added
	* Water withdrawals and water consumption by power plants are now calculated using new input variables elec/WUbPPT and web-app/LpWOU
	* The RPS is now calculated as a share of electricity demand after net imports rather than a share of potential electricity output.  Added explanatory comment to model structure regarding RPS calculation approach.
	* Fixed bug preventing web app from displaying policy lever for banning new lignite power plants
	* Fixed omission of demand response implementation costs to industry from electricity sector total on Debugging Assistance sheet
	* Fixed omission of utility payments for demand response services from total OM expenditures cost metric
	* Cash flows associated with importing and exporting electricity are assigned to the new "foreign entities" cash flow entity
	* The policy lever that toggles between BAU and non-BAU mandated capacity construction schedules is now subscripted by power plant type
	* Power plant retirements are now quantized by the minimum power plant capacity, elec/MPPC
	* Early retirements of power plants for economic reasons now takes into account fixed O&M costs (in addition to variable O&M and fuel costs)
	* Plants whose fuel + variable O&M + fixed O&M costs are below the average such costs for all power plants in a given year may no longer be retired early for economic reasons in that year
	* Other small accuracy improvements to early retirement calculations
* Industry Sector
	* New Policy: reduction in non-energy, non-agriculture industry product demand (e.g. material efficiency, product longevity, re-use, intensification of product use, etc.)
	* New Policy: reduction in fossil fuel exports
	* The carbon tax now endogenously drives adoption of process emissions abatement measures, where it is financially advantageous to do so.  The process emissions policy levers now affect any remaining emissions after price-driven abatement.
	* Added calculation of cash flow changes due to changes in production by industries (including reduced sales of outputs and reduced purchases of inputs)
	* Changes in production levels of domestic fuel industries are now calculated explicitly from fuel use, import, and export data, rather than being estimated using elasticities
	* indst/BPoIFUfE BAU Proportion of Industrial Fuel Used for Energy is now subscripted by industry category
	* The industrial fuel shifting policy has been generalized to cover all fuel combinations and consolidated into a single lever.  It now contains data allowing shifting to a mixture of electricity and hydrogen, based on each industry's electrification potential.
	* The model now differentiates between industry expenses that vary with production and those that do not (indst/FoNEtVwP)
	* The industrial fuel shifting policy is now subscripted by industry type
	* The cost of implementing industrial energy efficiency and fuel shifting policies per unit energy (indst/CtIEPpUESoS) now accepts time series data
* Agriculture, Land Use and Forestry
	* New Policy: shift animal product use to non-animal product use
	* land/BLACE renamed land/BLAPE BAU LULUCF Anthropogenic Pollutant Emissions and subscripted by pollutant
* Buildings Sector
	* The Retrofitting policy has been rebuilt.  It is now subscripted by building type and allows the user to set a share of preexisting buildings to be affected.  New input varible bldgs/BRESaC governs energy savings and costs by component type.
	* The building component electrification policy has been generalized to support shifting to any combination of fuels specified in a new input variable, bldgs/RBFF.  In the U.S. dataset, this policy continues to be used as an electrification policy.
	* The building fuel shifting policy is now subscripted by building component
	* bldgs/BFoCSbQL now reads separate input files for urban and rural residential, so it can be adapted for regions that want to use different data for these building types
	* Implemented correction factor that aligns BAU Components Energy Use with the value from input data variable BCEU BAU Components Energy Use
	* bldgs/CL Component Lifetime is now subscripted by building type
	* Fixed omission of changes in the cost of biomass burned in buildings from the total change in biomass and biofuel supplier cash flow
	* Fixed bug where building component electrification could be mistaken for efficiency changes when calculating changes in cost of new building components
* Financial Calculations and Outputs
	* The Cash Flow Entity subscript has been redesigned.  It now contains the following nine entities: government, nonenergy industries, labor and consumers, foreign entities, electricity suppliers, coal suppliers, natural gas and petroleum suppliers, biomass and biofuel suppliers, other energy suppliers.  This helps with tracking cash flow allocations more uniformly and allows handling of imports and exports to/from the modeled region.
	* Cash flow allocations have been redesigned for improved accuracy, clarity, and code uniformity across sectors and cash flow entities
	* Changes in cash flow for each of the nine cash flow entities are now disaggregated into changes in domestic revenue, changes in export revenue, changes in energy expenditures, and changes in non-energy expenditures
	* Cash flow changes by entity now include cash flows pertaining to imports, exports, and changes in industrial production (including changes in industrial inputs and outputs)
	* Updated the "CapEx + OpEx" cost metric to include carbon tax on process emissions
	* Changed the "CapEx + OpEx (revenue-neutral carbon tax)" metric to include carbon tax on process emissions, and to treat all changes in taxes and subsidies as revenue neutral, not only carbon taxes
	* Added output variables to allow rebates of taxes and rebates of withdrawn subsidies to be graphed separately, for regions where this is desired
	* Removed the "Total Outlays" cost metric (and its revenue-neutral version), as they are now superfluous
	* Improved accuracy of calculation of change in thermal fuel subsidies paid, particularly in scenarios with high carbon prices
* CCS
	* CCS capital equipment and OM costs are now allocated to electricity sources within the electricity sector and to industries within the industry sector
* District Heat
	* District heat "shift from coal to other fuels" policy has been generalized to permit shifting from any combination of fuel types.  In the U.S. model, the target fuel is now hydrogen.
* Cross-Sector
	* New Policy: Fuel Price Deregulation
	* A new control lever, plcy-ctrl-ctr/BENCEfCT, allows non-CO2 emissions to be exempted from the carbon tax
	* New Policy: Toggle Whether Carbon Tax Affects Process Emissions (reverses the behavior of the corresponding control lever in the policy case)
	* New Policy: Toggle Whether Carbon Tax Affects Non CO2 Emissions (reverses the behavior of the corresponding control lever in the policy case)
	* A new control lever, plcy-ctrl-ctr/BAEPAbCiGC, controls whether policy-driven changes in electricity generators' costs affect electricity prices
	* The fixed electricity pricing policy has been repurposed as a policy that toggles whether policies affect electricity prices, reversing the default behavior specified in plcy-ctrl-ctr/BAEPAbCiGC
	* add-outputs/SCoHIbP now reads separate input files for buildings and industry, so it can be adapted for regions that want to use different data for these sectors
	* Cleaned up earlier advancement of first simulated year to 2018
	* Updated acronym-key.xlsx with more detail on variable update priorities and when specific variables should be updated
* Updated input data in variables fuels/BS, trans/SYVbT, trans/SYFAFE, trans/BNVFE, trans/BHNVFEAL, trans/BAADTbVT, trans/BCDTRtSY, trans/BESP, elec/BGDPbES, elec/BDSBaPCF, indst/BIFUbC, indst/BPoIFUfE, bldgs/DSCF, ccs/CPbE and ccs/CSA.
* A new CSV Export Tool (located in InputData) can be used to speed the process of exporting some or all of the input data required by the model (from the blue tabs of the Excel files).
* Internals
	* Optimized the memory use of the largest variables, allowing continued growth of EPS model without exceeding the memory limits in Vensim 7.x-series programs
	* Greatly reduced the number of equations needed in certain variables on the Fuels Sheet, in the Electricity Sector, and in Web App Support Variables via improved use of subscript mapping
* Web App
	* Added ten graphs pertaining to energy imports, exports, production, and associated revenue and expenditures
	* Added eight single-sector CO2e graphs
	* Added seven graphs showing components of cash flow changes for particular cash flow entities
	* Added four graphs with sector-specific CO2e wedge diagrams
	* Added three graphs of fuel price by sector for new fuel types
	* Added two graphs showing water withdrawals and water consumption by power plant type
	* Added two graphs of industry fuel use excluding feedstocks
	* Added graph of electricity demand by sector
	* Added graph of hydrogen electrolyzer capital cost
	* Added graph color key to WebAppData.xlsx to assist in customizing graphs for different regional EPS adaptations
	* Added medium-size output currency unit (in web-app/OCCF), used in three technology cost graphs
	* Fixed transposed labels on "Direct Cash Flow Changes (by Actor)" graph
	* Removed some duplicative variables in the calculations for the CO2e by Sector graph
	* Removed agriculture and "water + waste" from Industry sector fuel use graphs, as these are considered separate sectors
* Python Scripts
	* A new Python script enables the simulation of carbon cap-and-trade policies by estimating emissions permit prices
	* A new output variables list file, "OutputVarsForCarbonCapToTaxScript.lst" works in conjunction with the new Python script
	* A new documentation page describes how to use the Python script to simulate cap-and-trade policies
	* Sync software (such as DropBox or Google Drive) will no longer interrupt batch runs by locking the output .vdf file

### **1.4.3-us-v2 - May 31, 2019**

* Updated US input data to latest year sources (including EIA AEO 2019 and EPA Greenhouse Gas Inventory 2019)
* Industry Sector
	* Applied a scaling factor to methane process emissions from natural gas and petroleum systems to account for a [recent study](https://science.sciencemag.org/content/361/6398/186) showing that the EPA Greenhouse Gas Inventory underreports methane leaks
	* Corrected a minor formula error in natural gas methane emissions
* Buildings Sector
	* Corrected formula in bldgs/DSCF to average the low and mid technology progress cases, while omitting the constant technology case.
	* Smoothed the first 3 years of bldgs/BCEU data for certain components to avoid sharp discontinuities in Retiring Components Potential Energy use during the model run
	* Fixed minor error in bldgs/BCEU district heat projections
* Transportation Sector
	* BEV and PHEV vehicle prices were updated in trans/BNVP to reflect weighted averages of all relevant AEO vehicle types (e.g., 100-, 200-, and 300- mile range BEVs). The BEV calculation includes an additional $4,000 to represent the perceived range anxiety cost. The BAU EV subsidy percent (trans/BESP) was also updated to reflect updated vehicle prices.
	* Corrected minor error in trans/BS for jet fuel
	* Updated lifetime of buses in trans/AVL
	* Updated price of battery passenger HDVs to use the current electric bus price, scaled to show the same price decrease as passenger LDVs
	* The share of new passenger LDVs and HDVs that can be electric was changed to reach 100% by 2050 in trans/MPNVbT
	* The maximum biofuel blending allowed in aviation, ships, and rail, found in trans/MPoEFUbVT, was changed from 0% to now reach 20% by 2040
* Electricity Sector
	* Changed the Renewable Portfolio Standard policy to a Clean Energy Standard, to better reflect national conversations around electricity sector decarbonization. Qualifying resource definitions were updated in elec/RQSD and elec/BRQSD, and the BAU standard in elec/BRPSPTY was updated to reflect state RPS/CES targets and BAU hydro and nuclear capacity.
	* Updated elec/MCGLT to allow more renewable energy additions each year. A multiplier was applied to the existing offshore wind values, and solar PV was adjusted to allow for the same annual additions as wind, once significant solar deployment is achieved. Also included a minor update to value for natural gas.
	* Changed the petroleum value for elec/NSDoDC to be the same as natural gas peaker plants. The previous standard deviation in petroleum plant dispatch costs was so wide that the model over-dispatched petroleum relative to other projections.
	* Updated Norm St Dev of New Capital Costs for solar in elec/NSDoNCC to reflect recent data from Berkeley Lab
	* Changed reference source for onshore and offshore wind peak time capacity factors in elec/PTCF
	* Changed offshore wind methodology in elec/CCaMC to use weighted average of the low annual technology baseline (ATB) overnight capital costs
	* To avoid nuclear curtailment, which is not representative of real-world systems, elec/BDSBaPCF and elec/BGDPbES were changed to allow nuclear to bid at peak capacity factor and have 100% guaranteed dispatch, respectively.
* Other Model Components
	* Updated natural gas and coal prices in fuels/BFCpUEbS to use AEO short-term forecasts, which are then scaled by trends in the AEO reference case. This change more accurately reflects near-term fossil fuel prices.
* Web App
	* Exposed the electric freight LDV sales mandate policy in the web interface.
	* Updated the maximum slider settings for the Clean Energy Standard and policy guidance for Fuel Economy Standards, Building Component Electrification, Early Retirement of Power Plants, Grid-Scale Electricity Storage, Reduce Plant Downtime, Clean Energy Standard, Industry Energy Efficiency Standards, and Subsidy for Electricity Production

### **1.4.3 - Mar 30, 2019**

* Industry sector
	* The coal-to-NG policy has been repurposed as an electrification policy (to accompany the existing NG-to-electricity policy). Policy name and description in WebAppData updated accordingly.
	* The minimum achievable percentage of clinker in cement has been reduced to 60% (from 70%) based on newer data sources
* Buildings Sector
	* Added explanatory note regarding "BCEU BAU Components Energy Use" on the "Buildings - Main" sheet in Vensim
	* The default implementation schedule for the accelerated retrofitting policy now ramps in linearly
	* Fixed minor error in referenced year in urban residential buildings' cooling electricity use
* Transportation Sector
	* Improved accuracy of Fleet Average Fuel Economy calculations, particularly in cases with early ramp-in of a 100% EV sales mandate
	* Fixed error in start year number of buses
	* Corrected extrapolation formula for freight LDVs in trans/BHNVFEAL
	* Removed propane-powered freight LDVs from natural gas LDVs category in trans/SYVbT
	* Replaced two duplicate variables in Transportation cash flow calculations with shadow versions of their equivalents
	* Added check to prevent impossible (>100%) values in "Minimum Required EV Sales Perc"
* Electricity Sector
	* Corrected formula in elec/NSDoDC Normalized Standard Deviation of Dispatch Costs
	* Fixed bug where elec/FPCbS was not being read in from input data file
	* Electricity producers no longer have foresight to future year additional RPS policy setting values until the first year when the RPS policy comes into effect (as years before this may be in the past, when divergence from BAU is undesirable)
* Other Model Components
	* Fuel Price Multiplier for Sensitivity Analysis Runs now affects only the policy case, not the BAU case, allowing for elasticities and price-based retirement mechanisms to function fully
	* Updated example of high-importance variable in acronymn-key.xlsx "About" tab
	* Copied source graph into endo-learn/PDiBCpDoC
* Web App
	* In the web app, revenue-neutral carbon tax versions of cost outputs are now shown by default.	The standard versions of these cost outputs are still available (and are now labeled "no revenue use assumption").
	* The four web app cost output graphs now disaggregate changes in cost into (1) Fuel + O&M, (2) Capital Equipment, (3) Subsidies & Other, if applicable, (4) Carbon Tax Rebate, if applicable, and (5) Total
	* Removed Waste Management and Agriculture from existing Industry sector process emissions graphs for consistency in defining these activities as separate sectors
	* Corrected unit labels in several web app graphs in the "Transport: Fleet Composition by Technology" category
	* Added new web app output graph: Fuel Use by Vehicle Type
	* Added web app output graph of Total CO2e Emissions by Industry
	* Added web app output graph of Total CO2e Emissions by Pollutant (from the Industry sector)
	* Fixed minor typos in web app policy descriptions for Accelerated Retrofitting (Buildings sector) and Carbon Tax
	* Fixed unit label for CCS equipment technology cost web app output graph (MT to metric ton)
	* Updated web app guidance text for building components retrofitting policy to match current model structure
* Python Scripts and Cost Curve Generator
	* An Excel-based Cost Curve Generator has been added to the model distribution, including instructions and pre-loaded example data
	* A copy of CreateContributionTestScript.py set up for the EI reference scenario has been added to the model distribution
	* CreateCombinationsScript.py and CreateContributionTestScript.py now share a common, simplified format for their policy lists
	* The Python scripts' policy lists have been updated to include all enabled policies in WebAppData. Policy short names and group names now match their names in WebAppData.
	* The default variables specified in OutputVarsToExport.lst are now the ones needed to create a cost curve using the Cost Curve Generator

### **1.4.2-us-v2 - Jan 23, 2019**

* U.S. input data updated to latest year sources (including EIA AEO 2018)
* U.S. currency unit changed from inflation-adjusted 2012 USD to inflation-adjusted 2018 USD
* First simulated year advanced to 2018 (from 2017)
* Fixed small errors in formulas for elec/NSDoNCC and elec/NSDoDC
* Updated data for HDVs in trans/MPNVbT, improving calculations of alternative fuel HDV deployment
* Updated NDC reference scenario to continue to narrowly hit its target, given lower BAU emissions in 2025


### **1.4.2 - Aug 14, 2018**

* Transportation Sector
	* New Policy Lever: Conventional Pollutant Standards
	* The effect of changes in fuel economy on separately-regulated, conventional pollutants is now handled properly and can be customized to different regions using new input variable trans/SRPbVT
	* Updated to latest edition of data source (BTS NTS table 1-11), used for certain vehicle types in trans/SYVbT
	* Improved calculations for freight ships in trans/AVLo and trans/BAADTbVT
	* Changed trans/MPoEFUbVT to prevent the LCFS policy from increasing the share of electricity in plug-in hybrids' fuel mix
* Electricity Sector
	* Fixed incorrect calculation of grid battery capacity when affected by the grid battery promotion policy using a non-standard policy implementation schedule
	* Fixed error in the check for negative additions to grid battery storage capacity
	* Improved calculation of the BAU Transmission Connectivity Coefficient (elec/FPC-BTCC) in the U.S. input dataset
	* It is now possible to customize the number of flexibility points used per MW of flexibility-demanding resources in new input variable elec/FPCbS
* Industry Sector
	* Fixed missing Industry Category subscript in model structure for variables indst/PPRiFUfIIaIoE and indst/PPRiFUfICaWHR
	* Fixed missing label in .csv file for indst/PPRiFUfERoIF
	* Removed Industrial Fuel subscript from a few variables in the Industry sector that were not making use of the subscript
	* Coal-to-NG and NG-to-electricity maximum allowable web app policy settings increased, and guidance text for electrification updated
* Endogenous Learning
	* endo-learn/PDiBCpDoC updated with latest year's data
* Fuels
	* fuels/BFCpUEbS now includes sheets (containing zeroes) for hydro, wind, solar, and geothermal, to facilitate repurposing one or more of these subscript elements to a fuel-using plant type when the EPS is adapted to a new region
* Web Application
	* Agriculture and waste management are no longer grouped with the industry sector on the following graphs: Emissions- CO2e by Sector, Emissions- Energy-Related CO2 by Sector, Emissions- Energy-Related CO2 by Sector (reallocated electricity & heat)
* Python Scripts
	* Python script CreatePermutationsScript.py renamed CreateCombinationsScript.py so the name better reflects the behavior
	* The Contribution Test and Combinations Python scripts now include a setting allowing for the selection of the desired policy implementation schedule file

### **1.4.1 - June 22, 2018**

* Fixed error in max electricity curtailment threshold
* Improved electricity curtailment calculations
* Weighted average vehicle fuel prices are now calculated even for vehicle technologies that have zero vehicles, so the model can properly assess the NPV lifetime costs of starting to deploy those vehicles
* Fixed erroneous, extremely small (3 BTU/year) heat demand from building envelope components

### **1.4.0 - June 4, 2018**

* Improvements
	* Output graphs
		* The web application interface now supports two-tier menus for selection of all output graph types
		* Many new output graphs have been added to the web application interface, providing easier access to data that formerly was only visible in the downloadable model.	Examples include: fuel and technology prices, electricity curtailment, transport demand, vehicle sales by technology, and more.
		* The "Web Application Support Variables" sheet has been completely rebuilt.	It is now better-organized and matches the graph navigation structure in the web app.
	* Endogenous Learning
		* Endogenous learning calculations are now handled on a separate "Endogenous Learning" sheet.	Input data structure updated accordingly.
		* Technologies subject to endogenous learning (onshore wind, offshore wind, solar PV, CCS, batteries) now consider cumulative global deployment in addition to in-region deployment when determining technological advancement.
		* Hard costs and soft costs for capacity types subject to endogenous learning are now tracked separately.	Endogenous learning only affects hard costs.
		* New Policy Lever: Reduce soft costs of capacity construction
	* Policy Implementation Schedules
		* The user may now select from up to nine different policy implementation schedules via a slider in Vensim and may save that selection into the associated scenario (.cin) file.	It is no longer necessary to rename .csv files in plcy-schd/FoPITY/ in order to run scenarios that use different policy implementation schedules.
		* The default policy implementation schedule now starts phasing in policies from 2019 rather than from 2018 (except the RPS, as utilities change their behavior in response to future RPS values).	Updated U.S. NDC scenario accordingly.
	* Electricity Sector
		* Added imported electricity to graphs of electricity output by type and change in electricity output by type
		* Added a control lever that allows emissions associated with imported electricity to be included in reported emissions totals for the modeled region.	Enhanced elec/EIaE accordingly.
		* Added a third type of BAU Electricity Sector subsidy (reducing the cost of capacity construction).	The new subsidies are properly affected by the existing BAU subsidy reduction policy.
		* Now only a share of Transmission Capacity Across Modeled Region Border provides flexibility points
		* Transmission Capacity Across Modeled Region Border now contributes to peak demand reduction
		* Improved accuracy of calculation of change in grid battery costs
		* The cost of providing demand response (DR) services is now included in cash flow calculations
		* Replaced elec/MPCFR with an internal calculation, improving accuracy
	* Transportation Sector
		* The mechanism for estimating LCFS credit quantities and prices has been completely rebuilt
		* The user now has the ability to override model-calculated carbon intensity ratios for transportation fuels used in the LCFS by specifying ratios in trans/CIRbTF
		* The improvement rate of EV fuel economy in trans/BNVFE now uses a cited source instead of an assumption
		* Cost-driven travel demand rebound effect now influences annual average distance traveled by vehicle type rather than affecting vehicle sales
		* A new output variable, Fraction of Buildable Vehicles Actually Built, is now available
	* CCS
		* ccs/CPbE can now be toggled between OECD and non-OECD regions to improve ease of adapting this variable to different countries
		* Removed unnecessary input variable ccs/CCEL
	* Other improvements
		* bldgs/DSCF now supports time-series data
		* Removed the words "End Year" from three Industry sector input variable names (the three starting with indst/PPRiFUf)
		* indst/PERAC Step 4 now includes a separate process emissions multiplier for each agriculture-related policy rather than using a single multiplier for all agriculture-related policies
* Depreciated Elements
	* Removed stub for certain GDP-related calculations and associated input variable, add-outputs/BGRC
	* Removed Clean Power Plan compliance test and associated input variables, add-outputs/CPPCS and one of three variables in indst/EoP
* Bug Fixes
	* Start Year Cargo Dist Transported now uses an INITIAL() statement to prevent its value from changing during the model run
	* Fixed incorrect value for start year max share of newly sold light freight trucks that may have diesel engines (in trans/MPNVbT)
	* Fixed double-counting of the small amount of fossil fuels used to generate electricity in the buildings sector (natural gas-powered fuel cells and diesel backup generators)
	* Fixed decimal point error in lignite mass conversion factor
	* Fixed omission of biomass burned in industrial facilities from total biomass consumption
	* Fixed inconsistent use of IPCC AR4/AR5 GWP values in indst/PERAC Step 4
	* Fixed error in energy accounting for commercial components retrofitting policy after retrofit components reach end-of-life

### **1.3.2 - Mar 26, 2018**

* Updates and Improvements
	* Updated first simulated year from 2016 to 2017
		* Updated start year data in elec/CCAMC (wind and solar), elec/SYC, trans/SYVbT, and trans/SYFAFE
		* Adjusted trans/BHNVFEAL to no longer need to be updated when advancing the model's first simulated year
		* Updated policy implementation schedule to phase in policy effects from 2018
	* Transportation Sector
		* Endogenous learning now is applied to the battery component of EVs, not to the total EV price, and learning is based on cumulative deployment of all EVs (HDVs, LDVs, motorbikes) rather than calculated separately by vehicle type
		* Improved accuracy of passenger LDV BAU New Vehicle Price input data by accounting for sales shares by vehicle size class
		* Added output variable for fleet average fuel economy (both by technology type and summed across types) converted into localized units
		* Removed trans/SYTSFU Start Year Transportation Sector Fuel Used and replaced it with an internal calculation that helps to avoid possible discontinuities in Last Year Transportation Sector Fuel Used when transitioning from the first to the second simulated year
	* Buildings Sector
		* Improved mechanism for estimating the share of buildings sector energy use attributable to new components each year
		* The buildings sector now tracks potential energy use by building components directly rather than tracking differences from BAU, enabling calibration of bldgs/SoCEUtiNTY
		* Greatly improved and simplified internal handling of building component retrofitting policy
		* Removed input data variable bldgs/FoLRfCTbRP as it is no longer needed
	* Electricity Sector
		* Battery storage and electric vehicles now help to reduce peak electricity demand
		* Peak electricity demand reductions from demand response, battery storage, and electric vehicles are now affected by the transmission connectivity coefficient
		* The generation capacity lifetime extension policy now applies only to nuclear plants and is implemented as an immediate delay rather than a change in steady-state retirement rate
	* Industry Sector
		* Updated max bound for Industrial energy efficiency standards policy with improved, more recent source
		* Changed name of policy "Fraction of CO2e from Vented Byproduct Gasses Avoided" to "Fraction of F Gases Avoided" to better reflect the role of the policy in the model (and to fix a spelling error)
	* Added additional "very high" and "to be determined via calibration" priority tiers for input data variable replacement in acronym-key.xlsx
	* Added capability to localize output units for cargo distance, coal/lignite, natural gas, and liquid fuels
	* Added support for setting policy implementation schedules via the web app interface
* Bug Fixes
	* Fixed issue with first two financial graphs in Vensim "Web Application Support" tab not appearing
	* Replaced two duplicate variables in the Transportation sector with shadow versions of their equivalents
	* Fixed omission of Buildings Sector biomass from "Total Fuel Use" variable (and its BAU equivalent)
	* Fixed omission of light and heavy rail transit vehicles when calculating trans/SYVbT value for passenger rail
	* Fixed off-by-one-year data in plugin hybrid light freight truck prices
	* Removed folder and acronym-key entry for left-over, unused variable trans/FoVSwMB
	* Fixed issue calculating "Share of Energy Carrier Use by Sector" for district heat when policies reduce non-CHP district heat use to zero
	* Prevented impossible (>100%) settings for industrial fuel shifting and for building component electrification from exceeding total amount of fuel available to be shifted
	* Fixed issue with R&D levers failing to affect natural gas power plants
	* Fixed too low value for maximum possible deployment rate of diesel engine freight LDVs in trans/MPNVbT
	* Fixed issue where potential industry process emissions reductions in each year could not be higher than potential reductions in the end year
	* Fixed issue where U.S. non-CO2 process emissions MAC curves were being scaled by total GHGs instead of non-CO2 GHGs
* Python Scripts
	* Changed group numbers to group names in ContributionTest Python script
	* Added several Transportation sector policies to Python scripts
	* Updated names of F-gas reduction and nuclear plant lifetime extension policies
	* CreateContributionTestScript.py now includes a BAU run (all policies disabled) when set to Disable mode and a full policy run (all policies enabled) when set to Enable mode

### **1.3.1 - Sept 13, 2017**

* BAU Transmission Connectivity Coefficient is now a time-series input variable, and it increases by the same percentage as does BAU Transmission Capacity in the U.S. input dataset
* Fuel Economy Standards policy lever is now subscripted by vehicle technology
* Electric vehicles now provide flexibility points in the electricity sector
* Electric vehicles now use an endogenous learning curve based on cumulative deployment to estimate price declines
* In trans/BNVP, changed which rows of input data source are sampled for different LDV types to better reflect present-day average prices
* In trans/BNVP, fixed off-by-one-year error in freight LDV pricing
* trans/MPNVbT now uses sigmoidal interpolation for new technologies and linear interpolation for mature technologies (instead of always using linear interpolation)

### **1.3.0 - Aug 28, 2017**

* Transportation Sector has been completely rebuilt
	* The model now tracks numbers of vehicles explicitly
	* A "Vehicle Technology" subscript has been introduced, and vehicles are divided among six technology categories
	* The "Vehicle Electrification" policy has been replaced with a set of three different policies for EV promotion: EV subsidy, EV perks, and minimum required EV sales percentage
	* A Low Carbon Fuel Standard calculation mechanism has been added.	It is controlled by a BAU LCFS input variable and an LCFS policy lever, both new.
	* Almost all input variables for the Transportation Sector have been updated with new data or replaced with different variables entirely, reflecting the needs of the new model structure.
	* Transportation sector R&D policies are now subscripted by vehicle technology instead of by vehicle type
	* Eight transportation sector-specific graphs have been added to the "Transportation - Main" sheet in Vensim.	Four of them are also available in the web interface.
* Industry sector input data for BAU process emissions and potential process emissions abatement at various cost tiers (indst/BPEiC and indst/PERAC) have been updated with an improved methodology
* Biofuel and biomass CO2 emissions are now lifecycle, and a toggle has been added to fuels/PEI to adjust this behavior easily when adapting the model to different regions.
* U.S. NDC target adjustment updated to improve accuracy and to harmonize NDC-covered emissions with EPS-modeled emissions where they differ (such as emissions from international shipping fuel use)
* Added District Heating CO2e output graph to Web Application Support Variables
* Bug Fixes
	* Corrected omission of paratransit buses from share of all buses owned by government
	* Fixed bug in Electricity sector CO2/CO2e graph appearing in Vensim
	* Added "BAU Max Capacity Buildable from Lookups" since an input to the non-BAU version varies with policies
	* Added "BAU Normalized Std Dev of New Output Costs" since inputs to the non-BAU version vary with policies
	* Fixed case of letter in filename of plcy-ctrl-ctr/BEPEfCT
	* Fixed name of one variable in OutputVarsToExport.lst
	* Fixed District Heating CO2e graph appearing in Vensim
	* Removed superceded year (2015) from RPS calculations and implented check to ensure total RPS percentage in policy case (BAU plus user's setting) cannot exceed 100%
* Reference Scenario Changes
	* Removed CPP scenario
	* Updated CO2eMin scenario to use new transportation sector policy levers
	* Added NDC scenario, which narrowly hits the U.S. NDC target
	* Updated EIRec scenario to be a fresh recommendation, no longer aiming to narrowly hit the U.S. NDC target
* Added System Requirements section to Structural Overview.	Required version of Vensim has been updated to 7.1.

### **1.2.4 - May 16, 2017**

* Renamed "wind" to "onshore wind"
* Renamed "coal" to "hard coal"
* Added lignite as a fuel type and as a power plant type
* Added "offshore wind" as an electricity source
* The share of district heat from CHP facilities in the BAU case may now vary by fuel type
* Effects of shifting from a district heat source that uses less CHP to a district heat source that uses more CHP are now calculated
* If a plant type starts with non-zero capacity and is retired down to zero capacity, no more will be built in future years (preventing the model from building and immediately retiring a small amount of capacity of expensive plant types in each year)
* BAU future declines in capacity construction cost updated to more recent source
* Fixed bug in early retirement calculations that would cause improper retirement of cheaper-than-BAU sources in years they became less cheap than in the prior year
* Made three shortened Buildings sector subscript names consistent with naming of other subscripts (removing a work-around for a Vensim bug that doesn't exist in recent versions of Vensim)
* Added seven new graph types and associated output variables to increase graph options for web apps
* Used quantization to eliminate noise in several output graphs: human lives saved, social benefits from emissions reduction, change in fuel and O&M expenditures
* Fixed bug in input data for normalized standard deviation of dispatch costs
* Updated reference scenarios, python scripts, WebAppData

### **1.2.3 - Apr 19, 2017**

* Various changes to support cost curves (a new graph type) in the web interface
* Fixed typo in Freight TDM policy in Python scripts
* Contribution test Python script now defaults to "Disable" mode
* Emissions indices for non-CO2 pollutants from power plants now use a more up-to-date set of values from the same source (the GREET1 model)
* Fixed incorrectly alphabetized entry in acronym-key.xlsx
* elec/BECF is now a time series variable
* Expected capacity factors for power plants can no longer fall below what is guaranteed under the guaranteed dispatch mechanism
* Price-based early retirement of power plants has been improved
* The feebate policy is now set as a percentage of the global best practice feebate rate, to improve usability of this lever
* The carbon tax and subsidy for electricity production by fuel policies now are input in the local currency unit rather than in U.S. dollars.	(Only affects to non-U.S. versions of the simulator.)
* Fixed and variable O&M costs for power plants are now differentiated by power plant quality tier
* Plants are now flagged as peakers and flagged as flexibility point providers via separate input files (elec/BPaFF), so better support regions that ramp baseload plants (such as coal) for flexibility purposes
* Minor math correction in calculating the sum of standard deviations of power plant capital and non-capital costs
* Normalized Standard Deviation of Dispatch Costs now reflects variance in both fuel and O&M costs (rather than just variance in fuel costs)
* BAU capacity retirements now reflect 2016 actual retirements and AEO 2017 (No CPP scenario) for future years
* To better match EIA data in other input variables, Start Year generating capacity now is based on net summer capacity rather than nameplate capacity
* Updated peak time capacity factors to reflect switch to net summer capacity
* Updated elec/MCGLT to use the 97.5 percentile of capacity build instead of max values (applies to all sources except wind, solar, and solar thermal)
* elec/ARpUIiRC calculation methodology improved
* Updated to more recent source for land/BLACE
* Changed CO2e by Sector graph from stacked area to multiple line graph to better handle negative values from LULUCF
* Updated included reference scenarios to continue to narrowly hit their targets after other model changes

### **1.2.2 - Mar 6, 2017**

* Fixed bug in guaranteed dispatch mechanism when the user flags a plant type not usually used for peaking as a peaker
* Peaking plant types may now participate in least cost dispatch with any remaining potential output after being processed by the guaranteed dispatch mechanism
* elec/CCAMC data updated for natural gas peaking plants
* Fixed bug where components used to replace retrofit building components (due to the retrofitting policy) had too little energy consumption
* Fixed bug in efficiency adjustment for policy-driven increases in electric vehicles
* Industry sector adjustment to production levels is now dependent not only on changes in fuel cost but also changes in fuel efficiency (i.e. cost of fuel per unit industrial output)
* The TDM policy lever is now subscripted by cargo type and includes data for freight mode shifting potential

### **1.2.1 - Feb 13, 2017**

* The Land Use and Forestry sector has been completely redesigned and rebuilt.
	* The model now handles more calculations in Vensim, simplifying the process of supplying input data for this sector.
	* Results are now available in terms of land areas (as well as emissions, cash flows, and changes in land value, as before).
	* Two new policies have been added to this sector (but are not used by the U.S. version of the simulator): forest restoration and peatland restoration.
	* The approach to crediting abatement for policies that avoid sudden, one-time emissions events (such as a peat fire or clearcutting a section of forest) has been improved.
* Support for two new graph types in the web app that show contributions of specific policy groups to the abatement from the entire package: wedge diagrams and cost curves
* Key to policy acronyms used within indst/PERAC added to "Process Emissions Reductions and Costs.xlsx"
* Fixed meaning of elec/MPPC in Acronym Key
* Updated elec/MCGLT and elec/MPCbS with improved U.S. data
* trans/AVLo and trans/AADTbVT are now time-series variables
* Fixed bug where BAU subsidies input data for geothermal and petroleum-fired power plants were transposed
* Added line for "Geothermal" subscript to "End Existing Subsidies" policy in WebAppData
* In web app, changed the CO2e emissions by sector graphs into a single stacked area graph
* Added graph of CO2e emissions by sector to Policy Control Center sheet
* QUANTUM() functions used to dampen noise due to rounding error in financial outputs have been consolidated and moved to the non-output versions of the financial cost/savings variables, and the dampening is now controlled by a new parameter, cost-outputs/CFQS
* Four electricity sector input variables related to the guaranteed dispatch mechanism are now time series variables
* Added scaling factors to calculation flow for add-outputs/SCoHIbP to facilitate adaptation to other countries/regions
* Added output version of Total Primary Energy variable for use in web app in some EPS adaptations

### **1.2.0 - Jan 3, 2017**

* Extension through 2050 and data update
	* The model now reads in INITIAL TIME and FINAL TIME from .csv input data files
	* The first simulated year has been advanced from 2015 to 2016 and the final simulated year has been advanced from 2030 to 2050
	* The following input data variables have been updated with more recent data sources, have been extended to 2050, or (usually) both: add-outputs/BGRC, add-outputs/CPPCS, add-outputs/SCoHIbP, bldgs/BASoBC, bldgs/BCEU, bldgs/BDEQ (2 variables), bldgs/CpUDSC, ccs/CPbE (3 variables), ccs/CSA (2 variables), elec/BBSC, elec/BCpUC, elec/BCR, elec/BPHC, elec/BPMCCS, elec/BRPSPTY, elec/BTaDLP, elec/CCAMC, elec/DRC (2 variables), elec/EIaE (2 variables), elec/PMCCS, elec/PTCF, elec/RM, elec/SLF, elec/SYC (2 variables), fuels/BFCpUEbS, fuels/BFTRbF, fuels/BS, fuels/PEI, indst/BIFU, indst/BPEiC, indst/PERAC, indst/PPRiEYFUfICaWHR, indst/PPRiEYFUfIIaIoE, land/BLACE, land/VFC, plcy-schd/FoPITY, trans/AADTbVT, trans/BFFU, trans/BFoEToFU, trans/FoVSwMB, trans/VFP (3 variables), web-app/BCF (3 variables)
	* The default policy implementation schedule now begins policies in 2017 rather than 2016 and scales them in linearly or sigmoidally through 2050 rather than 2030
	* Policy lever settings in all policy packages have been updated to be compatible with the new implementation schedule
	* Guidance text and max lever bounds (in WebAppData), max lever bounds in Vensim executable, and default policy values in Python scripts updated to be compatible with new model run end year of 2050
* New and Changed Policy and Control Levers
	* Electricity Sector: Ban construction of new power plants of user-specified types
	* Electricity Sector: Use Non BAU RPS Qualifying Source Definitions
	* Cross-Sector: The Carbon Tax policy is now subscripted by sector
	* District Heat Sector: convert coal use to other fuels
	* Added control lever allowing user to exempt process emissions from the carbon tax
* Large Updates to Existing Components
	* Industry Sector - Main sheet has been visually reorganized for clarity
	* Industry sector fuel use calculations more accurately sum effects of efficiency and fuel shifting policies
	* Carbon tax effect on process emissions now affects industrial production levels
	* Transportation sector cash flows now account for the difference in purchase price between electric and non-electric vehicles
* Small Updates to Existing Components
	* BTaDLP BAU Transmission and Distribution Loss Percentage is now a time-series input variable
	* Ensured Y-Min is zero in electricity capacity and output graphs
	* Power plant construction in each year is now quantized by the minimum capacity of a single power plant of each type
	* Moved calculation of revenue-neutral carbon tax policy package costs from the "Additional Outputs" sheet to the "Cost Outputs" sheet
	* Methane captured by an industry now reduces that industry's natural gas usage (to a minimum of zero)
	* Improved calculation of percentage change in industrial production levels in response to fuel price changes
	* Industrial fuel use now includes the fuel used for non-energy purposes in cash flow and total primary energy calculations
	* Changes in cash flow due to spending on vehicles now consider the fraction of vehicles sold within the model boundary
	* District heat CHP policy is now classified in a new "District Heat" sector in the Policy Control Center and web app
	* Added data for several missing vehicle types to "Average Vehicle Loading," "Average Annual Dist Traveled by Vehicle Type," and "BAU Avg Vehicle Price"
	* Changed the importance rating (when updating the model for a new region) for PTCF Peak Time Capacity Factors from "medium" to "high"
	* Fuel price adjustments due to electricity cost changes or removed subsidies now only affect fuels used in a given sector (those with a non-zero BAU price) to improve clarity of model output
	* BIFU BAU Industrial Fuel Use input data are no longer assumed to include fuel used to power BAU CCS process, as this is handled in CCS sector input variables.	BIFU renamed BIFUbC.
	* Added graph of Anthropogenic LULUCF impact to "Land Use and Forestry" sheet in Vensim
	* Added graph of CO2 sequestration to "Carbon Capture & Sequestration" sheet in Vensim
	* Added graph of CO2 emissions to "District Heating" sheet in Vensim
* Web app interface-focused updates
	* The web app now groups subscripts of policy levers under a second-tier menu
	* Updated WebAppData display names for R&D policies to comply with new web app menu structure
	* Added "Targets" tab to WebAppData for specifying targets to be shown on Total CO2e graph in web app
	* R&D fuel use reduction lever for building envelope is no longer included in web app (as envelope does not use fuel)
	* Two jet fuel-related levers are no longer included in the web app (as policies affecting jet fuel are insufficiently important to merit inclusion in the web app interface)
	* In web app output graphs, "Electricity Output" is renamed "Electricity Generation" and "Electricity Generation Capacity" is renamed "Electricity Capacity"
	* In web app, "Reduced Nonmethane GHG Venting" renamed "Reduce F-gases" and description text updated accordingly
	* Added new "Policy Group" column to WebAppData to support new graph types in web app
	* All graphs in web app now specify "/ year" in the Y-axis unit label to make it clearer that the graphs are not cumulative totals
	* WebAppData "OutputGraphs" tab updated with info to support two new graph types
	* WebAppData output graphs now consolidate "Consumption of Petroleum Gasoline," "Consumption of Petroleum Diesel," and "Consumption of Jet Fuel" into a single "Consumption of Petroleum Fuels" graph
	* Removed "Consumption of Biofuel Gasoline" and "Consumption of Biofuel Diesel" graphs from web app because they were seldom used.	(These outputs are still available in the downloadable version of the model.)
* Bug Fixes
	* Added ".cin" extension to the name of "Scenario_CO2eMin" in CreateDataLoggingScript.py file list
	* Added missing HTML anchors in documentation for three policies: distributed solar carve-out, distributed solar subsidy, avoid deforestation
	* Fixed bug in Python scripts relating to policy to reduce downtime of natural gas nonpeaker plants
	* Fixed bug in CpUDSC Cost per Unit Dist Solar Cap
	* Fixed Distributed Solar Capacity Caused by Mandate This Year in cases when existing capacity is zero
	* Fixed bug in "New Peaker Capacity Desired for Peak Load Purposes by Type" when at least one energy source has zero peak time capacity factor
	* Fixed a source URL in BPEiC BAU Process Emissions in CO2e
	* Fixed bug where energy efficiency policies in Industry reduced total fuel use rather than fuel use for energy purposes
	* Fixed bug in name of battery storage policy in Python scripts
	* Changed name of "Induced Foreign GHG Emissions" to "Induced Foreign Emissions" because we no longer limit this to GHGs
	* Changed industry fuel use calculation flow to avoid introducing noise from rounding error
	* Fixed bug where carbon tax effect on capital cost of new power plants due to embedded carbon content was not reflected in cash flow calculations
	* CO2 captured by CCS for each industrial sector and electricity source is now capped at the total amount of CO2 generated by that industrial sector or electricity source
	* Cost reductions for CCS technology achieved through endogenous learning are no longer lost if CCS sequestration rate declines in a later year of the model run

### **1.1.4 - July 25, 2016**

* New policy: Fraction of Natural Gas Use Converted to Other Fuels (Industry Sector).	Updated Python scripts with new policy.
* New input data variable: PIFURfE Percentage Industry Fuel Use Reduction for Electricity
* RIFF Recipient Industrial Fuel Fractions is now a category and contains separate input data files for the recipient fuel types when switching from coal and the recipient fuel types when switching from natural gas
* RM Reserve Margin is now a time-series input data variable to support countries with projected future reserve margins that vary by year
* Added "Fuel Price Multiplier for Sensitivity Analysis Runs" to facilitate introducing variance in fuel prices during Monte Carlo simulations
* Improved input data for (Buildings Sector) Elasticity of Component Price with Respect to Energy Use
* Fixed bug where subsidy for distributed solar capacity only was only paid for distributed solar capacity caused by the subsidy instead of all new distributed solar capacity

### **1.1.3 - June 28, 2016**

* Fixed swapped U.S. web app guidance text between Methane Capture and Methane Destruction policies
* Added limit to ensure process emissions reductions for a given industry and pollutant cannot exceed total process emissions of that pollutant from that industry
* Updated guidance text on R&D policies in web app to reflect change in model start year (from a previous model update)
* Updated CCS lever guidance text to reflect change in data source (from a previous model update)

### **1.1.2 - May 12, 2016**

* Increase in Distributed PV in the BAU case is no longer allowed to be negative for purposes of calculating the effects of a subsidy on distributed solar deployment
* Fixed bug where costs of commercial building components purchased due to the accelerated retrofitting policy were omitted
* The Industry Sector emissions graph in Vensim is now CO2e (not CO2), to better illustrate the effects of process emissions policies, and is labeled "Industry and Agriculture CO2e Emissions" for clarity
* In the Electricity Sector, the capacity that may be retired early in a single year for policy-driven economic reasons is now capped at the amount of capacity that may be built of plant types not subject to cost-based early retirement in that year
* Reduced expenditures by government on subsidies for thermal fuels due to the Reduction of BAU Subsidies policy are now properly counted
* Fixed a few typos in Python scripts
* Fixed two incorrectly alphabetized entries and one omission in acronym-key.xlsx
* Updated Pollutant Emissions Intensities to GREET 2015 (from GREET 2014).
* Adjusted GREET pollutant emissions intensities to be based on higher heating values (gross energy content) of fuels, to match the format of the energy use data from EIA.	Adjustment can be toggled on/off to assist in internationalization.
* Updated to a more recent source for solar PV in MCGLT Max Capacity Growth Lookup Table

### **1.1.1 - Apr 2, 2016**

* "Fuel Weighted Percent Change in Production due to Policies" no longer gives an error when a country's input dataset doesn't assign any fuel usage to one of the model's Industry categories
* Added "MPCFR Maximum Possible Capacity Factor Reduction" to more realistically model rare situations in which peaker plants that are providing necessary flexibility points retire, leaving the model in extreme FP deficit
* Graph definition file no longer specifies Y-axis maximum on Vensim CO2e graph (to aid in internationalization)
* "Fraction of Buildable Capacity Actually Built" and its BAU equivalent now report "1" when no capacity is buildable, rather than a divide-by-zero error
* Which plant types are treated as peakers is now specified in a new input variable, "Boolean Is This Plant Type a Peaker" (for instance, because different countries may use petroleum as a peaking or non-peaking resource).	Affects behavior in peaking construction, in dispatch, and in flexibility point calculations.
* Changed name of variable "Fraction of Peakers that are Combustion Turbines" to "Fraction of Peakers that Provide Flexibility Points"
* Changed name of variable "Flexibility Points Provided Per Unit NG Peaker Capacity" to remove the term "NG"
* Added "BAU" to name of variable "FPC BAU Transmission Connectivity Coefficient."	A non-BAU version is calculated in the policy case.
* Added "BRPSPTY BAU RPS Percentage This Year" to acronym key.
* "Percentage of RPS Qualifying Potential Output to Seek This Year" is now set to zero if the slopes to all future RPS values are negative (i.e. if we have more RPS resources than we will need in any future year of the model run).
* Changed default implementation schedule for Avoid Deforestation policy to phase in linearly
* Added "FPC Target Maximum Fraction of Flexibility Points Used" and a few calculated variables to avoid building flexibility-using resources beyond a given flexibility point threshold (by default, 140% FP usage), to avoid situations where newly built plants result in a net decrease in electricity output following curtailment, due to the one-year delay associated with recognizing the impacts of newly built plants on available FP and on curtailment rates.

### **1.1.0 - Mar 24, 2016**

* New Components
	* A distributed generation module has been added to the Buildings and Appliances Sector.
	* Geothermal and petroleum-fired power plants have been added.
	* Natural gas power plants have been split into two types: natural gas peaker plants and natural gas non-peaker plants.
	* Electricity imports and exports have been added.
	* Implemented endogenous, capacity-based learning curves for wind, solar PV (utility-scale and distributed), batteries, and CCS.
	* Implemented new mechanism for constructing peaking power plant types (petroleum-fired and natural gas peakers).
* New Policy Levers
	* Electricity Sector: Reduce Transmission and Distribition Losses
	* Electricity Sector: Reduce Plant Downtime
	* Electricity Sector: Change Electricity Imports
	* Electricity Sector: Change Electricity Exports
	* Buildings Sector: Distributed Solar Carve-Out
	* Buildings Sector: Distributed Solar Subsidy
	* Land Use Sector: Avoid Deforestation
* Major Improvements to Existing Components
	* The Renewable Portfolio Standard policy lever is now additional to a BAU RPS level.	It uses a new phase-in mechanism that minimizes shocks for electricity suppliers to better reflect their likely behavior in response to this policy.
	* The price-based power plant early retirement mechanism has been redesigned.	It is now more realistic in situations with strong economic incentives for retirement, and it does not affect the BAU case.
	* The mechanism for determining how much capacity of each electricity source may be built in a given year has been redesigned.	It is now dependent on installed capacity only for wind and solar PV.
	* Flexibility points are no longer a hard limit on renewables construction or dispatch.	As before, renewables remain unconstrained until capacity equals flexibility points.	Thereafter, capacity factor of renewables is reduced proportionately to the overage of capacity beyond flexibility points.
	* Consolidated vehicle suppliers, building component suppliers, and industrial equipment suppliers into a single cash flow entity, "capital equipment suppliers".	The land use and forestry sector now also makes use of this new cash flow entity.
	* Updated graphs and output variables to include new power plant types and distributed generation (solar and non-solar).	Updated graph color scheme.
	* Cost outputs have been rebuilt for clarity and now have their own sheet.	Minor updates to several cash flow sheets to provide variables in the uniform format expected by the new cost outputs sheet.
	* The contract-based dispatch mechanism has been renamed the guaranteed dispatch mechanism.	The BAU version of this mechanism is now always used in the BAU case, and the control lever that used to govern this behavior has been removed.	The policy “Boolean Use Contract Based Dispatch in Policy Case” has been renamed “Boolean Use Non BAU Guaranteed Dispatch Settings” and has been modified to work analogously to “Boolean Use Non BAU Mandated Capacity Construction Schedule."
	* Added the concept of "Bid" capacity factors, which are expected or peak time capacity factors (varying by plant type).	This system increases the importance of the electricity dispatch mechanisms.	Not used for peaking plant types.
* Data Updates
	* The simulator's first calculated year has been advanced from 2013 to 2015.
	* Numerous data sources have been updated to their most current versions.
	* BAU Subsidies have been updated to account for changes in legislation.
	* The U.S. dataset no longer splits preexisting plants into "retiring" and "nonretiring" categories, to better reflect the fact that retirements in the U.S. do not correlate with specific technological or quality properties.	The model retains both of these quality tiers structurally, so that non-U.S. countries may still choose to make use of this distinction in their own datasets.
	* In the Buildings Sector, the "residential" building type has been split into "urban residential" and "rural residential".	Three policies are now subscripted by building type.
	* All three included reference scenarios (CPP, EI, CO2eMin) have been updated to still hit their emissions targets (narrowly, for CPP and EI).
	* Updated capital cost of new coal plants to include CCS, reflecting the latest regulations.
	* BAU fuel costs now rely on the EIA Short-Term Energy Outlook for values through 2016, increasing accuracy relative to the EIA Annual Energy Outlook.
* Minor Improvements
	* Future demand response capacity in the BAU case now assumes linear rather than geometric growth, in line with FERC data source.
	* Normalized Standard Deviation of New Output Costs is now a calculated variable, based on a weighted average of the Normalized Standard Dev of Dispatch Costs and the Normalized Std Dev of Capital Costs.
	* Removed the BAU Regional Support Variance Multiplier, as these effects should now be accounted for in the normalized standard deviations.
	* Added a collection of “Additional Electricity Sector Outputs” useful for examining the behavior of this sector in detail.
	* Transmission capacity across the modeled region border now contributes to flexibility points.
	* Added variable specifying the fraction of vehicles sold within the model boundary.	Those transportation policies that do not affect vehicles sold outside the modeled region now scale down their effects in proportion to the fraction of vehicles not sold within the region.
	* In the Industry Sector, induced emissions beyond the model boundary (due to leakage) are no longer included in the modeled emissions total.	Leaked emissions are now only reported as a separate variable.
	* The graph on the Buildings sector page now shows total CO2 emissions from the sector (summed across all three building types).
	* Simplified input data calculations for various electricity plant properties (such as heat rates and expected capacity factors).
	* Changed the names of many policies to remove " by End Year" and " in End Year" (which was a hold-over from before the simulator possessed a policy implementation schedule).
	* In web app support sheet, "Billion Dollars" changed to "Output Currency Unit" and now draws from a .csv file, to aid in internationalization.
	* Updated the default set of variables specified in OutputVarsToExport.lst for Python script users.
	* The control lever "Boolean Use Twenty Year GWP Values" now pulls data from a .csv file rather than being set in Vensim like a policy lever.
	* The BAU and Policy Case dispatch priorities and dispatch percentages now guarantee that natural gas peakers and petroleum-fired power plants will dispatch at their expected capacity factors.
	* Renamed Non Hydro Storage to Battery Storage (to reflect the cost input data being used in the model).
	* Biomass is now a value Buildings Sector fuel.
* Bug Fixes
	* Corrected input data for BAU amount and potential amount of CCS.
	* Corrected flexibility point and transmission connectivity coefficient calculations.

### **1.0.3 - Feb 2, 2016**

* Added new output variable: Human Lives Saved from Reduced Particulate Pollution.	Added graphs to Policy Control Center and web app.

### **1.0.2 - Jan 4, 2016**

* Fixed bug where subsidies paid by government for generation of electricity were not being counted correctly in the "Change in Total Outlays" cost metric
* Fixed minor issues in web app guidance text for the feebate and two forestry policies
* Simplified structure for calculating carbon taxes and revenue-neutral carbon tax package costs
* Expanded acronym-key.xlsx with an "About" tab containing general information and a key to the folders at the root of the InputData folder
* "BAU New Cargo Dist Transported" now automatically uses input data when available and otherwise uses a lifetime-based estimate
* Updated input data for "BAU Capacity Retirements before Price Effects" to reflect actual power plant retirements in years 2013-2015
* Defined default colors for lines and stacked areas in Vensim-based electricity and cash-flow-by-entity graphs

### **1.0.1 - Oct 30, 2015**

* Added calculation of amount of carbon taxes paid on fuel, on process emissions, and total
* Added new cost outputs for the main two cost metrics (change in capital fuel and labor expenditures; total change in outlays) using the revenue-neutral carbon tax assumption
* Added web app support versions of the two new cost outputs.	Updated GraphDefinitions.vgd and WebAppData.xlsx accordingly.
* Added a new column to acronym-key.xlsx (in InputData) specifying the relative priority of replacing the data for each variable when adapting the model to a new country or region

### **1.0.0 - Oct 20, 2015**

* Initial Release
