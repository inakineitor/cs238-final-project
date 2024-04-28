import geopandas as gpd

# load the maps
california_tracts = gpd.read_file('/Users/rheaacharya/Downloads/tl_2010_06_tract10/tl_2010_06_tract10.shp')
colorado_tracts = gpd.read_file('/Users/rheaacharya/Downloads/tl_2010_08_tract10/tl_2010_08_tract10.shp')
georgia_tracts = gpd.read_file('/Users/rheaacharya/Downloads/tl_2010_13_tract10/tl_2010_13_tract10.shp')
louisiana_tracts = gpd.read_file('/Users/rheaacharya/Downloads/tl_2010_22_tract10/tl_2010_22_tract10.shp')
massachusetts_tracts = gpd.read_file('/Users/rheaacharya/Downloads/tl_2010_25_tract10/tl_2010_25_tract10.shp')
newjersey_tracts = gpd.read_file('/Users/rheaacharya/Downloads/tl_2010_34_tract10/tl_2010_34_tract10.shp')
northcarolina_tracts = gpd.read_file('/Users/rheaacharya/Downloads/tl_2010_37_tract10/tl_2010_37_tract10.shp')
ohio_tracts = gpd.read_file('/Users/rheaacharya/Downloads/tl_2010_39_tract10/tl_2010_39_tract10.shp')
pennsylvania_tracts = gpd.read_file('/Users/rheaacharya/Downloads/tl_2010_42_tract10/tl_2010_42_tract10.shp')
virginia_tracts = gpd.read_file('/Users/rheaacharya/Downloads/tl_2010_51_tract10/tl_2010_51_tract10.shp')
washington_tracts = gpd.read_file('/Users/rheaacharya/Downloads/tl_2010_53_tract10/tl_2010_53_tract10.shp')
maps = [(california_tracts, "california"), (colorado_tracts, "colorado"), 
        (georgia_tracts, "georgia"), (louisiana_tracts, "louisiana"),
        (massachusetts_tracts, "massachusetts"), (newjersey_tracts, "newjersey"),
        (northcarolina_tracts, "northcarolina"), (ohio_tracts, "ohio"), 
        (pennsylvania_tracts, "pennsylvania"), (virginia_tracts, "virginia"),
        (washington_tracts, "washington")]

epsilon = []
# convert to binary
for state in maps:
    print(state[1])
    # print(len(state))
    i = 0
    for index, row in state[0].iterrows():
        polygon = row['geometry']
        wkb_polygon = polygon.wkb
        shape = wkb_polygon[0:4]
        value = int.from_bytes(shape, byteorder='little')
        if value != 769:
            i += 1
            # print("Shape for Polygon {}: {}".format(index, value))
    epsilon.append((state[1], len(state[0]), i))
    print(i/len(state[0]))
    print(len(state[0]))

# count the number of 