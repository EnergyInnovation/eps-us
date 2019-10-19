# CreateDataLoggingScript.py
#
# Developed by Jeffrey Rissman
#
# This is a Python script that is used to generate a Vensim command script.
# The Vensim command script runs simulations based on a list of .cin
# settings files and logs the output to separate, tab-separated files.


# File Names
# ----------
# Rather than including input and output file names in the code below, we assign all the file
# names to variables in this section.  This allows the names to be easily changed if desired.
ModelFile = "EPS.mdl" # The name of the Vensim model file (typically with .mdl or .vpm extension)
OutputScript = "GeneratedDataLoggingScript.cmd" # The desired filename of the Vensim command script to be generated
OutputVarsFile = "OutputVarsToExport.lst" # The name of the file containing a list of variables to be included in the RunResultsFile
SettingsFiles = ["","Scenario_NDC.cin","Scenario_EI.cin","Scenario_CO2eMin.cin"]
	# This is the list of settings files to be tested, with .cin extensions.
	# Include a blank entry (e.g. "") to include BAU case.

	
# Generate Vensim Command Script
# ------------------------------
# We use a SAVELIST to reduce the size of the output files, since we are generating one per run.
f = open(OutputScript, 'w')
f.write('SPECIAL>LOADMODEL|"' + ModelFile + '"\n\n')
f.write("SIMULATE>SAVELIST|" + OutputVarsFile + "\n")

for SettingsFile in SettingsFiles:

	# The RunName is the name of the SettingsFile without the .cin extension.  It is used as the filename for the VDF file
	# that Vensim creates (or "NoSettings"), and it is included in a column in the RunResultsFile.
	SettingsFileNameLen = len(SettingsFile)
	if SettingsFileNameLen < 5:
		RunName = "NoSettings"
	else:
		RunName = SettingsFile[:SettingsFileNameLen - 4]
	RunResultsFile = RunName + ".tsv" # The desired filename for the file containing model run results
	
	f.write("SIMULATE>RUNNAME|" + RunName + "\n")
	f.write("SIMULATE>READCIN|" + SettingsFile + "\n")
	f.write("MENU>RUN|O\n")
	f.write("MENU>VDF2TAB|" + RunName + ".vdf|" + RunResultsFile + "|" + OutputVarsFile + "|||||:")
	f.write(RunName)
	f.write("\n\n")

# Since Vensim fails to clear the savelist entry in the program after script execution, we need to do it here
# before the script exits.
f.write("SIMULATE>SAVELIST|\n")

# We are done writing the Vensim command script and therefore close the file.
f.close()