import re
import json



def parse_for_albums():
    
    album_set = set()

    with open("bd_web_page_copy.txt", 'r') as infile:
        
        upper = "[A-Z]"
        lower = "[a-z]"
        number = "[0-9]"
        
        for line in infile:
            
            album = "";
            
            # remove num plays and dates from end of line
            
            rev_line = line[::-1]; # reverse line
            rev_line = rev_line[1:] # remove "/n"
            
            if rev_line[0] == "0" and re.search(number,rev_line[1]) is None:
                rev_line = rev_line[1:];
            else:
                rev_line = rev_line.split(" ", 1)[1];
                rev_line = rev_line[25:];
            
            line = rev_line[::-1];    
            # print(line)
            
            album_pos = 0;
            x = 0;
            while x < len(line) - 1:
                if line[x] == "M" and line[x + 1] == "c":
                    x += 1; # move passed "Mc"
                elif re.search(lower,line[x]) and re.search(upper,line[x+1]):
                    album_pos = x + 1
                    album_name = line[album_pos:];
                    album_name = album_name.strip();
                    album_set.add(album_name);
                x += 1
            
    infile.close()
    #  additional albums to add to list. 
    album_set.add('“Love And Theft”');

    return album_set;

def check_for_other_albums(album_set):
    
    outFile = open("missing_albums.txt", "+w");
    
    with open("bd_web_page_copy.txt", 'r') as inFile:
        for line in inFile:
            pos = -1;
            found = 0;
            for album in album_set:
                pos = line.find(album)
                if pos > -1:
                    found = 1
            if found == 0:
                outFile.write(line);
        
    outFile.close();
    return;

album_set_1 = parse_for_albums()     

print(len(album_set_1));

for album in album_set_1:
    print(album)        
    
check_for_other_albums(album_set_1)  
print("check complete")
    


