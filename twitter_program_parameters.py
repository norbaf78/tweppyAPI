# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 15:45:07 2020

@author: Fabio Roncato
"""
numberOfTweets = 1000


#follow_user = True
#search_words =""" (#MS OR #multiplesclerosis OR #ms OR #MultipleSclerosis OR #SclerosiMultipla OR
#                    #sclerosimultipla OR #SM OR #sm) AND ("#art" OR "#ART" OR "#Artwork" OR "#ARTWORK")"""
#filename = "tweet_ms_artwork.geojson"

follow_user = False
search_words =""" (#MS OR #multiplesclerosis OR #ms OR #MultipleSclerosis OR #SclerosiMultipla OR
                   #sclerosimultipla OR #SM OR #sm) """
filename = "tweet_ms.geojson"


search_words_no_retweet = search_words + " -filter:retweets"
date_since = "2019-09-01"
date_until = "2019-09-29"
