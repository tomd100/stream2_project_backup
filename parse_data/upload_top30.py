import re
from pymongo import MongoClient
import json
import csv

from auth import MONGODB_URI

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def get_top_30():
    
    song_list = [];
    top_30_list = [];
    
    #--------------------------------------------------------------------------- 
    # Download all songs from mongodb
    
    song_list = list(download_mongo("bob_dylan_songs"))
    
    for song in song_list:
        if song["song_chart_pos"] != "-1":
            top_30_list.append(song)

    return top_30_list
    
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def upload_mongo(song_list):
    
    database_name = "stream2_project";
    collection_name= "top_30_songs";
    
    with MongoClient(MONGODB_URI) as conn:
        db = conn[database_name];
        collection = db[collection_name];
        existing_collections = db.collection_names();

        if collection_name in existing_collections:
            collection.drop();
       
        collection.insert_many(song_list)

# ------------------------------------------------------------------------------
        
def download_mongo(collection_name):
    
    database_name = "stream2_project";
    # collection_name= "bob_dylan_songs";
    
    fields = {'song_title': True, 'song_chart_pos': True, 'album': True, 'album_year': True, 
        'first_date': True, 'last_date': True, 'num_plays': True, '_id': False}
    
    with MongoClient(MONGODB_URI) as conn:
        db = conn[database_name];
        collection = db[collection_name];
        song_list = collection.find(projection=fields)
        song_list = list(song_list);
        
    return song_list

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

top_30_list = get_top_30()
upload_mongo(top_30_list)





                        
                    
