# CreatePermutationsScript.py
#
# Developed by Jeffrey Rissman
#
# This is a Python script that is used to generate a Vensim command script.
# The Vensim command script will enable Vensim to run simulations of many policies.
# Depending on the user's setting in this Python script, the resulting command script
# will either run simulations with all unique combinations of settings of enabled
# policies, or it will run one simulation for each setting of each enabled policy
# (in isolation) plus one BAU run (all policies off). Which policies should be enabled
# and what settings should be included in the Vensim simulations are specified here in
# the Python script, prior to using it to generate a Vensim command script.


# File Names
# ----------
# Rather than including input and output file names in the code below, we assign all the file
# names to variables in this section.  This allows the names to be easily changed if desired.
ModelFile = "EPS-beta.mdl" # The name of the Vensim model file (typically with .mdl or .vpm extension)
OutputScript = "GeneratedPermutationsScript.cmd" # The desired filename of the Vensim command script to be generated
RunResultsFile = "RunResults.tsv" # The desired filename for TSV file containing model run results
OutputVarsFile = "OutputVarsToExport.lst" # The name of the file containing a list of variables to be included in the RunResultsFile
                                          # May optionally also be used as a SAVELIST for Vensim (see below)

# Other Settings
# --------------
RunName = "MostRecentRun" # The desired name for all runs performed.  Used as the filename for the VDF files that Vensim
						  # creates and included in a separate column in the RunResultsFile.
MinPolicyCols = 0 # At least this many columns for policy settings will be added to the RunResultsFile.  If you have enabled
				  # fewer policies than this, the extra columns will be blank.  The purpose of this setting is to make it
				  # easier to append various RunResultsFiles together, when they use different numbers of enabled policies,
				  # and still have the columns line up correctly.
IndividualPoliciesOnly = False # When this setting is enabled, instead of testing all combinations of enabled policies, the
							   # script tests each setting of each enabled policy in isolation.  (This is a subset of the
							   # tests that are done when all combinations are tested.)


# Index definitions
# -----------------
# Each policy is a Python list.  The numbers below are a key to the meaning of the four entries
# that compose each policy, so we can refer to them by meaningful names in the code.
# Note that the fourth entry in each policy, Settings, is itself a list that contains various
# setting values.  Do not change any names or numbers in this section.
Enabled = 0
LongName = 1
ShortName = 2
Settings = 3


# Policy Options
# --------------
# This section specifies which policies should be included in the Vensim command script
# (called here "enabled" policies) and what setting values for those policies should
# be included.  Unless you have enabled "IndividualPoliciesOnly" mode, all non-repeating
# combinations of the settings for enabled policies will
# be included in the Vensim command script, so do not enable too many policies at once, or
# Vensim will be unable to complete the necessary runs in a reasonable amount of time.
# Each policy is on a single line.  You may change the first entry of each policy to
# "True" to enable the policy or "False" to disable it.
# The fourth entry in each policy is a list of setting values enclosed with square brackets.
# You may change these values, add more values (separated by commas), and delete values.
# Any enabled policy must have a minimum of one setting value.  A policy that is disabled
# and a policy with a setting of zero produce identical results.

# Transportation Sector Policies
ElecPsgrLDVs = (False,"Percent Nonelec Vehicles Shifted to Elec by End Year[passenger,LDVs]","ElecPsgrLDVs",[0,.11,.32])
ElecPsgrHDVs = (False,"Percent Nonelec Vehicles Shifted to Elec by End Year[passenger,HDVs]","ElecPsgrHDVs",[0,.06,.19])
Feebate = (False,"LDVs Feebate Rate","Feebate",[0,48500,145500])
FuelEconLDVs = (False,"Percentage Additional Improvement of Fuel Economy Std by End Year[LDVs]","FuelEconLDVs",[0,.23,.7])
FuelEconHDVs = (False,"Percentage Additional Improvement of Fuel Economy Std by End Year[HDVs]","FuelEconHDVs",[0,.3,.91])
TDM = (False,"Fraction of TDM Package Implemented by End Year","TDM",[0,.25,.75])

# Buildings and Appliances Sector Policies
RebateResHeating = (False,"Boolean Rebate Program for Efficient Components[residential,heating]","RebateResHeating",[0,1])
RebateResCooling = (False,"Boolean Rebate Program for Efficient Components[residential,cooling and ventilation]","RebateResCooling",[0,1])
RebateResAppliances = (False,"Boolean Rebate Program for Efficient Components[residential,appliances]","RebateResAppliances",[0,1])
ComponentStdsHeating = (False,"Reduction in E Use Allowed by Component Eff Std by End Year[heating]","ComponentStdsHeating",[0,.12,.36])
ComponentStdsCooling = (False,"Reduction in E Use Allowed by Component Eff Std by End Year[cooling and ventilation]","ComponentStdsCooling",[0,.12,.36])
ComponentStdsEnvelope = (False,"Reduction in E Use Allowed by Component Eff Std by End Year[envelope]","ComponentStdsEnvelope",[0,.12,.36])
ComponentStdsLighting = (False,"Reduction in E Use Allowed by Component Eff Std by End Year[lighting]","ComponentStdsLighting",[0,.12,.36])
ComponentStdsAppliances = (False,"Reduction in E Use Allowed by Component Eff Std by End Year[appliances]","ComponentStdsAppliances",[0,.12,.36])
ComponentStdsOther = (False,"Reduction in E Use Allowed by Component Eff Std by End Year[other component]","ComponentStdsOther",[0,.12,.36])
ImprovedLabeling = (False,"Boolean Improved Device Labeling","ImprovedLabeling",[0,1])
ContractorEdu = (False,"Boolean Improved Contractor Edu and Training","ContractorEdu",[0,1])
ElecBldgCpnt = (False,"Percent New Nonelec Component Sales Shifted to Elec by End Year","ElecBldgCpnt",[0,.09,.26])
RetrofittingHeating = (False,"Fraction of Components Replaced Annually due to Retrofitting Policy[heating]","RetrofittingHeating",[0,.01,.04])
RetrofittingCooling = (False,"Fraction of Components Replaced Annually due to Retrofitting Policy[cooling and ventilation]","RetrofittingCooling",[0,.01,.04])
RetrofittingEnvelope = (False,"Fraction of Components Replaced Annually due to Retrofitting Policy[envelope]","RetrofittingEnvelope",[0,.01,.04])
RetrofittingLighting = (False,"Fraction of Components Replaced Annually due to Retrofitting Policy[lighting]","RetrofittingLighting",[0,.01,.04])
RetrofittingAppliances = (False,"Fraction of Components Replaced Annually due to Retrofitting Policy[appliances]","RetrofittingAppliances",[0,.01,.04])
RetrofittingOther = (False,"Fraction of Components Replaced Annually due to Retrofitting Policy[other component]","RetrofittingOther",[0,.01,.04])

# Electricity Supply Sector Policies
RPS = (False,"Renewable Portfolio Std Percentage in End Year","RPS",[0,.13,.39])
DemandResponse = (False,"Fraction of Additional Demand Response Potential Achieved","DemandResponse",[0,.25,.75])
SubsidyCoal = (False,"Subsidy for Elec Production by Fuel[coal es]","SubsidyCoal",[0,13.5,40.5])
SubsidyNatGas = (False,"Subsidy for Elec Production by Fuel[natural gas es]","SubsidyNatGas",[0,13.5,40.5])
SubsidyNuclear = (False,"Subsidy for Elec Production by Fuel[nuclear es]","SubsidyNuclear",[0,13.5,40.5])
SubsidyHydro = (False,"Subsidy for Elec Production by Fuel[hydro es]","SubsidyHydro",[0,13.5,40.5])
SubsidyWind = (False,"Subsidy for Elec Production by Fuel[wind es]","SubsidyWind",[0,13.5,40.5])
SubsidySolarPV = (False,"Subsidy for Elec Production by Fuel[solar PV es]","SubsidySolarPV",[0,13.5,40.5])
SubsidySolarTherm = (False,"Subsidy for Elec Production by Fuel[solar thermal es]","SubsidySolarTherm",[0,13.5,40.5])
SubsidyBiomass = (False,"Subsidy for Elec Production by Fuel[biomass es]","SubsidyBiomass",[0,13.5,40.5])
EarlyRetCoal = (False,"Annual Additional Capacity Retired due to Early Retirement Policy[coal es]","EarlyRetCoal",[0,8519,25558])
EarlyRetNatGas = (False,"Annual Additional Capacity Retired due to Early Retirement Policy[natural gas es]","EarlyRetNatGas",[0,453,1358])
EarlyRetNuclear = (False,"Annual Additional Capacity Retired due to Early Retirement Policy[nuclear es]","EarlyRetNuclear",[0,145,435])
EarlyRetHydro = (False,"Annual Additional Capacity Retired due to Early Retirement Policy[hydro es]","EarlyRetHydro",[0,2654,7961])
LifeExtCoal = (False,"Generation Capacity Lifetime Extension[coal es]","LifeExtCoal",[0,5,15])
LifeExtNatGas = (False,"Generation Capacity Lifetime Extension[natural gas es]","LifeExtNatGas",[0,5,15])
LifeExtNuclear = (False,"Generation Capacity Lifetime Extension[nuclear es]","LifeExtNuclear",[0,5,15])
LifeExtHydro = (False,"Generation Capacity Lifetime Extension[hydro es]","LifeExtHydro",[0,5,15])
LifeExtWind = (False,"Generation Capacity Lifetime Extension[wind es]","LifeExtWind",[0,5,15])
LifeExtSolarPV = (False,"Generation Capacity Lifetime Extension[solar PV es]","LifeExtSolarPV",[0,5,15])
LifeExtSolarTherm = (False,"Generation Capacity Lifetime Extension[solar therm es]","LifeExtSolarTherm",[0,5,15])
LifeExtBiomass = (False,"Generation Capacity Lifetime Extension[biomass es]","LifeExtBiomass",[0,5,15])
MandatedCapConst = (False,"Boolean Use Non BAU Mandated Capacity Construction Schedule","MandatedCapConst",[0,1])
GridStorage = (False,"Additional Non Hydro Storage Annual Growth Percentage","GridStorage",[0,.009,.026])
ContractBasedDispatch = (False,"Boolean Use Contract Based Dispatch in Policy Case","ContractBasedDispatch",[0,1])
TransmissionGrowth = (False,"Percentage Increase in Transmission Capacity vs BAU by End Year","TransmissionGrowth",[0,.2,.5])

# Industrial Sector Policies
RedNonmethVent = (False,"Fraction of CO2e from Vented Byproduct Gasses Avoided by End Year","RedNonmethVent",[0,.25,.75])
MethaneDestr = (False,"Fraction of Methane Destruction Opportunities Achieved by End Year","MethaneDestr",[0,.25,.75])
WorkerTraining = (False,"Fraction of Addressable Process Emissions Avoided via Worker Training by End Year","WorkerTraining",[0,.25,.75])
ClinkerSubst = (False,"Fraction of Cement Clinker Substitution Made by End Year","ClinkerSubst",[0,.25,.75])
MethaneCapture = (False,"Fraction of Methane Capture Opportunities Achieved by End Year","MethaneCapture",[0,.25,.75])
EarlyRetIndustry = (False,"Fraction of Energy Savings from Early Facility Retirement Achieved","EarlyRetIndustry",[0,.33,1])
ImprSystemDesign = (False,"Fraction of Installation and System Integration Issues Remedied by End Year","ImprSystemDesign",[0,.33,1])
CogenWasteHeat = (False,"Fraction of Potential Cogeneration and Waste Heat Recovery Adopted by End Year","CogenWasteHeat",[0,.33,1])
IndstFuelSwitch = (False,"Fraction of Coal Use Converted to Other Fuels by End Year","IndstFuelSwitch",[0,.1,.31])
IndstEffStdsCement = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU by End Year[cement and other carbonates]","IndstEffStdsCement",[0,.05,.14])
IndstEffStdsNGPS = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU by End Year[natural gas and petroleum systems]","IndstEffStdsNGPS",[0,.05,.14])
IndstEffStdsIronSteel = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU by End Year[iron and steel]","IndstEffStdsIronSteel",[0,.05,.14])
IndstEffStdsChemicals = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU by End Year[chemicals]","IndstEffStdsChemicals",[0,.05,.14])
IndstEffStdsMining = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU by End Year[mining]","IndstEffStdsMining",[0,.05,.14])
IndstEffStdsWasteMgmt = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU by End Year[waste management]","IndstEffStdsWasteMgmt",[0,.05,.14])
IndstEffStdsOtherInd = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU by End Year[other industries]","IndstEffStdsOtherInd",[0,.05,.14])

# Cross-Sector Policies
CarbonTaxTrspt = (False,"Carbon Tax by End Year[transportation sector]","CarbonTaxTrspt",[0,17.5,52.5])
CarbonTaxElec = (False,"Carbon Tax by End Year[electricity sector]","CarbonTaxElec",[0,17.5,52.5])
CarbonTaxResBldg = (False,"Carbon Tax by End Year[residential buildings sector]","CarbonTaxResBldg",[0,17.5,52.5])
CarbonTaxComBldg = (False,"Carbon Tax by End Year[commercial buildings sector]","CarbonTaxComBldg",[0,17.5,52.5])
CarbonTaxIndst = (False,"Carbon Tax by End Year[industry sector]","CarbonTaxIndst",[0,17.5,52.5])
CCSGrowth = (False,"Fraction of Potential Additional CCS Achieved","CCSGrowth",[0,.33,1])
NonMarketElecPrice = (False,"Boolean Prevent Policies from Affecting Electricity Prices","NonMarketElecPrice",[0,1])
RmvBAUSubsidies = (False,"Percent Reduction in BAU Subsidies","RmvBAUSubsidies",[0,.33,1])
ConvertNonCHPHeat = (False,"Fraction of Non CHP Heat Production Converted to CHP by End Year","ConvertNonCHPHeat",[0,.1,.3])

FuelTaxTransElec = (False,"Additional Fuel Tax Rate by Fuel by End Year[electricity,transportation sector]","FuelTaxTransElec",[0,.04,.13])
FuelTaxTransNatGas = (False,"Additional Fuel Tax Rate by Fuel by End Year[natural gas,transportation sector]","FuelTaxTransNatGas",[0,.04,.13])
FuelTaxTransPetGas = (False,"Additional Fuel Tax Rate by Fuel by End Year[petroleum gasoline,transportation sector]","FuelTaxTransPetGas",[0,.04,.13])
FuelTaxTransPetDies = (False,"Additional Fuel Tax Rate by Fuel by End Year[petroleum diesel,transportation sector]","FuelTaxTransPetDies",[0,.04,.13])
FuelTaxTransBioGas = (False,"Additional Fuel Tax Rate by Fuel by End Year[biofuel gasoline,transportation sector]","FuelTaxTransBioGas",[0,.04,.13])
FuelTaxTransBioDies = (False,"Additional Fuel Tax Rate by Fuel by End Year[biofuel diesel,transportation sector]","FuelTaxTransBioDies",[0,.04,.13])
FuelTaxTransJetFuel = (False,"Additional Fuel Tax Rate by Fuel by End Year[jet fuel,transportation sector]","FuelTaxTransJetFuel",[0,.04,.13])

FuelTaxElecCoal = (False,"Additional Fuel Tax Rate by Fuel by End Year[coal,electricity sector]","FuelTaxElecCoal",[0,.04,.13])
FuelTaxElecNatGas = (False,"Additional Fuel Tax Rate by Fuel by End Year[natural gas,electricity sector]","FuelTaxElecNatGas",[0,.04,.13])
FuelTaxElecNuclear = (False,"Additional Fuel Tax Rate by Fuel by End Year[nuclear,electricity sector]","FuelTaxElecNuclear",[0,.04,.13])
FuelTaxElecBiomass = (False,"Additional Fuel Tax Rate by Fuel by End Year[biomass,electricity sector]","FuelTaxElecBiomass",[0,.04,.13])

FuelTaxBlgResElec = (False,"Additional Fuel Tax Rate by Fuel by End Year[electricity,residential buildings sector]","FuelTaxBlgResElec",[0,.04,.13])
FuelTaxBlgResCoal = (False,"Additional Fuel Tax Rate by Fuel by End Year[coal,residential buildings sector]","FuelTaxBlgResCoal",[0,.04,.13])
FuelTaxBlgResNatGas = (False,"Additional Fuel Tax Rate by Fuel by End Year[natural gas,residential buildings sector]","FuelTaxBlgResNatGas",[0,.04,.13])
FuelTaxBlgResPetDies = (False,"Additional Fuel Tax Rate by Fuel by End Year[petroleum diesel,residential buildings sector]","FuelTaxBlgResPetDies",[0,.04,.13])

FuelTaxBlgComElec = (False,"Additional Fuel Tax Rate by Fuel by End Year[electricity,commercial buildings sector]","FuelTaxBlgComElec",[0,.04,.13])
FuelTaxBlgComCoal = (False,"Additional Fuel Tax Rate by Fuel by End Year[coal,commercial buildings sector]","FuelTaxBlgComCoal",[0,.04,.13])
FuelTaxBlgComNatGas = (False,"Additional Fuel Tax Rate by Fuel by End Year[natural gas,commercial buildings sector]","FuelTaxBlgComNatGas",[0,.04,.13])
FuelTaxBlgComPetDies = (False,"Additional Fuel Tax Rate by Fuel by End Year[petroleum diesel,commercial buildings sector]","FuelTaxBlgComPetDies",[0,.04,.13])

FuelTaxIndElec = (False,"Additional Fuel Tax Rate by Fuel by End Year[electricity,industry sector]","FuelTaxIndElec",[0,.04,.13])
FuelTaxIndCoal = (False,"Additional Fuel Tax Rate by Fuel by End Year[coal,industry sector]","FuelTaxIndCoal",[0,.04,.13])
FuelTaxIndNatGas = (False,"Additional Fuel Tax Rate by Fuel by End Year[natural gas,industry sector]","FuelTaxIndNatGas",[0,.04,.13])
FuelTaxIndBiomass = (False,"Additional Fuel Tax Rate by Fuel by End Year[biomass,industry sector]","FuelTaxIndBiomass",[0,.04,.13])
FuelTaxIndPetDies = (False,"Additional Fuel Tax Rate by Fuel by End Year[petroleum diesel,industry sector]","FuelTaxIndPetDies",[0,.04,.13])


# Building the Policy List
# ------------------------
# Every policy, whether enabled or not, appears on a list below called "PotentialPolicies".
# Now we construct the actual list of policies to be included (named "Policies") by
# checking which of the policies have been enabled.
PotentialPolicies = (ElecPsgrLDVs, ElecPsgrHDVs, Feebate, FuelEconLDVs, FuelEconHDVs, TDM, RebateResHeating, RebateResCooling, RebateResAppliances, ComponentStdsHeating, ComponentStdsCooling, ComponentStdsEnvelope, ComponentStdsLighting, ComponentStdsAppliances, ComponentStdsOther, ImprovedLabeling, ContractorEdu, ElecBldgCpnt, RetrofittingHeating, RetrofittingCooling, RetrofittingEnvelope, RetrofittingLighting, RetrofittingAppliances, RetrofittingOther, RPS, DemandResponse, SubsidyCoal, SubsidyNatGas, SubsidyNuclear, SubsidyHydro, SubsidyWind, SubsidySolarPV, SubsidySolarTherm, SubsidyBiomass, EarlyRetCoal, EarlyRetNatGas, EarlyRetNuclear, EarlyRetHydro, LifeExtCoal, LifeExtNatGas, LifeExtNuclear, LifeExtHydro, LifeExtWind, LifeExtSolarPV, LifeExtSolarTherm, LifeExtBiomass, MandatedCapConst, GridStorage, ContractBasedDispatch, TransmissionGrowth, RedNonmethVent, MethaneDestr, WorkerTraining, ClinkerSubst, MethaneCapture, EarlyRetIndustry, ImprSystemDesign, CogenWasteHeat, IndstFuelSwitch, IndstEffStdsCement, IndstEffStdsNGPS, IndstEffStdsIronSteel, IndstEffStdsChemicals, IndstEffStdsMining, IndstEffStdsWasteMgmt, IndstEffStdsOtherInd, CarbonTaxTrspt, CarbonTaxElec, CarbonTaxResBldg, CarbonTaxComBldg, CarbonTaxIndst, CCSGrowth, NonMarketElecPrice, RmvBAUSubsidies, ConvertNonCHPHeat, FuelTaxTransElec, FuelTaxTransNatGas, FuelTaxTransPetGas, FuelTaxTransPetDies, FuelTaxTransBioGas, FuelTaxTransBioDies, FuelTaxTransJetFuel, FuelTaxElecCoal, FuelTaxElecNatGas, FuelTaxElecNuclear, FuelTaxElecBiomass, FuelTaxBlgResElec, FuelTaxBlgResCoal, FuelTaxBlgResNatGas, FuelTaxBlgResPetDies, FuelTaxBlgComElec, FuelTaxBlgComCoal, FuelTaxBlgComNatGas, FuelTaxBlgComPetDies, FuelTaxIndElec, FuelTaxIndCoal, FuelTaxIndNatGas, FuelTaxIndBiomass, FuelTaxIndPetDies)
Policies = []
for PotentialPolicy in PotentialPolicies:
	if PotentialPolicy[Enabled]:
		Policies.append(PotentialPolicy)

		
# Next, we define two functions that build lists of policy settings.  One builds a list of all combinations
# of settings.  The other builds a list of each setting of each enabled policy tested individually (plus
# the BAU case).  Which function will be called is determined by the user's setting for the
# "IndividualPoliciesOnly" variable above.

def BuildPolicyCombinationsSettingsList():

	# We need to use unusual syntax to generate our list of non-repeating policy setting combinations
	# (see below).  To make a statement whose syntax works for an arbitrary number of policies, I
	# found it clearest and easiest to build the required statement as a string (so that I can
	# append to it using for loops), then execute the string as code at the end.  This next segment
	# constructs the string we plan to execute.  An example of what it should look like when it's
	# done appears in a comment below.
	
	ExpressionToBuildList = "PolicySettingCombinations = [ ("
	for Policy in Policies:
		ExpressionToBuildList += ("P" + str(Policies.index(Policy)) + ", ")
	ExpressionToBuildList = ExpressionToBuildList[:-2]
	ExpressionToBuildList += ") "
	for Policy in Policies:
		ExpressionToBuildList += ("for P" + str(Policies.index(Policy)) + " in range(len(" + Policy[ShortName] + "[Settings])) ")
	ExpressionToBuildList += "]"

	# At this point, ExpressionToBuildList contains a command similar to the following example (which assumes
	# only the CarbonTax, CCSGrowth, and TDM policies are enabled):
	# PolicySettingCombinations = [ (P0, P1, P2) for P0 in range(len(CarbonTax[Settings])) for P1 in range(len(CCSGrowth[Settings])) for P2 in range(len(TDM[Settings])) ]


	# Now we execute the expression, which generates a list containing non-repeating combinations of
	# our policy settings for each enabled policy.  Since we are inside a function, we need to give the
	# resulting variable global scope, so we pass globals() as the second argument to exec().  See the
	# Python 3 documentation for more details.
	exec(ExpressionToBuildList, globals())

	# Now we have created a list called "PolicySettingCombinations" which contains values such as
	# (if three policies, which each have three possible settings, are enabled):
	# [(0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 1, 0), (0, 1, 1), (0, 1, 2), (0, 2, 0)... (2, 2, 2)]
	
	return PolicySettingCombinations


def BuildIndividualPoliciesSettingList():
	
	CurrentPackageSettings = []
	for PolicyNum in Policies:
		CurrentPackageSettings.append(0) # We add a number of zeroes to the BAU package equal to the number of policies in the package
	
	PolicySettingCombinations = []
	PolicySettingCombinations.append(CurrentPackageSettings)
	
	for Policy in Policies:
		for Setting in range(1, len(Policy[Settings])): # We start at 1 because we don't need to repeat (0, 0, ... 0) for each policy.
			CurrentPackageSettings = [] # We have to empty and rebuild this list for each setting rather than overwriting
										# the last setting's value because Python's pass-by-object-reference paradigm
										# causes it to update the item we already appended to PolicySettingCombinations
										# along with the update to CurrentPackageSettings.
			for PolicyNum in Policies:
				CurrentPackageSettings.append(0) # We add a number of zeroes to each package equal to the number of policies
												 # in the package
			CurrentPackageSettings[Policies.index(Policy)] = Setting
			PolicySettingCombinations.append(CurrentPackageSettings)
	
	return PolicySettingCombinations


# We invoke the function that corresponds to the setting the user selected for the
# "IndividualPoliciesOnly" variable.  If no policies were enabled, we instead produce
# an error and exit.  (We write the error to the text file, because many users won't
# be using a console and won't see the message produced by sys.exit().
# Lastly, since the two modes should be identical when only a single policy is enabled,
# but Combinations mode fails because the policy settings are lists of ints rather than
# lists of lists, we cause the IndividualPoliciesOnly function to handle this particular
# case.

if len(Policies) < 1:
	f = open(OutputScript, 'w')
	ErrorMessage = "Error: No policies were enabled in the Python script.  Before running the script, you must enable at least one policy."
	f.write(ErrorMessage)
	f.close()
	import sys
	sys.exit(ErrorMessage)
elif IndividualPoliciesOnly or len(Policies) == 1:
	PolicySettingCombinations = BuildIndividualPoliciesSettingList()
else:
	PolicySettingCombinations = BuildPolicyCombinationsSettingsList()


# Generate Vensim Command Script
# ------------------------------
# We begin by creating a new file to serve as the Vensim command script (overwriting
# any older version at that filename).  We then tell Vensim to load
# the model file, and we give it a RUNNAME that will be used for all runs.  (It is
# overwritten each run, and the Vensim command file generated by this script
# always contains multiple runs, unless you only have one enabled policy and one
# setting value for that policy.)
f = open(OutputScript, 'w')
f.write('SPECIAL>LOADMODEL|"' + ModelFile + '"\n')
f.write("SIMULATE>RUNNAME|" + RunName + "\n")

# The following options may be useful in certain cases, but they cause Vensim to
# produce an output window for each simulation that acknowledges the completion of
# the command.  These output windows accumulate over the course of many runs and
# cause slow-downs (and potentially crashes).  Therefore, these lines are usually
# best left commented out, unless you are doing only a few runs.
# f.write("SPECIAL>NOINTERACTION\n")
# f.write("SIMULATE>SAVELIST|" + OutputVarsFile + "\n")
f.write("\n")

# Only for the first entry in the TSV file, we wish to include the "Time" row and
# overwrite any existing TSV file of that name.  Other entries append to the TSV file.
FirstEntryDone = False

# We track a run number, so that we can number the runs in the output file (because
# each run will have multiple rows- one for each output variable).
CurrentRunNumber = 1

# We need a single run of Vensim for each PolicySettingCombination.  We start by clearing
# any policy changes from old runs by reading the NoPolicies.cin file.
# Then, each run must have one SIMULATE>SETVAL instruction for each enabled policy.
# The most complex details here are the bits that look up the values of the settings
# for each policy.  We next array references- for example, "Policies[ActivePolicy]"
# refers to a single policy, which is itself a list.  Therefore, to reference an element
# of that list, we add another bracketed clause to the right, such as "[LongName]" if
# we want the long name text string for that policy.
for PolicySettingCombination in PolicySettingCombinations:
	
	for ActivePolicy in range(len(Policies)):	
		f.write("SIMULATE>SETVAL|" + Policies[ActivePolicy][LongName] + "=" + str(Policies[ActivePolicy][Settings][PolicySettingCombination[ActivePolicy]]) + "\n")
	
	# We add a RUN instruction now that we've added all the SETVAL instructions.
	f.write("MENU>RUN|O\n")
	
	# Lastly, we copy the results from the .vdf file generated by Vensim to a TSV file.
	# The complexity of this section is partly due to Vensim's required syntax for the
	# VDF2TAB function.  Please see the page on that function in the Vensim reference
	# manual for details.  But the general idea is that at the end (after the series of
	# vertical bars), we can add columns for arbitrary text, and we use this functionality
	# to add entries to the spreadsheet showing what policy settings were used for this run.
	# Then we add blank columns if we haven't added enough policy columns to satisfy the
	# MinPolicyCols setting.
	if FirstEntryDone:
		f.write("MENU>VDF2TAB|" + RunName + ".vdf|" + RunResultsFile + "|" + OutputVarsFile + "|+!||||:")
	else:
		f.write("MENU>VDF2TAB|" + RunName + ".vdf|" + RunResultsFile + "|" + OutputVarsFile + "|||||:")
		FirstEntryDone = True
	f.write(RunName)
	f.write("\tCurrentRunNumber=" + str(CurrentRunNumber))
	CurrentRunNumber += 1
	PolicyCols = 0
	for Policy in Policies:
		f.write("\t" + Policy[ShortName] + "=" + str(Policy[Settings][PolicySettingCombination[Policies.index(Policy)]]))
		PolicyCols += 1
	ExtraCols = max(0, MinPolicyCols - PolicyCols)
	for Cols in range(0, ExtraCols):
		f.write("\t")
	f.write("\n\n")

# We are done writing the Vensim command script and therefore close the file.
f.close()
