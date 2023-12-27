import os
import pandas as pd
import matplotlib as plt
import folium
from geopy.geocoders import Bing
from folium.plugins import HeatMap


geolocator = Bing(api_key="AqjmiNHvJvjQEzYWYWsorqP7jC-F741tsJ7RsNM9Fxs_sSaR6ieRJbAAJBbZgkVb")

smallSet = pd.read_csv(r"C:\Users\galta\Downloads\Insignificant_16_17_18_19_20.xlsx - Small_16_17_18_19_20.csv")
smallSet.drop(['Official Notified Name(1)', 'Official Notified Phone (1)', 'Official Notified Name (2)', 'Official Notified Phone (2)'], axis = 1, inplace = True)
pd.set_option('display.max.columns', None)
print(smallSet)
smallSet.drop(['Substation', 'Planned Incident ID', 'Circuit Type'], axis = 1, inplace = True) #axis = 1 means columns, axis = 0 means rows, inplace means if it's editing itself

print(smallSet)

smallSet.dropna(axis = 0, subset = ['Street Name'], inplace = True) #removes rows in which certain streets are NaN

smallSet = smallSet[smallSet['City/Town'].str.contains("andover", case = False)].copy() #will work on this later - certain streets are listed as NaN, need to fix to move on - EDIT: fixed
print(smallSet)


location = geolocator.geocode("River Street Andover MA")
print(location.latitude, location.longitude)

print(smallSet.iloc[1]['Street Name'])

map_object = folium.Map(location = [location.latitude, location.longitude])
map_object.save("map.html")
map_object


heatMapCoords = []


#xCoords = []
#yCoords = []

smallSet['Street Name'] = smallSet['Street Name'] + " Andover MA 01810"
for i in range(len(smallSet)):
    #print((geolocator.geocode(smallSet.iloc[i]['Street Name']).latitude),(geolocator.geocode(smallSet.iloc[i]['Street Name']).longitude))
    rowCoords = [geolocator.geocode(smallSet.iloc[i]['Street Name']).latitude, geolocator.geocode(smallSet.iloc[i]['Street Name']).longitude]
    heatMapCoords.append(rowCoords)
    #xCoords.append(geolocator.geocode(smallSet.iloc[i]['Street Name']).latitude)
    #yCoords.append(geolocator.geocode(smallSet.iloc[i]['Street Name']).longitude)

#heatMapCoords = [xCoords, yCoords]

print("START HERE")

testData = [
    [42.6163209, -71.1542474],
    [42.62123777, -71.14677463],
    [42.70494602, -71.13411734],
    [42.64060632, -71.14474505],
    [42.65934982, -71.18007087],
]

HeatMap(heatMapCoords).add_to(map_object)
map_object.save("map.html")
