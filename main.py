#from crypt import methods
from asyncio.windows_events import NULL
from pickle import GET
from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from pymongo import MongoClient
from flask_cors import CORS
import certifi
import plotly.express as px
import plotly.graph_objects as go
import csv
import copy

# Instantiation
app = Flask(__name__)


cluster = MongoClient("mongodb+srv://team1:team1@cluster0.pmmnz.mongodb.net/smallData?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = cluster["smallData"]
crimeData = db["smallCrime"]
team1 = cluster["team1"]
descriptionDb = team1["description"]
districtDb = team1["district"]
time = team1["time"]
weaponDb = team1["weapon"]
monthDb = team1["month"]
inoutDb = team1["inout"]
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

def createMonthChartData(weapon, crime, location, time, inout):
    
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    dataArr = []
    monthDict = {}
    if (crime == None or location == None or time == None or weapon == None or inout == None) or (crime == "NO_FILTER" and location == "NO_FILTER" and time =="NO_FILTER" and weapon =="NO_FILTER" and inout =="NO_FILTER"):
        data = monthDb.find({})
        for result in data:
            dataArr.append(result)
        monthDict = dataArr[0]
        del monthDict["_id"]
        del monthDict[""]
        print(monthDict)
    
    else:
        monthsDict = {"Weapon":weapon, "Description" : crime, "District" : location, "Inside_Outside" : inout, "Time" : time}
        deleted = []
        
        for m in monthsDict.keys():
            if months[m] == "NO_FILTER":
                deleted.append(m)
        for delete in deleted:
            del monthsDict[delete]

        for month in months:
            tempDict = copy.deepcopy(monthsDict)
            tempDict["Month"] = month
            monthDict[month] = len(list(master.find(tempDict)))

    return monthDict
    

def createTimeChartData(weapon, crime, location, inout, month):
    
    times = ["Morning","Late Night","Evening","Afternoon"]
    dataArr = []
    timeDict = {}
    if (crime == None or location == None or month == None or weapon == None or inout == None) or (crime == "NO_FILTER" and location == "NO_FILTER" and month =="NO_FILTER" and weapon =="NO_FILTER" and inout =="NO_FILTER"):
        data = time.find({})
        for result in data:
            dataArr.append(result)
        timeDict = dataArr[0]
        del timeDict["_id"]
        del timeDict[""]
        print(timeDict)
    
    else:
        timesDict = {"Weapon":weapon, "Description" : crime, "District" : location, "Inside_Outside" : inout, "Month":month}
        deleted = []
        
        for t in timesDict.keys():
            if times[t] == "NO_FILTER":
                deleted.append(t)
        for delete in deleted:
            del timesDict[delete]

        for timed in times:
            tempDict = copy.deepcopy(timesDict)
            tempDict["Time"] = timed
            timeDict[timed] = len(list(master.find(tempDict)))

    return timeDict

def createDistrictChartData(weapon, crime, time, inout, month):
    
    district = ["SOUTHEAST","EASTERN","SOUTHERN","CENTRAL","NORTHEAST","SOUTHWEST","NORTHWEST","NORTHERN","WESTERN"]
    dataArr = []
    districtDict = {}
    if (crime == None or time == None or month == None or weapon == None or inout == None) or (crime == "NO_FILTER" and time == "NO_FILTER" and month =="NO_FILTER" and weapon =="NO_FILTER" and inout =="NO_FILTER"):
        data = districtDb.find({})
        for result in data:
            dataArr.append(result)
        districtDict = dataArr[0]
        del districtDict["_id"]
        del districtDict[""]
        print(districtDict)
    
    else:
        districtsDict = {"Weapon":weapon, "Description" : crime, "Time":time, "Inside_Outside" : inout, "Month":month}
        deleted = []
        
        for d in districtsDict.keys():
            if districtsDict[d] == "NO_FILTER":
                deleted.append(d)
        for delete in deleted:
            del districtsDict[delete]

        for dis in district:
            tempDict = copy.deepcopy(districtsDict)
            tempDict["District"] = dis
            districtDict[dis] = len(list(master.find(tempDict)))

    return districtDict

def createDescriptionChartData(weapon, location, time, inout, month):
    
    description = ["LARCENY","LARCENY FROM AUTO","ROBBERY - COMMERCIAL","COMMON ASSAULT","AGG. ASSAULT","AUTO THEFT","BURGLARY","ROBBERY - STREET","ROBERT - RESIDENCE","ROBBERY - CARJACKING","SHOOTING","ARSON","RAPE","HOMICIDE"]
    dataArr = []
    descriptionDict = {}
    if (location == None or time == None or month == None or weapon == None or inout == None) or (location == "NO_FILTER" and time == "NO_FILTER" and month =="NO_FILTER" and weapon =="NO_FILTER" and inout =="NO_FILTER"):
        data = descriptionDb.find({})
        for result in data:
            dataArr.append(result)
        descriptionDict = dataArr[0]
        del descriptionDict["_id"]
        del descriptionDict[""]
        print(descriptionDict)
    
    else:
        descriptionsDict = {"Weapon":weapon, "District":location, "Time":time, "Inside_Outside" : inout, "Month":month}
        deleted = []
        
        for d in descriptionsDict.keys():
            if descriptionsDict[d] == "NO_FILTER":
                deleted.append(d)
        for delete in deleted:
            del descriptionsDict[delete]

        for d in description:
            tempDict = copy.deepcopy(descriptionsDict)
            tempDict["Description"] = d
            descriptionDict[d] = len(list(master.find(tempDict)))

    return descriptionDict

def createInOutChartData(weapon, crime, location, time, month):
    
    inout = ["Outside","Inside","I","O"]
    dataArr = []
    inoutDict = {}
    if (location == None or time == None or month == None or weapon == None or crime == None) or (location == "NO_FILTER" and time == "NO_FILTER" and month =="NO_FILTER" and weapon =="NO_FILTER" and crime =="NO_FILTER"):
        data = inoutDb.find({})
        for result in data:
            dataArr.append(result)
        inoutDict = dataArr[0]
        del inoutDict["_id"]
        del inoutDict[""]
        print(inoutDict)
    
    else:
        InOutDict = {"Weapon":weapon, "District":location, "Time":time, "Description" :crime, "Month":month}
        deleted = []
        
        for io in InOutDict.keys():
            if InOutDict[io] == "NO_FILTER":
                deleted.append(io)
        for delete in deleted:
            del InOutDict[delete]

        for io in inout:
            tempDict = copy.deepcopy(InOutDict)
            tempDict["Inside_Outside"] = io
            inoutDict[io] = len(list(master.find(tempDict)))

    return inoutDict


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
    if (crime == None or location == None or time == None or month == None or inout == None) or (crime == "NO_FILTER" and location == "NO_FILTER" and time =="NO_FILTER" and month=="NO_FILTER" and inout=="NO_FILTER"):
        data = weaponDb.find({})
        for result in data:
            dataArr.append(result)
        weaponDict = dataArr[0]
        del weaponDict["_id"]
        del weaponDict[""]
        print(weaponDict)

    else:
        weapons = {"Description" : crime, "District" : location, "Inside_Outside" : inout, "Time" : time, "Month" : month}
        deleted = []
        
        for w in weapons.keys():
            if weapons[w] == "NO_FILTER":
                deleted.append(w)
        for delete in deleted:
            del weapons[delete]
        
        for weapon in weaponsList:
            tempDict = copy.deepcopy(weapons)
            tempDict["Weapon"] = weapon
            weaponDict[weapon] = len(list(master.find(tempDict)))
        
        
    del weaponDict["NA"]


    # labels = []
    # values = []
    # print(weaponDict)
    # for item in weaponDict:
    #     print(item)
    #     labels.append(item)
    #     #values.append(weaponDict.get(item, default=None))

    # print(labels, values)
    # pieChart = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent',
    #                          insidetextorientation='radial'
    #                         )])
    # print(weaponDict)

    return weaponDict
    
if __name__ == "__main__":
    crimes = []
    crimeDataCol = crimeData.find({}).limit(2)
    for thing in crimeDataCol:
        crimes.append(thing)
    app.run(debug=True)
