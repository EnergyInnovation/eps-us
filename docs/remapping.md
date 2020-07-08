---
layout: page
title:  "Remapping Subscript Elements"
---

## Contents

| Section | Remapping Potential |
| ------- | ----------------- |
| [About Subscript Elements and Remapping](#about)                                | |
| [Power Plant Types](#power_plant_types)                                         | good |
| [Industries](#industries)                                                       | impossible |
| [Industrial Process Emissions Policies](#industrial_process_emissions_policies) | very limited |
| [Cash Flow Entities](#cash_flow_entities)                                       | impossible |
| [Building Type](#building_type)                                                 | good |
| [Building Component](#building_component)                                       | limited |
| [Vehicle Type and Cargo Type](#vehicle_type_and_cargo_type)                     | good |
| [Fuels](#fuels)                                                                 | very limited |
| [Hydrogen Production Pathway](#hydrogen_production_pathway)                     | good |
| [Land Use Policy](#land_use_policy)                                             | good |


## About Subscript Elements and Remapping<a name="about"></a>

The Energy Policy Simulator (EPS) uses subscripts (array dimensions) to manage data.  Examples of subscripts include "Industry Category," "Building Type," "Electricity Source," and so forth.  Each subscript contains various elements.  For example, the "Building Type" subscript contains three elements: urban residential, rural residential, and commercial.  All subscripts and their elements can be viewed by [downloading the model](download.html), opening it in Vensim Model Reader, and clicking the "Subscripts" button.

When adapting the EPS to a new geography, we are sometimes asked if we can add additional elements to a subscript or modify the elements that are inside a subscript, in order to better match the available subscript elements to the particularities of that geography.  Extending a subscript (adding additional elements) requires a structural edit to the core EPS executable (EPS.mdl, EPS.vpmx) and can be tedious, due to the careful connections that must be made throughout the model to ensure all calculations are completed and the new elements are added to the appropriate output graphs.  On the other hand, changing the meaning of an existing subscript element can be done entirely in input data (e.g. by modifying the Excel and CSV input data files).  We call this "remapping" a subscript element.

Remapping a subscript is possible, but caution must be taken.  In some cases, the model structure treats certain elements differently from others, based on the model's understanding of what those subscript elements mean.  This can make certain output graphs inaccurate if remapping is done inappropriately.  This documentation page aims to help clarify which subscript elements may be remapped and under what constraints.

## Power Plant Types<a name="power_plant_types"></a>

The 16 elements of the "Electricity Source" subscript are: hard coal, natural gas nonpeaker, nuclear, hydro, onshore wind, solar PV, solar thermal, biomass, geothermal, petroleum, natural gas peaker, lignite, offshore wind, crude oil, heavy or residual fuel oil, and municipal solid waste.  (This does not include distributed generation, which is handled in the Buildings sector and is not part of this subscript.)  Remapping of power plant types is possible given the following constraints:

- The six power plant types that do not use fuel (hydro, onshore wind, offshore wind, solar PV, solar thermal, and geothermal) can only be mapped to power plant types that do not use fuel.  (The Total Primary Energy (TPE) calculation converts renewable electricity generation to equivalent primary energy, whereas it uses actual fuel consumed for the fuel-using plant types.)  Even if the fuel use is accounted for elsewhere, so there is no additional fuel use in the Electricity sector (e.g. if you wish to represent electricity from co-generation facilities whose fuel use is included in the Industry or District Heat sectors), you must not remap one of the plant types that do not use fuel, because TPE will be wrong.  In that case, remap one of the fuel-using plant types and set its heat rate to zero.

- The power plant types that use fuel can only be remapped to plant types that use another fuel provided by the same cash flow entity.  For example, hard coal and lignite are both provided by the "coal suppliers" cash flow entity.  You can remap one of these elements to another fuel provided by "coal suppliers" (such as anthracite, bituminous, or sub-bituminous coal), or even to cogeneration from district heating facilities that burn coal (being careful to adjust the heat rate to account only for any fuel use assigned to these facilities in the District Heating sector).  But you cannot remap "lignite" to a fuel provided by a different cash flow entity, such as "black liquor" (which would be supplied by the "biomass and biofuel suppliers" cash flow entity).  Otherwise, positive and negative cash flows associated with the fuel for the remapped power plant will be assigned to the wrong cash flow entity.

Remember that when remapping, you likely will need to update not only a variety of variables within the electricity sector (e.g. start year capacity, heat rate, expected capacity factors, etc.) but also pollutant emissions intensities and pollutant emissions intensity improvement rates (in the Fuels section).

## Industries<a name="industries"></a>

The 8 elements of the "Industry Category" subscript are: cement and other carbonates, natural gas and petroleum systems, iron and steel, chemicals, coal mining, waste management, agriculture, other industries.

- Industries (as well as agriculture and waste management) cannot be remapped.

- Industries are structurally associated with particular ISIC Code categories used in the input-output model.

- Industries are structurally associated with particular process emissions types (e.g. in "Fraction of Process Emissions Reductions by Pollutant") and policy levers (e.g. in "This Year Change in Process Emissions by Policy and Industry").  These associations are also present in difficult-to-change input data (e.g. indst/BPEiC and indst/PERAC).  This rules out any remapping that would change the type of process emissions that an industry emits or which policies can be used to reduce those process emissions.

- Two industries are energy suppliers and have corresponding elements in the cash flow entities subscript (natural gas and petroleum systems, and coal mining).  The revenues of these industries are affected by endogenously-calculated changes in demand for the associated fuels (i.e. in "Change in Revenue by Industry").  There are other, complex ways in which the revenues of these industries are handled differently from other industries.  Remapping one of these industries would invalidate the revenue calculations.

- Agriculture and waste management are displayed individually in output graphs and are not displayed as part of the "Industry" sector in the web interface.

- Agriculture has special handling with respect to the "shift from animal to nonanimal products" policy lever, though this lever could be disabled in the web interface.

## Industrial Process Emissions Policies<a name="industrial_process_emissions_policies"></a>

The nine industrial process emissions policies are a subset of the "Policy" subscript and also are used in the "Industry by Process Emissions Policy" subscript  The nine elements are: methane capture, methane destruction, f gas substitution, f gas destruction, f gas recovery, f gas inspct maint retrofit, cropland and rice measures, livestock measures, and cement measures.  Each policy lever represents a "bucket" of different technical strategies (summed up from a major EPA report, for non-CO2 gases), and the exact composition of those buckets can change, as long as the following guidelines are respected:

- Each policy's name can be updated in the web interface.  Abatement potential and cost data can be updated in indst/PERAC.  This can represent a variety of differences in technical measures and approaches to broadly abate the same gas from the same industry.

- Each policy can only affect a specific set of industries (e.g. in "This Year Change in Process Emissions by Policy and Industry").  A new policy must affect those same industries, or a subset of them (e.g. by setting its potential to zero for the industry/industries you don't want it to affect).  The remapped policy cannot affect an industry that the original policy did not.

- The pollutant (greenhouse gas) affected by each policy cannot be changed, as this is part of model structure (e.g. in "Fraction of Process Emissions Reductions by Pollutant").

- The methane capture policy cannot be remapped, as it reduces the natural gas demand of the industry capturing the methane by the amount captured.

- The livestock measures policy cannot be remapped, as its effects scale down with increasing use of the "shift from animal to nonanimal products" lever.

For example, you could remap the "cement clinker substitution" policy to "cement measures" and add data about the cost and reduction potential of alternative cement chemistries to the existing data on clinker substitution in PERAC, so this lever represents doing both of these technical measures (depending on the lever's setting).  You could also consolidate all F-gas measures into a smaller number of levers (by default, four levers), or remap "Crop and Rice Measures" to a different policy that affects methane and nitrous oxide in the agriculture industry.

## Cash Flow Entities<a name="cash_flow_entities"></a>

The nine cash flow entities (entities to whom the EPS can assign positive and negative cash flows) are: government, nonenergy industries, labor and consumers, foreign entities, electricity suppliers, coal suppliers, natural gas and petroleum suppliers, biomass and biofuel suppliers, and other energy suppliers.

- Cash flow entities cannot be remapped.  The finances of the five energy-supplying cash flow entities are structurally linked to the sales and prices of associated fuels.  The other four broad entities also have model structure defining aspects of their cash flows.  For example, tax revenues go to the "government" and the labor fraction of operations and maintenance costs goes to "labor and consumers."

## Building Type<a name="building_type"></a>

The three elements of the "Building Type" subscript are: urban residential, rural residential, and commercial.

- Building types may be remapped freely, as long as the resulting categories are non-overlapping and encompass all buildings.  For example, the "urban residential" subscript can be remapped to "residential" and contain data for all residential buildings, without regard to an urban/rural split.  The "commercial" buildings subscript could be split into two types of commercial buildings, such as "private nonresidential buildings" and "public nonresidential buildings," but in that case, the fuel costs (which can vary by building type) may need to be updated, in fuels/BFCpUEbS.

## Building Component<a name="building_component"></a>

The six elements of the "Building Component" subscript are: heating, cooling and ventilation, envelope, lighting, appliances, and other components.

- Heating, cooling and ventilation, and envelope cannot be remapped.  Envelope improvements are structurally used as a multiplier that reduces the energy demand of heating and cooling systems.  (The "heating" subscript here represents heating the air in a building, not operating a water heater.  Water heaters are part of the "appliances" subscript.)  Envelope elements themselves do not consume energy.

- The lighting, appliances, and "other components" subscripts can be remapped freely, so long as the total amount of energy used in buildings (except to operate industrial machinery or electricity generation equipment) is equal to the sum of the energy used by all of the "building component" subscript elements.  For example, it would be possible to remap "appliances" to "cooking equipment," so long as the energy used by all non-cooking appliances were added to the "other components" category.

## Vehicle Type and Cargo Type<a name="vehicle_type_and_cargo_type"></a>

The six elements of the "Vehicle Type" subscript are: LDVs, HDVs, aircraft, rail, ships, and motorbikes.  The two elements of the cargo type subscript are: passenger and freight.

- Vehicle types can be remapped freely within the same cargo type.

- If remapping a freight vehicle to a passenger vehicle, or vice versa, you must remember to use different units (e.g. passenger-miles or freight ton-miles) in various input variables for that one vehicle type, and you must update WebAppData to switch the vehicle type from the passenger travel demand graph to the freight travel demand graph (or vice versa) without changing the output variable name.

- No special handling is required when remapping between a non-road and an on-road vehicle mode, but you may wish to check to ensure the LCFS policy is correctly set to cover or exclude the remapped vehicle type in trans/BVTStL.

## Fuels<a name="fuels"></a>

Fuels appear in a variety of subscripts, including "All Fuels" and sector-specific fuel subscripts, such as "Industrial Fuel" or "Transportation Fuel."

- Fuels are structurally assigned to specific cash flow entities (producers), as well as to specific sectors and equipment types (consumers).  Any changed fuel must be produced by the same cash flow entity and used by the same sectors as the original fuel.  For example, "biofuel gasoline" may represent corn ethanol, cellulosic ethanol, or some other sort of liquid biofuel used in on-road vehicles, by changing its properties in variables such as fuels/PEI and fuels/BFCpUEbS.

- If the remapped fuel is used in the same sectors but in different types of equipment, this may necessitate changes in numerous variables in the relevant sector.  For example, remapping "biofuel gasoline" to "bio-jet fuel" would require changes in the transportation sector that specify which fuel types different vehicle technologies and vehicles may use.  This is likely to be even more difficult in other sectors, such as electricity supply and industry.  Therefore, it is strongly recommended that the remapped fuel be one used by the same types of equipment or industries as the original fuel.

## Hydrogen Production Pathway<a name="hydrogen_production_pathway"></a>

The hydrogen production pathway subscript includes five pathways: electrolysis, natural gas reforming, coal gasification, biomass gasification, and thermochemical water splitting.

- Hydrogen production pathways may be remapped freely.  This subscript was designed to facilitate remapping, and also, there is the expectation that no EPS deployment is likely to use all of the available subscript elements.

## Land Use Policy<a name="land_use_policy"></a>

The six land use policies are a subset of the "Policy" subscript and also are used in the "Land Use Policy" subscript  The elements are: forest set asides, afforestation and reforestation, forest management, avoid deforestation, peatland restoration, and forest restoration.

- All of the land use policies except "forest management" can be freely remapped, so long as the new policy preserves or changes land in a way that continually reduces emissions or sequesters CO<sub>2</sub> relative to the BAU case *on all lands that have been affected by the policy in any prior year of the model run*.  For example, "afforestation and reforestation" introduces trees to a certain number of acres per year, but all of the acreage that has been afforested sequesters CO<sub>2</sub> every year, as the trees continue to grow.  These land use policies are structurally set up to function this way.

- The "forest management" policy can be freely remapped, so long as the new policy only reduces emissions or sequesters CO<sub>2</sub> on lands that are targeted by that policy in that year.  Any lands that were targeted in prior years *do not continue to abate emissions*, unless those lands are freshly targeted by the policy.  For example, a policy of bringing goats to eat invasive plants and keep their population in check could be represented, as long as the invasive species soon returns (in a year or two) if the goats cease to be brought to a previously-grazed area.

- Land use policies were designed to facilitate remapping, and also, there is the expectation that no EPS deployment is likely to use all of the available subscript elements.

