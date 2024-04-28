import geopandas as gpd


# Load the attribute table (DBF file)
attribute_table = gpd.read_file('/Users/rheaacharya/Downloads/tl_2010_22_county10/tl_2010_22_county10.dbf')

# Load the shapefile
districts = gpd.read_file('/Users/rheaacharya/Downloads/tl_2010_22_county10/tl_2010_22_county10.shp')

# Display the first few rows of the attribute table to see its structure
print(districts.head())
# Optionally, you can list all column names to see what information is available
# print(districts.columns)

# Display the first few rows of the attribute table to see its structure
# print(attribute_table.head())

# Optionally, you can list all column names to see what information is available
#print(attribute_table.columns)

#data = {'geometry': [districts.geometry.Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])]}
# Assuming 'COUNTYFP10' is the column name for County FIPS codes
duplicate_counties = districts['COUNTYFP10'].value_counts()

# Filter for counties that appear more than once
duplicate_counties = duplicate_counties[duplicate_counties > 1]

polygons = districts['geometry']
polygons = polygons[polygons.is_simple]
print(len(polygons))
# Get the count of duplicated counties
num_duplicate_counties = len(duplicate_counties)

print(num_duplicate_counties)
print(len(districts))

# for attr_name in dir(districts.polygon[0]):
    # if not attr_name.startswith('__'):  # Skip dunder methods
       #  print(attr_name)

# print(len(districts["geometry"][1]))

from osgeo import ogr

def count_rings_in_polygons(shapefile_path):
    # Open the shapefile
    datasource = ogr.Open(shapefile_path)
    if datasource is None:
        print("Could not open shapefile")
        return

    layer = datasource.GetLayer()

    # Iterate through features
    for feature in layer:
        geometry = feature.GetGeometryRef()
        # Check if the geometry is a polygon
        if geometry.GetGeometryType() == ogr.wkbPolygon:
            # Get the number of rings for the polygon
            num_rings = geometry.GetGeometryCount()
            print("Number of rings in polygon {}: {}".format(feature.GetFID(), num_rings))

    datasource = None  # Close the datasource

# Example usage
shapefile_path = 'tl_2010_22_county10.shp'
count_rings_in_polygons(shapefile_path)
row_with_county_099 = districts[districts['COUNTYFP10'] == '099']

# districts = gpd.read_file('/Users/rheaacharya/Downloads/tl_2010_06_tract10/tl_2010_06_tract10.shp')
for index, row in districts.iterrows():
    # Get the geometry of the current polygon
    polygon = row['geometry']
    
    # Convert the polygon to WKB (Well-Known Binary) format
    wkb_polygon = polygon.wkb
    
    bytes_36_to_39 = wkb_polygon[0:4]
    
    # Convert bytes to integer in little-endian format
    value = int.from_bytes(bytes_36_to_39, byteorder='little')
    
    # Print the value
    print("Value of bytes 36 through 39 for Polygon {}: {}".format(index, value))


indiana = gpd.read_file('/Users/rheaacharya/Downloads/tl_2010_18_county10/tl_2010_18_county10.shp')

for index, row in indiana.iterrows():
    # Get the geometry of the current polygon
    polygon = row['geometry']
    
    # Convert the polygon to WKB (Well-Known Binary) format
    wkb_polygon = polygon.wkb
    
    # Access byte 36
    byte_0 = wkb_polygon[0]
    byte_36 = wkb_polygon[36]
    
    # print("Indiana Byte 0 of Polygon {}: {}".format(index, byte_0))
    # print("Indiana Byte 36 of Polygon {}: {}".format(index, byte_36))

indiana_tracts = gpd.read_file('/Users/rheaacharya/Downloads/tl_2010_18_tract10/tl_2010_18_tract10.shp')

# for index, row in indiana_tracts.iterrows():
    # Get the geometry of the current polygon
   # polygon = row['geometry']
    
    # Convert the polygon to WKB (Well-Known Binary) format
    # wkb_polygon = polygon.wkb
    
    # Access byte 36
    # byte_0 = wkb_polygon[0]
    # byte_36 = wkb_polygon[1]
    
    # print("Indiana Tract Byte 0 of Polygon {}: {}".format(index, byte_0))
    # if byte_36 != 3:
        # print("Indiana Tract Byte 36 of Polygon {}: {}".format(index, byte_36))

california_tracts = gpd.read_file('/Users/rheaacharya/Downloads/tl_2010_06_tract10/tl_2010_06_tract10.shp')
for index, row in california_tracts.iterrows():
    # Get the geometry of the current polygon
    polygon = row['geometry']
    
    # Convert the polygon to WKB (Well-Known Binary) format
    wkb_polygon = polygon.wkb
    
    bytes_36_to_39 = wkb_polygon[36:40]
    
    # Convert bytes to integer in little-endian format
    value = int.from_bytes(bytes_36_to_39, byteorder='little')
    
    # Print the value
   #  print("Value of bytes 36 through 39 for Polygon {}: {}".format(index, value))
    
    # print("California Tract Byte 0 of Polygon {}: {}".format(index, byte_0))
    # if byte_36 != 192:
        #print("California Tract Byte 36 of Polygon {}: {}".format(index, byte_36))