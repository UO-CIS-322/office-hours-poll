"""
Combine dumped poll results
"""

import arrow
import json 

# Mongo database
from pymongo import MongoClient
import CONFIG

from choices import CHOICES


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

record_count = 0
for record in collection.find( { "kind": "office hours poll" } ):
    name = record["name"]
    print("***  {}".format(name))
    if 'TEST' in name or 'test' in name:
        print("    Skipping {}".format(record["name"]))
        continue
    record_count += 1
    # del record['_id']
    # print(json.dumps(record, sort_keys=True, indent=4 ))
    times = record["times"]
    for dayname, periods in times.items():
        print("{} {}".format(dayname, periods))
        for period in periods:
            counts[dayname][period] += 1

print("\n== {} responses ==".format(record_count))
# Dump in order from CHOICES
print("\n==SUMMARY==")
for day in CHOICES:
    dayname = day["day"]
    for period in day["periods"]:
        print("{} {}: {}".format(dayname,period, counts[dayname][period]))

