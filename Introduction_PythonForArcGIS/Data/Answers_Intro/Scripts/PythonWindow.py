import arcpy

layer_name = 'Illinois Counties'

expression = 'ACSMEDHINC <= 40000'

arcpy.SelectLayerByAttribute_management(layer_name, 'NEW_SELECTION', expression)

arcpy.SelectLayerByAttribute_management(layer_name, 'CLEAR_SELECTION')

arcpy.env.workspace = r'C:\...\Data\Illinois.gdb' # Change the path...

disolve_felds = ['STATE_NAME', 'ST_ABBREV']

arcpy.Dissolve_management(layer_name, 'Illinois', disolve_felds, '', 'SINGLE_PART', 'DISSOLVE_LINES')

arcpy.PolygonToLine_management('Illinois', 'Illinois_Boundary')

csv_file = r'C:\...\Data\CSV\JeopardyContestants_LatLon.csv' # Change the path...

arcpy.CopyRows_management(csv_file, 'JeopardyContestants_Table')

arcpy.MakeXYEventLayer_management('JeopardyContestants_Table', 'lon', 'lat', 'Jeopardy Contestants')

arcpy.Select_analysis('Jeopardy Contestants', 'JeopardyContestants', '"lat" IS NOT NULL OR "lon" IS NOT NULL')

arcpy.Buffer_analysis('JeopardyContestants', 'JeopardyContestants_Buffer', '5 Miles', 'FULL', 'ROUND', 'ALL', '', 'GEODESIC')

arcpy.Clip_analysis('JeopardyContestants_Buffer', 'Illinois', 'JeopardyContestants_Buffer_Clip')

arcpy.Intersect_analysis(['Illinois Counties', 'JeopardyContestants_Buffer_Clip'], 'Illinois_Counties_Intersect', 'ALL')
