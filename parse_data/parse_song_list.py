import re
from pymongo import MongoClient
import json

from auth import MONGODB_URI

# from get_album_list2 import 

# ------------------------------------------------------------------------------

def parse_text():
    
    album_list = [];
    song_list = []

    with open("../text_files/album_list.txt", "r") as albumFile:
        for line in albumFile:
            line = line[:-1]    # remove end-of-line char
            album_list.append(line);
    albumFile.close();

    with open("../text_files/bd_web_page_copy.txt", 'r') as inFile:
        
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
            
        #----------------------------------------------------------------------- 
            # Line now does not include the album name.
            # Find dates
            
            date_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            
            # Find first and second date, if they exist
            pos = find_dates(line);
            if pos == 0:
                dates = ""
                first_date = "";
                last_date = "";
            else:
                dates = line[pos:pos + 26]; 
                dates = dates.strip();                
                line = line.replace(dates, ' ');
                
                dates = dates.split(" ");
                dates = " ".join(dates[:3]), " ".join(dates[3:]);
                first_date = fix_date(dates[0]);
                last_date = fix_date(dates[1]);
                

        #----------------------------------------------------------------------- 
                # Search for album and remove if exists
                album = get_album(line);
            

            
        #----------------------------------------------------------------------- 
                 # grab chars befre the first space from end    
            
                rev_line = line[::-1];      # reverse the line
                end_chars = rev_line.split(" ",1);
    
            if end_chars[0].isdigit():
                num_plays = int(end_chars[0][::-1]);
                song_title = end_chars[1][::-1].strip();
            else:
                num_plays = 0;
                song_title = rev_line[1:][::-1].strip();    # strip off 0 char and reverse
            
        #----------------------------------------------------------------------- 
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

# ------------------------------------------------------------------------------

def find_dates(line):
    p1 = -1;
    p2 = -1
    pos = -1;
    date_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    
    for date in date_list:
        date = " " + date + " ";
        pos = line.find(date);
        if pos > -1:
            if p1 > pos or p1 == -1:
                p1 = pos; 

    if p1 > -1:
        for date in date_list:
            date = " " + date + " ";
            pos = line[p1 + 1:].find(date);
            if pos > -1:
                if p2 > pos or p2 == -1:
                    p2 = pos;
    if p2 == 12:
        return p1 + 1;
    else:
        return 0;

# ------------------------------------------------------------------------------


def fix_date(date):
    date_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    
    date = date.split(" ");
    
    month_text = date[0];    
    month = date_list.index(month_text) + 1; 
    if month < 10:
        month = "0" + str(month);
    else:
        month = str(month);
    
    day = date[1];
    day = day.split(",");
    day = day[0]
    
    year = date[2]
    
    new_date = day + "/" + month + "/" + year;

    return new_date;

    
# ------------------------------------------------------------------------------

def return_album(line):
    pos = -1;
    len_album = 0;

    for a in album_list:
        if line[:9] == "Bob Dylan":
            pos = line.find(a, 9); 
        else:
            pos = line.find(a, 3); 
        if pos > -1: 
            if len(a) > len_album:  # Some album names are also within larger album names
                len_album = len(a);
                album = a;
                
    if album != "":
        rev_line = line[::-1];
        rev_album = album[::-1];
        rev_line = rev_line.replace(rev_album, ' ', 1);
        line = rev_line[::-1];
    
    return album

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

# ------------------------------------------------------------------------------
        
def download_mongo():
    
    database_name = "stream2_project";
    collection_name= "bob_dylan_songs";
    
    with MongoClient(MONGODB_URI) as conn:
        db = conn[database_name];
        collection = db[collection_name];

        song_list = list(collection.find({}));
        
    return song_list

# ------------------------------------------------------------------------------

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
    print("\n")
    
    outFile = open("../text_files/song_list.txt", "+w")    
    song_list_sorted = list(song_set);
    song_list_sorted.sort()
    
    for x, song in enumerate(song_list_sorted):
        outFile.write(song);
        if x < len(song_list_sorted) - 1:
            outFile.write("\n");
    outFile.close()
    
    # Verify that all songs in top-30 are in overall song list
    
    song_list_import = [];
    top_30_list = [];
    
    with open("../text_files/song_list.txt", "r") as songFile:
        for line in songFile:
            song_list_import.append(line.strip());
    songFile.close();
    
    with open("../text_files/top_30_bd_tracks.txt", "r") as topFile:
        for line in topFile:
            line = line.split(",",1)
            top_30_list.append(line[1].strip());
    topFile.close();
    
    for song in top_30_list:
        if song not in song_list_import:
            print(song)
    return
# ------------------------------------------------------------------------------

song_list = parse_text();     
# upload_mongo(song_list);

# song_list = download_mongo();
# verify_data(song_list);




                        
                    
