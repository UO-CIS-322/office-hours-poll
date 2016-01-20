"""
Configuration of flask application.
Everything that could be different between running
on your development platform or on ix.cs.uoregon.edu
(or on a different deployment target) shoudl be here.
"""
DEBUG = True
PORT = 5000

# Cookie key was obtained by:
#   import uuid
#   str(uuid.uuid4())
# We do it just once so that multiple processes
# will share the same key. 
COOKIE_KEY = '0166c5c7-c4fc-4b20-9bcb-219733271fde'

### My local development environment
MONGO_PORT=27333 # On gnat, irian
DEBUG = True
MONGO_PW = "twfwif"
MONGO_USER = "instructor"
MONGO_URL = "mongodb://instructor:twfwif@localhost:27333/cis322"  # on Gnat
MONGO_NOAUTH_URL = "mongodb://localhost:27333"   #  Use with 'localhost exception', running MongoDB in 'noauth' mode
