---
layout: page
title:  "Web Application Support Variables"
---

The "Web Application Support Variables" sheet contains a variety of outputs, many (but not all) of which are used in the web application interface for the Energy Policy Simulator (EPS).  In general, the EPS uses a single unit for each type of quantity: BTUs for energy, grams for pollutants, etc.  These are often not the best units for display on the graphs in the web application.  Accordingly, another purpose of this page is to convert each output to the units that will be used in the web application.

Most users of the Vensim model will not need to examine or use the variables on this page.  However, referring to this page can be a way to view a variety of interesting and important outputs (useful if you are unsure what sort of model outputs might be worth examining), and it can be a convenient means of seeing certain outputs converted into more meaningful units.  This may sometimes save you the trouble of performing a unit conversion yourself.

## Unit Conversions

Various unit conversion factors are arrayed in the top left side of the sheet.  The following screenshot shows the conversion factors:

![unit conversion factors](web-app-support-UnitConvFactors.png)

Many of these factors, colored in light green, are universally true and so should not be adjusted by the model user, even if customizing the model for a different country.  For example, there will always be one million MWh per TWh and one thousand grams per kilogram.  Conversion factors for coal, natural gas, and liquid fuels (petroleum gasoline, petroleum diesel, biofuel gasoline, biofuel diesel, and jet fuel) can vary by country, because the chemical composition of these fuels may vary from place to place and from year to year.  (In fact, they are implemented as time series in the U.S. model, because the energy content of petroleum gasoline and of biofuel gasoline change very slightly during the model run.)

Dollars per Output Currency Unit converts the model's internal currency unit (dollars) into whatever currency output unit is most appropriate for the modeled country or region.  In the U.S., the output currency units are "billions of US dollars."

## Output Variables

Variables available for use in the web application are arrayed in three columns.  The first two columns are for single-variable graphs in the web app.  This means that any given scenario only shows up as a single line on the graph.  For example, "CO2e Emissions (Total)" and "Natural Gas Consumption (Total)" are single-variable graphs.  The web application allows the user to display many scenarios as different curves on a single-variable graph.

The third column provides output variables that support multi-variable graphs in the web app.  This means that a single scenario shows up as a set of different lines or stacked areas on the graph.  For example, "Electricity Generation Capacity by Type" is a multi-variable graph.  The web application can only show one scenario at a time on a multi-variable graph.

As you move up and down in a column, graphs are grouped into categories designated by colored, tall, thin boxes.  For example, the first column includes a section of "Financial" graphs, a section of "CO<sub>2</sub>e" graphs, a section of "Elec" (electricity) graphs, and a section of "Coal" graphs.

By convention in the EPS, output variables' names always begin with the word "Output" (and no other variables' names begin with the word "Output").

In most cases, each variable is converted via the relevant conversion factor to obtain its "Output" version.  A small graph to the right of the variable displays data from that output variable.  As an example, here is a screenshot of the model structure and graph for the "Output Total CO2e Emissions" variable:

![output CO2e emissions structure and graph](web-app-support-OutputCO2e.png)

These graphs are included on this page as a way to quickly visually check that each output variable is producing data and to verify that the units used by the output variable result in reasonable axis labels.  These small graphs are not intended to be used for data analysis, as they generally lack sufficient detail.  If you wish to perform data analysis in Vensim, you should instead follow the guidelines discussed in the help pages in the [How to Conduct Analysis in Vensim Model Reader section](how-to-conduct-analysis.html).