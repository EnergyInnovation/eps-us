# CreateContributionTestScript.py
#
# Developed by Jeffrey Rissman
#
# This is a Python script that is used to generate a Vensim command script.
# The Vensim command script will perform one run with all enabled policies
# and one run with each defined subset (or "group") within the set of enabled
# policies turned off or turned on (depending on a user setting in this script).


# File Names
# ----------
# Rather than including input and output file names in the code below, we assign all the file
# names to variables in this section.  This allows the names to be easily changed if desired.
ModelFile = "EPS-beta.mdl" # The name of the Vensim model file (typically with .mdl or .vpm extension)
OutputScript = "GeneratedContributionTestScript.cmd" # The desired filename of the Vensim command script to be generated
RunResultsFile = "ContributionTestResults.tsv" # The desired filename for TSV file containing model run results
OutputVarsFile = "OutputVarsToExport.lst" # The name of the file containing a list of variables to be included in the RunResultsFile
                                          # May optionally also be used as a SAVELIST for Vensim (see below)

# Other Settings
# --------------
RunName = "MostRecentRun" # The desired name for all runs performed.  Used as the filename for the VDF files that Vensim creates
EnableOrDisableGroups = "Enable" # Should each group be enabled or disabled in turn?
								 # Essentially, this is testing either the contribution of a group in the proximity of the
								 # BAU case ("Enable") or in the proximity of a scenario defined in the non-zero values of
								 # the policies listed below ("Disable").


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
Group = 4


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
# The fifth entry in each policy is its group number.  By default, each policy has its
# own group number.  Change these numbers so multiple policies share a group number (or a
# group name in quotes, like "financial policies") to cause them to be enabled or disabled
# together.

# Transportation Sector Policies
ElecPsgrLDVs = (False,"Percent Nonelec Vehicles Shifted to Elec by End Year[passenger,LDVs]","ElecPsgrLDVs",[0,.11,.32],1)
ElecPsgrHDVs = (False,"Percent Nonelec Vehicles Shifted to Elec by End Year[passenger,HDVs]","ElecPsgrHDVs",[0,.06,.19],2)
Feebate = (False,"LDVs Feebate Rate","Feebate",[0,48500,145500],3)
FuelEconLDVs = (False,"Percentage Additional Improvement of Fuel Economy Std by End Year[LDVs]","FuelEconLDVs",[0,.23,.7],4)
FuelEconHDVs = (False,"Percentage Additional Improvement of Fuel Economy Std by End Year[HDVs]","FuelEconHDVs",[0,.3,.91],5)
TDM = (False,"Fraction of TDM Package Implemented by End Year","TDM",[0,.25,.75],6)

# Buildings and Appliances Sector Policies
RebateResHeating = (False,"Boolean Rebate Program for Efficient Components[residential,heating]","RebateResHeating",[0,1],7)
RebateResCooling = (False,"Boolean Rebate Program for Efficient Components[residential,cooling and ventilation]","RebateResCooling",[0,1],8)
RebateResAppliances = (False,"Boolean Rebate Program for Efficient Components[residential,appliances]","RebateResAppliances",[0,1],9)
ComponentStdsHeating = (False,"Reduction in E Use Allowed by Component Eff Std by End Year[heating]","ComponentStdsHeating",[0,.12,.36],10)
ComponentStdsCooling = (False,"Reduction in E Use Allowed by Component Eff Std by End Year[cooling and ventilation]","ComponentStdsCooling",[0,.12,.36],11)
ComponentStdsEnvelope = (False,"Reduction in E Use Allowed by Component Eff Std by End Year[envelope]","ComponentStdsEnvelope",[0,.12,.36],12)
ComponentStdsLighting = (False,"Reduction in E Use Allowed by Component Eff Std by End Year[lighting]","ComponentStdsLighting",[0,.12,.36],13)
ComponentStdsAppliances = (False,"Reduction in E Use Allowed by Component Eff Std by End Year[appliances]","ComponentStdsAppliances",[0,.12,.36],14)
ComponentStdsOther = (False,"Reduction in E Use Allowed by Component Eff Std by End Year[other component]","ComponentStdsOther",[0,.12,.36],15)
ImprovedLabeling = (False,"Boolean Improved Device Labeling","ImprovedLabeling",[0,1],16)
ContractorEdu = (False,"Boolean Improved Contractor Edu and Training","ContractorEdu",[0,1],17)
ElecBldgCpnt = (False,"Percent New Nonelec Component Sales Shifted to Elec by End Year","ElecBldgCpnt",[0,.09,.26],18)
RetrofittingHeating = (False,"Fraction of Components Replaced Annually due to Retrofitting Policy[heating]","RetrofittingHeating",[0,.01,.04],19)
RetrofittingCooling = (False,"Fraction of Components Replaced Annually due to Retrofitting Policy[cooling and ventilation]","RetrofittingCooling",[0,.01,.04],20)
RetrofittingEnvelope = (False,"Fraction of Components Replaced Annually due to Retrofitting Policy[envelope]","RetrofittingEnvelope",[0,.01,.04],21)
RetrofittingLighting = (False,"Fraction of Components Replaced Annually due to Retrofitting Policy[lighting]","RetrofittingLighting",[0,.01,.04],22)
RetrofittingAppliances = (False,"Fraction of Components Replaced Annually due to Retrofitting Policy[appliances]","RetrofittingAppliances",[0,.01,.04],23)
RetrofittingOther = (False,"Fraction of Components Replaced Annually due to Retrofitting Policy[other component]","RetrofittingOther",[0,.01,.04],24)

# Electricity Supply Sector Policies
RPS = (False,"Renewable Portfolio Std Percentage in End Year","RPS",[0,.13,.39],25)
DemandResponse = (False,"Fraction of Additional Demand Response Potential Achieved","DemandResponse",[0,.25,.75],26)
SubsidyCoal = (False,"Subsidy for Elec Production by Fuel[coal es]","SubsidyCoal",[0,13.5,40.5],27)
SubsidyNatGas = (False,"Subsidy for Elec Production by Fuel[natural gas es]","SubsidyNatGas",[0,13.5,40.5],28)
SubsidyNuclear = (False,"Subsidy for Elec Production by Fuel[nuclear es]","SubsidyNuclear",[0,13.5,40.5],29)
SubsidyHydro = (False,"Subsidy for Elec Production by Fuel[hydro es]","SubsidyHydro",[0,13.5,40.5],30)
SubsidyWind = (False,"Subsidy for Elec Production by Fuel[wind es]","SubsidyWind",[0,13.5,40.5],31)
SubsidySolarPV = (False,"Subsidy for Elec Production by Fuel[solar PV es]","SubsidySolarPV",[0,13.5,40.5],32)
SubsidySolarTherm = (False,"Subsidy for Elec Production by Fuel[solar thermal es]","SubsidySolarTherm",[0,13.5,40.5],33)
SubsidyBiomass = (False,"Subsidy for Elec Production by Fuel[biomass es]","SubsidyBiomass",[0,13.5,40.5],34)
EarlyRetCoal = (False,"Annual Additional Capacity Retired due to Early Retirement Policy[coal es]","EarlyRetCoal",[0,8519,25558],35)
EarlyRetNatGas = (False,"Annual Additional Capacity Retired due to Early Retirement Policy[natural gas es]","EarlyRetNatGas",[0,453,1358],36)
EarlyRetNuclear = (False,"Annual Additional Capacity Retired due to Early Retirement Policy[nuclear es]","EarlyRetNuclear",[0,145,435],37)
EarlyRetHydro = (False,"Annual Additional Capacity Retired due to Early Retirement Policy[hydro es]","EarlyRetHydro",[0,2654,7961],38)
LifeExtCoal = (False,"Generation Capacity Lifetime Extension[coal es]","LifeExtCoal",[0,5,15],39)
LifeExtNatGas = (False,"Generation Capacity Lifetime Extension[natural gas es]","LifeExtNatGas",[0,5,15],40)
LifeExtNuclear = (False,"Generation Capacity Lifetime Extension[nuclear es]","LifeExtNuclear",[0,5,15],41)
LifeExtHydro = (False,"Generation Capacity Lifetime Extension[hydro es]","LifeExtHydro",[0,5,15],42)
LifeExtWind = (False,"Generation Capacity Lifetime Extension[wind es]","LifeExtWind",[0,5,15],43)
LifeExtSolarPV = (False,"Generation Capacity Lifetime Extension[solar PV es]","LifeExtSolarPV",[0,5,15],44)
LifeExtSolarTherm = (False,"Generation Capacity Lifetime Extension[solar therm es]","LifeExtSolarTherm",[0,5,15],45)
LifeExtBiomass = (False,"Generation Capacity Lifetime Extension[biomass es]","LifeExtBiomass",[0,5,15],46)
MandatedCapConst = (False,"Boolean Use Non BAU Mandated Capacity Construction Schedule","MandatedCapConst",[0,1],47)
GridStorage = (False,"Additional Non Hydro Storage Annual Growth Percentage","GridStorage",[0,.009,.026],48)
ContractBasedDispatch = (False,"Boolean Use Contract Based Dispatch in Policy Case","ContractBasedDispatch",[0,1],49)
TransmissionGrowth = (False,"Percentage Increase in Transmission Capacity vs BAU by End Year","TransmissionGrowth",[0,.2,.5],50)

# Industrial Sector Policies
RedNonmethVent = (False,"Fraction of CO2e from Vented Byproduct Gasses Avoided by End Year","RedNonmethVent",[0,.25,.75],51)
MethaneDestr = (False,"Fraction of Methane Destruction Opportunities Achieved by End Year","MethaneDestr",[0,.25,.75],52)
WorkerTraining = (False,"Fraction of Addressable Process Emissions Avoided via Worker Training by End Year","WorkerTraining",[0,.25,.75],53)
ClinkerSubst = (False,"Fraction of Cement Clinker Substitution Made by End Year","ClinkerSubst",[0,.25,.75],54)
MethaneCapture = (False,"Fraction of Methane Capture Opportunities Achieved by End Year","MethaneCapture",[0,.25,.75],55)
EarlyRetIndustry = (False,"Fraction of Energy Savings from Early Facility Retirement Achieved","EarlyRetIndustry",[0,.33,1],56)
ImprSystemDesign = (False,"Fraction of Installation and System Integration Issues Remedied by End Year","ImprSystemDesign",[0,.33,1],57)
CogenWasteHeat = (False,"Fraction of Potential Cogeneration and Waste Heat Recovery Adopted by End Year","CogenWasteHeat",[0,.33,1],58)
IndstFuelSwitch = (False,"Fraction of Coal Use Converted to Other Fuels by End Year","IndstFuelSwitch",[0,.1,.31],59)
IndstEffStdsCement = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU by End Year[cement and other carbonates]","IndstEffStdsCement",[0,.05,.14],60)
IndstEffStdsNGPS = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU by End Year[natural gas and petroleum systems]","IndstEffStdsNGPS",[0,.05,.14],61)
IndstEffStdsIronSteel = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU by End Year[iron and steel]","IndstEffStdsIronSteel",[0,.05,.14],62)
IndstEffStdsChemicals = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU by End Year[chemicals]","IndstEffStdsChemicals",[0,.05,.14],63)
IndstEffStdsMining = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU by End Year[mining]","IndstEffStdsMining",[0,.05,.14],64)
IndstEffStdsWasteMgmt = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU by End Year[waste management]","IndstEffStdsWasteMgmt",[0,.05,.14],65)
IndstEffStdsOtherInd = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU by End Year[other industries]","IndstEffStdsOtherInd",[0,.05,.14],66)

# Cross-Sector Policies
CarbonTaxTrspt = (False,"Carbon Tax by End Year[transportation sector]","CarbonTaxTrspt",[0,17.5,52.5],67)
CarbonTaxElec = (False,"Carbon Tax by End Year[electricity sector]","CarbonTaxElec",[0,17.5,52.5],68)
CarbonTaxResBldg = (False,"Carbon Tax by End Year[residential buildings sector]","CarbonTaxResBldg",[0,17.5,52.5],69)
CarbonTaxComBldg = (False,"Carbon Tax by End Year[commercial buildings sector]","CarbonTaxComBldg",[0,17.5,52.5],70)
CarbonTaxIndst = (False,"Carbon Tax by End Year[industry sector]","CarbonTaxIndst",[0,17.5,52.5],71)
CCSGrowth = (False,"Fraction of Potential Additional CCS Achieved","CCSGrowth",[0,.33,1],72)
NonMarketElecPrice = (False,"Boolean Prevent Policies from Affecting Electricity Prices","NonMarketElecPrice",[0,1],73)
RmvBAUSubsidies = (False,"Percent Reduction in BAU Subsidies","RmvBAUSubsidies",[0,.33,1],74)
ConvertNonCHPHeat = (False,"Fraction of Non CHP Heat Production Converted to CHP by End Year","ConvertNonCHPHeat",[0,.1,.3],75)

FuelTaxTransElec = (False,"Additional Fuel Tax Rate by Fuel by End Year[electricity,transportation sector]","FuelTaxTransElec",[0,.04,.13],76)
FuelTaxTransNatGas = (False,"Additional Fuel Tax Rate by Fuel by End Year[natural gas,transportation sector]","FuelTaxTransNatGas",[0,.04,.13],77)
FuelTaxTransPetGas = (False,"Additional Fuel Tax Rate by Fuel by End Year[petroleum gasoline,transportation sector]","FuelTaxTransPetGas",[0,.04,.13],78)
FuelTaxTransPetDies = (False,"Additional Fuel Tax Rate by Fuel by End Year[petroleum diesel,transportation sector]","FuelTaxTransPetDies",[0,.04,.13],79)
FuelTaxTransBioGas = (False,"Additional Fuel Tax Rate by Fuel by End Year[biofuel gasoline,transportation sector]","FuelTaxTransBioGas",[0,.04,.13],80)
FuelTaxTransBioDies = (False,"Additional Fuel Tax Rate by Fuel by End Year[biofuel diesel,transportation sector]","FuelTaxTransBioDies",[0,.04,.13],81)
FuelTaxTransJetFuel = (False,"Additional Fuel Tax Rate by Fuel by End Year[jet fuel,transportation sector]","FuelTaxTransJetFuel",[0,.04,.13],82)

FuelTaxElecCoal = (False,"Additional Fuel Tax Rate by Fuel by End Year[coal,electricity sector]","FuelTaxElecCoal",[0,.04,.13],83)
FuelTaxElecNatGas = (False,"Additional Fuel Tax Rate by Fuel by End Year[natural gas,electricity sector]","FuelTaxElecNatGas",[0,.04,.13],84)
FuelTaxElecNuclear = (False,"Additional Fuel Tax Rate by Fuel by End Year[nuclear,electricity sector]","FuelTaxElecNuclear",[0,.04,.13],85)
FuelTaxElecBiomass = (False,"Additional Fuel Tax Rate by Fuel by End Year[biomass,electricity sector]","FuelTaxElecBiomass",[0,.04,.13],86)

FuelTaxBlgResElec = (False,"Additional Fuel Tax Rate by Fuel by End Year[electricity,residential buildings sector]","FuelTaxBlgResElec",[0,.04,.13],87)
FuelTaxBlgResCoal = (False,"Additional Fuel Tax Rate by Fuel by End Year[coal,residential buildings sector]","FuelTaxBlgResCoal",[0,.04,.13],88)
FuelTaxBlgResNatGas = (False,"Additional Fuel Tax Rate by Fuel by End Year[natural gas,residential buildings sector]","FuelTaxBlgResNatGas",[0,.04,.13],89)
FuelTaxBlgResPetDies = (False,"Additional Fuel Tax Rate by Fuel by End Year[petroleum diesel,residential buildings sector]","FuelTaxBlgResPetDies",[0,.04,.13],90)

FuelTaxBlgComElec = (False,"Additional Fuel Tax Rate by Fuel by End Year[electricity,commercial buildings sector]","FuelTaxBlgComElec",[0,.04,.13],91)
FuelTaxBlgComCoal = (False,"Additional Fuel Tax Rate by Fuel by End Year[coal,commercial buildings sector]","FuelTaxBlgComCoal",[0,.04,.13],92)
FuelTaxBlgComNatGas = (False,"Additional Fuel Tax Rate by Fuel by End Year[natural gas,commercial buildings sector]","FuelTaxBlgComNatGas",[0,.04,.13],93)
FuelTaxBlgComPetDies = (False,"Additional Fuel Tax Rate by Fuel by End Year[petroleum diesel,commercial buildings sector]","FuelTaxBlgComPetDies",[0,.04,.13],94)

FuelTaxIndElec = (False,"Additional Fuel Tax Rate by Fuel by End Year[electricity,industry sector]","FuelTaxIndElec",[0,.04,.13],95)
FuelTaxIndCoal = (False,"Additional Fuel Tax Rate by Fuel by End Year[coal,industry sector]","FuelTaxIndCoal",[0,.04,.13],96)
FuelTaxIndNatGas = (False,"Additional Fuel Tax Rate by Fuel by End Year[natural gas,industry sector]","FuelTaxIndNatGas",[0,.04,.13],97)
FuelTaxIndBiomass = (False,"Additional Fuel Tax Rate by Fuel by End Year[biomass,industry sector]","FuelTaxIndBiomass",[0,.04,.13],98)
FuelTaxIndPetDies = (False,"Additional Fuel Tax Rate by Fuel by End Year[petroleum diesel,industry sector]","FuelTaxIndPetDies",[0,.04,.13],99)


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


# Exit with an error if no policies were enabled in the script.  We write the error to the output
# file because it's likely a user will run this without a console and won't be able to see the
# message produced by sys.exit()
if len(Policies) < 1:
	f = open(OutputScript, 'w')
	ErrorMessage = "Error: No policies were enabled in the Python script.  Before running the script, you must enable at least one policy."
	f.write(ErrorMessage)
	f.close()
	import sys
	sys.exit(ErrorMessage)


# Building the Groups List
# ------------------------
# We create a list of all the unique groups that are used by enabled policies.
Groups = []
for Policy in Policies:
	if Policy[Group] not in Groups:
		Groups.append(Policy[Group])


# Generate Vensim Command Script
# ------------------------------
# We begin by creating a new file to serve as the Vensim command script (overwriting
# any older version at that filename).  We then tell Vensim to load
# the model file, and we give it a RUNNAME that will be used for all runs.  (It is
# overwritten each run.)
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

def PerformRunsWithEnabledGroups():

	# First, we do a run with all of the groups disabled
	f.write("MENU>RUN|O\n")
	f.write("MENU>VDF2TAB|" + RunName + ".vdf|" + RunResultsFile + "|" + OutputVarsFile + "|||||:")
	f.write("\tEnabledPolicyGroup=None")
	f.write("\tEnabledPolicies=None\n\n")

	# Next, we do a run with each group enabled in turn
	for EnabledGroup in Groups:

		# We create an empty string that we'll use to track the policies enabled in each group
		EnabledPolicies=""

		# We activate policies if their group name matches the currently enabled group
		for Policy in Policies:
			if Policy[Group] == EnabledGroup:
				f.write("SIMULATE>SETVAL|" + Policy[LongName] + "=" + str(Policy[Settings][1]) + "\n")
				# We add the policy to the EnabledPolicies string
				if len(EnabledPolicies) > 0:
					EnabledPolicies += ", "
				EnabledPolicies += Policy[ShortName]
		# We perform our run and log the output
		f.write("MENU>RUN|O\n")
		f.write("MENU>VDF2TAB|" + RunName + ".vdf|" + RunResultsFile + "|" + OutputVarsFile + "|+!||||:")
		f.write("\tEnabledPolicyGroup=" + str(EnabledGroup))
		f.write("\tEnabledPolicies=" + EnabledPolicies + "\n\n")

def PerformRunsWithDisabledGroups():

	# First, we do a run with all of the groups enabled
	for Policy in Policies:
		f.write("SIMULATE>SETVAL|" + Policy[LongName] + "=" + str(Policy[Settings][1]) + "\n")
	f.write("MENU>RUN|O\n")
	f.write("MENU>VDF2TAB|" + RunName + ".vdf|" + RunResultsFile + "|" + OutputVarsFile + "|||||:")
	f.write("\tDisabledPolicyGroup=None")
	f.write("\tDisabledPolicies=None\n\n")

	# Next, we do a run with each group disabled in turn
	for DisabledGroup in Groups:

		# We create an empty string that we'll use to track the policies disabled in each group
		DisabledPolicies=""

		# We activate policies if their group name does not match the currently disabled group
		for Policy in Policies:
			if Policy[Group] != DisabledGroup:
				f.write("SIMULATE>SETVAL|" + Policy[LongName] + "=" + str(Policy[Settings][1]) + "\n")
			# Otherwise, we add the policy to the DisabledPolicies string
			else:
				if len(DisabledPolicies) > 0:
					DisabledPolicies += ", "
				DisabledPolicies += Policy[ShortName]
		# We perform our run and log the output
		f.write("MENU>RUN|O\n")
		f.write("MENU>VDF2TAB|" + RunName + ".vdf|" + RunResultsFile + "|" + OutputVarsFile + "|+!||||:")
		f.write("\tDisabledPolicyGroup=" + str(DisabledGroup))
		f.write("\tDisabledPolicies=" + DisabledPolicies + "\n\n")

if EnableOrDisableGroups == "Enable":
	PerformRunsWithEnabledGroups()
else:
	PerformRunsWithDisabledGroups()

# We are done writing the Vensim command script and therefore close the file.
f.close()