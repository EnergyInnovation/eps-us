# DuplicateScheduleTool.py
#
# This script is used to modify FractionOfPolicyImplementedThisYear.py
# by duplicating one of its policy schedules using a new policy schedule number.


# Global Constants
# ----------------
InputFileName = "FractionOfPolicyImplementedThisYear.py"
OutputFileName = "FractionOfPolicyImplementedThisYear-Modified.py"
ErrorLogFileName = "DuplicateScheduleTool-Error-Log.txt"
ExistingScheduleNumber = 7
NewScheduleNumber = 8
ValidScheduleNumbers = (1,2,3,4,5,6,7,8,9)

# Functions
# ---------

def CheckForErrors():
  ErrorFound = 0
  ErrorLog = open(ErrorLogFileName, 'w')

  # Open the InputFile and load the lines it contains
  InputFile = open(InputFileName, "r")
  OldLines = InputFile.readlines()

  # Ensure input file and output file have different filenames
  if InputFileName == OutputFileName:
    ErrorLog.write("InputFileName and OutputFileName must not be the same.\n")
    ErrorFound = 1

  # Ensure schedule numbers are valid
  if ExistingScheduleNumber not in ValidScheduleNumbers:
    ErrorLog.write("ExistingScheduleNumber must be an integer 1 through 9.\n")
    ErrorFound = 1
  if NewScheduleNumber not in ValidScheduleNumbers:
    ErrorLog.write("NewScheduleNumber must be an integer 1 through 9.\n")
    ErrorFound = 1

  # Ensure SearchString is found
  SearchString = '("Schedule '+str(ExistingScheduleNumber)
  SearchStringFound = 0
  for Line in OldLines:
    if SearchString in Line:
      SearchStringFound = 1
  if SearchStringFound == 0:
    ErrorLog.write("Existing schedule number "+str(ExistingScheduleNumber)+" not found.\n")
    ErrorFound = 1

  # Ensure ReplacementString doens't already exist in the InputFile
  ReplacementString = '("Schedule '+str(NewScheduleNumber)
  ReplacementStringFound = 0
  for Line in OldLines:
    if ReplacementString in Line:
      ReplacementStringFound = 1
  if ReplacementStringFound == 1:
    ErrorLog.write("New schedule number "+str(NewScheduleNumber)+" already exists in the input file.\n")
    ErrorFound = 1

  # Each policy schedule must be specified on a single line
  SplitScheduleFound = 0
  for Line in OldLines:
    if Line.startswith("    (2"):
      SplitScheduleFound = 1
  if SplitScheduleFound == 1:
    ErrorLog.write("Each policy schedule in the input file must be specified on a single line, not split across lines.\n")
    ErrorFound = 1

  ErrorLog.close()
  return(ErrorFound)


# Main Program
# ------------

if CheckForErrors() == 0:

  import os
  if os.path.exists(ErrorLogFileName):
    os.remove(ErrorLogFileName)

  # Prepare files for reading and writing
  InputFile = open(InputFileName, "r")
  OuputFile = open(OutputFileName, 'w')

  # Format the search string and replacement string
  SearchString = '("Schedule '+str(ExistingScheduleNumber)
  ReplacementString = '("Schedule '+str(NewScheduleNumber)

  # Load all the lines in the InputFile
  OldLines = InputFile.readlines()

  # Create an empty list to hold the lines for the output file
  NewLines = []

  for Line in OldLines:

    # We copy every line, whether or not it includes the search string
    NewLines.append(Line)

    # Then, if the line includes the search string, we update the schedule number and add it to NewLines
    if SearchString in Line:
      UpdatedLine = Line.replace(SearchString, ReplacementString)
      NewLines.append(UpdatedLine)

  # We write the set of NewLines to the output file
  OuputFile.writelines(NewLines)

  InputFile.close()
  OuputFile.close()
