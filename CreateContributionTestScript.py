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
ModelFile = "EPS.mdl" # The name of the Vensim model file (typically with .mdl or .vpm extension)
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
ElecPsgrLDVs = (False,"Percent Nonelec Vehicles Shifted to Elec[passenger,LDVs]","ElecPsgrLDVs",[0,1],1)
ElecPsgrHDVs = (False,"Percent Nonelec Vehicles Shifted to Elec[passenger,HDVs]","ElecPsgrHDVs",[0,1],2)
Feebate = (False,"LDVs Feebate Rate","Feebate",[0,2000],3)
FuelEconLDVs = (False,"Percentage Additional Improvement of Fuel Economy Std[LDVs]","FuelEconLDVs",[0,1],4)
FuelEconHDVs = (False,"Percentage Additional Improvement of Fuel Economy Std[HDVs]","FuelEconHDVs",[0,.66],5)
TDM = (False,"Fraction of TDM Package Implemented","TDM",[0,1],6)

# Buildings and Appliances Sector Policies
RebateHeating = (False,"Boolean Rebate Program for Efficient Components[heating]","RebateHeating",[0,1],7)
RebateCooling = (False,"Boolean Rebate Program for Efficient Components[cooling and ventilation]","RebateCooling",[0,1],8)
RebateAppliances = (False,"Boolean Rebate Program for Efficient Components[appliances]","RebateAppliances",[0,1],9)
BldgStdsUrbResHeating = (False,"Reduction in E Use Allowed by Component Eff Std[heating,urban residential]","BldgStdsUrbResHeating",[0,.22],10)
BldgStdsUrbResCooling = (False,"Reduction in E Use Allowed by Component Eff Std[cooling and ventilation,urban residential]","BldgStdsUrbResCooling",[0,.38],11)
BldgStdsUrbResEnvelope = (False,"Reduction in E Use Allowed by Component Eff Std[envelope,urban residential]","BldgStdsUrbResEnvelope",[0,.38],12)
BldgStdsUrbResLighting = (False,"Reduction in E Use Allowed by Component Eff Std[lighting,urban residential]","BldgStdsUrbResLighting",[0,.40],13)
BldgStdsUrbResAppliances = (False,"Reduction in E Use Allowed by Component Eff Std[appliances,urban residential]","BldgStdsUrbResAppliances",[0,.38],14)
BldgStdsUrbResOther = (False,"Reduction in E Use Allowed by Component Eff Std[other component,urban residential]","BldgStdsUrbResOther",[0,.11],15)
BldgStdsRurResHeating = (False,"Reduction in E Use Allowed by Component Eff Std[heating,rural residential]","BldgStdsRurResHeating",[0,.22],16)
BldgStdsRurResCooling = (False,"Reduction in E Use Allowed by Component Eff Std[cooling and ventilation,rural residential]","BldgStdsRurResCooling",[0,.38],17)
BldgStdsRurResEnvelope = (False,"Reduction in E Use Allowed by Component Eff Std[envelope,rural residential]","BldgStdsRurResEnvelope",[0,.38],18)
BldgStdsRurResLighting = (False,"Reduction in E Use Allowed by Component Eff Std[lighting,rural residential]","BldgStdsRurResLighting",[0,.40],19)
BldgStdsRurResAppliances = (False,"Reduction in E Use Allowed by Component Eff Std[appliances,rural residential]","BldgStdsRurResAppliances",[0,.38],20)
BldgStdsRurResOther = (False,"Reduction in E Use Allowed by Component Eff Std[other component,rural residential]","BldgStdsRurResOther",[0,.11],21)
BldgStdsComHeating = (False,"Reduction in E Use Allowed by Component Eff Std[heating,commercial]","BldgStdsComHeating",[0,.22],22)
BldgStdsComCooling = (False,"Reduction in E Use Allowed by Component Eff Std[cooling and ventilation,commercial]","BldgStdsComCooling",[0,.38],23)
BldgStdsComEnvelope = (False,"Reduction in E Use Allowed by Component Eff Std[envelope,commercial]","BldgStdsComEnvelope",[0,.38],24)
BldgStdsComLighting = (False,"Reduction in E Use Allowed by Component Eff Std[lighting,commercial]","BldgStdsComLighting",[0,.40],25)
BldgStdsComAppliances = (False,"Reduction in E Use Allowed by Component Eff Std[appliances,commercial]","BldgStdsComAppliances",[0,.38],26)
BldgStdsComOther = (False,"Reduction in E Use Allowed by Component Eff Std[other component,commercial]","BldgStdsComOther",[0,.11],27)
ImprovedLabeling = (False,"Boolean Improved Device Labeling","ImprovedLabeling",[0,1],28)
ContractorEdu = (False,"Boolean Improved Contractor Edu and Training","ContractorEdu",[0,1],29)
ElecCpntUrbRes = (False,"Percent New Nonelec Component Sales Shifted to Elec[urban residential]","ElecCpntUrbRes",[0,1],30)
ElecCpntRurRes = (False,"Percent New Nonelec Component Sales Shifted to Elec[rural residential]","ElecCpntRurRes",[0,1],31)
ElecCpntCom = (False,"Percent New Nonelec Component Sales Shifted to Elec[commercial]","ElecCpntCom",[0,1],32)
RetrofittingHeating = (False,"Fraction of Commercial Components Replaced Annually due to Retrofitting Policy[heating]","RetrofittingHeating",[0,.034],33)
RetrofittingCooling = (False,"Fraction of Commercial Components Replaced Annually due to Retrofitting Policy[cooling and ventilation]","RetrofittingCooling",[0,.034],34)
RetrofittingEnvelope = (False,"Fraction of Commercial Components Replaced Annually due to Retrofitting Policy[envelope]","RetrofittingEnvelope",[0,.034],35)
RetrofittingLighting = (False,"Fraction of Commercial Components Replaced Annually due to Retrofitting Policy[lighting]","RetrofittingLighting",[0,.034],36)
RetrofittingAppliances = (False,"Fraction of Commercial Components Replaced Annually due to Retrofitting Policy[appliances]","RetrofittingAppliances",[0,.034],37)
RetrofittingOther = (False,"Fraction of Commercial Components Replaced Annually due to Retrofitting Policy[other component]","RetrofittingOther",[0,.034],38)
DistSolarCarveOut = (False,"Min Fraction of Total Elec Demand to be Met by Distributed Solar PV","DistSolarCarveOut",[0,.24],39)
DistSolarSubsidy = (False,"Perc Subsidy for Distributed Solar PV Capacity","DistSolarSubsidy",[0,.5],40)

# Electricity Supply Sector Policies
RPS = (False,"Additional Renewable Portfolio Std Percentage","RPS",[0,.88],41)
DemandResponse = (False,"Fraction of Additional Demand Response Potential Achieved","DemandResponse",[0,1],42)
SubsidyNuclear = (False,"Subsidy for Elec Production by Fuel[nuclear es]","SubsidyNuclear",[0,60],43)
SubsidyWind = (False,"Subsidy for Elec Production by Fuel[wind es]","SubsidyWind",[0,60],44)
SubsidySolarPV = (False,"Subsidy for Elec Production by Fuel[solar PV es]","SubsidySolarPV",[0,60],45)
SubsidySolarTherm = (False,"Subsidy for Elec Production by Fuel[solar thermal es]","SubsidySolarTherm",[0,60],46)
SubsidyBiomass = (False,"Subsidy for Elec Production by Fuel[biomass es]","SubsidyBiomass",[0,60],47)
EarlyRetCoal = (False,"Annual Additional Capacity Retired due to Early Retirement Policy[coal es]","EarlyRetCoal",[0,10000],48)
EarlyRetNuclear = (False,"Annual Additional Capacity Retired due to Early Retirement Policy[nuclear es]","EarlyRetNuclear",[0,10000],49)
LifeExtNuclear = (False,"Generation Capacity Lifetime Extension[nuclear es]","LifeExtNuclear",[0,20],50)
GridStorage = (False,"Additional Battery Storage Annual Growth Percentage","GridStorage",[0,.16],51)
TransmissionGrowth = (False,"Percentage Increase in Transmission Capacity vs BAU","TransmissionGrowth",[0,1.13],52)
ReduceTnDLoss = (False,"Percentage TnD Losses Avoided","ReduceTnDLoss",[0,.4],53)
RedDowntimeNGPreRet = (False,"Percentage Reduction in Plant Downtime[natural gas nonpeaker es,preexisting retiring]","RedDowntimeNGPreRet",[0,.6],54)
RedDowntimeWindNew = (False,"Percentage Reduction in Plant Downtime[wind es,newly built]","RedDowntimeWindNew",[0,.25],55)
RedDowntimeSolarPVNew = (False,"Percentage Reduction in Plant Downtime[solar PV es,newly built]","RedDowntimeSolarPVNew",[0,.3],56)
ChngElecImports = (False,"Percent Change in Electricity Imports","ChngElecImports",[0,1],57)
ChngElecExports = (False,"Percent Change in Electricity Exports","ChngElecExports",[0,1],58)
BanNewCoal = (False,"Boolean Ban New Power Plants[coal es]","BanNewCoal",[0,1],59)
BanNewNGNonpeaker = (False,"Boolean Ban New Power Plants[natural gas nonpeaker es]","BanNewNGNonpeaker",[0,1],60)
BanNewNuclear = (False,"Boolean Ban New Power Plants[nuclear es]","BanNewNuclear",[0,1],61)
BanNewHydro = (False,"Boolean Ban New Power Plants[hydro es]","BanNewHydro",[0,1],62)

# Industrial (Non-Agriculture) Sector Policies
ReduceFGases = (False,"Fraction of CO2e from Vented Byproduct Gasses Avoided","ReduceFGases",[0,1],63)
MethaneDestr = (False,"Fraction of Methane Destruction Opportunities Achieved","MethaneDestr",[0,1],64)
WorkerTraining = (False,"Fraction of Addressable Process Emissions Avoided via Worker Training","WorkerTraining",[0,1],65)
ClinkerSubst = (False,"Fraction of Cement Clinker Substitution Made","ClinkerSubst",[0,1],66)
MethaneCapture = (False,"Fraction of Methane Capture Opportunities Achieved","MethaneCapture",[0,1],67)
EarlyRetIndustry = (False,"Fraction of Energy Savings from Early Facility Retirement Achieved","EarlyRetIndustry",[0,1],68)
ImprSystemDesign = (False,"Fraction of Installation and System Integration Issues Remedied","ImprSystemDesign",[0,1],69)
CogenWasteHeat = (False,"Fraction of Potential Cogeneration and Waste Heat Recovery Adopted","CogenWasteHeat",[0,1],70)
IndstSwitchFromCoal = (False,"Fraction of Coal Use Converted to Other Fuels","IndstSwitchFromCoal",[0,.25],71)
IndstSwitchFromNG = (False,"Fraction of Natural Gas Use Converted to Other Fuels","IndstSwitchFromNG",[0,.25],72)
IndstEffStdsCement = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[cement and other carbonates]","IndstEffStdsCement",[0,.08],73)
IndstEffStdsNGPS = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[natural gas and petroleum systems]","IndstEffStdsNGPS",[0,.08],74)
IndstEffStdsIronSteel = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[iron and steel]","IndstEffStdsIronSteel",[0,.08],75)
IndstEffStdsChemicals = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[chemicals]","IndstEffStdsChemicals",[0,.08],76)
IndstEffStdsMining = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[mining]","IndstEffStdsMining",[0,.08],77)
IndstEffStdsWasteMgmt = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[waste management]","IndstEffStdsWasteMgmt",[0,.08],78)
IndstEffStdsAg = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[agriculture]","IndstEffStdsAg",[0,.08],79)
IndstEffStdsOtherInd = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other industries]","IndstEffStdsOtherInd",[0,.08],80)

# Agriculture, Land Use, and Forestry Policies
CroplandMgmt = (False,"Fraction of Abatement from Cropland Management Achieved","CroplandMgmt",[0,1],81)
RiceCultivMeasures = (False,"Fraction of Abatement from Rice Cultivation Measures Achieved","RiceCultivMeasures",[0,1],82)
LivestockMeasures = (False,"Fraction of Abatement from Livestock Measures Achieved","LivestockMeasures",[0,1],83)
SetAsides = (False,"Fraction of Abatement from Forest Set Asides Achieved","SetAsides",[0,1],84)
AfforestAndReforest = (False,"Fraction of Abatement from Afforestation and Reforestation Achieved","AfforestAndReforest",[0,.45],85)
ImprForestMgmt = (False,"Fraction of Abatement from Improved Forest Management Achieved","ImprForestMgmt",[0,1],86)

# District Heat Policies
ConvertNonCHPHeat = (False,"Fraction of Non CHP Heat Production Converted to CHP","ConvertNonCHPHeat",[0,1],87)
HeatSwitchFromCoal = (False,"Fraction of District Heat Coal Use Converted to Other Fuels","HeatSwitchFromCoal",[0,1],88)

# Cross-Sector Policies
CarbonTaxTrans = (False,"Carbon Tax[transportation sector]","CarbonTaxTrans",[0,300],89)
CarbonTaxElec = (False,"Carbon Tax[electricity sector]","CarbonTaxElec",[0,300],90)
CarbonTaxResBldg = (False,"Carbon Tax[residential buildings sector]","CarbonTaxResBldg",[0,300],91)
CarbonTaxComBldg = (False,"Carbon Tax[commercial buildings sector]","CarbonTaxComBldg",[0,300],92)
CarbonTaxIndst = (False,"Carbon Tax[industry sector]","CarbonTaxIndst",[0,300],93)
CCSGrowth = (False,"Fraction of Potential Additional CCS Achieved","CCSGrowth",[0,1],94)
FuelTaxElec = (False,"Additional Fuel Tax Rate by Fuel[electricity]","FuelTaxElec",[0,.2],95)
FuelTaxCoal = (False,"Additional Fuel Tax Rate by Fuel[coal]","FuelTaxCoal",[0,.2],96)
FuelTaxNatGas = (False,"Additional Fuel Tax Rate by Fuel[natural gas]","FuelTaxNatGas",[0,.2],97)
FuelTaxPetGas = (False,"Additional Fuel Tax Rate by Fuel[petroleum gasoline]","FuelTaxPetGas",[0,.2],98)
FuelTaxPetDies = (False,"Additional Fuel Tax Rate by Fuel[petroleum diesel]","FuelTaxPetDies",[0,.2],99)
RmvBAUSubsidiesCoal = (False,"Percent Reduction in BAU Subsidies[coal]","RmvBAUSubsidiesCoal",[0,1],100)
RmvBAUSubsidiesNatGas = (False,"Percent Reduction in BAU Subsidies[natural gas]","RmvBAUSubsidiesNatGas",[0,1],101)
RmvBAUSubsidiesNucl = (False,"Percent Reduction in BAU Subsidies[nuclear]","RmvBAUSubsidiesNucl",[0,1],102)
RmvBAUSubsidiesSolar = (False,"Percent Reduction in BAU Subsidies[solar]","RmvBAUSubsidiesSolar",[0,1],103)
RmvBAUSubsidiesPetGas = (False,"Percent Reduction in BAU Subsidies[petroleum gasoline]","RmvBAUSubsidiesPetGas",[0,1],104)
RmvBAUSubsidiesPetDies = (False,"Percent Reduction in BAU Subsidies[petroleum diesel]","RmvBAUSubsidiesPetDies",[0,1],105)

# Building the Policy List
# ------------------------
# Every policy, whether enabled or not, appears on a list below called "PotentialPolicies".
# Now we construct the actual list of policies to be included (named "Policies") by
# checking which of the policies have been enabled.
PotentialPolicies = (ElecPsgrLDVs, ElecPsgrHDVs, Feebate, FuelEconLDVs, FuelEconHDVs, TDM, RebateHeating, RebateCooling, RebateAppliances, BldgStdsUrbResHeating, BldgStdsUrbResCooling, BldgStdsUrbResEnvelope, BldgStdsUrbResLighting, BldgStdsUrbResAppliances, BldgStdsUrbResOther, BldgStdsRurResHeating, BldgStdsRurResCooling, BldgStdsRurResEnvelope, BldgStdsRurResLighting, BldgStdsRurResAppliances, BldgStdsRurResOther, BldgStdsComHeating, BldgStdsComCooling, BldgStdsComEnvelope, BldgStdsComLighting, BldgStdsComAppliances, BldgStdsComOther, ImprovedLabeling, ContractorEdu, ElecCpntUrbRes, ElecCpntRurRes, ElecCpntCom, RetrofittingHeating, RetrofittingCooling, RetrofittingEnvelope, RetrofittingLighting, RetrofittingAppliances, RetrofittingOther, DistSolarCarveOut, DistSolarSubsidy, RPS, DemandResponse, SubsidyNuclear, SubsidyWind, SubsidySolarPV, SubsidySolarTherm, SubsidyBiomass, EarlyRetCoal, EarlyRetNuclear, LifeExtNuclear, GridStorage, TransmissionGrowth, ReduceTnDLoss, RedDowntimeNGPreRet, RedDowntimeWindNew, RedDowntimeSolarPVNew, ChngElecImports, ChngElecExports, BanNewCoal, BanNewNGNonpeaker, BanNewNuclear, BanNewHydro, ReduceFGases, MethaneDestr, WorkerTraining, ClinkerSubst, MethaneCapture, EarlyRetIndustry, ImprSystemDesign, CogenWasteHeat, IndstSwitchFromCoal, IndstSwitchFromNG, IndstEffStdsCement, IndstEffStdsNGPS, IndstEffStdsIronSteel, IndstEffStdsChemicals, IndstEffStdsMining, IndstEffStdsWasteMgmt, IndstEffStdsAg, IndstEffStdsOtherInd, CroplandMgmt, RiceCultivMeasures, LivestockMeasures, SetAsides, AfforestAndReforest, ImprForestMgmt, ConvertNonCHPHeat, HeatSwitchFromCoal, CarbonTaxTrans, CarbonTaxElec, CarbonTaxResBldg, CarbonTaxComBldg, CarbonTaxIndst, CCSGrowth, FuelTaxElec, FuelTaxCoal, FuelTaxNatGas, FuelTaxPetGas, FuelTaxPetDies, RmvBAUSubsidiesCoal, RmvBAUSubsidiesNatGas, RmvBAUSubsidiesNucl, RmvBAUSubsidiesSolar, RmvBAUSubsidiesPetGas, RmvBAUSubsidiesPetDies)
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