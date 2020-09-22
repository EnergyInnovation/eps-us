---
layout: page
title:  "Notes on Unit Conversion"
---
## Working Units and Output Units

The Energy Policy Simulator (EPS) takes in input data and produces output data of a variety of types, including quantities of energy, money, distance, mass of pollutant emissions, etc.  In any given deployment of the model, the units used to represent these quantities can be customized to reflect the units familiar in the modeled region.

The EPS has two types of units: working units and output units.  Working units are used in model input data, and they are carried through most calculations in the model's structure in Vensim.  Therefore, when vieweing data in Vensim, except for output variables on the "Web App Support Variables" sheet, you will generally be viewing data in working units.

Output units are those used in the web app interface, and also in the output variables on the "Web App Support Variables" tab in Vensim.

Working units are chosen for uniformity, even if they may have an inconvenient order of magnitude.  For example, the working unit of energy in all model deployments is BTU, and quantities of energy often are very large numbers (and emissions per unit energy of combusted fuel are very small numbers).  Similarly, the working unit for all pollutant emissions is grams, even though different pollutants may have emissions that are orders of magnitude larger or smaller than each other.

Output units are chosen to be familiar to users in the modeled region, and to have a convenient order of magnitude (generally so that the numerical values range from 0.1 to 9999, preferably 1 to 999).  Chosen output units vary with every model deployment, and different subscripts of the same variable may use different output units.  For example, in the U.S. model, the variable "Vehicles" is an internal variable with working unit "vehicles" - e.g. the number of vehicles in the U.S.  That variable is used to create two output variables, "Output Vehicles in Millions" (with unit "million vehicles") and "Output Vehicles in Thousands" (with unit "thousand vehicles").  The web app graphs display light-duty passenger vehicles (cars and SUVs) in millions of vehicles, but they display heavy-duty passenger vehicles (buses) in thousands of vehicles.  This is because cars and SUVs are far more numerous than buses in the U.S.

Most EPS deployments inherit the working units from the U.S. EPS.  This is because these models often inherit one or more input data files from the U.S. deployment (for example, they may scale U.S. values to fill in a data gap), and it is therefore often most convenient to simply retain U.S. working units.  This requires that each regional deployment convert its input data into these working units.  For example, Chinese energy input data in tons of coal equivalent, or TCOE (in the China EPS) and Canadian input data in Joules (in the Canada EPS) may both be convered to BTU in the input data files.

The main working units of the EPS are:

|Unit Type|Working Unit|
|-|-|
|Currency|2012 U.S. dollars|
|Energy (except electricity)|BTU|
|Electricity generation|MWh|
|Electricity capacity|MW|
|Pollutant emissions|grams|
|Distance|miles|
|Land Area|acres|
|Water Volume|liters|
|Grid Flexibility|flexibility points|
|Public Health Outcomes|incidents|
|Number of vehicles|vehicles|
|Number of jobs|jobs|

Working units are converted to output units in several variables located in the InputData\web-app folder.  This conversion is normally straightforward.  However, two cases deserve further explanation: converting electricity and energy units, and converting currency types/years.

## Electricity - Energy Unit Conversions

While thermal (and nuclear) energy sources use BTU as their working unit, the working unit for electricity is MWh.  This helps keep electricity energy units parallel to capacity units (where the working unit is MW) and avoids the confusion that can arise when electricity is expressed in BTU by users expecting a heat rate rather than a unit conversion.  A heat rate is an efficiency with which BTUs of a fuel can be converted to electricity in a power plant.  A perfecly efficient power plant would have a heat rate equal to the pure unit conversion factor between BTU and MWh.

In electricity-specific output graphs, typically no unit conversion is necessary beyond converting MWh into GWh or TWh, a simple change of order of magnitude.  However, some output graphs show multiple types of energy together, often as stacked areas.  In order to represent electricity on these graphs, it is necessary to convert it to a non-electricity energy output unit, such as quadrillion BTU (quads).  An example is Transportation Sector fuel use by fuel type.  The EPS must use the pure unit conversion, not a heat rate, to convert electricity use for inclusion on these graphs.

For the most part, the EPS only uses heat rates only when representing an actual conversion of thermal or nuclear fuel into electricity.  These conversions occur within the electricity sector and are not relevant for output unit conversion.

However, in output graphs of total primary energy, electricity from renewables (wind, solar, geothermal, etc.) has no upstream source.  If this electricity were displayed alongside other energy types using a pure unit conversion, it would look far smaller than primary energy from fuels used to generate electricity (two thirds or more of the energy in thermal fuels can be lost when burning them for electricity), so a direct unit conversion under-represents the role of renewables in the energy mix.  The EPS follows the convention typically used in China, where the electricity from renewables is converted to energy units not with a pure unit conversion, but with the heat rate of the typical preexisting hard coal power plant at model start.  (In models where the hard coal subscript is repurposed- as of 2019, this applies only to Saudi Arabia, where that subscript is used for crude oil- the heat rate of this plant type is used.)

## Currency Unit Conversions

Currency units have two relevant dimensions: a currency type (e.g. U.S. dollars, Polish złoty, Chinese yuan, etc.) and a currency year (e.g. 2012 USD, 2018 USD, etc.).  When converting currency units between types and currency years, the order in which you do these conversions affects the result.  This is because currency conversion rates have fluctuated and different currencies have experienced different rates of inflation over the years.

For example, suppose you start with 100 2013 Chinese yuan.  If you first convert the yuan to 2013 USD, you get 15.51 2013 USD.  Then, if you convert 2013 USD to 2018 USD, you get 16.72 2018 USD.  In contrast, if you first convert the 2013 yuan to 2018 yuan, you get 109.36 2018 yuan.  Then, if you convert 2018 yuan to 2018 USD, you get 16.52 2018 USD.  While the difference between 16.72 and 16.52 2018 USD may seem small, the difference can amount to millions or billions of dollars in certain output variables, and the difference can be substantially larger on a percentage basis if the currency conversion happens in a year when the currencies experienced an unusual spike in their exchange rates.  We do not wish to allow currency exchange rate fluctuations to influence our results.

As a result, we must establish a standard ordering, which we use when converting currency units in input files.  This way, we can reverse the operation in the conversion factors that produce output units.  The standard used in EPS input files is: convert currency type first, then convert currency year.  Accordingly, in the output conversion factors, we use the opposite order: we convert currency year first, then currency type.

This ordering is selected because when we adapt the EPS to a foreign country, some of the input files typically are retained from the U.S. model and thus only have a year conversion applied in the input data.  Accordingly, we need to undo that conversion (year) before we apply a new conversion (currency type) in the output variable.  Since year conversion has to come first in the output conversion factors, it has to come second in the input variables.
