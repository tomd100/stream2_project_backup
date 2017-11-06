from flask import Flask
from flask import render_template
from pymongo import MongoClient
import json
import os

from auth import MONGODB_URI

mongo_db_name = "stream2_project"
collection_name = "bob_dylan_songs"

fields = {'song_title': True, 'song_chart_pos': True, 'album': True, 'album_year': True, 'first_date': True, 'last_date': True, 'num_plays': True, '_id': False}

with MongoClient(MONGODB_URI) as conn:
    db = conn[mongo_db_name];
    collection = db[collection_name];
    song_list = collection.find(projection=fields, limit=55000);

song_list = list(song_list);
for song in song_list:
    if not song["last_date"][:1].isdigit() and song["last_date"] != "" :
        print(song["last_date"])
