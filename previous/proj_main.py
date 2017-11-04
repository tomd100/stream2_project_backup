from flask import Flask, request, render_template
from pymongo import MongoClient
import json

from auth import get_api, MONGODB_URI
from add_mongo import serachTwitter

   
database_name = "stream2_project";
collection_name= "bob_dylan_songs";

with MongoClient(MONGODB_URI) as conn:
    db = conn[database_name];
    collection = db[collection_name];
    existing_collections = db.collection_names();



app = Flask(__name__)

previous_searches = set()


@app.route("/")
def show_search_page():
    return render_template("search.html")

@app.route("/search")
def do_search():
    q = request.args.get('query')
    n = int(request.args.get('num'))
    
    previous_searches.add(q)
    
    # search twitter
    tweets = get_by_search(q, n)
    
    DBS_NAME = "tweets"
    COLLECTION_NAME = q
    
    # with MongoClient(MONGODB_URI) as conn:
    # 	collection = conn[DBS_NAME][COLLECTION_NAME]
    # 	collection.insert_many(tweets)

    with MongoClient(MONGODB_URI) as conn:
        db = conn[MONGO_DB_NAME]
        collection = db[q]
        collections_we_have = db.collection_names()
        
        # Search Twitter    
        if q in collections_we_have:
            #Get it from Mongo
            tweets = collection.find()
        else:
            #Get it from Twitter and save to Mongo
            print(n)
            tweets = get_by_search(q, n)
            collection.insert_many(tweets)
            
    return render_template("results.html", searched_for=q, the_tweets=tweets)
    
@app.route("/previous")
def show_previous():
    return render_template("previous.html", search_terms = previous_searches)
    

if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
    


