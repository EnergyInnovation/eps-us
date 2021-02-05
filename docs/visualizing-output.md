---
layout: page
title:  "Visualizing Output"
---

After you have run the model, there are three ways to visualize the outputs.  You may rely on the set of graphs that are built into the Energy Policy Simulator (EPS) (which appear on various sheets of the model), you may generate graphs of any variable using Vensim, or you may copy tabular data and import them into another program, such as a spreadsheet, before graphing them there.

## The EPS's Built-In Graphs

The EPS includes about twenty graphs that were set up by the model developer.  The specific variables shown on these graphs, as well as the graph style (line or stacked area, sometimes axis scale) have been pre-selected and cannot be changed using Vensim Model Reader.  These graphs include:

* Total CO<sub>2</sub>e emissions, PM<sub>2.5</sub> emissions, cash flow change, change in outlays compared to monetized social benefits, human lives saved from reduced particulate pollution, and four electricity-related graphs located on the "Policy Control Center" sheet
* A CO<sub>2</sub> graph specific to each of the four major sectors located on that sector's "Main" sheet
* A financial graph specific to each of the four major sectors located on that sector's "Cash Flow" sheet
* Four electricity-related graphs located on the "Electricity Sector - Main" sheet
* (There also exist many small graphs on the "Web Application and Support Variables" sheet, but these are not set up to be used for analysis.)

Once the model has been run, the data from the topmost currently-loaded run (generally the most recent run) will always be shown in the built-in graphs.

No special technique or controls are involved in analyzing the data on the built-in graphs.  It may be helpful to zoom in on some of them.  This can be done by holding down the "control" key and rolling the mouse wheel up (while the mouse is hovering over the main view in Vensim Model Reader).

## Producing Your Own Graphs in Vensim

After the model has been run, you may click on any variable to make it the active variable.  That variable's name will appear in the title bar for the Vensim Model Reader window after the model's filename.  (The title bar will read approximately "Vensim:EPS.mdl Var:[active variable]".)

Navigate to the "Cross-Sector Totals" sheet and scroll to the top left.  Click once on the "Total CO<sub>2</sub>e Emissions" variable to make it the active variable.  Then, click the "Graph" button on the left side of the screen.

![Graph button](visualizing-output-GraphButton.png)

A graph showing total CO<sub>2</sub>e emissions appears in an output window, as shown below.  You can drag any edge to resize this window.  Five small buttons in the upper left allow you to close the window, lock the window (prevent it from being closed), print the graph, copy the graph to the clipboard, or save the graph as a file.

![Total CO2e Emissions graph](visualizing-output-CO2eGraph.png)

You may graph a subscripted variable.  Click on the "Total Pollutant Emissions" variable, then click the Graph button.  A graph appears, and the key indicates twelve lines are on the graph- one for each of the twelve pollutants in the model.  However, most of the lines are stacked on top of each other near the X axis, because CO<sub>2</sub> emissions are so much larger than the emissions of other pollutants.  The graph may look similar to the screenshot below, where only CO<sub>2</sub> and F gases (which are represented in CO<sub>2</sub>e terms) are visible above the X-axis:

![Total Pollutant Emissions graph](visualizing-output-PollutantsGraph.png)

In order to see the other lines, it is necessary to hide the lines for CO<sub>2</sub>e and F gases, so Vensim selects a Y-axis scale that allows more lines to be seen.  Click the "Subscripts" button near the upper right of the window:

![Subscripts button](visualizing-output-SubscriptsButton.png)

This opens the subscripts window.  This window allows you to toggle the display of various subscript elements off and on.  If it is not already active, click on the tab titled "Pollutant 12/12".  The window should look like this:

![Subscripts window](visualizing-output-SubscriptsWindow.png)

If you instead see a view with three boxes (labeled "Subranges" "Available Elements" and "Selected Elements"), then you are in the "Full" view.  Click the "Simple" button in the lower right to switch the Pollutants tab to simple view, and it will look like the screenshot above.

Click on the "CO<sub>2</sub>" and "F gases" rows to de-select them.  The name of the tab changes to "Pollutant 10/12".  Close the subscripts window, then click on the "Graph" button again.  (If "Total Pollutant Emissions" is no longer the active variable, you will need to first click it to make it active again.)  Now the Total Pollutant Emissions graph only has lines for ten pollutants, and many more of them are visible above the X-axis.  It should look similar to the following screenshot:

![Total Pollutant Emissions graph](visualizing-output-PollutantsGraph2.png)

You may also include more than one variable on the same graph.  Open the Subscripts window, ensure the "Pollutants" tab is selected, and click the "None" button to deselect all the pollutants.  Then click on "CO<sub>2</sub>" to select only that pollutant.  Close the subscripts window.

Now, in the upper left corner of the "Cross-Sector Totals" sheet, click on "Transportation Sector Pollutant Emissions."  Hold shift, then click on "Electricity Sector Pollutant Emissions," which appears immediately below.  Then click on the "Graph" button.  A graph titled "Selected Variables" appears that shows the CO<sub>2</sub> emissions for these two sectors, as in the following screenshot:

![graph of CO2 from two sectors](visualizing-output-TwoSectorCO2.png)

This method only works if the two variables are on the same sheet.  If you select a new variable that is on a different sheet from the variable you last selected, even if you hold shift, the selected variable(s) on the inactive sheet will not be included in the graph.

If the two variables you selected have different units, Vensim will create multiple Y axis labels at different scales- one set of labels for each of the units used by a selected variable.  For example, graphing "Total CO<sub>2</sub>e Emissions" and "Total Electricity Demand" together will yield one scale in g CO<sub>2</sub>e and one scale in MWh, as shown in the following screenshot:

![graph of Total CO2e Emissions and Total Electricity Demand](visualizing-output-DifferentUnits.png)

## Copying Tabular Data for Use in Another Program

Graphs generated on command in Vensim Model Reader can be good for getting a quick sense of a variable's behavior, but the graphs seldom look very good and are not customizable.  Often, it is best to copy the data in tabular form and graph it in a program that provides more options and produces nicer-looking output, such as Microsoft Excel or another spreadsheet program.

To do this, select one or more variables, then click on the "Table" button on the left side of the screen.

![Table button](visualizing-output-TableButton.png)

A table appears that includes all of the selected variables.  (Often, variables with longer variable names will overlap some of the table entries- this cannot be corrected in Vensim Model Reader, which does not support changing the size of the first table column, but it does not affect the data.)  Here is a screenshot of the Table window showing data for the "Total CO<sub>2</sub>e Emissions" variable:

![Table window](visualizing-output-TableWindow.png)

You can include variables on more than one Vensim sheet in the same table, even though variables on non-active sheets will not be included in a table if you select a variable on a new sheet before clicking the "Table" button.  Instead, add the variables to the table sequentially, without closing the table in between variables.  For example, select one or more variables on the Cross-Sector Totals tab, click the "Table" button, and then left-click in the main Vensim window.  The table vanishes, but it has not been closed- it is simply behind the main Vensim window.  Now, switch to another sheet.  Select one or more variables and click the "Table" button.  The existing table will be brought to the front and the selected variables will be added to the bottom of the table.

Once you have the variables you want in the table, click the fourth small button in the upper left corner of the Table window, which copies the table data to the clipboard (as tab-separated values).  Now, open the program you wish to use for analysis or graphing, such as a spreadsheet program, and paste the data in from the clipboard.  If your analysis or graphing program will not accept pasted data directly, you can instead use the fifth button in the Table window to save the data as a text file (again, as tab-separated values), then open that text file in your program.  The following screenshot points out the location of these two buttons.

![Table export buttons](visualizing-output-TableExportButtons.png)