#-------------------------------------------------------------------------------
# Name:        IllinoisInJeopardy_Standalone.py
# Purpose:     Script to figure out where Jeopardy! contestants live.
#
# Author:      Whitacre, James
#
# Created:     17/10/2016
# Copyright:   (c) James Whitacre 2016
# Licence:     None...its free!
#-------------------------------------------------------------------------------

# Import Modules
import arcpy


# Parameters

# Inputs:
# CSV File with XY coordinates
# Replace the '...' with the location where you placed your downloaded data
csv_file = r'C:\...\Data\CSV\JeopardyContestants_LatLon.csv'

# Fields that holds the lat and long values
lon = 'lon' # this is the x value
lat = 'lat' # this is the y value

# Spatial reference CSV XY coordinates
csv_spatialref = arcpy.SpatialReference('WGS 1984')

# Counties feature class
counties = 'Illinois_Counties'

# Outputs:
# Contestants Intersect Feature Class or Shapefile
fc_output = 'JeopardyContestants_Income'

# Sum of Contestants by County Table
tbl_output = 'JeopardyContestants_ByCounty'


# Environments

# Replace the '...' with the location where you placed your downloaded data
#print(arcpy.ListEnvironments())
arcpy.env.workspace = r'C:\...\Data\Illinois.gdb'
arcpy.env.overwriteOutput = True


# Processes

try:
    # Indent all processes...

    # Copy CSV table to geodatabase stand-alone table

    xy_table = 'JeopardyContestants_Table'

    arcpy.CopyRows_management(csv_file, xy_table)

    print(arcpy.Describe(csv_file).name + ' converted to table.')


    # Convert table to XY Layer

    field_list = [field.name for field in arcpy.ListFields(xy_table)]

    if lat in field_list and lon in field_list:
        print('{} and {} fields exist'.format(lat, lon))

    else:

        print('{} or {} fields DO NOT exist. Check field names.'.format(lat, lon))

    xy_layer = 'Jeopardy Contestants'

    arcpy.MakeXYEventLayer_management(xy_table, lon, lat, xy_layer)

    print('XY Layer created')


    # Make the XY Layer a permanent point feature class or shapefile based on user input

    xy_features = 'JeopardyContestants'
    expression = '{} IS NOT NULL OR {} IS NOT NULL'.format(lat, lon)

    arcpy.Select_analysis(xy_layer, xy_features, expression)

    print('XY Layer is now permanent')


    # Intersect the points with counties layer and include all fields from both layers

    arcpy.Intersect_analysis([xy_features, counties], fc_output, 'ALL', '', 'INPUT')

    print('{} and {} intersect complete'.format(xy_features, counties))


    # Sum the number of contestants from each county and total winnings and output as a table

    arcpy.Frequency_analysis(fc_output, tbl_output, 'NAME_1', 'totalwinnings')

    print('Contestants by county summary complete. Script complete.')

# Print any errors from any geoprocessing tools if they fail
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
    print('Could not complete script')

# Add a general error print statement
except:
    print('Could not complete script')