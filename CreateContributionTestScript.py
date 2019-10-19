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
EnableOrDisableGroups = "Disable" # Should each group be enabled or disabled in turn?
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
# The second and third entries are the long and short name of the policy, used internally
# by this script.  Do not change these names.
# The fourth entry in each policy is a list of setting values enclosed with square brackets.
# You may change these values, add more values (separated by commas), and delete values.
# Any enabled policy must have a minimum of one setting value.  A policy that is disabled
# and a policy with a setting of zero produce identical results.
# The fifth entry in each policy is its group name.  By default, each policy is in its
# own group.  Change these names so multiple policies share a name (like "financial
# policies") to cause them to be enabled or disabled together.

# Transportation Sector Policies
Feebate = (False,"LDVs Feebate Rate","Feebate",[0,1],"FeebateGroup")
FuelEconLDVs = (False,"Percentage Additional Improvement of Fuel Economy Std[gasoline vehicle,LDVs]","FuelEconLDVs",[0,1],"FuelEconLDVsGroup")
FuelEconHDVs = (False,"Percentage Additional Improvement of Fuel Economy Std[diesel vehicle,HDVs]","FuelEconHDVs",[0,.66],"FuelEconHDVsGroup")
FuelEconAircraft = (False,"Percentage Additional Improvement of Fuel Economy Std[nonroad vehicle,aircraft]","FuelEconAircraft",[0,.54],"FuelEconAircraftGroup")
FuelEconRail = (False,"Percentage Additional Improvement of Fuel Economy Std[nonroad vehicle,rail]","FuelEconRail",[0,.2],"FuelEconRailGroup")
FuelEconShips = (False,"Percentage Additional Improvement of Fuel Economy Std[nonroad vehicle,ships]","FuelEconShips",[0,.2],"FuelEconShipsGroup")
FuelEconMtrbks = (False,"Percentage Additional Improvement of Fuel Economy Std[gasoline vehicle,motorbikes]","FuelEconMtrbks",[0,.74],"FuelEconMtrbksGroup")
PsgrTDM = (False,"Fraction of TDM Package Implemented[passenger]","PsgrTDM",[0,1],"PsgrTDMGroup")
FrgtTDM = (False,"Fraction of TDM Package Implemented[freight]","FrgtTDM",[0,1],"FrgtTDMGroup")
LCFS = (False,"Additional LCFS Percentage","LCFS",[0,.2],"LCFSGroup")

# Buildings and Appliances Sector Policies
RebateHeating = (False,"Boolean Rebate Program for Efficient Components[heating]","RebateHeating",[0,1],"RebateHeatingGroup")
RebateCooling = (False,"Boolean Rebate Program for Efficient Components[cooling and ventilation]","RebateCooling",[0,1],"RebateCoolingGroup")
RebateAppliances = (False,"Boolean Rebate Program for Efficient Components[appliances]","RebateAppliances",[0,1],"RebateAppliancesGroup")
BldgStdsUrbResHeating = (False,"Reduction in E Use Allowed by Component Eff Std[heating,urban residential]","BldgStdsUrbResHeating",[0,.22],"BldgStdsUrbResHeatingGroup")
BldgStdsUrbResCooling = (False,"Reduction in E Use Allowed by Component Eff Std[cooling and ventilation,urban residential]","BldgStdsUrbResCooling",[0,.38],"BldgStdsUrbResCoolingGroup")
BldgStdsUrbResEnvelope = (False,"Reduction in E Use Allowed by Component Eff Std[envelope,urban residential]","BldgStdsUrbResEnvelope",[0,.38],"BldgStdsUrbResEnvelopeGroup")
BldgStdsUrbResLighting = (False,"Reduction in E Use Allowed by Component Eff Std[lighting,urban residential]","BldgStdsUrbResLighting",[0,.40],"BldgStdsUrbResLightingGroup")
BldgStdsUrbResAppliances = (False,"Reduction in E Use Allowed by Component Eff Std[appliances,urban residential]","BldgStdsUrbResAppliances",[0,.38],"BldgStdsUrbResAppliancesGroup")
BldgStdsUrbResOther = (False,"Reduction in E Use Allowed by Component Eff Std[other component,urban residential]","BldgStdsUrbResOther",[0,.11],"BldgStdsUrbResOtherGroup")
BldgStdsRurResHeating = (False,"Reduction in E Use Allowed by Component Eff Std[heating,rural residential]","BldgStdsRurResHeating",[0,.22],"BldgStdsRurResHeatingGroup")
BldgStdsRurResCooling = (False,"Reduction in E Use Allowed by Component Eff Std[cooling and ventilation,rural residential]","BldgStdsRurResCooling",[0,.38],"BldgStdsRurResCoolingGroup")
BldgStdsRurResEnvelope = (False,"Reduction in E Use Allowed by Component Eff Std[envelope,rural residential]","BldgStdsRurResEnvelope",[0,.38],"BldgStdsRurResEnvelopeGroup")
BldgStdsRurResLighting = (False,"Reduction in E Use Allowed by Component Eff Std[lighting,rural residential]","BldgStdsRurResLighting",[0,.40],"BldgStdsRurResLightingGroup")
BldgStdsRurResAppliances = (False,"Reduction in E Use Allowed by Component Eff Std[appliances,rural residential]","BldgStdsRurResAppliances",[0,.38],"BldgStdsRurResAppliancesGroup")
BldgStdsRurResOther = (False,"Reduction in E Use Allowed by Component Eff Std[other component,rural residential]","BldgStdsRurResOther",[0,.11],"BldgStdsRurResOtherGroup")
BldgStdsComHeating = (False,"Reduction in E Use Allowed by Component Eff Std[heating,commercial]","BldgStdsComHeating",[0,.22],"BldgStdsComHeatingGroup")
BldgStdsComCooling = (False,"Reduction in E Use Allowed by Component Eff Std[cooling and ventilation,commercial]","BldgStdsComCooling",[0,.38],"BldgStdsComCoolingGroup")
BldgStdsComEnvelope = (False,"Reduction in E Use Allowed by Component Eff Std[envelope,commercial]","BldgStdsComEnvelope",[0,.38],"BldgStdsComEnvelopeGroup")
BldgStdsComLighting = (False,"Reduction in E Use Allowed by Component Eff Std[lighting,commercial]","BldgStdsComLighting",[0,.40],"BldgStdsComLightingGroup")
BldgStdsComAppliances = (False,"Reduction in E Use Allowed by Component Eff Std[appliances,commercial]","BldgStdsComAppliances",[0,.38],"BldgStdsComAppliancesGroup")
BldgStdsComOther = (False,"Reduction in E Use Allowed by Component Eff Std[other component,commercial]","BldgStdsComOther",[0,.11],"BldgStdsComOtherGroup")
ImprovedLabeling = (False,"Boolean Improved Device Labeling","ImprovedLabeling",[0,1],"ImprovedLabelingGroup")
ContractorEdu = (False,"Boolean Improved Contractor Edu and Training","ContractorEdu",[0,1],"ContractorEduGroup")
ElecCpntUrbRes = (False,"Percent New Nonelec Component Sales Shifted to Elec[urban residential]","ElecCpntUrbRes",[0,1],"ElecCpntUrbResGroup")
ElecCpntRurRes = (False,"Percent New Nonelec Component Sales Shifted to Elec[rural residential]","ElecCpntRurRes",[0,1],"ElecCpntRurResGroup")
ElecCpntCom = (False,"Percent New Nonelec Component Sales Shifted to Elec[commercial]","ElecCpntCom",[0,1],"ElecCpntComGroup")
RetrofittingHeating = (False,"Fraction of Commercial Components Replaced Annually due to Retrofitting Policy[heating]","RetrofittingHeating",[0,.034],"RetrofittingHeatingGroup")
RetrofittingCooling = (False,"Fraction of Commercial Components Replaced Annually due to Retrofitting Policy[cooling and ventilation]","RetrofittingCooling",[0,.034],"RetrofittingCoolingGroup")
RetrofittingEnvelope = (False,"Fraction of Commercial Components Replaced Annually due to Retrofitting Policy[envelope]","RetrofittingEnvelope",[0,.034],"RetrofittingEnvelopeGroup")
RetrofittingLighting = (False,"Fraction of Commercial Components Replaced Annually due to Retrofitting Policy[lighting]","RetrofittingLighting",[0,.034],"RetrofittingLightingGroup")
RetrofittingAppliances = (False,"Fraction of Commercial Components Replaced Annually due to Retrofitting Policy[appliances]","RetrofittingAppliances",[0,.034],"RetrofittingAppliancesGroup")
RetrofittingOther = (False,"Fraction of Commercial Components Replaced Annually due to Retrofitting Policy[other component]","RetrofittingOther",[0,.034],"RetrofittingOtherGroup")
DistSolarCarveOut = (False,"Min Fraction of Total Elec Demand to be Met by Distributed Solar PV","DistSolarCarveOut",[0,.24],"DistSolarCarveOutGroup")
DistSolarSubsidy = (False,"Perc Subsidy for Distributed Solar PV Capacity","DistSolarSubsidy",[0,.5],"DistSolarSubsidyGroup")

# Electricity Supply Sector Policies
RPS = (False,"Additional Renewable Portfolio Std Percentage","RPS",[0,.88],"RPSGroup")
DemandResponse = (False,"Fraction of Additional Demand Response Potential Achieved","DemandResponse",[0,1],"DemandResponseGroup")
SubsidyNuclear = (False,"Subsidy for Elec Production by Fuel[nuclear es]","SubsidyNuclear",[0,60],"SubsidyNuclearGroup")
SubsidyWind = (False,"Subsidy for Elec Production by Fuel[onshore wind es]","SubsidyWind",[0,60],"SubsidyWindGroup")
SubsidySolarPV = (False,"Subsidy for Elec Production by Fuel[solar PV es]","SubsidySolarPV",[0,60],"SubsidySolarPVGroup")
SubsidySolarTherm = (False,"Subsidy for Elec Production by Fuel[solar thermal es]","SubsidySolarTherm",[0,60],"SubsidySolarThermGroup")
SubsidyBiomass = (False,"Subsidy for Elec Production by Fuel[biomass es]","SubsidyBiomass",[0,60],"SubsidyBiomassGroup")
EarlyRetCoal = (False,"Annual Additional Capacity Retired due to Early Retirement Policy[hard coal es]","EarlyRetCoal",[0,10000],"EarlyRetCoalGroup")
EarlyRetNuclear = (False,"Annual Additional Capacity Retired due to Early Retirement Policy[nuclear es]","EarlyRetNuclear",[0,10000],"EarlyRetNuclearGroup")
LifeExtNuclear = (False,"Nuclear Capacity Lifetime Extension","LifeExtNuclear",[0,20],"LifeExtNuclearGroup")
GridStorage = (False,"Additional Battery Storage Annual Growth Percentage","GridStorage",[0,.16],"GridStorageGroup")
TransmissionGrowth = (False,"Percentage Increase in Transmission Capacity vs BAU","TransmissionGrowth",[0,1.13],"TransmissionGrowthGroup")
ReduceTnDLoss = (False,"Percentage TnD Losses Avoided","ReduceTnDLoss",[0,.4],"ReduceTnDLossGroup")
RedDowntimeNGPreRet = (False,"Percentage Reduction in Plant Downtime[natural gas nonpeaker es,preexisting retiring]","RedDowntimeNGPreRet",[0,.6],"RedDowntimeNGPreRetGroup")
RedDowntimeWindNew = (False,"Percentage Reduction in Plant Downtime[onshore wind es,newly built]","RedDowntimeWindNew",[0,.25],"RedDowntimeWindNewGroup")
RedDowntimeSolarPVNew = (False,"Percentage Reduction in Plant Downtime[solar PV es,newly built]","RedDowntimeSolarPVNew",[0,.3],"RedDowntimeSolarPVNewGroup")
ChngElecImports = (False,"Percent Change in Electricity Imports","ChngElecImports",[0,1],"ChngElecImportsGroup")
ChngElecExports = (False,"Percent Change in Electricity Exports","ChngElecExports",[0,1],"ChngElecExportsGroup")
BanNewCoal = (False,"Boolean Ban New Power Plants[hard coal es]","BanNewCoal",[0,1],"BanNewCoalGroup")
BanNewNGNonpeaker = (False,"Boolean Ban New Power Plants[natural gas nonpeaker es]","BanNewNGNonpeaker",[0,1],"BanNewNGNonpeakerGroup")
BanNewNuclear = (False,"Boolean Ban New Power Plants[nuclear es]","BanNewNuclear",[0,1],"BanNewNuclearGroup")
BanNewHydro = (False,"Boolean Ban New Power Plants[hydro es]","BanNewHydro",[0,1],"BanNewHydroGroup")

# Industrial (Non-Agriculture) Sector Policies
ReduceFGases = (False,"Fraction of F Gases Avoided","ReduceFGases",[0,1],"ReduceFGasesGroup")
MethaneDestr = (False,"Fraction of Methane Destruction Opportunities Achieved","MethaneDestr",[0,1],"MethaneDestrGroup")
WorkerTraining = (False,"Fraction of Addressable Process Emissions Avoided via Worker Training","WorkerTraining",[0,1],"WorkerTrainingGroup")
ClinkerSubst = (False,"Fraction of Cement Clinker Substitution Made","ClinkerSubst",[0,1],"ClinkerSubstGroup")
MethaneCapture = (False,"Fraction of Methane Capture Opportunities Achieved","MethaneCapture",[0,1],"MethaneCaptureGroup")
EarlyRetIndustry = (False,"Fraction of Energy Savings from Early Facility Retirement Achieved","EarlyRetIndustry",[0,1],"EarlyRetIndustryGroup")
ImprSystemDesign = (False,"Fraction of Installation and System Integration Issues Remedied","ImprSystemDesign",[0,1],"ImprSystemDesignGroup")
CogenWasteHeat = (False,"Fraction of Potential Cogeneration and Waste Heat Recovery Adopted","CogenWasteHeat",[0,1],"CogenWasteHeatGroup")
IndstSwitchFromCoal = (False,"Fraction of Hard Coal Use Converted to Other Fuels","IndstSwitchFromCoal",[0,.25],"IndstSwitchFromCoalGroup")
IndstSwitchFromNG = (False,"Fraction of Natural Gas Use Converted to Other Fuels","IndstSwitchFromNG",[0,.25],"IndstSwitchFromNGGroup")
IndstEffStdsCement = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[cement and other carbonates]","IndstEffStdsCement",[0,.08],"IndstEffStdsCementGroup")
IndstEffStdsNGPS = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[natural gas and petroleum systems]","IndstEffStdsNGPS",[0,.08],"IndstEffStdsNGPSGroup")
IndstEffStdsIronSteel = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[iron and steel]","IndstEffStdsIronSteel",[0,.08],"IndstEffStdsIronSteelGroup")
IndstEffStdsChemicals = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[chemicals]","IndstEffStdsChemicals",[0,.08],"IndstEffStdsChemicalsGroup")
IndstEffStdsMining = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[mining]","IndstEffStdsMining",[0,.08],"IndstEffStdsMiningGroup")
IndstEffStdsWasteMgmt = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[waste management]","IndstEffStdsWasteMgmt",[0,.08],"IndstEffStdsWasteMgmtGroup")
IndstEffStdsAg = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[agriculture]","IndstEffStdsAg",[0,.08],"IndstEffStdsAgGroup")
IndstEffStdsOtherInd = (False,"Percentage Improvement in Eqpt Efficiency Standards above BAU[other industries]","IndstEffStdsOtherInd",[0,.08],"IndstEffStdsOtherIndGroup")

# Agriculture, Land Use, and Forestry Policies
CroplandMgmt = (False,"Fraction of Abatement from Cropland Management Achieved","CroplandMgmt",[0,1],"CroplandMgmtGroup")
RiceCultivMeasures = (False,"Fraction of Abatement from Rice Cultivation Measures Achieved","RiceCultivMeasures",[0,1],"RiceCultivMeasuresGroup")
LivestockMeasures = (False,"Fraction of Abatement from Livestock Measures Achieved","LivestockMeasures",[0,1],"LivestockMeasuresGroup")
SetAsides = (False,"Fraction of Forest Set Asides Achieved","SetAsides",[0,1],"SetAsidesGroup")
AfforestAndReforest = (False,"Fraction of Afforestation and Reforestation Achieved","AfforestAndReforest",[0,1],"AfforestAndReforestGroup")
ImprForestMgmt = (False,"Fraction of Improved Forest Management Achieved","ImprForestMgmt",[0,1],"ImprForestMgmtGroup")

# District Heat Policies
ConvertNonCHPHeat = (False,"Fraction of Non CHP Heat Production Converted to CHP","ConvertNonCHPHeat",[0,1],"ConvertNonCHPHeatGroup")
HeatSwitchFromCoal = (False,"Fraction of District Heat Hard Coal Use Converted to Other Fuels","HeatSwitchFromCoal",[0,1],"HeatSwitchFromCoalGroup")

# Cross-Sector Policies
CarbonTaxTrans = (False,"Carbon Tax[transportation sector]","CarbonTaxTrans",[0,300],"CarbonTaxTransGroup")
CarbonTaxElec = (False,"Carbon Tax[electricity sector]","CarbonTaxElec",[0,300],"CarbonTaxElecGroup")
CarbonTaxResBldg = (False,"Carbon Tax[residential buildings sector]","CarbonTaxResBldg",[0,300],"CarbonTaxResBldgGroup")
CarbonTaxComBldg = (False,"Carbon Tax[commercial buildings sector]","CarbonTaxComBldg",[0,300],"CarbonTaxComBldgGroup")
CarbonTaxIndst = (False,"Carbon Tax[industry sector]","CarbonTaxIndst",[0,300],"CarbonTaxIndstGroup")
CCSGrowth = (False,"Fraction of Potential Additional CCS Achieved","CCSGrowth",[0,1],"CCSGrowthGroup")
FuelTaxElec = (False,"Additional Fuel Tax Rate by Fuel[electricity]","FuelTaxElec",[0,.2],"FuelTaxElecGroup")
FuelTaxCoal = (False,"Additional Fuel Tax Rate by Fuel[hard coal]","FuelTaxCoal",[0,.2],"FuelTaxCoalGroup")
FuelTaxNatGas = (False,"Additional Fuel Tax Rate by Fuel[natural gas]","FuelTaxNatGas",[0,.2],"FuelTaxNatGasGroup")
FuelTaxPetGas = (False,"Additional Fuel Tax Rate by Fuel[petroleum gasoline]","FuelTaxPetGas",[0,.2],"FuelTaxPetGasGroup")
FuelTaxPetDies = (False,"Additional Fuel Tax Rate by Fuel[petroleum diesel]","FuelTaxPetDies",[0,.2],"FuelTaxPetDiesGroup")
RmvBAUSubsidiesCoal = (False,"Percent Reduction in BAU Subsidies[hard coal]","RmvBAUSubsidiesCoal",[0,1],"RmvBAUSubsidiesCoalGroup")
RmvBAUSubsidiesNatGas = (False,"Percent Reduction in BAU Subsidies[natural gas]","RmvBAUSubsidiesNatGas",[0,1],"RmvBAUSubsidiesNatGasGroup")
RmvBAUSubsidiesNucl = (False,"Percent Reduction in BAU Subsidies[nuclear]","RmvBAUSubsidiesNucl",[0,1],"RmvBAUSubsidiesNuclGroup")
RmvBAUSubsidiesSolar = (False,"Percent Reduction in BAU Subsidies[solar]","RmvBAUSubsidiesSolar",[0,1],"RmvBAUSubsidiesSolarGroup")
RmvBAUSubsidiesPetGas = (False,"Percent Reduction in BAU Subsidies[petroleum gasoline]","RmvBAUSubsidiesPetGas",[0,1],"RmvBAUSubsidiesPetGasGroup")
RmvBAUSubsidiesPetDies = (False,"Percent Reduction in BAU Subsidies[petroleum diesel]","RmvBAUSubsidiesPetDies",[0,1],"RmvBAUSubsidiesPetDiesGroup")

# Building the Policy List
# ------------------------
# Every policy, whether enabled or not, appears on a list below called "PotentialPolicies".
# Now we construct the actual list of policies to be included (named "Policies") by
# checking which of the policies have been enabled.
PotentialPolicies = (Feebate, FuelEconLDVs, FuelEconHDVs, FuelEconAircraft, FuelEconRail, FuelEconShips, FuelEconMtrbks, PsgrTDM, FrgtTDM, LCFS, RebateHeating, RebateCooling, RebateAppliances, BldgStdsUrbResHeating, BldgStdsUrbResCooling, BldgStdsUrbResEnvelope, BldgStdsUrbResLighting, BldgStdsUrbResAppliances, BldgStdsUrbResOther, BldgStdsRurResHeating, BldgStdsRurResCooling, BldgStdsRurResEnvelope, BldgStdsRurResLighting, BldgStdsRurResAppliances, BldgStdsRurResOther, BldgStdsComHeating, BldgStdsComCooling, BldgStdsComEnvelope, BldgStdsComLighting, BldgStdsComAppliances, BldgStdsComOther, ImprovedLabeling, ContractorEdu, ElecCpntUrbRes, ElecCpntRurRes, ElecCpntCom, RetrofittingHeating, RetrofittingCooling, RetrofittingEnvelope, RetrofittingLighting, RetrofittingAppliances, RetrofittingOther, DistSolarCarveOut, DistSolarSubsidy, RPS, DemandResponse, SubsidyNuclear, SubsidyWind, SubsidySolarPV, SubsidySolarTherm, SubsidyBiomass, EarlyRetCoal, EarlyRetNuclear, LifeExtNuclear, GridStorage, TransmissionGrowth, ReduceTnDLoss, RedDowntimeNGPreRet, RedDowntimeWindNew, RedDowntimeSolarPVNew, ChngElecImports, ChngElecExports, BanNewCoal, BanNewNGNonpeaker, BanNewNuclear, BanNewHydro, ReduceFGases, MethaneDestr, WorkerTraining, ClinkerSubst, MethaneCapture, EarlyRetIndustry, ImprSystemDesign, CogenWasteHeat, IndstSwitchFromCoal, IndstSwitchFromNG, IndstEffStdsCement, IndstEffStdsNGPS, IndstEffStdsIronSteel, IndstEffStdsChemicals, IndstEffStdsMining, IndstEffStdsWasteMgmt, IndstEffStdsAg, IndstEffStdsOtherInd, CroplandMgmt, RiceCultivMeasures, LivestockMeasures, SetAsides, AfforestAndReforest, ImprForestMgmt, ConvertNonCHPHeat, HeatSwitchFromCoal, CarbonTaxTrans, CarbonTaxElec, CarbonTaxResBldg, CarbonTaxComBldg, CarbonTaxIndst, CCSGrowth, FuelTaxElec, FuelTaxCoal, FuelTaxNatGas, FuelTaxPetGas, FuelTaxPetDies, RmvBAUSubsidiesCoal, RmvBAUSubsidiesNatGas, RmvBAUSubsidiesNucl, RmvBAUSubsidiesSolar, RmvBAUSubsidiesPetGas, RmvBAUSubsidiesPetDies)
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
	
	# Finally, we do a run with all of the policy groups enabled (a full policy case run)
	f.write("MENU>RUN|O\n")
	f.write("MENU>VDF2TAB|" + RunName + ".vdf|" + RunResultsFile + "|" + OutputVarsFile + "|+!||||:")
	f.write("\tEnabledPolicyGroup=All")
	f.write("\tEnabledPolicies=All\n\n")
	
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
	
	# Finally, we do a run with all of the groups disabled (a BAU case run)
	f.write("MENU>RUN|O\n")
	f.write("MENU>VDF2TAB|" + RunName + ".vdf|" + RunResultsFile + "|" + OutputVarsFile + "|+!||||:")
	f.write("\tDisabledPolicyGroup=All")
	f.write("\tDisabledPolicies=All\n\n")
	
if EnableOrDisableGroups == "Enable":
	PerformRunsWithEnabledGroups()
else:
	PerformRunsWithDisabledGroups()

# We are done writing the Vensim command script and therefore close the file.
f.close()