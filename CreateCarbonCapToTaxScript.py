# CreateCarbonCapToTaxScript.py
#
# Developed by Jeffrey Rissman
#
# This is a Python script that is used to generate a Vensim command script.
# The Vensim command script will enable Vensim to produce a series of simulations
# that allow you to determine the carbon tax rate (lever setting) equivalent
# to a particular carbon cap policy that you wish to model.
#
# DOCUMENTATION
# Detailed documentation on how to use this script is available online at:
# https://us.energypolicy.solutions/docs/simulating-cap-and-trade.html


# File Names
# ----------
# Rather than including input and output file names in the code below, we assign all the file
# names to variables in this section.  This allows the names to be easily changed if desired.
ModelFile = "EPS.mdl" # The name of the Vensim model file (typically with .mdl or .vpm extension)
FirstYear = "2020" # The first year you wish to include in the output file (cannot be prior to first simulated year)
FinalYear = "2050" # The last year you wish to include in the output file (cannot be later than last simulated year)
OutputScript = "GeneratedCarbonCapToTaxScript.cmd" # The desired filename of the Vensim command script to be generated
RunResultsFile = "RunResults.tsv" # The desired filename for TSV file containing model run results
OutputVarsFile = "OutputVarsForCarbonCapToTaxScript.lst"	# The name of the file containing a list of variables
															# to be included in the RunResultsFile
															# May optionally also be used as a SAVELIST
															# for Vensim (see below)


# Complementary Policies
# ----------------------
# You may test the carbon cap in the context of a set of other policies, called complementary
# policies in this script.  These are read in from a scenario file (with .cin extension).
# Leave this blank (put nothing between the quotes, like this: "")
# if you wish to test the carbon cap without any other policies.
# IMPORTANT NOTES:
# Any carbon tax settings in the ComplementaryPoliciesFile will be ignored.
# Any policy schedule selection made in the ComplementaryPoliciesFile will be ignored.
ComplementaryPoliciesFile = "Scenario_NDC.cin"


# Policy Schedule
# ---------------
# Specify the number of the policy implementation schedule file to use (in InputData/plcy-schd/FoPITY).
# This overrides any policy schedule setting that may exist in the ComplementaryPoliciesFile.
PolicySchedule = 1


# Carbon Cap Floor and Ceiling
# ----------------------------
# Here, set the lower and upper bounds of the emissions permit prices that you
# wish to test.  If the carbon cap policy has a floor or ceiling price, use
# those values.  If there is no floor, use zero.  If there is no ceiling, use
# a value you deem sufficiently high to be unlikely to be exceeded.
#
# If the floor and ceiling change over time, and you want to find the permit
# price for multiple years, enter the lowest floor among the years of interest
# and enter the highest ceiling among the years of interest.  This avoids the
# need to run the script more than once.
#
# Values are expressed in the model's input currency units (which vary by EPS deployment)
# per ton CO2e.  For example, in the U.S. EPS, the units are $/ton CO2e.
#
# IMPORTANT NOTE: Remember to adjust the floor and cap in this script to account
# for your chosen policy implementation schedule.  This script specifies the
# carbon tax lever setting that will be used, which is fully in effect only in
# years with an implementation value of 1.  Therefore, you must INCREASE the
# floor and ceiling values in this script if you are testing a year where the
# implementation schedule is less than one.  For example, if you are interested
# in the emissions permit price in 2030, and the policy schedule for the carbon
# tax in 2030 is 0.5 (i.e. 50% implemented), then the 2030 floor and 2030 ceiling
# prices (from the carbon cap legal text) must be doubled to obtain the lever
# settings to enter in this script.
#
# If interested in permit prices in multiple years, FIRST adjust all the floor and
# celing prices to reflect the carbon tax policy implementation schedule, THEN
# enter the lowest floor and the highest ceiling prices here.
PriceFloor = 10
PriceCeiling = 15


# Covered Sectors
# ---------------
# Enable sectors that are covered under the same carbon cap.
# If each sector, or specific sets of sectors, have individual (non-pooled)
# carbon caps, run this script multiple times, testing each set of sectors
# that share a single carbon cap separately.
Sectors = {
	"transportation sector": False,
	"electricity sector": True,
	"residential buildings sector": False,
	"commercial buildings sector": False,
	"industry sector": True
}


# Other Settings
# --------------
RunName = "MostRecentRun" # The desired name for all runs performed.  Used as the filename for the .vdfx files that Vensim creates.



# Building the Covered Sector List
# --------------------------------
CoveredSectors = []
for Sector in Sectors:
	if Sectors[Sector]:
		CoveredSectors.append(Sector)


# Error Checking
# --------------
# Give error and exit if no sectors were enabled
if len(CoveredSectors) < 1:
	f = open(OutputScript, 'w')
	ErrorMessage = "Error: No sectors were enabled in the Python script.  Before running the script, you must enable at least one sector."
	f.write(ErrorMessage)
	f.close()
	import sys
	sys.exit(ErrorMessage)	
		
# Give error and exit if price ceiling is not greater than price floor
if PriceCeiling <= PriceFloor:
	f = open(OutputScript, 'w')
	ErrorMessage = "Error: PriceCeiling must be greater than PriceFloor."
	f.write(ErrorMessage)
	f.close()
	import sys
	sys.exit(ErrorMessage)


# Generate Vensim Command Script
# ------------------------------
# We begin by creating a new file to serve as the Vensim command script (overwriting
# any older version at that filename).  We then tell Vensim to load
# the model file, and we give it a RUNNAME that will be used for all runs.  (It is
# overwritten each run, and the Vensim command file generated by this script
# always contains multiple runs.)
f = open(OutputScript, 'w')
f.write('SPECIAL>LOADMODEL|"' + ModelFile + '"\n')
f.write("SIMULATE>RUNNAME|" + RunName + "\n")

# The following options may be useful in certain cases, but they may slow Vensim down
# or increase the odds that Vensim crashes during execution of a batch of runs (though
# it is hard to tell for sure).  These lines are usually best left commented out.
# f.write("SPECIAL>NOINTERACTION\n")
# f.write("SIMULATE>SAVELIST|" + OutputVarsFile + "\n")
f.write("\n")


# Only for the first entry in the TSV file, we wish to include the "Time" row and
# overwrite any existing TSV file of that name.  Other entries append to the TSV file.
FirstEntryDone = False


# We start the price at the price floor, and we will increment by one
# currency unit with each model run.
CurrentPrice = PriceFloor

while CurrentPrice <= PriceCeiling:

	# We have to read in the .cin file for every simulation.
	# Therefore, we have to override its policy implementation schedule setting
	# and carbon tax policy settings for every simulation.
	f.write("SIMULATE>READCIN|" + ComplementaryPoliciesFile + "\n")
	f.write("SIMULATE>SETVAL|Policy Implementation Schedule Selector=" + str(PolicySchedule) + "\n")

	# We check each sector.  If it is enabled, we write a SETVAL command to specify the current price.
	# If it is not enabled, we write a SETVAL command to set it to zero.
	for Sector in Sectors:
		if Sectors[Sector]:
			f.write("SIMULATE>SETVAL|Additional Carbon Tax Rate[" + Sector + "]=" + str(CurrentPrice) + "\n")
		else:
			f.write("SIMULATE>SETVAL|Additional Carbon Tax Rate[" + Sector + "]=0\n")

	# We add a RUN instruction now that we've added all the SETVAL instructions.
	f.write("MENU>RUN|O\n")
	
	# Lastly, we copy the results from the .vdfx file generated by Vensim to a TSV file.
	# The complexity of this section is partly due to Vensim's required syntax for the
	# VDF2TAB function.  Please see the page on that function in the Vensim reference
	# manual for details.  But the general idea is that at the end (after the series of
	# vertical bars), we can add columns for arbitrary text, and we use this functionality
	# to add entries to the spreadsheet showing the current price and which sectors were
	# enabled for this run.
	if FirstEntryDone:
		f.write("MENU>VDF2TAB|" + RunName + ".vdfx|" + RunResultsFile + "|" + OutputVarsFile + "|+!||" + FirstYear + "|" + FinalYear + "|:")
	else:
		f.write("MENU>VDF2TAB|" + RunName + ".vdfx|" + RunResultsFile + "|" + OutputVarsFile + "|||" + FirstYear + "|" + FinalYear + "|:")
		FirstEntryDone = True

	# Include a column for CurrentPrice in the output file, then increment CurrentPrice
	f.write("CurrentPrice=\t" + str(CurrentPrice))
	CurrentPrice += 1

	# Adding a column specifying which sectors were enabled for this run
	NumSectorsRemaining = len(CoveredSectors)
	f.write("\tCovered sectors=")
	for Sector in CoveredSectors:
		f.write(Sector)
		NumSectorsRemaining -= 1
		if NumSectorsRemaining > 0:
			f.write(", ")
	f.write("\n")

	# We instruct Vensim to delete the .vdfx file, to prevent it from getting picked up by
	# sync software, such as DropBox or Google Drive.  If sync software locks the file,
	# Vensim won't be able to overwrite it on the next model run, ruining the batch.
	f.write("FILE>DELETE|" + RunName + ".vdfx")
	f.write("\n\n")

# We are done writing the Vensim command script and therefore close the file.
f.close()
