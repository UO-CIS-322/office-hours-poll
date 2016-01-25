"""
Dump the MongoDB database as text
"""

# Mongo database
from pymongo import MongoClient
from bson.json_util import dumps

import CONFIG
try: 
    dbclient = MongoClient(CONFIG.MONGO_URL)
    db = dbclient.cis322
    collection = db.poll

except:
    print("Failure opening database.  Is Mongo running? Correct password?")
    sys.exit(1)


#
# Read database --- May be useful to see what is in there,
# even after you have a working 'insert' operation in the flask app,
# but they aren't very readable.  If you have more than a couple records,
# you'll want a loop for printing them in a nicer format. 
#

records = [ ] 
for record in collection.find( { "kind": "office hours poll" } ):
    print(dumps(record))

