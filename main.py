#from crypt import methods
from asyncio.windows_events import NULL
from pickle import GET
from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from pymongo import MongoClient
from flask_cors import CORS
import certifi
import csv

# Instantiation
app = Flask(__name__)


cluster = MongoClient("mongodb+srv://team1:team1@cluster0.pmmnz.mongodb.net/smallData?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = cluster["smallData"]
crimeData = db["smallCrime"]
team1 = cluster["team1"]
description = team1["description"]
district = team1["district"]
time = team1["time"]
weaponDb = team1["weapon"]
# Settings
CORS(app)

# Routes

@app.route('/')
def index():
    return render_template("home.html", crimes=crimes)

@app.route('/home')
def home():

    return render_template("home.html", crimes=crimes)
    
@app.route('/map')
def map():
    return render_template("map.html", crimes=crimes)

@app.route('/data')
def data():
    formFilters = []
    formFilters.append(request.form.get("crime"))
    formFilters.append(request.form.get("weapon"))
    formFilters.append(request.form.get("location"))
    formFilters.append(request.form.get("time"))
    weaponStat = createPieChartData(formFilters[0], formFilters[1], formFilters[2], formFilters[3])
    return render_template("data.html", crimes=crimes, formFilters=formFilters, weaponStat = weaponStat)

@app.route('/addDataFilter', methods=["POST"])
def addDataFilter():
    formFilters = []
    formFilters.append(request.form.get("crime"))
    formFilters.append(request.form.get("weapon"))
    formFilters.append(request.form.get("location"))
    formFilters.append(request.form.get("time"))

    weaponStat = createPieChartData(formFilters[0], formFilters[1], formFilters[2], formFilters[3])
    return render_template("data.html", crimes=crimes, formFilters=formFilters, weaponStat = weaponStat)

def createPieChartData(crime, weapon, location, time):
    crimeStats = []

    if((crime == None or crime == "NO_FILTER") and
        (weapon == None or weapon == "NO_FILTER") and 
        (location == None or location == "NO_FILTER") and 
        (time == None or time == "NO_FILTER")):
        crimeData = weaponDb.find({})
        test = []
        for item in crimeData:
           test.append(item)
        
        counter =0
        theLoop = test[0]
        for key in theLoop:
            if counter != 0:
                crimeStats.append(int(theLoop.get(key)))
            counter += 1

    return crimeStats

if __name__ == "__main__":
    crimes = []
    crimeDataCol = crimeData.find({}).limit(2)
    for thing in crimeDataCol:
        crimes.append(thing)
    app.run(debug=True)
