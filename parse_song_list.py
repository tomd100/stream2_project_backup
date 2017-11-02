import re
from pymongo import MongoClient
import json

from auth import MONGODB_URI

# from get_album_list2 import 

def parse_text():
    
    album_list = [];
    song_list = []

    with open("./text_files/album_list.txt", "r") as albumFile:
        for line in albumFile:
            line = line[:-1]
            album_list.append(line);
    albumFile.close();

    with open("./text_files/bd_web_page_copy.txt", 'r') as inFile:
        
        for line in inFile:
            
            line = line[:-1]; # remove end-of-line char.            
            
            # print(line);
            
            song = {};
            
            song_title = "";
            album = "";
            dates = "";
            first_date = "";
            last_date = "";
            num_plays = 0;
            
            # Search for album and remove if exists
            pos = -1;
            len_album = 0;

            for a in album_list:
                pos = line.find(a);
                if pos > 0: # 0 and not -1 this is because a song may have the same name as an album
                    if len(a) > len_album:  # Some album names are also within larger album names
                        len_album = len(a);
                        album = a;

            if album != "":
                line = line.replace(album, ' ')   ;
            
            # Line now does not include the album name.
            # Find dates
            
            date_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            
            pos = -1;
            min_pos = -1;
            for date in date_list:
                date = " " + date + " "
                pos = line.find(date);
                if pos > -1:
                    if min_pos == -1:
                        min_pos = pos;
                    elif min_pos > pos:
                        min_pos = pos
                        
            if min_pos > -1:
                dates = line[min_pos:min_pos + 26];
                dates = dates.strip();
                
                line = line.replace(dates, ' '); 
                
                dates = dates.split(" ");
                dates = " ".join(dates[:3]), " ".join(dates[3:]);
                first_date = dates[0];
                last_date = dates[1];

            # grabn chars befre the first space from end    
            rev_line = line[::-1];      # reverse the line
            end_chars = rev_line.split(" ",1);

            if end_chars[0].isdigit():
                num_plays = int(end_chars[0][::-1]);
                song_title = end_chars[1][::-1].strip();
            else:
                num_plays = 0;
                song_title = rev_line[1:][::-1].strip();    # strip off 0 char and reverse

            # print("song: {0}".format(song_title));
            # print("album: {0}".format(album));
            # print("first date: {0}".format(first_date));
            # print("last date: {0}".format(last_date));
            # print("num plays: {0}".format(num_plays));
            # print("\n")

            song['song_title'] = song_title;
            song['album'] = album;
            song["first_date"] = first_date;
            song["last_date"] = last_date;
            song["num_plays"] = num_plays
                
            song_list.append(song);

    outFile = open("output.json", "+w")    
    outFile.write(json.dumps(song_list));
    outFile.close()
    
    inFile.close()
    return song_list



def upload_mongo(song_list):
    
    database_name = "stream2_project";
    collection_name= "bob_dylan_songs";
    
    with MongoClient(MONGODB_URI) as conn:
        db = conn[database_name];
        collection = db[collection_name];
        existing_collections = db.collection_names();

        if collection_name in existing_collections:
            collection.drop();
       
        outFile = open("output.json", "+w")    
        outFile.write(json.dumps(song_list));
        outFile.close()
         
        collection.insert_many(song_list)

        
def download_mongo():
    
    database_name = "stream2_project";
    collection_name= "bob_dylan_songs";
    
    with MongoClient(MONGODB_URI) as conn:
        db = conn[database_name];
        collection = db[collection_name];

        song_list = list(collection.find({}));
        
    return song_list

def verify_data(song_list):
    
    album_set = set();
    song_set = set();
    id_set = set();
    
    for song in song_list:
        album_set.add(song["album"]);
        song_set.add(song["song_title"]);
        id_set.add(song["_id"]);
    
    print("Total records: {0}".format(len(song_list)));    
    print("Total unique albums: {0}".format(len(album_set)));    
    print("Total unique songs: {0}".format(len(song_set)));    
    print("Total unique ids (mongo): {0}".format(len(id_set)));    
    
    return
        
song_list = parse_text();     
upload_mongo(song_list);

song_list = download_mongo();
verify_data(song_list);




                        
                    
