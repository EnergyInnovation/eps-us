---
layout: page
title:  "Selecting Ouput Variables for Any Python Script"
---

All three of the Python scripts included in the Energy Policy Simulator (EPS) model distribution rely on a text file called "OutputVarsToExport.lst" to determine which variables in the EPS the user wishes to have included in the output file(s).  Therefore, before using any of the Python scripts, it is best to set up the OutputVarsToExport.lst file so that all of the variables you are interested in will be included in the results.

Despite its unusual ".lst" extension, "OutputVarsToExport.lst" is an ordinary text file and can be opened in Notepad++ or another text editor.  The file simply contains the names of variables (defined inside the EPS), listed one per line.  The OutputVarsToExport.lst file is distributed containing a few variable names as an example.  You may wish to delete some or all of the variable names that already exist in this file, to avoid cluttering up your run results file with output of variables in which you have no interest.  (By default, the variables listed are all from the "Web Application Support Variables" sheet and begin with the word "Output".  That word is not a command; it is simply part of the variable names.)

The best way to decide which variables to include in the OutputVarsToExport.lst file is to open the model in Vensim Model Reader and to locate the variables in which you are interested.  Then you simply copy each variable's name to a new line in the OutputVarsToExport.lst file.  For example, you might decide that you are interested in the "Transportation Sector Pollutant Emissions" variable from the "Transportation - Main" sheet.  If so, you simply add the text "Transportation Sector Pollutant Emissions" (without the quotes) to a blank line in the OuputVarsToExport.lst file.  Below is a screenshot of the OuputVarsToExport.lst file, open in Notepad++, after deleting the example variable entries and adding an entry for "Transportation Sector Pollutant Emissions":

![one variable in OutputVarsToExport.lst file](selecting-output-variables-OneVarEntry.png)

If you include the name of a subscripted variable in the OutputVarsToExport.lst file, the results file will include one entry for each subscripted element of that variable.  For example, the "Transportation Sector Pollutant Emissions" variable is subscripted by pollutant, and the "Pollutant" subscript has twelve entries (CO2, NOx, SOx, PM10, etc.).

To limit the output to certain elements of a subscripted variable, you can list those elements in square brackets after the name of the variable in the OutputVarsToExport.lst file.  Only one element may be specified per line, so you will need to repeat the variable name if you want to log the output of more than one element of the same variable.  For example, if I am interested in just the CO2, CH4, and N2O pollutants from the Transportation sector, my OuputVarsToExport.lst file would look like this:

![subscript elements of one variable in OutputVarsToExport.lst file](selecting-output-variables-SubscriptsEntry.png)

For variables with more than one subscript, you must specify a value for every subscript in order to precisely identify a single element.  For example, the "Fleet Fuel Use" variable on the "Transportation - Main" page is subscripted by vehicle type and cargo type.  So, if I wanted to log the fuel usage of light-duty passenger vehicles, I would need to add the following line (without the quotes) to the OuputVarsToExport.lst file: "Fleet Fuel Use[LDVs,passengers]"

If you are uncertain of the different values that a subscript may take, you can open the "Subscripts" control panel (using the button in the upper right) and click on the tab for the relevant subscript.  The possible values that subscript may take will be listed there.