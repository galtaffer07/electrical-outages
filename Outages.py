import os
import pandas as pd
import matplotlib as plt
import folium
from geopy.geocoders import Bing


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

m = folium.Map(location = (location.latitude, location.longitude)).save("map.html")

smallSet['Street Name'] = smallSet['Street Name'] + "Andover MA 01810"
for i in range(len(smallSet.index)):
    print(geolocator.geocode(smallSet.iloc[i]['Street Name']))#.latitude, geolocator.geocode(smallSet.iloc[i]['Street Name']).longitude)



#WHERE I LEFT OFF: trying to figure out how to display the heat map - coordinates are wrong (one is from DRC) but most should be correct

                      
