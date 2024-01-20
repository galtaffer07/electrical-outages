import os
import pandas as pd
import matplotlib as plt
import folium
from geopy.geocoders import Bing
from folium.plugins import HeatMap
import tqdm


geolocator = Bing(api_key="AqjmiNHvJvjQEzYWYWsorqP7jC-F741tsJ7RsNM9Fxs_sSaR6ieRJbAAJBbZgkVb")

smallSet = pd.read_csv(r"C:\Users\galta\Downloads\Insignificant_16_17_18_19_20.xlsx - Small_16_17_18_19_20.csv.stem_andover_with_coords.csv")
#smallSet.drop(['Official Notified Name(1)', 'Official Notified Phone (1)', 'Official Notified Name (2)', 'Official Notified Phone (2)'], axis = 1, inplace = True)
pd.set_option('display.max.columns', None)
#smallSet.drop(['Substation', 'Planned Incident ID', 'Circuit Type'], axis = 1, inplace = True) #axis = 1 means columns, axis = 0 means rows, inplace means if it's editing itself
#smallSet.dropna(axis = 0, subset = ['Street Name'], inplace = True) #removes rows in which certain streets are NaN

bigSet = pd.read_csv(r"C:\Users\galta\Downloads\big_16_17_18_19_20.xlsx - big_16_17_18_19_20.csv.stem_andover_with_coords.csv")
#bigSet.drop(['Official Notified Name(1)', 'Official Notified Phone (1)', 'Official Notified Name (2)', 'Official Notified Phone (2)'], axis = 1, inplace = True)
#bigSet.drop(['Substation', 'Planned Incident ID', 'Circuit Type'], axis = 1, inplace = True)
#bigSet.dropna(axis = 0, subset = ['Street Name'], inplace = True)
#andoverSet = bigSet[bigSet['City/Town'] == "ANDOVER"].copy()

unplannedSet2021 = pd.read_csv(r"C:\Users\galta\Downloads\Copy of 2021_UnplannedInsignificant.xlsx - UnplannedInsigOutagesRpt.csv.stem_andover_with_coords.csv")
#unplannedSet2021.drop(['Official Notified Name(1)', 'Official Notified Phone (1)', 'Official Notified Name (2)', 'Official Notified Phone (2)'], axis = 1, inplace = True)
#unplannedSet2021.drop(['Substation', 'Planned Incident ID', 'Circuit Type'], axis = 1, inplace = True)
#unplannedSet2021.dropna(axis = 0, subset = ['Street Name'], inplace = True)
#andoverSet = unplannedSet2021[unplannedSet2021['City/Town'] == "ANDOVER"].copy()

unplannedBig2021 = pd.read_csv(r"C:\Users\galta\Downloads\Copy of 2021_Big.xlsx - UnplannedSigOutagesRpt.csv.stem_andover_with_coords.csv")
#unplannedBig2021.drop(['Official Notified Name(1)', 'Official Notified Phone (1)', 'Official Notified Name (2)', 'Official Notified Phone (2)'], axis = 1, inplace = True)
#unplannedBig2021.drop(['Substation', 'Planned Incident ID', 'Circuit Type'], axis = 1, inplace = True)
#unplannedBig2021.dropna(axis = 0, subset = ['Street Name'], inplace = True)
#andoverSet = unplannedBig2021[unplannedBig2021['City/Town'] == "ANDOVER"].copy()

unplannedSet2022 = pd.read_csv(r"C:\Users\galta\Downloads\Copy of 2022_InsignificantOutages.xlsx - UnplannedInsigOutagesRpt.csv.stem_andover_with_coords.csv")
#unplannedSet2022.drop(['Official Notified Name(1)', 'Official Notified Phone (1)', 'Official Notified Name (2)', 'Official Notified Phone (2)'], axis = 1, inplace = True)
#unplannedSet2022.drop(['Substation', 'Planned Incident ID', 'Circuit Type'], axis = 1, inplace = True)
#unplannedSet2022.dropna(axis = 0, subset = ['Street Name'], inplace = True)
#andoverSet = unplannedSet2022[unplannedSet2022['City/Town'] == "ANDOVER"].copy()

unplannedBig2022 = pd.read_csv(r"C:\Users\galta\Downloads\Copy of 2022_Big.xlsx - UnplannedSigOutagesRpt.csv.stem_andover_with_coords.csv")
#unplannedBig2022.drop(['Official Notified Name(1)', 'Official Notified Phone (1)', 'Official Notified Name (2)', 'Official Notified Phone (2)'], axis = 1, inplace = True)
#unplannedBig2022.drop(['Substation', 'Planned Incident ID', 'Circuit Type'], axis = 1, inplace = True)
#unplannedBig2022.dropna(axis = 0, subset = ['Street Name'], inplace = True)
#andoverSet = unplannedBig2022[unplannedBig2022['City/Town'] == "ANDOVER"].copy()

andoverSet = pd.concat([smallSet, bigSet, unplannedSet2021, unplannedBig2021, unplannedSet2022, unplannedBig2022])

location = geolocator.geocode("River Street Andover MA")

map_object = folium.Map(location = [location.latitude, location.longitude])
map_object.save("map.html")

heatMapCoords = []

latitudes = []
longitudes = []

for i in tqdm.trange(len(andoverSet)):
    heatMapCoords.append([andoverSet.iloc[i]['Latitude'], andoverSet.iloc[i]['Longitude']])

HeatMap(heatMapCoords).add_to(map_object)
map_object.save("map.html")

newMapObject = folium.Map(location = [location.latitude, location.longitude])
newMapObject.save("dot_map.html")

streetName = []
coordinateList =[]

andoverSet['Count'] = 1

perStreetInfo = (
    andoverSet
    .groupby(['Street Name'])
    .aggregate({'Original # Customer Affected' : 'sum',
                'Count' : 'sum',
                'Latitude': 'first',
                'Longitude': 'first'})


)
# Now we can just loop over streets rather than outages
for street_name, street_info in (perStreetInfo.iterrows()):
    radius = street_info['Original # Customer Affected'] / 50 # rescale this if needed
    if radius < 30:
        radius= 30
    count = street_info['Count']
    if count > 100:
        color = "dark_red"
    elif count > 40:
        color = "red"
    elif count > 20:
        color = "yellow"
    else:
        color = "green"
    folium.Circle(
        location=[street_info['Latitude'], street_info['Longitude']],
        radius=radius,
        color="black",
        weight=1,
        fill_opacity=0.6,
        opacity=1,
        fill_color= color,
        fill=False,  # gets overridden by fill_color
        popup="People affected: " + str(street_info['Original # Customer Affected']),
        tooltip="Amount of outages: " + str(count),
    ).add_to(newMapObject)

streetNameCounts = andoverSet.groupby('Street Name').size().reset_index(name='Count')
print(streetNameCounts)
pd.set_option('display.max_rows', None)
print(perStreetInfo)
        

#print(streetName)

newMapObject.save("dot_map.html")

#print(perStreetInfo.groupby('Street Name').size().reset_index(name='Count'))
    
