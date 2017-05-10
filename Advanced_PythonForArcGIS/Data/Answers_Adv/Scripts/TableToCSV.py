#-------------------------------------------------------------------------------
# Name:        TableToCSV.py
# Purpose:     <Some important purpose.>
# Author:      <Name, Your>
# Created:     17/10/2016
# Copyright:   (c) <Your Name> 2016
# Licence:     <licence>
#-------------------------------------------------------------------------------

# Import Modules
import arcpy
import csv


# Parameters

# Path to the input feature class or standalone table
# input_table = r"C:\...\Data\Illinois.gdb\Illinois_Counties" # Replace the '...' with the location where you placed your downloaded data
input_table = r"C:\Users\jvwhit\Documents\ILGISA\Data\Answers_Adv\Illinois.gdb\Illinois_Counties"

# Path to the output CSV file (this CSV file will not exist)
# output_csv = r"C:\...\Data\CSV\Illinois_Counties.csv" # Replace the '...' with the location where you placed your downloaded data
output_csv = r"C:\Users\jvwhit\Documents\ILGISA\Data\Answers_Adv\CSV\Illinois_Counties.csv"

# Processes

# Read in a feature class or standalone table
# Read the feature class or standalone table field names
field_list = [field.name for field in arcpy.ListFields(input_table) if field.name != "Shape"] # Added an if statement

print(field_list) # Do this to make sure it works

# Read the data
data = []
with arcpy.da.SearchCursor(input_table, field_list) as cursor:
    for row in cursor:
        data.append(list(row)) # Added a list function to convert the tuple

print(data[:10]) # Print the first 10 rows to check the data


# Write the field names to a new CSV file
# Write the data to the new CSV file
with open(output_csv, 'wb') as csv_file: # For some reason, 'w' add an extra line between rows...

    csv_file = csv.writer(csv_file) # Creates a CSV writer object
    csv_file.writerow(field_list) # Writes out one line: the fields
    csv_file.writerows(data) # Writes out all data from the list of lists

print("Finished! Open the file located at {}".format(output_csv)) # Lets you know that the script is finished
