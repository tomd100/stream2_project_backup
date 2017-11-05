from pymongo import MongoClient
import json
import csv

from auth import MONGODB_URI

mongo_db_name = "stream2_project"
collection_name = "top_30_tracks"

top_30_dict = {}
top_30_list = [];

with open('text_files/top_30_tracks.csv', newline ='') as inFile:
    reader = csv.reader(inFile, delimiter = ",", quoting=csv.QUOTE_NONE)
    for row in reader:
        top_30_dict["position"] = row[0];
        top_30_dict["song_title"] = row[1];
        top_30_list.append(top_30_dict.copy());

with MongoClient(MONGODB_URI) as conn:
    db = conn[mongo_db_name];
    collection = db[collection_name];
    collection.drop();
    collection.insert_many(list(top_30_list));
