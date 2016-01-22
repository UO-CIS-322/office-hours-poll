"""
Combine dumped poll results
"""

import arrow
import json 

# Mongo database
from pymongo import MongoClient
import CONFIG

CHOICES = [ { "day": "Tuesday",
              "periods": [ "11:30a", "12:00p", "12:30p", "1:00p", "1:30p",
                           "2:00p", "2:30p", "3:00p", "5:00p", "5:30p" ]}, 
            { "day": "Wednesday",
              "periods": [ "10:00a", "10:30a", "11:00a", "11:30a", "12:00p",
                           "2:30p", "3:00p", "3:30p", "4:00p", "4:30p", "5:00p",
                           "5:30p" ]}, 
            { "day": "Thursday",
              "periods": [ "9:00a", "9:30a", "11:30a", "12:00p", "12:30p", "1:00p", "1:30p",
                           "2:00p", "2:30p", "3:00p", "5:00p", "5:30p" ]}, 
            ]


counts  = { }
for day in CHOICES:
    dayname = day["day"]
    counts[dayname] = { }
    for period in day["periods"]:
        counts[dayname][period] = 0
try: 
    dbclient = MongoClient(CONFIG.MONGO_URL)
    db = dbclient.cis322
    collection = db.poll

except:
    print("Failure opening database.  Is Mongo running? Correct password?")
    sys.exit(1)

for record in collection.find( { "kind": "office hours poll" } ):
    print("***  {}".format(record["name"]))
    # del record['_id']
    # print(json.dumps(record, sort_keys=True, indent=4 ))
    times = record["times"]
    for dayname, periods in times.items():
        print("{} {}".format(dayname, periods))
        for period in periods:
            counts[dayname][period] += 1

# Dump in order from CHOICES
print("\n\n==SUMMARY==")
for day in CHOICES:
    dayname = day["day"]
    for period in day["periods"]:
        print("{} {}: {}".format(dayname,period, counts[dayname][period]))

