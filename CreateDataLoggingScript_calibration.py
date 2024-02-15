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
FirstYear = "2021" # The first year you wish to include in the output file (cannot be prior to first simulated year)
FinalYear = "2050" # The last year you wish to include in the output file (cannot be later than last simulated year)
OutputScript = "GeneratedDataLoggingScript.cmd" # The desired filename of the Vensim command script to be generated
OutputVarsFile = "OutputVarsToExport-Calibration.lst" # The name of the file containing a list of variables to be included in the RunResultsFile
SettingsFiles = [""]
	# This is the list of settings files to be tested, with .cin extensions.
	# Include a blank entry (e.g. "") to include BAU case.

	
# Generate Vensim Command Script
# ------------------------------
# We use a SAVELIST to reduce the size of the output files, since we are generating one per run.
f = open(OutputScript, 'w')
f.write('SPECIAL>LOADMODEL|"' + ModelFile + '"\n\n')
f.write("SIMULATE>SAVELIST|" + OutputVarsFile + "\n")

for SettingsFile in SettingsFiles:

	# The RunName is the name of the SettingsFile without the .cin extension.  It is used as the filename for the .vdfx file
	# that Vensim creates (or "NoSettings"), and it is included in a column in the RunResultsFile.
	SettingsFileNameLen = len(SettingsFile)
	if SettingsFileNameLen < 5:
		RunName = "NoSettings"
	else:
		RunName = SettingsFile[:SettingsFileNameLen - 4]
	RunResultsFile = RunName + ".tsv" # The desired filename for the file containing model run results
	
	# Generate an empty output file with a time row, to work around bug where Vensim includes multiple Time rows if you
	# don't suppress all time rows.  We overwrite any output file that may exist at this filename.
	tsv = open(RunResultsFile, 'w')
	tsv.write("Time\t" + RunName + "\t")
	YearToWrite = FirstYear
	while(YearToWrite <= FinalYear):
		tsv.write(YearToWrite)
		if(YearToWrite != FinalYear):
			tsv.write("\t")
		else:
			tsv.write("\n")
		YearToWrite = str(int(YearToWrite)+1)
	tsv.close()

	# Write directions to set the run name, read the settings, run the simulation, and append the results to the RunResultsFile.
	f.write("SIMULATE>RUNNAME|" + RunName + "\n")
	f.write("SIMULATE>READCIN|" + SettingsFile + "\n")
	f.write("MENU>RUN|O\n")
	f.write("MENU>VDF2TAB|" + RunName + ".vdfx|" + RunResultsFile + "|" + OutputVarsFile + "|+!||" + FirstYear + "|" + FinalYear + "|:")
	f.write(RunName)
	f.write("\n")

	# We instruct Vensim to delete the .vdfx file, to prevent it from getting picked up by
	# sync software, such as DropBox or Google Drive.  If sync software locks the file,
	# Vensim won't be able to overwrite it on the next model run, ruining the batch.
	f.write("FILE>DELETE|" + RunName + ".vdfx")
	f.write("\n\n")

# Since Vensim fails to clear the savelist entry in the program after script execution, we need to do it here
# before the script exits.
f.write("SIMULATE>SAVELIST|\n")

# We are done writing the Vensim command script and therefore close the file.
f.close()