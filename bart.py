import logging
from flask import Flask, render_template
from flask_ask import Ask, request, session, statement, question, convert_errors
from bart_trip import BartTrip
from station_codes import *
import dynamo

app = Flask(__name__)
AWS_ACCESS_KEY_ID = "AKIAIKJDRMFDXJ5PXPCA"
AWS_SECRET_ACCESS_KEY = "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"
ask = Ask(app, '/')
prefs = None

class NoHomeStationException(Exception):
    pass

def get_home_station():
    global prefs
    try:
        home_station = prefs['home_station'].lower()
        home_station_verify = station_name(home_station)
    except KeyError,Exception:
        raise NoHomeStationException

@ask.on_session_started
def new_session():
    global prefs
    t = dynamo.table('pogo_alexa_userinfo',(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY))
    key = 'bart:' + session.user.userId
    prefs = t[key]

@ask.intent('SetHomeStationIntent', convert={'station': station_code})
def set_home_station(station):
    global prefs
    prefs['home_station'] = station
    try:
        return statement("Home station set to {}".format(station_name(station)))
    except Exception:
        return question("Sorry, I don't recognize the station name {}. Can you try again?".format(station))
    
if __name__=='__main__':
    app.run(debug=True)

