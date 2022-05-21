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
timeDb = team1["time"]
weaponDb = team1["weapon"]
monthDb = team1["month"]
inoutDb = team1["inout"]
filtered = team1["Filtered"]
master = team1["Master"]
neighborhoodDb = team1["neighborhood"]
historyDb = team1["history"]
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
    monthDict = createMonthChartData(crime, location, time, weapon, inout)
    inoutDict = createInOutChartData(crime, location, time, weapon, month)
    districtDict = createDistrictChartData(crime, inout, time, weapon, month)
    descriptionDict = createDescriptionChartData(location, inout, time, weapon, month)
    timeDict = createTimeChartData(location, inout, crime, weapon, month)
    neighborhoodDict = createNeighborhoodData()
    historyDict = createHistoryData()
    return render_template("data.html", weaponDict = weaponDict, monthDict = monthDict, inoutDict = inoutDict, districtDict = districtDict, descriptionDict = descriptionDict, timeDict = timeDict, neighborhoodDict = neighborhoodDict, historyDict = historyDict)
    
@app.route('/addDataFilter', methods=["POST"])
def addDataFilter():
    crime = request.form.get("crime")
    weapon = request.form.get("weapon")
    location = request.form.get("location")
    time = request.form.get("time")
    month = request.form.get("month")
    inout = request.form.get("inside/outside")
    weaponDict = createPieChartData(crime, location, time, month, inout)
    monthDict = createMonthChartData(crime, location, time, weapon, inout)
    inoutDict = createInOutChartData(crime, location, time, weapon, month)
    districtDict = createDistrictChartData(crime, inout, time, weapon, month)
    descriptionDict = createDescriptionChartData(location, inout, time, weapon, month)
    timeDict = createTimeChartData(location, inout, crime, weapon, month)
    neighborhoodDict = createNeighborhoodData()
    historyDict = createHistoryData()
    return render_template("data.html", weaponDict = weaponDict, monthDict = monthDict, inoutDict = inoutDict, districtDict = districtDict, descriptionDict = descriptionDict, timeDict = timeDict, neighborhoodDict = neighborhoodDict, historyDict = historyDict)

def createMonthChartData(crime, location, time, weapon, inout):
    
    monthsList = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    dataArr = []
    monthDict = {}
    if (crime == None or location == None or time == None or weapon == None or inout == None) or (crime == "NO_FILTER" and location == "NO_FILTER" and time =="NO_FILTER" and weapon =="NO_FILTER" and inout =="NO_FILTER"):
        data = monthDb.find({})
        for result in data:
            dataArr.append(result)
        monthDict = dataArr[0]
        del monthDict["_id"]
    
    else:
        months = {"Weapon":weapon, "Description" : crime, "District" : location, "Inside_Outside" : inout, "Time" : time}
        deleted = []
        
        for m in months.keys():
            if months[m] == "NO_FILTER":
                deleted.append(m)
        for delete in deleted:
            del months[delete]

        for month in monthsList:
            tempDict = copy.deepcopy(months)
            tempDict["Month"] = month
            monthDict[month] = len(list(master.find(tempDict)))

    return monthDict
    

def createTimeChartData(location, inout, crime, weapon, month):
    
    timeList = ["Morning","Late Night","Evening","Afternoon"]
    dataArr = []
    timeDict = {}
    if (crime == None or location == None or month == None or weapon == None or inout == None) or (crime == "NO_FILTER" and location == "NO_FILTER" and month =="NO_FILTER" and weapon =="NO_FILTER" and inout =="NO_FILTER"):
        data = timeDb.find({})
        for result in data:
            dataArr.append(result)
        timeDict = dataArr[0]
        del timeDict["_id"]
    
    else:
        times = {"Weapon":weapon, "Description" : crime, "District" : location, "Inside_Outside" : inout, "Month":month}
        deleted = []
        
        for t in times.keys():
            if times[t] == "NO_FILTER":
                deleted.append(t)
        for delete in deleted:
            del times[delete]

        print(times)
        for tm in timeList:
            tempDict = copy.deepcopy(times)
            tempDict["Time"] = tm
            timeDict[tm] = len(list(master.find(tempDict)))

    print(len(list(master.find({"District" : "SOUTHEAST", "Time": "Morning"}))))
    return timeDict

def createDistrictChartData(crime, inout, time, weapon, month):
    
    districtList = ["SOUTHEAST","EASTERN","SOUTHERN","CENTRAL","NORTHEAST","SOUTHWEST","NORTHWEST","NORTHERN","WESTERN"]
    dataArr = []
    districtDict = {}
    if (crime == None or time == None or month == None or weapon == None or inout == None) or (crime == "NO_FILTER" and time == "NO_FILTER" and month =="NO_FILTER" and weapon =="NO_FILTER" and inout =="NO_FILTER"):
        data = districtDb.find({})
        for result in data:
            dataArr.append(result)
        districtDict = dataArr[0]
        del districtDict["_id"]
        del districtDict[""]
    
    else:
        districts = {"Weapon":weapon, "Description" : crime, "Time":time, "Inside_Outside" : inout, "Month":month}
        deleted = []
        
        for d in districts.keys():
            if districts[d] == "NO_FILTER":
                deleted.append(d)
        for delete in deleted:
            del districts[delete]

        for dis in districtList:
            tempDict = copy.deepcopy(districts)
            tempDict["District"] = dis
            districtDict[dis] = len(list(master.find(tempDict)))

    return districtDict

def createDescriptionChartData(location, inout, time, weapon, month):
    
    descriptionList = ["LARCENY","LARCENY FROM AUTO","ROBBERY - COMMERCIAL","COMMON ASSAULT","AGG. ASSAULT","AUTO THEFT","BURGLARY","ROBBERY - STREET","ROBERT - RESIDENCE","ROBBERY - CARJACKING","SHOOTING","ARSON","RAPE","HOMICIDE"]
    dataArr = []
    descriptionDict = {}
    if (location == None or time == None or month == None or weapon == None or inout == None) or (location == "NO_FILTER" and time == "NO_FILTER" and month =="NO_FILTER" and weapon =="NO_FILTER" and inout =="NO_FILTER"):
        data = descriptionDb.find({})
        for result in data:
            dataArr.append(result)
        descriptionDict = dataArr[0]
        del descriptionDict["_id"]
    
    else:
        descriptions = {"Weapon":weapon, "District":location, "Time":time, "Inside_Outside" : inout, "Month":month}
        deleted = []
        
        for d in descriptions.keys():
            if descriptions[d] == "NO_FILTER":
                deleted.append(d)
        for delete in deleted:
            del descriptions[delete]

        for d in descriptionList:
            tempDict = copy.deepcopy(descriptions)
            tempDict["Description"] = d
            descriptionDict[d] = len(list(master.find(tempDict)))

    return descriptionDict

def createInOutChartData(crime, location, time, weapon, month):
    
    inoutList = ["Outside","Inside","NA"]
    dataArr = []
    inoutDict = {}
    if (location == None or time == None or month == None or weapon == None or crime == None) or (location == "NO_FILTER" and time == "NO_FILTER" and month =="NO_FILTER" and weapon =="NO_FILTER" and crime =="NO_FILTER"):
        data = inoutDb.find({})
        for result in data:
            dataArr.append(result)
        inoutDict = dataArr[0]
        del inoutDict["_id"]
        del inoutDict[""]
    
    else:
        inout = {"Weapon":weapon, "District":location, "Time":time, "Description" :crime, "Month":month}
        deleted = []
        
        for io in inout.keys():
            if inout[io] == "NO_FILTER":
                deleted.append(io)
        for delete in deleted:
            del inout[delete]

        for io in inoutList:
            tempDict = copy.deepcopy(inout)
            tempDict["Inside_Outside"] = io
            inoutDict[io] = len(list(master.find(tempDict)))

    return inoutDict


def createPieChartData(crime, location, time, month, inout):
    """ NO_FILTER """
    """ weaponsList = ["HANDGUN", "BLUNT_OBJECT", "PERSONAL_WEAPONS", "FIREARM", "ASPHYXIATION", "KNIFE_CUTTING_INSTRUMENT", "OTHER","SHOTGUN", "UNKNOWN", "AUTOMATIC_FIREARM", "AUTOMATIC HANDGUN", "OTHER_FIREMARM","MOTOR_VEHICLE_VESSEL","RIFLE","NA"] """
    weaponsList = ["HANDGUN", "BLUNT_OBJECT", "PERSONAL_WEAPONS", "FIREARM", "ASPHYXIATION", "KNIFE_CUTTING_INSTRUMENT", "OTHER" , "SHOTGUN", "UNKNOWN", "AUTOMATIC_FIREARM", "AUTOMATIC HANDGUN", "OTHER_FIREMARM","MOTOR_VEHICLE_VESSEL","RIFLE","NA","POISON","FIRE_INCENDIARY_DEVICE","KNIFE","FIRE","HANDS","AUTOMATIC_RIFLE","DRUGS_NARCOTICS_SLEEPING_PILLS"]
    dataArr = []
    weaponDict = {}

    if (crime == None or location == None or time == None or month == None or inout == None) or (crime == "NO_FILTER" and location == "NO_FILTER" and time =="NO_FILTER" and month=="NO_FILTER" and inout=="NO_FILTER"):
        data = weaponDb.find({})
        for result in data:
            dataArr.append(result)
        weaponDict = dataArr[0]
        del weaponDict["_id"]
        del weaponDict[""]

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


    return weaponDict


def createNeighborhoodData():
    neighborhoodList = []
    #CENTRAL PARK HEIGHTS,WEST ARLINGTON,LAKELAND,MILLHILL,REMINGTON,OLIVER,HOWARD PARK,WOODBERRY,MONDAWMIN,RAMBLEWOOD,UNION SQUARE,EDMONDSON VILLAGE,MADISON PARK,INNER HARBOR,HANLON-LONGWOOD,FELLS POINT,CARE,MOUNT HOLLY,MIDTOWN-EDMONDSON,BROOKLYN,ABELL,BARCLAY,WAVERLY,GWYNNS FALLS,MCELDERRY PARK,PERRING LOCH,OLDTOWN,POPPLETON,GLENHAM-BELHAR,HARLEM PARK,WESTPORT,CURTIS BAY,YALE HEIGHTS,DRUID HEIGHTS,CANTON INDUSTRIAL AREA,LOCH RAVEN,BELAIR-EDISON,CEDARCROFT,HIGHLANDTOWN,SETON BUSINESS PARK,PEN LUCY,,PARKVIEW/WOODBROOK,CHERRY HILL,FEDERAL HILL,RESERVOIR HILL,CEDONIA,ALLENDALE,WEST FOREST PARK,WINCHESTER,DOWNTOWN,IRVINGTON,HARWOOD,PARKLANE,MOUNT VERNON,LIBERTY SQUARE,CANTON,CHARLES NORTH,DOLFIELD,CEDMONT,SHIPLEY HILL,BROADWAY EAST,WOODBOURNE HEIGHTS,CAMERON VILLAGE,PULASKI INDUSTRIAL AREA,REISTERSTOWN STATION,VIOLETVILLE,ELLWOOD PARK/MONUMENT,PIMLICO GOOD NEIGHBORS,WILHELM PARK,FOUR BY FOUR,WESTGATE,PENN NORTH,BOLTON HILL,PATTERSON PARK NEIGHBORHOOD,BEREA,CONCERNED CITIZENS OF FOREST PARK,COLDSTREAM HOMESTEAD MONTEBELLO,UPPER FELLS POINT,GLEN OAKS,WINSTON-GOVANS,WINDSOR HILLS,CHARLES VILLAGE,DORCHESTER,FRANKLINTOWN ROAD,BURLEITH-LEIGHTON,WASHINGTON VILLAGE/PIGTOWN,WRENLANE,ROSEMONT,SANDTOWN-WINCHESTER,LITTLE ITALY,FRANKFORD,EVERGREEN LAWN,NEW SOUTHWEST/MOUNT CLARE,EVERGREEN,SETON HILL,BALTIMORE HIGHLANDS,NORTH ROLAND PARK/POPLAR HILL,LOCUST POINT,ARMISTEAD GARDENS,RIVERSIDE,SOUTH BALTIMORE,SHARP-LEADENHALL,MIDDLE BRANCH/REEDBIRD PARKS,RICHNOR SPRINGS,FRANKLIN SQUARE,BELAIR-PARKSIDE,WOODMERE,EDGEWOOD,NEW NORTHWOOD,FOREST PARK,SAINT HELENA,BAYVIEW,SOUTH CLIFTON PARK,UNIVERSITY OF MARYLAND,GREEKTOWN,MIDDLE EAST,LAURAVILLE,CENTRAL FOREST PARK,UPLANDS,JOHNSTON SQUARE,MORRELL PARK,EAST ARLINGTON,UPTON,WALTHERSON,PATTERSON PLACE,JONESTOWN,MID-TOWN BELVEDERE,O'DONNELL HEIGHTS,GREENMOUNT WEST,OTTERBEIN,HAMILTON HILLS,EAST BALTIMORE MIDWAY,ORIGINAL NORTHWOOD,WASHINGTON HILL,LEVINDALE,BELVEDERE,PATTERSON PARK,LANGSTON HUGHES,PANWAY/BRADDISH AVENUE,MEDFIELD,CARROLL - CAMDEN INDUSTRIAL AREA,CARROLLTON RIDGE,EASTERWOOD,BROENING MANOR,BREWERS HILL,HAMPDEN,FAIRFIELD AREA,MOSHER,GREENSPRING,PARK CIRCLE,HOES HEIGHTS,GLEN,YORK-HOMELAND,SAINT AGNES,BIDDLE STREET,MONTEBELLO,PARKSIDE,WYNDHURST,PENROSE/FAYETTE STREET OUTREACH,MILTON-MONTFORD,KRESSON,ROSEMONT HOMEOWNERS/TENANTS,DUNBAR-BROADWAY,GROVE PARK,LAKE WALKER,HOLABIRD INDUSTRIAL PARK,ORANGEVILLE,DOWNTOWN WEST,BRIDGEVIEW/GREENLAWN,MEDFORD,CURTIS BAY INDUSTRIAL AREA,WALBROOK,HERITAGE CROSSING,NORTHWEST COMMUNITY ACTION,OLD GOUCHER,WAKEFIELD,MADISON-EASTEND,CHESWOLDE,WEST HILLS,COPPIN HEIGHTS/ASH-CO-EAST,NORTH HARFORD ROAD,CROSS COUNTRY,CARROLL-SOUTH HILTON,SAINT JOSEPHS,CARROLL PARK,GRACELAND PARK,ROSEMONT EAST,TOWANDA-GRANTLEY,CLIFTON PARK,BUTCHER'S HILL,HOLLINS MARKET,IDLEWOOD,ORCHARD RIDGE,FALLSTAFF,WESTFIELD,EDNOR GARDENS-LAKESIDE,BETTER WAVERLY,ASHBURTON,SABINA-MATTFELDT,HOPKINS BAYVIEW,WILSON PARK,DARLEY PARK,CALLAWAY-GARRISON,GUILFORD,KESWICK,RADNOR-WINSTON,TREMONT,CYLBURN,BOYD-BOOTH,HILLEN,GAY STREET,PENN-FALLSWAY,STONEWOOD-PENTWOOD-WINSTON,LOYOLA/NOTRE DAME,CHINQUAPIN PARK,OAKLEE,GARWYN OAKS,MOUNT WINANS,JOHNS HOPKINS HOMEWOOD,RIDGELY'S DELIGHT,BARRE CIRCLE,HOMELAND,DRUID HILL PARK,PLEASANT VIEW GARDENS,BEECHFIELD,PORT COVINGTON,LUCILLE PARK,ARLINGTON,EVESHAM PARK,ARCADIA,PURNELL,TUSCANY-CANTERBURY,ORANGEVILLE INDUSTRIAL AREA,LOWER EDMONDSON VILLAGE,OAKENSHAWE,MID-GOVANS,ROGNEL HEIGHTS,WYMAN PARK,STADIUM AREA,MORGAN STATE UNIVERSITY,WOODBOURNE-MCCABE,COLDSPRING,MAYFIELD,ROLAND PARK,KENILWORTH PARK,FAIRMONT,KERNEWOOD,LAKE EVESHAM,FRANKLINTOWN,JONES FALLS AREA,MOUNT WASHINGTON,CROSS KEYS,GREENMOUNT CEMETERY,SPRING GARDEN INDUSTRIAL AREA,EASTWOOD,HUNTING RIDGE,ROSEBANK,MORAVIA-WALTHER,LOCUST POINT INDUSTRIAL AREA,OVERLEA,FOREST PARK GOLF COURSE,HAWKINS POINT,TEN HILLS,MORGAN PARK,VILLAGES OF HOMELAND,BEVERLY HILLS,PERKINS HOMES,TAYLOR HEIGHTS,LOWER HERRING RUN PARK,DICKEYVILLE,GWYNNS FALLS/LEAKIN PARK,BELLONA-GITTINGS,SAINT PAUL,BLYTHEWOOD,MT PLEASANT PARK,HERRING RUN PARK,THE ORCHARDS,DUNDALK MARINE TERMINAL
    dataArr = []
    neighborhoodDict = {}

    data = neighborhoodDb.find({})
    for result in data:
        dataArr.append(result)
    neighborhoodDict = dataArr[0]
    del neighborhoodDict["_id"]
    del neighborhoodDict[""]

    print(neighborhoodDict)

    return neighborhoodDict

def createNeighborhoodData():
    neighborhoodList = []
    #CENTRAL PARK HEIGHTS,WEST ARLINGTON,LAKELAND,MILLHILL,REMINGTON,OLIVER,HOWARD PARK,WOODBERRY,MONDAWMIN,RAMBLEWOOD,UNION SQUARE,EDMONDSON VILLAGE,MADISON PARK,INNER HARBOR,HANLON-LONGWOOD,FELLS POINT,CARE,MOUNT HOLLY,MIDTOWN-EDMONDSON,BROOKLYN,ABELL,BARCLAY,WAVERLY,GWYNNS FALLS,MCELDERRY PARK,PERRING LOCH,OLDTOWN,POPPLETON,GLENHAM-BELHAR,HARLEM PARK,WESTPORT,CURTIS BAY,YALE HEIGHTS,DRUID HEIGHTS,CANTON INDUSTRIAL AREA,LOCH RAVEN,BELAIR-EDISON,CEDARCROFT,HIGHLANDTOWN,SETON BUSINESS PARK,PEN LUCY,,PARKVIEW/WOODBROOK,CHERRY HILL,FEDERAL HILL,RESERVOIR HILL,CEDONIA,ALLENDALE,WEST FOREST PARK,WINCHESTER,DOWNTOWN,IRVINGTON,HARWOOD,PARKLANE,MOUNT VERNON,LIBERTY SQUARE,CANTON,CHARLES NORTH,DOLFIELD,CEDMONT,SHIPLEY HILL,BROADWAY EAST,WOODBOURNE HEIGHTS,CAMERON VILLAGE,PULASKI INDUSTRIAL AREA,REISTERSTOWN STATION,VIOLETVILLE,ELLWOOD PARK/MONUMENT,PIMLICO GOOD NEIGHBORS,WILHELM PARK,FOUR BY FOUR,WESTGATE,PENN NORTH,BOLTON HILL,PATTERSON PARK NEIGHBORHOOD,BEREA,CONCERNED CITIZENS OF FOREST PARK,COLDSTREAM HOMESTEAD MONTEBELLO,UPPER FELLS POINT,GLEN OAKS,WINSTON-GOVANS,WINDSOR HILLS,CHARLES VILLAGE,DORCHESTER,FRANKLINTOWN ROAD,BURLEITH-LEIGHTON,WASHINGTON VILLAGE/PIGTOWN,WRENLANE,ROSEMONT,SANDTOWN-WINCHESTER,LITTLE ITALY,FRANKFORD,EVERGREEN LAWN,NEW SOUTHWEST/MOUNT CLARE,EVERGREEN,SETON HILL,BALTIMORE HIGHLANDS,NORTH ROLAND PARK/POPLAR HILL,LOCUST POINT,ARMISTEAD GARDENS,RIVERSIDE,SOUTH BALTIMORE,SHARP-LEADENHALL,MIDDLE BRANCH/REEDBIRD PARKS,RICHNOR SPRINGS,FRANKLIN SQUARE,BELAIR-PARKSIDE,WOODMERE,EDGEWOOD,NEW NORTHWOOD,FOREST PARK,SAINT HELENA,BAYVIEW,SOUTH CLIFTON PARK,UNIVERSITY OF MARYLAND,GREEKTOWN,MIDDLE EAST,LAURAVILLE,CENTRAL FOREST PARK,UPLANDS,JOHNSTON SQUARE,MORRELL PARK,EAST ARLINGTON,UPTON,WALTHERSON,PATTERSON PLACE,JONESTOWN,MID-TOWN BELVEDERE,O'DONNELL HEIGHTS,GREENMOUNT WEST,OTTERBEIN,HAMILTON HILLS,EAST BALTIMORE MIDWAY,ORIGINAL NORTHWOOD,WASHINGTON HILL,LEVINDALE,BELVEDERE,PATTERSON PARK,LANGSTON HUGHES,PANWAY/BRADDISH AVENUE,MEDFIELD,CARROLL - CAMDEN INDUSTRIAL AREA,CARROLLTON RIDGE,EASTERWOOD,BROENING MANOR,BREWERS HILL,HAMPDEN,FAIRFIELD AREA,MOSHER,GREENSPRING,PARK CIRCLE,HOES HEIGHTS,GLEN,YORK-HOMELAND,SAINT AGNES,BIDDLE STREET,MONTEBELLO,PARKSIDE,WYNDHURST,PENROSE/FAYETTE STREET OUTREACH,MILTON-MONTFORD,KRESSON,ROSEMONT HOMEOWNERS/TENANTS,DUNBAR-BROADWAY,GROVE PARK,LAKE WALKER,HOLABIRD INDUSTRIAL PARK,ORANGEVILLE,DOWNTOWN WEST,BRIDGEVIEW/GREENLAWN,MEDFORD,CURTIS BAY INDUSTRIAL AREA,WALBROOK,HERITAGE CROSSING,NORTHWEST COMMUNITY ACTION,OLD GOUCHER,WAKEFIELD,MADISON-EASTEND,CHESWOLDE,WEST HILLS,COPPIN HEIGHTS/ASH-CO-EAST,NORTH HARFORD ROAD,CROSS COUNTRY,CARROLL-SOUTH HILTON,SAINT JOSEPHS,CARROLL PARK,GRACELAND PARK,ROSEMONT EAST,TOWANDA-GRANTLEY,CLIFTON PARK,BUTCHER'S HILL,HOLLINS MARKET,IDLEWOOD,ORCHARD RIDGE,FALLSTAFF,WESTFIELD,EDNOR GARDENS-LAKESIDE,BETTER WAVERLY,ASHBURTON,SABINA-MATTFELDT,HOPKINS BAYVIEW,WILSON PARK,DARLEY PARK,CALLAWAY-GARRISON,GUILFORD,KESWICK,RADNOR-WINSTON,TREMONT,CYLBURN,BOYD-BOOTH,HILLEN,GAY STREET,PENN-FALLSWAY,STONEWOOD-PENTWOOD-WINSTON,LOYOLA/NOTRE DAME,CHINQUAPIN PARK,OAKLEE,GARWYN OAKS,MOUNT WINANS,JOHNS HOPKINS HOMEWOOD,RIDGELY'S DELIGHT,BARRE CIRCLE,HOMELAND,DRUID HILL PARK,PLEASANT VIEW GARDENS,BEECHFIELD,PORT COVINGTON,LUCILLE PARK,ARLINGTON,EVESHAM PARK,ARCADIA,PURNELL,TUSCANY-CANTERBURY,ORANGEVILLE INDUSTRIAL AREA,LOWER EDMONDSON VILLAGE,OAKENSHAWE,MID-GOVANS,ROGNEL HEIGHTS,WYMAN PARK,STADIUM AREA,MORGAN STATE UNIVERSITY,WOODBOURNE-MCCABE,COLDSPRING,MAYFIELD,ROLAND PARK,KENILWORTH PARK,FAIRMONT,KERNEWOOD,LAKE EVESHAM,FRANKLINTOWN,JONES FALLS AREA,MOUNT WASHINGTON,CROSS KEYS,GREENMOUNT CEMETERY,SPRING GARDEN INDUSTRIAL AREA,EASTWOOD,HUNTING RIDGE,ROSEBANK,MORAVIA-WALTHER,LOCUST POINT INDUSTRIAL AREA,OVERLEA,FOREST PARK GOLF COURSE,HAWKINS POINT,TEN HILLS,MORGAN PARK,VILLAGES OF HOMELAND,BEVERLY HILLS,PERKINS HOMES,TAYLOR HEIGHTS,LOWER HERRING RUN PARK,DICKEYVILLE,GWYNNS FALLS/LEAKIN PARK,BELLONA-GITTINGS,SAINT PAUL,BLYTHEWOOD,MT PLEASANT PARK,HERRING RUN PARK,THE ORCHARDS,DUNDALK MARINE TERMINAL
    dataArr = []
    neighborhoodDict = {}

    data = neighborhoodDb.find({})
    for result in data:
        dataArr.append(result)
    neighborhoodDict = dataArr[0]
    del neighborhoodDict["_id"]
    del neighborhoodDict[""]


    return neighborhoodDict

def createHistoryData():
    historyList = []

    dataArr = []
    historyDict = {}

    data = historyDb.find({})
    for result in data:
        dataArr.append(result)
    historyDict = dataArr[0]
    del historyDict["_id"]


    return historyDict
    
if __name__ == "__main__":
    crimes = []
    crimeDataCol = crimeData.find({}).limit(2)
    for thing in crimeDataCol:
        crimes.append(thing)
    app.run(debug=True)
