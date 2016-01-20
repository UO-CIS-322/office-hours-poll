"""
Simple Flask web site 
"""

import flask
from flask import request  # Data from a submitted form
from flask import url_for
from flask import jsonify # For AJAX transactions

import json
import logging

###
# Globals
###
app = flask.Flask(__name__)
import CONFIG
app.secret_key = CONFIG.COOKIE_KEY  # Should allow using session variables

from pymongo import MongoClient
try: 
    dbclient = MongoClient(CONFIG.MONGO_URL)
    db = dbclient.cis322
except:
    print("Failure opening database.  Is Mongo running? Correct password?")
    sys.exit(1)


# Half-hour periods 
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
###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
  flask.g.choicegroups = CHOICES
  return flask.render_template('poll.html')

#######################
# Form handler.  
# CIS 322 (399se) note:
#   You'll need to change this to a
#   a JSON request handler
#######################

@app.route("/_choose", methods = ["POST"])
def enter():
  """
  Poll has been submitted 
  """
  app.logger.debug("Processing submission")

  ## Shovel form input into a structure that
  ## we can JSONify:  A dict of lists 
  results = { 'kind': "office hours poll",
              'name': "",
              'times': { }
              }
  results["name"] = request.form.get("name")
  for row in CHOICES: 
    avail = request.form.getlist(row["day"])
    results["times"][row["day"]] = avail

  app.logger.debug("Got form data: {}".format(results))
  result = db.poll.insert_one(results)  # See PyMongo initialization above
  app.logger.debug("ID of inserted object: {}".format(result.inserted_id))

  return flask.redirect(url_for("thanks"))

@app.route("/thanks")
def thanks():
  app.logger.debug("Thanks")
  return flask.render_template('thanks.html')

#################
# Functions used within the templates
#################

@app.template_filter( 'filt' )
def format_filt( something ):
    """
    Example of a filter that can be used within
    the Jinja2 code
    """
    return "Not what you asked for"
  
###################
#   Error handlers
###################
@app.errorhandler(404)
def error_404(e):
  app.logger.warning("++ 404 error: {}".format(e))
  return flask.render_template('404.html'), 404

@app.errorhandler(500)
def error_500(e):
   app.logger.warning("++ 500 error: {}".format(e))
   assert app.debug == False #  I want to invoke the debugger
   return flask.render_template('500.html'), 500

@app.errorhandler(403)
def error_403(e):
  app.logger.warning("++ 403 error: {}".format(e))
  return flask.render_template('403.html'), 403



#############

# Set up to run from cgi-bin script, from
# gunicorn, or stand-alone.
#

if __name__ == "__main__":
    # Standalone. 
    app.debug = True
    app.logger.setLevel(logging.DEBUG)
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
else:
    # Running from cgi-bin or from gunicorn WSGI server, 
    # which makes the call to app.run.  Gunicorn may invoke more than
    # one instance for concurrent service.
    #FIXME:  Debug cgi interface 
    app.debug=False

