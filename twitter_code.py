# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 15:10:10 2020

@author: Fabio Roncato
"""
import tweepy
from twitter_credentials import *
from twitter_program_parameters import *


import geopandas
from shapely.geometry import Point
from geopy.geocoders import Nominatim
import os.path
import matplotlib.pyplot as plt



auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
user = api.me()
print("Stai utilizzando le credenziali dell'utente: " + user.name)


# if the geojson file is already present open it and append the new result. Otherwise create it
if(os.path.exists(filename)):
    gdf = geopandas.read_file(filename)
else:
    gdf = geopandas.GeoDataFrame(columns = ['id_str','user_id_str','user_screen_name','text','created_at',
                   'user_lang','user_location','longitude','latitude','geometry'])
geolocator = Nominatim(user_agent="my_application")


twitter_account_without_coordinate = 0 
new_twitter_user_added = 0
# Collect tweets
for tweet in tweepy.Cursor(api.search, q=search_words_no_retweet, lang="en", since=date_since).items(numberOfTweets):
    condition = tweet.id_str in gdf['id_str'].values # the tweet is already present
    
    if condition is False:
        if follow_user and tweet.user.id_str != user.id_str:
            api.create_friendship(tweet.user.id_str)
            print("friendship with " + tweet.user.screen_name)
        
        if(tweet.user.location is not None):
            location = geolocator.geocode(tweet.user.location)
            
        if(location is None):
            twitter_account_without_coordinate += 1
        else:               
            cleaned_text = tweet.text        
            new_row = {"id_str":tweet.id_str,"user_id_str":tweet.user.id_str,"user_screen_name":tweet.user.screen_name,
                       "text":cleaned_text,"created_at":tweet.created_at,"user_lang":tweet.user.lang,"user_location":tweet.user.location,
                       "longitude":location.longitude,"latitude":location.latitude,
                       "geometry":Point(location.longitude,location.latitude)}
    
            gdf = gdf.append(new_row, ignore_index = True)
            new_twitter_user_added += 1

print("new data from Twitter collected")


schema = geopandas.io.file.infer_schema(gdf)
schema['properties']['created_at'] = 'datetime'
gdf.to_file(filename, driver='GeoJSON', encoding="utf-8", schema = schema)

fig, ax = plt.subplots(figsize = (15,15))
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
world.plot(ax=ax, alpha = 0.4, column='pop_est', legend=True, legend_kwds={'label': "Twetter user by Country",
                                                                  'orientation': "horizontal"})
crs = {'init': 'epsg:4326'}
gdf.plot(ax=ax, markersize=5, color ='green')
plt.show()


print("twitter_account_without_coordinate: " + str(twitter_account_without_coordinate))
print("new_twitter_user_added: " + str(new_twitter_user_added))


#for tweet in tweepy.Cursor(api.search, search_strings).items(numberOfTweets):
#    print(tweet.text)

##for tweet in api.user_timeline("geeksforgeeks",count = numberOfTweets):
 ##   print(tweet.text)