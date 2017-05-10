#-------------------------------------------------------------------------------
# Name:        IllinoisInJeopardy_ScriptTool.py
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
csv_file = arcpy.GetParameterAsText(0) #r'C:\...\Data\CSV\JeopardyContestants_LatLon.csv' # Replace the '...' with the location where you placed your downloaded data

# Fields that holds the lat and long values
lon = arcpy.GetParameterAsText(1) # 'lon' # this is the x value
lat = arcpy.GetParameterAsText(2) #'lat' # this is the y value

# Spatial reference CSV XY coordinates
csv_spatialref = arcpy.GetParameterAsText(3) # arcpy.SpatialReference('WGS 1984')

# Counties feature class
counties = arcpy.GetParameterAsText(4) #'Illinois_Counties'

# Outputs:
# Contestants Intersect Feature Class or Shapefile
fc_output = arcpy.GetParameterAsText(5) # 'JeopardyContestants_Income'

# Sum of Contestants by County Table
tbl_output = arcpy.GetParameterAsText(6) # 'JeopardyContestants_ByCounty'


# Environments
# Managed by the tool, so we can comment out
#arcpy.env.workspace = #r'C:\...\Data\Illinois.gdb' # Replace the '...' with the location where you placed your downloaded data
#arcpy.env.overwriteOutput = True

arcpy.AddMessage("Starting the script...")

# Processes

try:

    # Copy CSV table to geodatabase stand-alone table

    xy_table = 'JeopardyContestants_Table'

    arcpy.CopyRows_management(csv_file, xy_table)

    arcpy.AddMessage(arcpy.Describe(csv_file).name + ' converted to table.')


    # Convert table to XY Layer

    field_list = [field.name for field in arcpy.ListFields(xy_table)]

    if lat in field_list and lon in field_list:
        arcpy.AddMessage('{} and {} fields exist'.format(lat, lon))

    else:
        arcpy.AddMessage('{} or {} fields DO NOT exist. Check field names.'.format(lat, lon))

    xy_layer = 'Jeopardy Contestants'

    arcpy.MakeXYEventLayer_management(xy_table, lon, lat, xy_layer)

    arcpy.AddMessage('XY Layer created')


    # Make the XY Layer a permanent point feature class or shapefile based on user input

    xy_features = 'JeopardyContestants'
    expression = '{} IS NOT NULL OR {} IS NOT NULL'.format(lat, lon)

    arcpy.Select_analysis(xy_layer, xy_features, expression)

    arcpy.AddMessage('XY Layer is now permanent')


    # Intersect the points with counties layer and include all fields from both layers

    arcpy.Intersect_analysis([xy_features, counties], fc_output, 'ALL', '', 'INPUT')

    arcpy.AddMessage('{} and {} intersect complete'.format(xy_features, counties))


    # Sum the number of contestants from each county and total winnings and output as a table

    arcpy.Frequency_analysis(fc_output, tbl_output, 'NAME_1', 'totalwinnings')

    arcpy.AddMessage('Contestants by county summary complete. Script complete.')

except arcpy.ExecuteError:
    arcpy.AddMessage(arcpy.GetMessages(2))
    arcpy.AddMessage('Could not complete script')

except:
    arcpy.AddMessage('Could not complete script')