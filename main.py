from flask import Flask
from flask import render_template
from pymongo import MongoClient
import json
import os

from auth import MONGODB_URI

app = Flask(__name__)

# mongo_host = 'localhost'
# mongo_port = 43805

# dbs_name = 'stream2_project'
# collection_name = 'bob_dylan_songs'

# mongodb_uri = os.environ.get('mongodb_uri')
dbs_name = os.environ.get('mongo_db_name','stream2_project')
collection_name = os.environ.get('mongo_collection_name','bob_dylan_songs')

fields = {'song_title': True, 'song_chart_pos': True, 'album': True, 'album_year': True, 'first_date': True, 'last_date': True, 'num_plays': True, '_id': False}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/songs")
def bob_dylan_songs():
    with MongoClient(MONGODB_URI) as conn:
        # define which collection we wish to access
        collection = conn[dbs_name][collection_name]
        # retrieve a result set only with the fields defined in fields
        # and limit the the results to 55000
        songs = collection.find(projection=fields, limit=55000)
        # convert projects to a list in a json object and return the json data
        return json.dumps(list(songs))

if __name__ == "__main__":
    app.run(host=os.getenv('ip', '0.0.0.0'),port=int(os.getenv('port', 8080)))