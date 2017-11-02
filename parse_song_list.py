import re
from flask import Flask, request, render_template
from pymongo import MongoClient
import os
import tweepy
import json

from auth import MONGODB_URI

# from get_album_list2 import 

def parse_text():
    
    album_list = [];
    number = "[0-9]"
    
    with open("./text_files/album_list.txt", "r") as albumFile:
        for line in albumFile:
            line = line[:-1]
            album_list.append(line);
    albumFile.close();
    
    song_list = []

    with open("./text_files/bd_web_page_copy.txt", 'r') as inFile:
        for line in inFile:
            
            song = {}
            
            song_title = "";
            album = "";
            dates = "";
            first_date = "";
            last_date = "";
            num_plays = 0;
            
            # capture album if it exists. 
        # for line in inFile:
        #     pos = -1;
        #     found = 0;
        #     for album in album_set:
        #         pos = line.find(album)
        #         if pos > -1:
        #             found = 1
        #     if found == 0:
        #         outFile.write(line);

            pos = -1;
            for a in album_list:
                pos = line.find(a)
                print(pos)
                if pos > -1:
                    print("found")
                    album = a;
            print(album)
            
            if album != "":
                line = line.replace(album, '')            
            # print(line);
            
            rev_line = line[::-1];      # reverse the line 
            rev_line = rev_line[1:]     # remove end-of-line char 

            if rev_line[0] == "0" and re.search(number,rev_line[1]) is None:
                num_plays = 0;
                dates = "";
                rev_line = rev_line[1:];
            else:
                # print(rev_line)
                # num_plays = int(rev_line.split(" ",1)[0]);  # Find first space after number of plays
                rev_line = rev_line.split(" ", 1)[1];       
                dates = rev_line[:25];
                rev_line = rev_line[25:];
                line = rev_line[::-1];
                
                dates = dates[::-1];
                dates = dates.split(" ");
                dates = " ".join(dates[:3]), " ".join(dates[3:]);
                first_date = dates[0];
                last_date = dates[1];

            # print("song: {0}".format(song_title, album, dates, num_plays))
            # print("album: {1}".format(song_title, album, dates, num_plays))
            # print("dates: {2}".format(song_title, album, dates, num_plays))
            # print("num plays: {3}".format(song_title, album, dates, num_plays))
        

            # song['song_title'] = song_title;
            # song['album'] = album;
            # song["first_date"] = first_date;
            # song["last_date"] = last_date;
            # song["num_plays"] = num_plays
                
            song_list.append(song);

            
            # outFile.write(song_title + ",");
            # outFile.write(album + ",");
            # outFile.write(first_date + ",");
            # outFile.write(last_date + ",");
            # outFile.write(str(num_plays)); 
            # outFile.write("\n");
    
    # outFile = open("output.json", "+w")    
    # outFile.write(json.dumps(song_list));
    # outFile.close()
    
    # print (song_list)
    
    inFile.close()
    return song_list



def load_mongo(song_list):
    
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
        
        
song_list = parse_text()     
# print(song_list)
# load_mongo(song_list)
                        
                    
