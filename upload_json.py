from flask import Flask
from flask import render_template
from pymongo import MongoClient
import json
import os

from auth import MONGODB_URI

mongo_db_name = "stream2_project"
collection_name = "bob_dylan_songs"

with open("bob_dylan_songs.json", "r") as inFile:
    song_list = json.load(inFile)

song_list = list(song_list);

with MongoClient(MONGODB_URI) as conn:
    db = conn[mongo_db_name];
    collection = db[collection_name];
    collection.drop();
    collection.insert_many(song_list);


    
