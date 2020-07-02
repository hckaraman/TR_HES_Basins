import arcpy

HES = r'C:\Users\cagri\Desktop\TR_HES_Basins\Data\HES\HES.shp'
Basins = r'C:\Users\cagri\Desktop\TR_HES_Basins\Data\HES\Basins.shp'

feature_class = HES



with arcpy.da.SearchCursor(feature_class, ['FID', 'SHAPE@']) as cursor:
    for row in cursor:
        sel = arcpy.SelectLayerByLocation_management("Basins", "INTERSECT", row[1])
        arcpy.CalculateField_management("Basins", "BID", row[0])
        print(row[0])
