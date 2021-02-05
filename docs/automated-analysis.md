---
layout: page
title:  "Automated Analysis with Python Scripts"
---

The Energy Policy Simulator (EPS) is distributed with several scripts written in the Python programming language.  The purpose of these scripts is to allow the model user to perform certain types of analysis or generate certain types of output that would be laborious to do manually.

## Scripts

Four scripts are included in the EPS model distribution:

- `CreateContributionTestScript.py` - This script helps you determine the contributions of individual policies or user-specified groups of policies to a policy package.  It is useful for generating wedge diagrams and policy cost curves.

- `CreateDataLoggingScript.py` - This script simply runs a series of scenarios, each specified by its own .cin file, and outputs the results.  It is useful if you have created a number of custom policy scenarios and wish to compare their performance with respect to particular output variables.  It is also useful when calibrating a newly-built EPS, to quickly and repeatedly output the same set of variables in the same order, to paste into a calibration spreadsheet.

- `CreateCombinationsScript.py` - This script is used to test every possible combination of a set of user-selected policy settings for a user-selected set of policies.  It is useful if you have a goal in mind, and you wish to search for a policy package that achieves your goal while maximizing or minimizing some other variable, such as meeting a carbon cap at lowest cost.

- `CreateCarbonCapToTaxScript.py` - This script allows you to simulate a carbon or GHG cap-and-trade policy, either alone or in conjunction with complementary policies.

### Output Variable Lists

The Python scripts rely on output variable lists, text files that include the names of variables that the user wants the scripts to include in the results file (one variable name per line).  The included variable lists are:

- `OutputVarsToExport.lst`
- `OutputVarsForCarbonCapToTaxScript.lst`

Three of the Python scripts rely on the `OutputVarsToExport.lst` file to know which variables to save, while the `CreateCarbonCapToTaxScript.py` script has its own output variable list.

## Required Software

Using the Python scripts requires software beyond that which is needed to simply run the EPS or edit its input data.  You must have a copy of Vensim DSS (the only tier of Vensim that supports scripting) and Python 3 installed on your system.  Although not strictly required, a text editor designed for programmers and capable of color-coding Python syntax, such as _Visual Studio Code_, is very helpful.

### Vensim DSS

Most features of the EPS can be used if you run the model in the free Vensim Model Reader, as discussed on the [Download and Installation Instructions](download.html) page.  However, you will need a copy of Vensim DSS to make use of the Python scripts included with the EPS.  Information on how to purchase Vensim DSS is available for Windows and Mac on [the official Vensim website](http://vensim.com/purchase/).  As of Oct. 15, 2020, a commercial license costs $1995, a public research license costs $998, and an academic license costs $798.

If you already own Vensim DSS, please be sure that it is version 8 or later, and you have installed the 64-bit version.  The EPS relies on features and bug fixes that were implemented in Vensim 8.  If you own Vensim Pro or DSS with a current maintenance subscription, you can download an updated version from the [Vensim download center](https://www.vensim.com/php-bin/download.html).  If your maintenance subscription is not current, you may log in using your old license key and renew your subscription for a fraction of the price of buying a new Vensim DSS license.

### Python 3

Python 3 is a free and open source programming language.  You can download and install Python 3 on your system from the [official Python website](https://www.python.org/).  It is available for many operating systems, including Windows and Mac.

### Text Editor for Programmers

Although it is not required to use the Python scripts, a text editor oriented toward programmers (and capable of color-coding Python syntax) is recommended.  Some good, free options include:

- [Visual Studio Code](https://code.visualstudio.com/), a full-featured editor, available for Windows, Mac, and Linux

- [Notepad++](https://notepad-plus-plus.org/), a lightweight option for Windows

- [BBEdit](https://www.barebones.com/products/bbedit/index.html), a lightweight option for Mac (works in "Free Mode")

## Python Scripts and Vensim Command Scripts

Python cannot interface with Vensim directly.  For scripting, Vensim only supports "Vensim Command Scripts," series of instructions written in Vensim's own scripting language.  This language is very simple and only allows the user to specify straightforward series of instructions, such as: load a model, adjust a variable setting, run the model, log the output data to a text file, etc.  It does not support common programming structures such as IF statements, FOR loops, etc.

These programming structures are necessary in order to perform the automated analysis we need.  Therefore, the Python scripts provided with the EPS are designed to write Vensim command scripts.

## Steps to Use Python Scripts

More detailed instructions about how to use each Python script are available on each script's own documentation page (which you can reach from the [EPS documentation index](index.html)).  However, the basic process is the same for all of the Python scripts:

1. Open the Python script you wish to use in your text editor.  Edit it to specify the parameters of the series of runs that you wish to perform.  Save and close the Python script.  It is recommended you use "save as" and save a copy of the Python script with a name that describes the edits you made.  This helps with file organization and ensures you always have a clean copy of the original Python script to refer to.

2. In your text editor, open the variable output list file used by the Python script (see the "Output Variable Lists" section above for details).  Edit it to include each of the variables that you wish to be included in the output file (and remove variables you do not want included).  This process is described more thoroughly on the [Selecting Ouput Variables for a Python Script](selecting-output-variables.html) documentation page.

3. Double-click the Python script to execute it.  It will produce a Vensim command script (with `.cmd` extension).

4. Open Vensim DSS.  Choose `File > Open Model`.  From the drop-down menu above the `Open` and `Cancel` buttons, select `Command Scripts (*.cmd)`.  Select the command script you just created and click `Open`.

5. Wait for Vensim to complete the series of runs.  Results will be found in a tab-separated values (`.tsv`) file inside the EPS model folder.  The name of the results file varies depending on which Python script you used.  You may open and graph the results in a spreadsheet program.
