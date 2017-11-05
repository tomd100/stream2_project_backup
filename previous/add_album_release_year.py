import re
from pymongo import MongoClient
import json

from auth import MONGODB_URI

def add_album_release_year():
    
    album_list = []
    album_years = []
    
    with open("../text_files/album_list.txt", "r") as albumFile:
        for line in albumFile:
            line = line[:-1]    # remove end-of-line char
            line = line.strip();
            album_list.append(line);
    albumFile.close();
    
    with open("../text_files/album_release_years.txt", "r") as albumFile:
        for line in albumFile:
            line = line[:-1]    # remove end-of-line char
            pos = line.find("(");
            album = line[:pos];
            album = album.strip();
            
            album_year = line[pos:]
            album_year = album_year[1:5]
            
            album_years.append((album, album_year))
    albumFile.close();
    
    outFile = open("../text_files/album_with_years.txt", "+w")
    for album in album_list:
        for album_year in album_years:
            if album.lower() == album_year[0].lower():
                outFile.write(album + "|" + album_year[1]);
                outFile.write("\n");
                
add_album_release_year()    

    