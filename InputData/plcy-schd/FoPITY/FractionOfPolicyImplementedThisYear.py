# FractionOfPolicyImplementedThisYear.py
#
# This script is used to generate .csv policy schedule files for all built-in (reference) scenarios.
# It creates schedules in the formats expected by Vensim and by the web app.  It also creates the
# Policy Elements file required to populate the relevant subscript in Vensim.


# Global Constants
# ----------------
MaxSchedules = 9
MaxSubscripts = 3
FirstYear = 2020
FinalYear = 2100 # This should be the final year supported by EPS.mdl (i.e., 2100), not the final year actually used in a given region.
RoundingDigits = 6


# Policy Implementation Schedules
# -------------------------------

PolicyElements = (

  # Transportation
  (("trans fuel economy standards","passenger","LDVs"),
    ((2020,0),(2021,0),(2050,1)),
    ((2020,0),(2025,0),(2035,1),(2050,1)),
    ((2020,0),(2021,0),(2050,1))
  ),
  (("trans fuel economy standards","passenger","HDVs"),
    ((2020,0),(2021,0),(2050,1)),
    ((2020,0),(2025,0),(2035,1),(2050,1)),
    ((2020,0),(2021,0),(2050,1))
  )
)


# Functions
# ---------

# Write Policy and Subscript Headers
def WritePolicyAndSubscriptHeaders():
  f.write("Policy,")
  for Subscript in range(1,MaxSubscripts+1):
    f.write("Subscript "+str(Subscript)+",")

# Write policy and subscript names, adding commas for unused subscripts
def WritePolicyAndSubscriptNames(PolicyElement):
  for PolicyProperty in range(MaxSubscripts+1):
    if len(PolicyElement[0])-1 >= PolicyProperty:
      f.write(PolicyElement[0][PolicyProperty]+",")
    else:
      f.write(",")

# Write a .csv file formatted for use by Vensim
def WriteVensimFile():

  # Write header row
  WritePolicyAndSubscriptHeaders()
  for Year in range(FirstYear,FinalYear):
    f.write(str(Year)+",")
  f.write(str(FinalYear)+"\n")
  
  # Write policy element rows
  for PolicyElement in PolicyElements:
  
    WritePolicyAndSubscriptNames(PolicyElement)
    
    # If we don't have data for a schedule, use the first schedule's data.
    if Schedule > len(PolicyElements[0])-1:
      ActiveSchedule = 1
    else:
      ActiveSchedule = Schedule
    
    # Write policy implementation percentages for each year
    for Year in range(FirstYear,FinalYear+1):
      # Find the ordered pairs most closely enclosing the active year
      PairBelow = PolicyElement[ActiveSchedule][0]
      PairAbove = PolicyElement[ActiveSchedule][len(PolicyElement[ActiveSchedule])-1]
      for OrderedPair in PolicyElement[ActiveSchedule]:
        if OrderedPair[0] <= Year:
          PairBelow = OrderedPair
        if OrderedPair[0] >= Year:
          PairAbove = OrderedPair
          break

      # If the enclosing pairs match each other, they also match the active year, so we
      # simply write the implementation schedule from one of the pairs.
      if PairAbove == PairBelow:
        ImplementationPerc = PairBelow[1]
      # Otherwise, we linearly interpolate between the enclosing pairs
      else:
        FractionBetweenYears = (Year-PairBelow[0])/(PairAbove[0]-PairBelow[0])
        ImplementationPerc = PairBelow[1]+FractionBetweenYears*(PairAbove[1]-PairBelow[1])

      # We round the implementation percentage to the correct number of digits and write it
      ImplementationPerc = round(ImplementationPerc, RoundingDigits)
      f.write(str(ImplementationPerc))
      # If this was not the last year, we add a comma
      if Year < FinalYear:
        f.write(",")
        
    # New line for next policy element
    f.write("\n")

# Write a .csv file formatted for use by the web app
def WriteWebAppFile():

  # Write header row
  WritePolicyAndSubscriptHeaders()
  for Year in range(FirstYear,FinalYear):
    f.write("Year,Imp %,")
  f.write("Year,Imp %\n")

  # Write policy element rows
  for PolicyElement in PolicyElements:
  
    WritePolicyAndSubscriptNames(PolicyElement)

    # If we don't have data for a schedule, use the first schedule's data.
    if Schedule > len(PolicyElements[0])-1:
      ActiveSchedule = 1
    else:
      ActiveSchedule = Schedule

    # Write schedule data
    for Year in range(FirstYear,FinalYear+1):
      if Year-FirstYear < len(PolicyElement[ActiveSchedule]):
        f.write(str(PolicyElement[ActiveSchedule][Year-FirstYear][0])+",")
        f.write(str(PolicyElement[ActiveSchedule][Year-FirstYear][1])+",")
      elif Year < FinalYear:
        f.write(",,")
    f.write(",\n")

def WritePolicyElementsFile():
  f.write("Policy Element Subscipt\n")
  for PolicyElement in PolicyElements:
    f.write(" X ".join(PolicyElement[0])+"\n")
 

# Main Program
# ------------

for Schedule in range(1,MaxSchedules+1):

  # Begin writing the .csv file for Vensim
  f = open("FoPITY-"+str(Schedule)+".csv", 'w')

  WriteVensimFile()

  # Done writing the .csv file for Vensim
  f.close()

  # Begin writing the .csv file for the web app
  f = open("FoPITY-"+str(Schedule)+"-WebApp.csv", 'w')
  
  WriteWebAppFile()

  # Done writing the .csv file for the web app
  f.close()

# Write policy elements file
f = open("FoPITY-policy-elements.csv",'w')

WritePolicyElementsFile()

# Done writing the policy elements file
f.close()
