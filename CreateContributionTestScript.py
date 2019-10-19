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
ElecPsgrLDVs = (False,"Percent Nonelec Vehicles Shifted to Elec[passenger,LDVs]","ElecPsgrLDVs",[0,.1],1)
ElecPsgrHDVs = (False,"Percent Nonelec Vehicles Shifted to Elec[passenger,HDVs]","ElecPsgrHDVs",[0,.1],2)
Feebate = (False,"LDVs Feebate Rate","Feebate",[0,1940],3)
FuelEconLDVs = (False,"Percentage Additional Improvement of Fuel Economy Std[LDVs]","FuelEconLDVs",[0,.22],4)
FuelEconHDVs = (False,"Percentage Additional Improvement of Fuel Economy Std[HDVs]","FuelEconHDVs",[0,.46],5)
TDM = (False,"Fraction of TDM Package Implemented","TDM",[0,1],6)

# Buildings and Appliances Sector Policies
RebateHeating = (False,"Boolean Rebate Program for Efficient Components[heating]","RebateHeating",[0,1],7)
RebateCooling = (False,"Boolean Rebate Program for Efficient Components[cooling and ventilation]","RebateCooling",[0,1],8)
RebateAppliances = (False,"Boolean Rebate Program for Efficient Components[appliances]","RebateAppliances",[0,1],9)
BldgStdsUrbResHeating = (False,"Reduction in E Use Allowed by Component Eff Std[heating,urban residential]","BldgStdsUrbResHeating",[0,.68],10)
BldgStdsUrbResCooling = (False,"Reduction in E Use Allowed by Component Eff Std[cooling and ventilation,urban residential]","BldgStdsUrbResCooling",[0,.68],11)
BldgStdsUrbResEnvelope = (False,"Reduction in E Use Allowed by Component Eff Std[envelope,urban residential]","BldgStdsUrbResEnvelope",[0,.68],12)
BldgStdsUrbResLighting = (False,"Reduction in E Use Allowed by Component Eff Std[lighting,urban residential]","BldgStdsUrbResLighting",[0,.68],13)
BldgStdsUrbResAppliances = (False,"Reduction in E Use Allowed by Component Eff Std[appliances,urban residential]","BldgStdsUrbResAppliances",[0,.68],14)
BldgStdsUrbResOther = (False,"Reduction in E Use Allowed by Component Eff Std[other component,urban residential]","BldgStdsUrbResOther",[0,.68],15)
BldgStdsRurResHeating = (False,"Reduction in E Use Allowed by Component Eff Std[heating,rural residential]","BldgStdsRurResHeating",[0,.68],116)
BldgStdsRurResCooling = (False,"Reduction in E Use Allowed by Component Eff Std[cooling and ventilation,rural residential]","BldgStdsRurResCooling",[0,.68],117)
BldgStdsRurResEnvelope = (False,"Reduction in E Use Allowed by Component Eff Std[envelope,rural residential]","BldgStdsRurResEnvelope",[0,.68],118)
BldgStdsRurResLighting = (False,"Reduction in E Use Allowed by Component Eff Std[lighting,rural residential]","BldgStdsRurResLighting",[0,.68],119)
BldgStdsRurResAppliances = (False,"Reduction in E Use Allowed by Component Eff Std[appliances,rural residential]","BldgStdsRurResAppliances",[0,.68],120)
BldgStdsRurResOther = (False,"Reduction in E Use Allowed by Component Eff Std[other component,rural residential]","BldgStdsRurResOther",[0,.68],121)
BldgStdsComHeating = (False,"Reduction in E Use Allowed by Component Eff Std[heating,commercial]","BldgStdsComHeating",[0,.68],122)
BldgStdsComCooling = (False,"Reduction in E Use Allowed by Component Eff Std[cooling and ventilation,commercial]","BldgStdsComCooling",[0,.68],123)
BldgStdsComEnvelope = (False,"Reduction in E Use Allowed by Component Eff Std[envelope,commercial]","BldgStdsComEnvelope",[0,.68],124)
BldgStdsComLighting = (False,"Reduction in E Use Allowed by Component Eff Std[lighting,commercial]","BldgStdsComLighting",[0,.68],125)
BldgStdsComAppliances = (False,"Reduction in E Use Allowed by Component Eff Std[appliances,commercial]","BldgStdsComAppliances",[0,.68],126)
BldgStdsComOther = (False,"Reduction in E Use Allowed by Component Eff Std[other component,commercial]","BldgStdsComOther",[0,.68],127)
ImprovedLabeling = (False,"Boolean Improved Device Labeling","ImprovedLabeling",[0,1],16)
ContractorEdu = (False,"Boolean Improved Contractor Edu and Training","ContractorEdu",[0,1],17)
ElecCpntUrbRes = (False,"Percent New Nonelec Component Sales Shifted to Elec[urban residential]","ElecCpntUrbRes",[0,.98],18)
ElecCpntRurRes = (False,"Percent New Nonelec Component Sales Shifted to Elec[rural residential]","ElecCpntRurRes",[0,.98],114)
ElecCpntCom = (False,"Percent New Nonelec Component Sales Shifted to Elec[commercial]","ElecCpntCom",[0,.98],115)
RetrofittingHeating = (False,"Fraction of Commercial Components Replaced Annually due to Retrofitting Policy[heating]","RetrofittingHeating",[0,.034],19)
RetrofittingCooling = (False,"Fraction of Commercial Components Replaced Annually due to Retrofitting Policy[cooling and ventilation]","RetrofittingCooling",[0,.034],20)
RetrofittingEnvelope = (False,"Fraction of Commercial Components Replaced Annually due to Retrofitting Policy[envelope]","RetrofittingEnvelope",[0,.034],21)
RetrofittingLighting = (False,"Fraction of Commercial Components Replaced Annually due to Retrofitting Policy[lighting]","RetrofittingLighting",[0,.034],22)
RetrofittingAppliances = (False,"Fraction of Commercial Components Replaced Annually due to Retrofitting Policy[appliances]","RetrofittingAppliances",[0,.034],23)
RetrofittingOther = (False,"Fraction of Commercial Components Replaced Annually due to Retrofitting Policy[other component]","RetrofittingOther",[0,.034],24)
DistSolarCarveOut = (False,"Min Fraction of Total Elec Demand to be Met by Distributed Solar PV","DistSolarCarveOut",[0,.04],25)
DistSolarSubsidy = (False,"Perc Subsidy for Distributed Solar PV Capacity","DistSolarSubsidy",[0,.5],26)

# Electricity Supply Sector Policies
RPS = (False,"Additional Renewable Portfolio Std Percentage","RPS",[0,.25],27)
DemandResponse = (False,"Fraction of Additional Demand Response Potential Achieved","DemandResponse",[0,1],28)
SubsidyNuclear = (False,"Subsidy for Elec Production by Fuel[nuclear es]","SubsidyNuclear",[0,35],29)
SubsidyWind = (False,"Subsidy for Elec Production by Fuel[wind es]","SubsidyWind",[0,35],30)
SubsidySolarPV = (False,"Subsidy for Elec Production by Fuel[solar PV es]","SubsidySolarPV",[0,35],31)
SubsidySolarTherm = (False,"Subsidy for Elec Production by Fuel[solar thermal es]","SubsidySolarTherm",[0,35],32)
SubsidyBiomass = (False,"Subsidy for Elec Production by Fuel[biomass es]","SubsidyBiomass",[0,35],33)
EarlyRetCoal = (False,"Annual Additional Capacity Retired due to Early Retirement Policy[coal es]","EarlyRetCoal",[0,10000],34)
EarlyRetNatGas = (False,"Annual Additional Capacity Retired due to Early Retirement Policy[natural gas nonpeaker es]","EarlyRetNatGas",[0,10000],35)
EarlyRetNuclear = (False,"Annual Additional Capacity Retired due to Early Retirement Policy[nuclear es]","EarlyRetNuclear",[0,10000],36)
EarlyRetHydro = (False,"Annual Additional Capacity Retired due to Early Retirement Policy[hydro es]","EarlyRetHydro",[0,10000],37)
LifeExtCoal = (False,"Generation Capacity Lifetime Extension[coal es]","LifeExtCoal",[0,20],38)
LifeExtNatGas = (False,"Generation Capacity Lifetime Extension[natural gas nonpeaker es]","LifeExtNatGas",[0,20],39)
LifeExtNuclear = (False,"Generation Capacity Lifetime Extension[nuclear es]","LifeExtNuclear",[0,20],40)
LifeExtHydro = (False,"Generation Capacity Lifetime Extension[hydro es]","LifeExtHydro",[0,20],41)
LifeExtWind = (False,"Generation Capacity Lifetime Extension[wind es]","LifeExtWind",[0,20],42)
LifeExtSolarPV = (False,"Generation Capacity Lifetime Extension[solar PV es]","LifeExtSolarPV",[0,20],43)
LifeExtSolarTherm = (False,"Generation Capacity Lifetime Extension[solar thermal es]","LifeExtSolarTherm",[0,20],44)
LifeExtBiomass = (False,"Generation Capacity Lifetime Extension[biomass es]","LifeExtBiomass",[0,20],45)
MandatedCapConst = (False,"Boolean Use Non BAU Mandated Capacity Construction Schedule","MandatedCapConst",[0,1],46)
GridStorage = (False,"Additional Non Hydro Storage Annual Growth Percentage","GridStorage",[0,.16],47)
ContractBasedDispatch = (False,"Boolean Use Contract Based Dispatch in Policy Case","ContractBasedDispatch",[0,1],48)
TransmissionGrowth = (False,"Percentage Increase in Transmission Capacity vs BAU","TransmissionGrowth",[0,.21],49)
ReduceTnDLoss = (False,"Percentage TnD Losses Avoided","ReduceTnDLoss",[0,.5],50)
RedDowntimeNGPreRet = (False,"Percentage Reduction in Plant Downtime[natural gas es,preexisting retiring]","RedDowntimeNGPreRet",[0,.6],53)
RedDowntimeWindNew = (False,"Percentage Reduction in Plant Downtime[wind es,newly built]","RedDowntimeWindNew",[0,.25],55)
RedDowntimeSolarPVNew = (False,"Percentage Reduction in Plant Downtime[solar PV es,newly built]","RedDowntimeSolarPVNew",[0,.3],56)
ChngElecImports = (False,"Percent Change in Electricity Imports","ChngElecImports",[0,1],57)
ChngElecExports = (False,"Percent Change in Electricity Exports","ChngElecExports",[0,1],58)

# Industrial Sector (Including Agriculture) Policies
RedNonmethVent = (False,"Fraction of CO2e from Vented Byproduct Gasses Avoided","RedNonmethVent",[0,1],59)
MethaneDestr = (False,"Fraction of Methane Destruction Opportunities Achieved","MethaneDestr",[0,1],60)
WorkerTraining = (False,"Fraction of Addressable Process Emissions Avoided via Worker Training","WorkerTraining",[0,1],61)
ClinkerSubst = (False,"Fraction of Cement Clinker Substitution Made","ClinkerSubst",[0,1],62)
MethaneCapture = (False,"Fraction of Methane Capture Opportunities Achieved","MethaneCapture",[0,1],63)
CroplandMgmt = (False,"Fraction of Abatement from Cropland Management Achieved","CroplandMgmt",[0,1],64)
RiceCultivMeasures = (False,"Fraction of Abatement from Rice Cultivation Measures Achieved","RiceCultivMeasures",[0,1],65)
LivestockMeasures = (False,"Fraction of Abatement from Livestock Measures Achieved","LivestockMeasures",[0,1],66)
EarlyRetIndustry = (False,"Fraction of Energy Savings from Early Facility Retirement Achieved","EarlyRetIndustry",[0,1],67)
ImprSystemDesign = (False,"Fraction of Installation and System Integration Issues Remedied","ImprSystemDesign",[0,1],68)
CogenWasteHeat = (False,"Fraction of Potential Cogeneration and Waste Heat Recovery Adopted","CogenWasteHeat",[0,1],69)
IndstFuelSwitch = (False,"Fraction of Coal Use Converted to Other Fuels","IndstFuelSwitch",[0,.17],70)
IndstEffStdsCement = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[cement and other carbonates]","IndstEffStdsCement",[0,.11],71)
IndstEffStdsNGPS = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[natural gas and petroleum systems]","IndstEffStdsNGPS",[0,.11],72)
IndstEffStdsIronSteel = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[iron and steel]","IndstEffStdsIronSteel",[0,.11],73)
IndstEffStdsChemicals = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[chemicals]","IndstEffStdsChemicals",[0,.11],74)
IndstEffStdsMining = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[mining]","IndstEffStdsMining",[0,.11],75)
IndstEffStdsWasteMgmt = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[waste management]","IndstEffStdsWasteMgmt",[0,.11],76)
IndstEffStdsAg = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[agriculture]","IndstEffStdsAg",[0,.11],77)
IndstEffStdsOtherInd = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other industries]","IndstEffStdsOtherInd",[0,.11],78)

# Land Use and Forestry Policies
SetAsides = (False,"Fraction of Abatement from Forest Set Asides Achieved","SetAsides",[0,.31],79)
AfforestAndReforest = (False,"Fraction of Abatement from Afforestation and Reforestation Achieved","AfforestAndReforest",[0,.45],80)
ImprForestMgmt = (False,"Fraction of Abatement from Improved Forest Management Achieved","ImprForestMgmt",[0,1],81)
AvoidDeforest = (False,"Fraction of Abatement from Avoided Deforestation Achieved","AvoidDeforest",[0,1],82)

# Cross-Sector Policies
CarbonTax = (False,"Carbon Tax","CarbonTax",[0,100],83)
CCSGrowth = (False,"Fraction of Potential Additional CCS Achieved","CCSGrowth",[0,1],84)
NonMarketElecPrice = (False,"Boolean Prevent Policies from Affecting Electricity Prices","NonMarketElecPrice",[0,1],85)
ConvertNonCHPHeat = (False,"Fraction of Non CHP Heat Production Converted to CHP","ConvertNonCHPHeat",[0,1],86)
FuelTaxElec = (False,"Additional Fuel Tax Rate by Fuel[electricity]","FuelTaxElec",[0,.2],87)
FuelTaxCoal = (False,"Additional Fuel Tax Rate by Fuel[coal]","FuelTaxCoal",[0,.2],88)
FuelTaxNatGas = (False,"Additional Fuel Tax Rate by Fuel[natural gas]","FuelTaxNatGas",[0,.2],89)
FuelTaxNuclear = (False,"Additional Fuel Tax Rate by Fuel[nuclear]","FuelTaxNuclear",[0,.2],90)
FuelTaxBiomass = (False,"Additional Fuel Tax Rate by Fuel[biomass]","FuelTaxBiomass",[0,.2],91)
FuelTaxPetGas = (False,"Additional Fuel Tax Rate by Fuel[petroleum gasoline]","FuelTaxPetGas",[0,.2],92)
FuelTaxPetDies = (False,"Additional Fuel Tax Rate by Fuel[petroleum diesel]","FuelTaxPetDies",[0,.2],93)
FuelTaxBioGas = (False,"Additional Fuel Tax Rate by Fuel[biofuel gasoline]","FuelTaxBioGas",[0,.2],94)
FuelTaxBioDies = (False,"Additional Fuel Tax Rate by Fuel[biofuel diesel]","FuelTaxBioDies",[0,.2],95)
FuelTaxJetFuel = (False,"Additional Fuel Tax Rate by Fuel[jet fuel]","FuelTaxJetFuel",[0,.2],96)
FuelTaxHeat = (False,"Additional Fuel Tax Rate by Fuel[heat]","FuelTaxHeat",[0,.2],97)
RmvBAUSubsidiesElec = (False,"Percent Reduction in BAU Subsidies[electricity]","RmvBAUSubsidiesElec",[0,1],98)
RmvBAUSubsidiesCoal = (False,"Percent Reduction in BAU Subsidies[coal]","RmvBAUSubsidiesCoal",[0,1],99)
RmvBAUSubsidiesNatGas = (False,"Percent Reduction in BAU Subsidies[natural gas]","RmvBAUSubsidiesNatGas",[0,1],100)
RmvBAUSubsidiesNucl = (False,"Percent Reduction in BAU Subsidies[nuclear]","RmvBAUSubsidiesNucl",[0,1],101)
RmvBAUSubsidiesHydro = (False,"Percent Reduction in BAU Subsidies[hydro]","RmvBAUSubsidiesHydro",[0,1],102)
RmvBAUSubsidiesWind = (False,"Percent Reduction in BAU Subsidies[wind]","RmvBAUSubsidiesWind",[0,1],103)
RmvBAUSubsidiesSolar = (False,"Percent Reduction in BAU Subsidies[solar]","RmvBAUSubsidiesSolar",[0,1],104)
RmvBAUSubsidiesBiom = (False,"Percent Reduction in BAU Subsidies[biomass]","RmvBAUSubsidiesBiom",[0,1],105)
RmvBAUSubsidiesPetGas = (False,"Percent Reduction in BAU Subsidies[petroleum gasoline]","RmvBAUSubsidiesPetGas",[0,1],106)
RmvBAUSubsidiesPetDies = (False,"Percent Reduction in BAU Subsidies[petroleum diesel]","RmvBAUSubsidiesPetDies",[0,1],107)
RmvBAUSubsidiesBioGas = (False,"Percent Reduction in BAU Subsidies[biofuel gasoline]","RmvBAUSubsidiesBioGas",[0,1],108)
RmvBAUSubsidiesBioDies = (False,"Percent Reduction in BAU Subsidies[biofuel diesel]","RmvBAUSubsidiesBioDies",[0,1],109)
RmvBAUSubsidiesJetFuel = (False,"Percent Reduction in BAU Subsidies[jet fuel]","RmvBAUSubsidiesJetFuel",[0,1],110)
RmvBAUSubsidiesHeat = (False,"Percent Reduction in BAU Subsidies[heat]","RmvBAUSubsidiesHeat",[0,1],111)

# Building the Policy List
# ------------------------
# Every policy, whether enabled or not, appears on a list below called "PotentialPolicies".
# Now we construct the actual list of policies to be included (named "Policies") by
# checking which of the policies have been enabled.
PotentialPolicies = (ElecPsgrLDVs, ElecPsgrHDVs, Feebate, FuelEconLDVs, FuelEconHDVs, TDM, RebateHeating, RebateCooling, RebateAppliances, BldgStdsUrbResHeating, BldgStdsUrbResCooling, BldgStdsUrbResEnvelope, BldgStdsUrbResLighting, BldgStdsUrbResAppliances, BldgStdsUrbResOther, BldgStdsRurResHeating, BldgStdsRurResCooling, BldgStdsRurResEnvelope, BldgStdsRurResLighting, BldgStdsRurResAppliances, BldgStdsRurResOther, BldgStdsComHeating, BldgStdsComCooling, BldgStdsComEnvelope, BldgStdsComLighting, BldgStdsComAppliances, BldgStdsComOther, ImprovedLabeling, ContractorEdu, ElecCpntUrbRes, ElecCpntRurRes, ElecCpntCom, RetrofittingHeating, RetrofittingCooling, RetrofittingEnvelope, RetrofittingLighting, RetrofittingAppliances, RetrofittingOther, DistSolarCarveOut, DistSolarSubsidy, RPS, DemandResponse, SubsidyNuclear, SubsidyWind, SubsidySolarPV, SubsidySolarTherm, SubsidyBiomass, EarlyRetCoal, EarlyRetNatGas, EarlyRetNuclear, EarlyRetHydro, LifeExtCoal, LifeExtNatGas, LifeExtNuclear, LifeExtHydro, LifeExtWind, LifeExtSolarPV, LifeExtSolarTherm, LifeExtBiomass, MandatedCapConst, GridStorage, ContractBasedDispatch, TransmissionGrowth, ReduceTnDLoss, RedDowntimeNGPreRet, RedDowntimeWindNew, RedDowntimeSolarPVNew, ChngElecImports, ChngElecExports, RedNonmethVent, MethaneDestr, WorkerTraining, ClinkerSubst, MethaneCapture, CroplandMgmt, RiceCultivMeasures, LivestockMeasures, EarlyRetIndustry, ImprSystemDesign, CogenWasteHeat, IndstFuelSwitch, IndstEffStdsCement, IndstEffStdsNGPS, IndstEffStdsIronSteel, IndstEffStdsChemicals, IndstEffStdsMining, IndstEffStdsWasteMgmt, IndstEffStdsAg, IndstEffStdsOtherInd, SetAsides, AfforestAndReforest, ImprForestMgmt, AvoidDeforest, CarbonTax, CCSGrowth, NonMarketElecPrice, ConvertNonCHPHeat, FuelTaxElec, FuelTaxCoal, FuelTaxNatGas, FuelTaxNuclear, FuelTaxBiomass, FuelTaxPetGas, FuelTaxPetDies, FuelTaxBioGas, FuelTaxBioDies, FuelTaxJetFuel, FuelTaxHeat, RmvBAUSubsidiesElec, RmvBAUSubsidiesCoal, RmvBAUSubsidiesNatGas, RmvBAUSubsidiesNucl, RmvBAUSubsidiesHydro, RmvBAUSubsidiesWind, RmvBAUSubsidiesSolar, RmvBAUSubsidiesBiom, RmvBAUSubsidiesPetGas, RmvBAUSubsidiesPetDies, RmvBAUSubsidiesBioGas, RmvBAUSubsidiesBioDies, RmvBAUSubsidiesJetFuel, RmvBAUSubsidiesHeat)
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