# CMSC 447 Spring 2022 Team 1
# Crime Data Upload to MongoDB
# Author: Connor Boie

from time import time_ns
from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from pymongo import MongoClient
from flask_cors import CORS
import certifi
import csv

cluster = MongoClient("mongodb+srv://team1:team1@cluster0.pmmnz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = cluster["team1"]
collection = db["Master"]
time = db["time"]
description = db["description"]
FilteredData = db["Filtered"]
district = db["district"]
monthDB = db["month"]
inout = db["inout"]
history = db["history"]

file = open("Part1_Crime_data.csv")
# file = open("Part1_Crime_data.csv")
csvreader = csv.reader(file)
header = next(csvreader)
print(header)
dataList = []
i = 0

# lists for the collections for number of occurences (for graphs)
timeList = []
descriptionList = []
weaponList = []
districtList = []
monthList = []
inoutList = []
historyList = []

# dictionaries for the collections for number of occurences (for graphs)
timeDict = {}
descriptionDict = {}
weaponDict = {}
districtDict = {}
inoutDict = {}
monthDict ={}
historyDict = {}

weapons = []
descriptions = []
districts = []
times = ["MORNING", "AFTERNOON", "EVENING", "LATE NIGHT"]
#months = ["April2020","May2020","June2020","July2020","August2020","September2020","October2020","November2020","December2020","January2021","February2021","March2021","April2021","May2021","June2021","July2021","August2021","September2021","October2021","November2021","December2021","January2022","February2022","March2022", "April2022", "Other"]
months = ["April","May","June","July","August","September","October","November","December","January","February","March", "April"]

nbs = set()

for row in csvreader:
    dataDict = {}
    for j in range(18):
        # First element in header list is messed up so manually create it
        if (j == 0): 
            pass
            # dataDict['X'] = row[j]
        # Rest of elements are fine to index
        else:
            if (j == 3):
                
                if row[j][6] == '4':
                    month = "Apr" 
                elif row[j][6] == '3':
                    month = "Mar"
                elif row[j][6] == '2' and row[j][5] == '0':    
                    month = "Feb"
                elif row[j][6] == '1' and row[j][5] == '0':    
                    month = "Jan"
                elif row[j][6] == '2' and row[j][5] == '1':    
                    month = "Dec"
                elif row[j][6] == '1' and row[j][5] == '1':    
                    month = "Nov"
                elif row[j][6] == '0' and row[j][5] == '1':    
                    month = "Oct"
                elif row[j][6] == '9':    
                    month = "Sep"
                elif row[j][6] == '8':    
                    month = "Aug"
                elif row[j][6] == '7':    
                    month = "Jul"
                elif row[j][6] == '6':    
                    month = "Jun"
                elif row[j][6] == '5':    
                    month = "May"

                year = row[j][0:4]

                monthYear = month + year

                if year[0] == "2" and year[2] != "0":

                    if monthYear in historyDict.keys():
                        historyDict[monthYear] += 1
                    else:
                        historyDict[monthYear] = 1

                # timeDict[row[j]] += 1
                if (row[j][11] == '0' and row[j][12] >= '6') or (row[j][11] == '1' and row[j][12] < '2') :
                    if "Morning" in timeDict.keys():
                        timeDict["Morning"] += 1
                    else:
                        timeDict["Morning"] = 1
                elif (row[j][11] == '1' and row[j][12] < '8'):
                    if "Afternoon" in timeDict.keys():
                        timeDict["Afternoon"] += 1
                    else:
                        timeDict["Afternoon"] = 1
                elif (row[j][11] == '1' and row [j][12] >= '8') or (row[j][11] == '2' and row[j][12] < '1'):
                    if "Evening" in timeDict.keys():
                        timeDict["Evening"] += 1
                    else:
                        timeDict["Evening"] = 1
                else:
                    if "Late Night" in timeDict.keys():
                        timeDict["Late Night"] += 1
                    else:
                        timeDict["Late Night"] = 1

                if row[j][6] == '4':
                    if "April" in monthDict.keys():
                        monthDict["April"] += 1
                    else:
                        monthDict["April"] = 1       
                elif row[j][6] == '3':
                    if "March" in monthDict.keys():
                        monthDict["March"] += 1
                    else:
                        monthDict["March"] = 1
                elif row[j][6] == '2' and row[j][5] == '0':    
                    if "February" in monthDict.keys():
                        monthDict["February"] += 1
                    else:
                        monthDict["February"] = 1
                elif row[j][6] == '1' and row[j][5] == '0':    
                    if "January" in monthDict.keys():
                        monthDict["January"] += 1
                    else:
                        monthDict["January"] = 1
                elif row[j][6] == '2' and row[j][5] == '1':    
                    if "December" in monthDict.keys():
                        monthDict["December"] += 1
                    else:
                        monthDict["December"] = 1
                elif row[j][6] == '1' and row[j][5] == '1':    
                    if "November" in monthDict.keys():
                        monthDict["November"] += 1
                    else:
                        monthDict["November"] = 1
                elif row[j][6] == '0' and row[j][5] == '1':    
                    if "October" in monthDict.keys():
                        monthDict["October"] += 1
                    else:
                        monthDict["October"] = 1
                elif row[j][6] == '9':    
                    if "September" in monthDict.keys():
                        monthDict["September"] += 1
                    else:
                        monthDict["September"] = 1
                elif row[j][6] == '8':    
                    if "August" in monthDict.keys():
                        monthDict["August"] += 1
                    else:
                        monthDict["August"] = 1
                elif row[j][6] == '7':    
                    if "July" in monthDict.keys():
                        monthDict["July"] += 1
                    else:
                        monthDict["July"] = 1
                elif row[j][6] == '6':    
                    if "June" in monthDict.keys():
                        monthDict["June"] += 1
                    else:
                        monthDict["June"] = 1
                elif row[j][6] == '5':    
                    if "May" in monthDict.keys():
                        monthDict["May"] += 1
                    else:
                        monthDict["May"] = 1

                
            elif (j == 6):
                if row[j] in descriptionDict.keys():
                    descriptionDict[row[j]] += 1
                else:
                    descriptionDict[row[j]] = 1
                    descriptions.append(row[j])
            elif (j == 7):
                io = row[j]
                if (io == "I"):
                    io = "Inside"
                if (io == "O"):
                    io = "Outside"
                if (io == ""):
                    io = "NA"
                if io in inoutDict.keys():
                    inoutDict[io] += 1
                else:
                    inoutDict[io] = 1
                    #inoutList.append(row[j])
            elif (j == 8):
                if row[j] in weaponDict.keys():
                    # weaponDict[row[j]] += 1
                    pass
                else:
                    # weaponDict[row[j]] = 1
                    weapons.append(row[j])
            elif (j == 10):
                if row[j] in districtDict.keys():
                    districtDict[row[j]] += 1
                else:
                    districtDict[row[j]] = 1
                    districts.append(row[j])

            ##### Uncomment when creating master list
            #####
            if j == 6 or j == 8 or j == 10 or j == 11:
                dataDict[header[j]] = row[j]
            elif j == 7:
                io = row[j]
                if row[j] == "I":
                    io = "Inside"
                elif row[j] == "O":
                    io = "Outisde"
                elif row[j] == "":
                    io = "NA"
                dataDict[header[j]] = io
            elif j == 3:
                if (row[j][11] == '0' and row[j][11] >= '6') or (row[j][11] == '1' and row[j][12] < '2') :
                    dataDict["Time"] = "Morning"
                elif (row[j][11] == '1' and row[j][12] < '8'):
                    dataDict["Time"] = "Afternoon"
                elif (row[j][11] == '1' and row[j][12] >= '8') or (row[j][11] == '2' and row[j][12] < '1'):
                    dataDict["Time"] = "Evening"
                else:
                    dataDict["Time"] = "Late Night"

                if row[j][6] == '4':
                    dataDict["Month"] = "April"
                elif row[j][6] == '3':
                    dataDict["Month"] = "March"
                elif row[j][6] == '2' and row[j][5] == '0':    
                    dataDict["Month"] = "February"
                elif row[j][6] == '1' and row[j][5] == '0':    
                    dataDict["Month"] = "January"
                elif row[j][6] == '2' and row[j][5] == '1':    
                    dataDict["Month"] = "December"
                elif row[j][6] == '1' and row[j][5] == '1':    
                    dataDict["Month"] = "November"
                elif row[j][6] == '0' and row[j][5] == '1':    
                    dataDict["Month"] = "October"
                elif row[j][6] == '9':    
                    dataDict["Month"] = "September"
                elif row[j][6] == '8':    
                    dataDict["Month"] = "August"
                elif row[j][6] == '7':    
                    dataDict["Month"] = "July"
                elif row[j][6] == '6':    
                    dataDict["Month"] = "June"
                elif row[j][6] == '5':    
                    dataDict["Month"] = "May"

            #####


    dataList.append(dataDict)
    # Displays how many entries have been added to the datalist        
    print(i)
    i = i + 1   

# counter = 0
# for item in dataList:
#     nbs.add(item["Neighborhood"])
#     print(counter)
#     counter += 1
# print(nbs)
# print(len(nbs))

##### Weapons Filtering ######
# counter = 0
# for weapon in weapons:
#     print(counter)
#     counter += 1

#     # if weapon not in weaponDict.keys():
#     weaponDict[weapon] = {}
#     for district in districts:
#         # if description not in weaponDict[weapon].keys():
#         weaponDict[weapon][district] = {}
#         for description in descriptions:
#             # if district not in weaponDict[weapon][description].keys():
#             weaponDict[weapon][district][description] = {}
#             for time in times:
#                 # if time not in weaponDict[weapon][description][district].keys():
#                 weaponDict[weapon][district][description][time] = {}
#                 for month in months:
#                     # if month not in weaponDict[weapon][description][district][month].keys():
#                     weaponDict[weapon][district][description][time][month] = {}
#                     for io in inout:
#                         # if inside/outside not in weaponDict[weapon][description][district][month][io].keys():
#                         weaponDict[weapon][district][description][time][month][io] = 0
                
# counter = 0
# for item in dataList:

#     wep = item["Weapon"]
#     dis = item["District"]
#     des = item["Description"]
#     io = item["Inside_Outside"]
#     time = ""
#     month = ""

    # if (item["CrimeDateTime"][11] == '0' and item["CrimeDateTime"][12] >= '6') or (item["CrimeDateTime"][11] == '1' and item["CrimeDateTime"][12] < '2') :
    #     time = "MORNING"
    # elif (item["CrimeDateTime"][11] == '1' and item["CrimeDateTime"][12] < '8'):
    #     time = "AFTERNOON"
    # elif (item["CrimeDateTime"][11] == '1' and item["CrimeDateTime"][12] >= '8') or (item["CrimeDateTime"][11] == '2' and item["CrimeDateTime"][12] < '1'):
    #     time = "EVENING"
    # else:
    #     time = "LATE NIGHT"

#     if item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '2' and item["CrimeDateTime"][6] == '4':
#         month = "April2022"
#     elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '2' and item["CrimeDateTime"][6] == '3':
#         month = "March2022"
#     elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '2' and item["CrimeDateTime"][6] == '2' and item["CrimeDateTime"][5] == '0':    
#         month = "February2022"
#     elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '2' and item["CrimeDateTime"][6] == '1' and item["CrimeDateTime"][5] == '0':    
#         month = "January2022"
#     elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '1' and item["CrimeDateTime"][6] == '2' and item["CrimeDateTime"][5] == '1':    
#         month = "December2021"
#     elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '1' and item["CrimeDateTime"][6] == '1' and item["CrimeDateTime"][5] == '1':    
#         month = "November2021"
#     elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '1' and item["CrimeDateTime"][6] == '0' and item["CrimeDateTime"][5] == '1':    
#         month = "October2021"
#     elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '1' and item["CrimeDateTime"][6] == '9':    
#         month = "September2021"
#     elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '1' and item["CrimeDateTime"][6] == '8':    
#         month = "August2021"
#     elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '1' and item["CrimeDateTime"][6] == '7':    
#         month = "July2021"
#     elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '1' and item["CrimeDateTime"][6] == '6':    
#         month = "June2021"
#     elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '1' and item["CrimeDateTime"][6] == '5':    
#         month = "May2021"
#     elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '1' and item["CrimeDateTime"][6] == '4':    
#         month = "April2021"
#     # elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '1' and item["CrimeDateTime"][6] == '3':    
#     #     month = "March2021"
#     # elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '1' and item["CrimeDateTime"][6] == '2' and item["CrimeDateTime"][5] == '0':    
#     #     month = "February2021"
#     # elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '1' and item["CrimeDateTime"][6] == '1' and item["CrimeDateTime"][5] == '0':    
#     #     month = "January2021"
#     # elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '0' and item["CrimeDateTime"][6] == '2' and item["CrimeDateTime"][5] == '1':    
#     #     month = "December2020"
#     # elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '0' and item["CrimeDateTime"][6] == '1' and item["CrimeDateTime"][5] == '1':    
#     #     month = "November2020"
#     # elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '0' and item["CrimeDateTime"][6] == '0' and item["CrimeDateTime"][5] == '1':    
#     #     month = "October2020"
#     # elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '0' and item["CrimeDateTime"][6] == '9':    
#     #     month = "September2020"
#     # elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '0' and item["CrimeDateTime"][6] == '8':    
#     #     month = "August2020"
#     # elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '0' and item["CrimeDateTime"][6] == '7':    
#     #     month = "July2020"
#     # elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '0' and item["CrimeDateTime"][6] == '6':    
#     #     month = "June2020"
#     # elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '0' and item["CrimeDateTime"][6] == '5':    
#     #     month = "May2020"
#     # elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '0' and item["CrimeDateTime"][6] == '4':    
#     #     month = "April2020"
#     else:
#         month = "Other"
    
#     weaponDict[wep][dis][des][time][month][io] += 1

# weaponList.append(weaponDict)
# FilteredData.insert_many(weaponList)

##############################


print(inoutDict)

# Put dictionaries of number of occurences in lists and send to respective databases
monthList.append(monthDict)
timeList.append(timeDict)
inoutList.append(inoutDict)
historyList.append(historyDict)
# descriptionList.append(descriptionDict)
# weaponList.append(weaponDict)
# districtList.append(districtDict)

history.insert_many(historyList)
#inout.insert_many(inoutList)
#month.insert_many(monthList)
#time.insert_many(timeList)
# description.insert_many(descriptionList)
# weapon.insert_many(weaponList)
# district.insert_many(districtList)

# Inserts every entry in the dataList into the database collection
# uncomment when inserting to master collection
#######
#collection.insert_many(dataList)
#######

file.close()
