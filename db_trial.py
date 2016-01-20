"""
Just to test database functions,
outside of Flask.

We want to open our MongoDB database,
insert a record, and read it back 
"""
# import arrow

# Mongo database
from pymongo import MongoClient
import CONFIG
try: 
    dbclient = MongoClient(CONFIG.MONGO_URL)
    db = dbclient.cis322
    collection = db.sample

except:
    print("Failure opening database.  Is Mongo running? Correct password?")
    sys.exit(1)

#
# Insertions:  I commented these out after the first
# run successfuly inserted them
# 

record = { "type": "sample", 
           "text": "This is the text I want to insert"
          }
collection.insert(record)

#
# Read database --- May be useful to see what is in there,
# even after you have a working 'insert' operation in the flask app,
# but they aren't very readable.  If you have more than a couple records,
# you'll want a loop for printing them in a nicer format. 
#

records = [ ] 
for record in collection.find( { "type": "sample" } ):
   records.append(
        { "type": record['type'],
           "text": record['text']
    })

print(records)
