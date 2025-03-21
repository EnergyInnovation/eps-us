import csv
import os

def create_csv_files():
    first_abbr_list = ["NOx", "PM25", "SOx"]
    second_abbr_list = ["male", "female", "white", "black", "asian", "otherrace", "hispanic", "nonhispanic"]
    directory = os.getcwd()
    
    for first in first_abbr_list:
        for second in second_abbr_list:
            filename = f"FoIPMbDT-{first}-{second}.csv"
            filepath = os.path.join(directory, filename)
            
            with open(filepath, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Column1", "Column2", "Column3"])  # Example headers
                
            print(f"Created: {filename}")

create_csv_files()
