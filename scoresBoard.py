# Read and write scores record with JSON

import json

def newScore(name, time) :
    player = {
        "name" : name,
        "time" : time
    }

    updateRecord(player)

def updateRecord(player, file = "scores.json") :    # Do we want to hard code the file name?
    with open(file, "r+") as scores :
        record = json.load(scores)
        insertSortedScore(record, player)
        scores.seek(0)
        json.dump(record, scores)
        scores.close

def insertSortedScore(record, player) :
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
newScore("mazeRunner", 8)

#/////////////////////////////////////////////////////////////////////////////#

def printTopRecord(file = "scores.json") :
    with open(file, "r") as scores :
        record = json.load(scores)
        rank = ["First", "Second", "Third"]

        for i in range(0, 3) :
            print(rank[i] + " place: " + record[i]["name"] 
            + " in " + str(record[i]["time"]) + " seconds!\n")
        scores.close

# Run printTopRecord() in server.py to display top 3 winners
printTopRecord()
