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
filtered = team1["Filtered"]
master = team1["Master"]
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
    crime = request.form.get("crime")
    weapon = request.form.get("weapon")
    location = request.form.get("location")
    time = request.form.get("time")
    month = request.form.get("month")
    inout = request.form.get("inside/outside")
    weaponDict = createPieChartData(crime, location, time, month, inout)
    return render_template("data.html", weaponDict = weaponDict)
    
@app.route('/addDataFilter', methods=["POST"])
def addDataFilter():
    crime = request.form.get("crime")
    weapon = request.form.get("weapon")
    location = request.form.get("location")
    time = request.form.get("time")
    month = request.form.get("month")
    inout = request.form.get("inside/outside")
    weaponDict = createPieChartData(crime, location, time, month, inout)
    return render_template("data.html", weaponDict = weaponDict)

def createPieChartData(crime, location, time, month, inout):
    """ NO_FILTER """
    """ weaponsList = ["HANDGUN", "BLUNT_OBJECT", "PERSONAL_WEAPONS", "FIREARM", "ASPHYXIATION", "KNIFE_CUTTING_INSTRUMENT", "OTHER","SHOTGUN", "UNKNOWN", "AUTOMATIC_FIREARM", "AUTOMATIC HANDGUN", "OTHER_FIREMARM","MOTOR_VEHICLE_VESSEL","RIFLE","NA"] """
    weaponsList = ["HANDGUN", "BLUNT_OBJECT", "PERSONAL_WEAPONS", "FIREARM", "ASPHYXIATION", "KNIFE_CUTTING_INSTRUMENT", "OTHER" , "SHOTGUN", "UNKNOWN", "AUTOMATIC_FIREARM", "AUTOMATIC HANDGUN", "OTHER_FIREMARM","MOTOR_VEHICLE_VESSEL","RIFLE","NA","POISON","FIRE_INCENDIARY_DEVICE","KNIFE","FIRE","HANDS","AUTOMATIC_RIFLE","DRUGS_NARCOTICS_SLEEPING_PILLS"]
    dataArr = []
    weaponDict = {}
    print(crime)
    print(location)
    print(time)
    print(month)
    print(inout)
    if crime == None or location == None or time == None or month == None or inout == None:
        data = weaponDb.find({})
        for result in data:
            dataArr.append(result)
        weaponDict = dataArr[0]
        del weaponDict["_id"]
        del weaponDict[""]
        del weaponDict["NA"]

    else:
        weaponDict = master.find({})
        for weapon in weaponsList:
            weaponDict[weapon] = len(list(master.find({"Weapon" : weapon, "Description" : crime, "District" : location, "Inside_Outside" : inout, "Time" : time, "Month" : month})))
            
    print(weaponDict)

    return weaponDict
    # if((crime == None or crime == "NO_FILTER") and
    #     (weapon == None or weapon == "NO_FILTER") and 
    #     (location == None or location == "NO_FILTER") and 
    #     (time == None or time == "NO_FILTER")):
    #     crimeData = weaponDb.find({})
    #     test = []
    #     for item in crimeData:
    #        test.append(item)
        
    #     counter =0
    #     theLoop = test[0]
    #     for key in theLoop:
    #         if counter != 0:
    #             crimeStats.append(int(theLoop.get(key)))
    #         counter += 1

    # return crimeStats

if __name__ == "__main__":
    crimes = []
    crimeDataCol = crimeData.find({}).limit(2)
    for thing in crimeDataCol:
        crimes.append(thing)
    app.run(debug=True)
