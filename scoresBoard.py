# Read and write scores record with JSON

import json

def new_score(name, time) :
    player = {
        "name" : name,
        "time" : time
    }

    updat_record(player)

def updat_record(player, file = "scores.json") :    # Do we want to hard code the file name?
    with open(file, "r+") as scores :
        record = json.load(scores)
        insert_sorted_score(record, player)
        scores.seek(0)
        print("test")
        print(record, scores)
        json.dump(record, scores)
        scores.close

def insert_sorted_score(record, player) :
    count = 0
    for ele in record :
        if ele["time"] < player["time"] :
            count += 1
        else :
            break
    record.insert(count, player)

    for ele in record :
        print(ele["name"] + ": " + str(ele["time"]))
    

# Run newScore("name", score) in server.py to add new record
new_score("someone else", 3)

#/////////////////////////////////////////////////////////////////////////////#

def print_top_record(file = "scores.json") :
    with open(file, "r") as scores :
        record = json.load(scores)
        rank = ["First", "Second", "Third"]

        for i in range(0, 3) :
            print(rank[i] + " place: " + record[i]["name"] 
            + " in " + str(record[i]["time"]) + " seconds!\n")
        scores.close

# Run printTopRecord() in server.py to display top 3 winners
print_top_record()
