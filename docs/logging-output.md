---
layout: page
title:  "Logging Output for Multiple Scenarios"
---

## Saving .cin Files with Policy Settings

After you have set policy levers (most easily done in SyntheSim mode, as described in the [Running the Model and Setting Policy Levers](running-the-model.html) section, your results are automatically saved to a file with a .vdf extension.  This is a large data file that contains numerical values for every variable in the model in every year of the model run.

You can also save your scenario settings to a text file with a .cin extension.  While in SyntheSim mode, after changing some policy levers, click the "Save Changes" button near the upper left of the screen, as shown in the following screenshot:

![save changes button](logging-output-SaveChangesButton.png)

You will then specify a name for the new ".cin" file that will be created.  The .cin file is a text file that specifies the values of any variables that you have changed from their default values (typically, any policies you have enabled).

Saving .cin files is useful because they take up very little disk space and can quickly be used to re-run the model with a particular group of settings, so that output data can be re-generated and placed into the variables in Vensim for analysis.  It is usually unnecessary to save the .vdf file for a given run if you have saved a .cin file for that run, since it is so fast and easy to perform that run again.  (Also, .cin files will almost always be compatible with future versions of the EPS, whereas .vdf files will not be.)

If you make many scenarios, you may acquire a large collection of .cin files.  You might wish to compare specific output data between these scenarios (for example, to find the one that has the lowest emissions).  Without a script, you would need to load each scenario one-at-a-time and note the amount of emissions.  The data logging Python script allows you to quickly compile a list containing the values of the output variables of your choice for each scenario you specify.

Three scenarios defined by .cin files are included in the model distribution.  By default, the data logging script is configured to use these scenarios.  We will use them in the following example.

## Editing the Data Logging Script

First, ensure that your OuputVarsToExport.lst file is properly configured, as described in [Selecting Output Variables for Any Python Script](selecting-output-variables.html).

Next, open the "CreateDataLoggingScript.py" file in a text editor such as Notepad++.  The first twenty lines are shown in the following screenshot:

![first lines of GenerateDataLoggingScript.py](logging-output-LoggingScript.png)

The only line that you are likely to wish to edit is line 17, which includes a list of the scenario files (.cin files) that should be tested.  By default, the script will test the BAU case (the entry with two adjacent double-quote marks, which has no associated .cin file) and each of the three included scenarios: the Clean Power Plan scenario, the Energy Innovation Recommended scenario, and the CO2e-minimizing scenario.  You may remove any of these scenarios from the list, and you may add an unlimited number of your own scenarios to the list.  Each scenario must be the complete filename of the ".cin" file that defines the scenario.  Like the examples provided, the scenario filename should be within the square brackets, surrounded by double quotes, and separated from the other filenames via a comma.

Save and close the GenerateDataLoggingScript.py file when you are done.

## Running the Data Logging Script

Run the GenerateDataLoggingScript.py file in Python 3.  (If the .py file extension is associated with Python 3, you can simply double-click the file to do this.)  Python creates a new file in the Energy Policy Solutions (EPS) model folder called "GeneratedDataLoggingScript.cmd".  This is a Vensim command script.

Open Vensim DSS.  From the "File" menu, choose "Open Model..."  In the "Name of Model to Open" dialogue box, you will see a drop-down menu in the lower right corner, just above the "Open" and "Cancel" buttons.  That menu starts with "Vensim Models" selected.  Change the setting to "Command Scripts (*.cmd)".  (If you do not see this option in your drop-down menu, then you are running a version of Vensim other than Vensim DSS.  See the page on [Automated Analysis with Python Scripts](automated-analysis.html) for details.)  The following screenshot shows the way this window looks under Windows 10:

![open script window](logging-output-OpenScriptWindow.png)

Click the "Open" button.  Vensim performs one run for each entry in the list of .cin files specified in the Python script.  If you kept the blank entry in the list, one run will also be done for the BAU case.  For each model run, Vensim produces one data file (with .vdf extension) and one text results file (with .tsv extension).  Each file will be named after the scenario that generated it.  (For example, the output files from the simulation based on the Scenario_EI.cin file will be named Scenario_EI.vdf and Scenario_EI.tsv.)  Output files for a BAU run (not based on a .cin file) will be named NoSettings.vdf and NoSettings.tsv.

The .tsv files are tab-separated values and can be opened in Microsoft Excel or another spreadsheet program, where the value of each variable specified in the OuputVarsToExport.lst file will be included for each year of the model run.  The .vdf files are Vensim data files.  They can be loaded in Vensim if you wish to examine the output from any variables in the model, or they may be deleted if you are only interested in the output for the variables specified in OutputVarsToExport.lst and included in the tab-separated values file.