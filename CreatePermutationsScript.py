# CreatePermutationsScript.py
#
# Developed by Jeffrey Rissman
#
# This is a Python script that is used to generate a Vensim command script.
# The Vensim command script will enable Vensim to run simulations of many policies.
# The resulting command script will run simulations with all unique combinations of
# settings of enabled policies. Which policies should be enabled
# and what settings should be included in the Vensim simulations are specified here in
# the Python script, prior to using it to generate a Vensim command script.


# File Names
# ----------
# Rather than including input and output file names in the code below, we assign all the file
# names to variables in this section.  This allows the names to be easily changed if desired.
ModelFile = "EPS.mdl" # The name of the Vensim model file (typically with .mdl or .vpm extension)
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
ElecPsgrLDVs = (False,"Percent Nonelec Vehicles Shifted to Elec[passenger,LDVs]","ElecPsgrLDVs",[0,.1])
ElecPsgrHDVs = (False,"Percent Nonelec Vehicles Shifted to Elec[passenger,HDVs]","ElecPsgrHDVs",[0,.1])
Feebate = (False,"LDVs Feebate Rate","Feebate",[0,1940])
FuelEconLDVs = (False,"Percentage Additional Improvement of Fuel Economy Std[LDVs]","FuelEconLDVs",[0,.22])
FuelEconHDVs = (False,"Percentage Additional Improvement of Fuel Economy Std[HDVs]","FuelEconHDVs",[0,.46])
TDM = (False,"Fraction of TDM Package Implemented","TDM",[0,1])

# Buildings and Appliances Sector Policies
RebateHeating = (False,"Boolean Rebate Program for Efficient Components[heating]","RebateHeating",[0,1])
RebateCooling = (False,"Boolean Rebate Program for Efficient Components[cooling and ventilation]","RebateCooling",[0,1])
RebateAppliances = (False,"Boolean Rebate Program for Efficient Components[appliances]","RebateAppliances",[0,1])
BldgStdsUrbResHeating = (False,"Reduction in E Use Allowed by Component Eff Std[heating,urban residential]","BldgStdsUrbResHeating",[0,.68])
BldgStdsUrbResCooling = (False,"Reduction in E Use Allowed by Component Eff Std[cooling and ventilation,urban residential]","BldgStdsUrbResCooling",[0,.68])
BldgStdsUrbResEnvelope = (False,"Reduction in E Use Allowed by Component Eff Std[envelope,urban residential]","BldgStdsUrbResEnvelope",[0,.68])
BldgStdsUrbResLighting = (False,"Reduction in E Use Allowed by Component Eff Std[lighting,urban residential]","BldgStdsUrbResLighting",[0,.68])
BldgStdsUrbResAppliances = (False,"Reduction in E Use Allowed by Component Eff Std[appliances,urban residential]","BldgStdsUrbResAppliances",[0,.68])
BldgStdsUrbResOther = (False,"Reduction in E Use Allowed by Component Eff Std[other component,urban residential]","BldgStdsUrbResOther",[0,.68])
BldgStdsRurResHeating = (False,"Reduction in E Use Allowed by Component Eff Std[heating,rural residential]","BldgStdsRurResHeating",[0,.68])
BldgStdsRurResCooling = (False,"Reduction in E Use Allowed by Component Eff Std[cooling and ventilation,rural residential]","BldgStdsRurResCooling",[0,.68])
BldgStdsRurResEnvelope = (False,"Reduction in E Use Allowed by Component Eff Std[envelope,rural residential]","BldgStdsRurResEnvelope",[0,.68])
BldgStdsRurResLighting = (False,"Reduction in E Use Allowed by Component Eff Std[lighting,rural residential]","BldgStdsRurResLighting",[0,.68])
BldgStdsRurResAppliances = (False,"Reduction in E Use Allowed by Component Eff Std[appliances,rural residential]","BldgStdsRurResAppliances",[0,.68])
BldgStdsRurResOther = (False,"Reduction in E Use Allowed by Component Eff Std[other component,rural residential]","BldgStdsRurResOther",[0,.68])
BldgStdsComHeating = (False,"Reduction in E Use Allowed by Component Eff Std[heating,commercial]","BldgStdsComHeating",[0,.68])
BldgStdsComCooling = (False,"Reduction in E Use Allowed by Component Eff Std[cooling and ventilation,commercial]","BldgStdsComCooling",[0,.68])
BldgStdsComEnvelope = (False,"Reduction in E Use Allowed by Component Eff Std[envelope,commercial]","BldgStdsComEnvelope",[0,.68])
BldgStdsComLighting = (False,"Reduction in E Use Allowed by Component Eff Std[lighting,commercial]","BldgStdsComLighting",[0,.68])
BldgStdsComAppliances = (False,"Reduction in E Use Allowed by Component Eff Std[appliances,commercial]","BldgStdsComAppliances",[0,.68])
BldgStdsComOther = (False,"Reduction in E Use Allowed by Component Eff Std[other component,commercial]","BldgStdsComOther",[0,.68])
ImprovedLabeling = (False,"Boolean Improved Device Labeling","ImprovedLabeling",[0,1])
ContractorEdu = (False,"Boolean Improved Contractor Edu and Training","ContractorEdu",[0,1])
ElecCpntUrbRes = (False,"Percent New Nonelec Component Sales Shifted to Elec[urban residential]","ElecCpntUrbRes",[0,.98])
ElecCpntRurRes = (False,"Percent New Nonelec Component Sales Shifted to Elec[rural residential]","ElecCpntRurRes",[0,.98])
ElecCpntCom = (False,"Percent New Nonelec Component Sales Shifted to Elec[commercial]","ElecCpntCom",[0,.98])
RetrofittingHeating = (False,"Fraction of Commercial Components Replaced Annually due to Retrofitting Policy[heating]","RetrofittingHeating",[0,.034])
RetrofittingCooling = (False,"Fraction of Commercial Components Replaced Annually due to Retrofitting Policy[cooling and ventilation]","RetrofittingCooling",[0,.034])
RetrofittingEnvelope = (False,"Fraction of Commercial Components Replaced Annually due to Retrofitting Policy[envelope]","RetrofittingEnvelope",[0,.034])
RetrofittingLighting = (False,"Fraction of Commercial Components Replaced Annually due to Retrofitting Policy[lighting]","RetrofittingLighting",[0,.034])
RetrofittingAppliances = (False,"Fraction of Commercial Components Replaced Annually due to Retrofitting Policy[appliances]","RetrofittingAppliances",[0,.034])
RetrofittingOther = (False,"Fraction of Commercial Components Replaced Annually due to Retrofitting Policy[other component]","RetrofittingOther",[0,.034])
DistSolarCarveOut = (False,"Min Fraction of Total Elec Demand to be Met by Distributed Solar PV","DistSolarCarveOut",[0,.04])
DistSolarSubsidy = (False,"Perc Subsidy for Distributed Solar PV Capacity","DistSolarSubsidy",[0,.5])

# Electricity Supply Sector Policies
RPS = (False,"Additional Renewable Portfolio Std Percentage","RPS",[0,.25])
DemandResponse = (False,"Fraction of Additional Demand Response Potential Achieved","DemandResponse",[0,1])
SubsidyNuclear = (False,"Subsidy for Elec Production by Fuel[nuclear es]","SubsidyNuclear",[0,35])
SubsidyWind = (False,"Subsidy for Elec Production by Fuel[wind es]","SubsidyWind",[0,35])
SubsidySolarPV = (False,"Subsidy for Elec Production by Fuel[solar PV es]","SubsidySolarPV",[0,35])
SubsidySolarTherm = (False,"Subsidy for Elec Production by Fuel[solar thermal es]","SubsidySolarTherm",[0,35])
SubsidyBiomass = (False,"Subsidy for Elec Production by Fuel[biomass es]","SubsidyBiomass",[0,35])
EarlyRetCoal = (False,"Annual Additional Capacity Retired due to Early Retirement Policy[coal es]","EarlyRetCoal",[0,10000])
EarlyRetNatGas = (False,"Annual Additional Capacity Retired due to Early Retirement Policy[natural gas nonpeaker es]","EarlyRetNatGas",[0,10000])
EarlyRetNuclear = (False,"Annual Additional Capacity Retired due to Early Retirement Policy[nuclear es]","EarlyRetNuclear",[0,10000])
EarlyRetHydro = (False,"Annual Additional Capacity Retired due to Early Retirement Policy[hydro es]","EarlyRetHydro",[0,10000])
LifeExtCoal = (False,"Generation Capacity Lifetime Extension[coal es]","LifeExtCoal",[0,20])
LifeExtNatGas = (False,"Generation Capacity Lifetime Extension[natural gas nonpeaker es]","LifeExtNatGas",[0,20])
LifeExtNuclear = (False,"Generation Capacity Lifetime Extension[nuclear es]","LifeExtNuclear",[0,20])
LifeExtHydro = (False,"Generation Capacity Lifetime Extension[hydro es]","LifeExtHydro",[0,20])
LifeExtWind = (False,"Generation Capacity Lifetime Extension[wind es]","LifeExtWind",[0,20])
LifeExtSolarPV = (False,"Generation Capacity Lifetime Extension[solar PV es]","LifeExtSolarPV",[0,20])
LifeExtSolarTherm = (False,"Generation Capacity Lifetime Extension[solar thermal es]","LifeExtSolarTherm",[0,20])
LifeExtBiomass = (False,"Generation Capacity Lifetime Extension[biomass es]","LifeExtBiomass",[0,20])
MandatedCapConst = (False,"Boolean Use Non BAU Mandated Capacity Construction Schedule","MandatedCapConst",[0,1])
GridStorage = (False,"Additional Non Hydro Storage Annual Growth Percentage","GridStorage",[0,.16])
ContractBasedDispatch = (False,"Boolean Use Contract Based Dispatch in Policy Case","ContractBasedDispatch",[0,1])
TransmissionGrowth = (False,"Percentage Increase in Transmission Capacity vs BAU","TransmissionGrowth",[0,.21])
ReduceTnDLoss = (False,"Percentage TnD Losses Avoided","ReduceTnDLoss",[0,.4])
RedDowntimeNGPreRet = (False,"Percentage Reduction in Plant Downtime[natural gas es,preexisting retiring]","RedDowntimeNGPreRet",[0,.6])
RedDowntimeWindNew = (False,"Percentage Reduction in Plant Downtime[wind es,newly built]","RedDowntimeWindNew",[0,.25])
RedDowntimeSolarPVNew = (False,"Percentage Reduction in Plant Downtime[solar PV es,newly built]","RedDowntimeSolarPVNew",[0,.3])
ChngElecImports = (False,"Percent Change in Electricity Imports","ChngElecImports",[0,1])
ChngElecExports = (False,"Percent Change in Electricity Exports","ChngElecExports",[0,1])

# Industrial Sector (Including Agriculture) Policies
RedNonmethVent = (False,"Fraction of CO2e from Vented Byproduct Gasses Avoided","RedNonmethVent",[0,1])
MethaneDestr = (False,"Fraction of Methane Destruction Opportunities Achieved","MethaneDestr",[0,1])
WorkerTraining = (False,"Fraction of Addressable Process Emissions Avoided via Worker Training","WorkerTraining",[0,1])
ClinkerSubst = (False,"Fraction of Cement Clinker Substitution Made","ClinkerSubst",[0,1])
MethaneCapture = (False,"Fraction of Methane Capture Opportunities Achieved","MethaneCapture",[0,1])
CroplandMgmt = (False,"Fraction of Abatement from Cropland Management Achieved","CroplandMgmt",[0,1])
RiceCultivMeasures = (False,"Fraction of Abatement from Rice Cultivation Measures Achieved","RiceCultivMeasures",[0,1])
LivestockMeasures = (False,"Fraction of Abatement from Livestock Measures Achieved","LivestockMeasures",[0,1])
EarlyRetIndustry = (False,"Fraction of Energy Savings from Early Facility Retirement Achieved","EarlyRetIndustry",[0,1])
ImprSystemDesign = (False,"Fraction of Installation and System Integration Issues Remedied","ImprSystemDesign",[0,1])
CogenWasteHeat = (False,"Fraction of Potential Cogeneration and Waste Heat Recovery Adopted","CogenWasteHeat",[0,1])
IndstFuelSwitch = (False,"Fraction of Coal Use Converted to Other Fuels","IndstFuelSwitch",[0,.17])
IndstEffStdsCement = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[cement and other carbonates]","IndstEffStdsCement",[0,.11])
IndstEffStdsNGPS = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[natural gas and petroleum systems]","IndstEffStdsNGPS",[0,.11])
IndstEffStdsIronSteel = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[iron and steel]","IndstEffStdsIronSteel",[0,.11])
IndstEffStdsChemicals = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[chemicals]","IndstEffStdsChemicals",[0,.11])
IndstEffStdsMining = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[mining]","IndstEffStdsMining",[0,.11])
IndstEffStdsWasteMgmt = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[waste management]","IndstEffStdsWasteMgmt",[0,.11])
IndstEffStdsAg = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[agriculture]","IndstEffStdsAg",[0,.11])
IndstEffStdsOtherInd = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other industries]","IndstEffStdsOtherInd",[0,.11])

# Land Use and Forestry Policies
SetAsides = (False,"Fraction of Abatement from Forest Set Asides Achieved","SetAsides",[0,.31])
AfforestAndReforest = (False,"Fraction of Abatement from Afforestation and Reforestation Achieved","AfforestAndReforest",[0,.45])
ImprForestMgmt = (False,"Fraction of Abatement from Improved Forest Management Achieved","ImprForestMgmt",[0,1])
AvoidDeforest = (False,"Fraction of Abatement from Avoided Deforestation Achieved","AvoidDeforest",[0,1])

# Cross-Sector Policies
CarbonTax = (False,"Carbon Tax","CarbonTax",[0,100])
CCSGrowth = (False,"Fraction of Potential Additional CCS Achieved","CCSGrowth",[0,1])
NonMarketElecPrice = (False,"Boolean Prevent Policies from Affecting Electricity Prices","NonMarketElecPrice",[0,1])
ConvertNonCHPHeat = (False,"Fraction of Non CHP Heat Production Converted to CHP","ConvertNonCHPHeat",[0,1])
FuelTaxElec = (False,"Additional Fuel Tax Rate by Fuel[electricity]","FuelTaxElec",[0,.2])
FuelTaxCoal = (False,"Additional Fuel Tax Rate by Fuel[coal]","FuelTaxCoal",[0,.2])
FuelTaxNatGas = (False,"Additional Fuel Tax Rate by Fuel[natural gas]","FuelTaxNatGas",[0,.2])
FuelTaxNuclear = (False,"Additional Fuel Tax Rate by Fuel[nuclear]","FuelTaxNuclear",[0,.2])
FuelTaxBiomass = (False,"Additional Fuel Tax Rate by Fuel[biomass]","FuelTaxBiomass",[0,.2])
FuelTaxPetGas = (False,"Additional Fuel Tax Rate by Fuel[petroleum gasoline]","FuelTaxPetGas",[0,.2])
FuelTaxPetDies = (False,"Additional Fuel Tax Rate by Fuel[petroleum diesel]","FuelTaxPetDies",[0,.2])
FuelTaxBioGas = (False,"Additional Fuel Tax Rate by Fuel[biofuel gasoline]","FuelTaxBioGas",[0,.2])
FuelTaxBioDies = (False,"Additional Fuel Tax Rate by Fuel[biofuel diesel]","FuelTaxBioDies",[0,.2])
FuelTaxJetFuel = (False,"Additional Fuel Tax Rate by Fuel[jet fuel]","FuelTaxJetFuel",[0,.2])
FuelTaxHeat = (False,"Additional Fuel Tax Rate by Fuel[heat]","FuelTaxHeat",[0,.2])
RmvBAUSubsidiesElec = (False,"Percent Reduction in BAU Subsidies[electricity]","RmvBAUSubsidiesElec",[0,1])
RmvBAUSubsidiesCoal = (False,"Percent Reduction in BAU Subsidies[coal]","RmvBAUSubsidiesCoal",[0,1])
RmvBAUSubsidiesNatGas = (False,"Percent Reduction in BAU Subsidies[natural gas]","RmvBAUSubsidiesNatGas",[0,1])
RmvBAUSubsidiesNucl = (False,"Percent Reduction in BAU Subsidies[nuclear]","RmvBAUSubsidiesNucl",[0,1])
RmvBAUSubsidiesHydro = (False,"Percent Reduction in BAU Subsidies[hydro]","RmvBAUSubsidiesHydro",[0,1])
RmvBAUSubsidiesWind = (False,"Percent Reduction in BAU Subsidies[wind]","RmvBAUSubsidiesWind",[0,1])
RmvBAUSubsidiesSolar = (False,"Percent Reduction in BAU Subsidies[solar]","RmvBAUSubsidiesSolar",[0,1])
RmvBAUSubsidiesBiom = (False,"Percent Reduction in BAU Subsidies[biomass]","RmvBAUSubsidiesBiom",[0,1])
RmvBAUSubsidiesPetGas = (False,"Percent Reduction in BAU Subsidies[petroleum gasoline]","RmvBAUSubsidiesPetGas",[0,1])
RmvBAUSubsidiesPetDies = (False,"Percent Reduction in BAU Subsidies[petroleum diesel]","RmvBAUSubsidiesPetDies",[0,1])
RmvBAUSubsidiesBioGas = (False,"Percent Reduction in BAU Subsidies[biofuel gasoline]","RmvBAUSubsidiesBioGas",[0,1])
RmvBAUSubsidiesBioDies = (False,"Percent Reduction in BAU Subsidies[biofuel diesel]","RmvBAUSubsidiesBioDies",[0,1])
RmvBAUSubsidiesJetFuel = (False,"Percent Reduction in BAU Subsidies[jet fuel]","RmvBAUSubsidiesJetFuel",[0,1])
RmvBAUSubsidiesHeat = (False,"Percent Reduction in BAU Subsidies[heat]","RmvBAUSubsidiesHeat",[0,1])

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


# We invoke the function that builds the list of policy setting combinations.
# If fewer than two policies were enabled, we instead produce an error
# and exit.  (We write the error to the text file, because many users won't
# be using a console and won't see the message produced by sys.exit().
# Note that the function BuildPolicyCombinationsSettingList() fails if there
# is only one enabled policy, so we do not invoke it unless there are at
# least two enabled policies.

if len(Policies) < 1:
	f = open(OutputScript, 'w')
	ErrorMessage = "Error: No policies were enabled in the Python script.  Before running the script, you must enable at least two policies."
	f.write(ErrorMessage)
	f.close()
	import sys
	sys.exit(ErrorMessage)
elif len(Policies) == 1:
	f = open(OutputScript, 'w')
	ErrorMessage = "Error: Only one policy was enabled in the Python script.  Before running the script, you must enable at least two policies."
	f.write(ErrorMessage)
	f.close()
	import sys
	sys.exit(ErrorMessage)
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
		f.write("\t-")
	f.write("\n\n")

# We are done writing the Vensim command script and therefore close the file.
f.close()
