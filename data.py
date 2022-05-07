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
collection = db["master"]
time = db["time"]
description = db["description"]
FilteredData = db["Filtered"]
district = db["district"]

file = open("test.csv")
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

# dictionaries for the collections for number of occurences (for graphs)
timeDict = {}
descriptionDict = {}
weaponDict = {}
districtDict = {}
inoutDict = {}

weapons = []
descriptions = []
districts = []
times = ["MORNING", "AFTERNOON", "EVENING", "LATE NIGHT"]
#months = ["April2020","May2020","June2020","July2020","August2020","September2020","October2020","November2020","December2020","January2021","February2021","March2021","April2021","May2021","June2021","July2021","August2021","September2021","October2021","November2021","December2021","January2022","February2022","March2022", "April2022", "Other"]
months = ["April2021","May2021","June2021","July2021","August2021","September2021","October2021","November2021","December2021","January2022","February2022","March2022", "April2022", "Other"]
inout = []

nbs = set()

for row in csvreader:
    dataDict = {}
    for j in range(18):
        # First element in header list is messed up so manually create it
        if (j == 0): 
            dataDict['X'] = row[j]
        # Rest of elements are fine to index
        else:
            if (j == 3):
                if row[j] in timeDict.keys():
                    timeDict[row[j]] += 1
                    # if (row[j][11] == '0' and row[j][12] >= '6') or (row[j][11] == '1' and row[j][12] < '2') :
                    #     print(row[j])
                    #     print("Morning")
                    # elif (row[j][11] == '1' and row[j][12] < '8'):
                    #     print(row[j])
                    #     print("Afternoon")
                    # elif (row[j][11] == '1' and row [j][12] >= '8') or (row[j][11] == '2' and row[j][12] < '1'):
                    #     print(row[j])
                    #     print("Evening")
                    # else:
                    #     print(row[j])
                    #     print("Late Night")
                else:
                    timeDict[row[j]] = 1
            elif (j == 6):
                if row[j] in descriptionDict.keys():
                    descriptionDict[row[j]] += 1
                else:
                    descriptionDict[row[j]] = 1
                    descriptions.append(row[j])
            elif (j == 7):
                if row[j] in inoutDict.keys():
                    inoutDict[row[j]] += 1
                else:
                    inoutDict[row[j]] = 1
                    inout.append(row[j])
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
            dataDict[header[j]] = row[j]
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
counter = 0
for weapon in weapons:
    print(counter)
    counter += 1

    # if weapon not in weaponDict.keys():
    weaponDict[weapon] = {}
    for district in districts:
        # if description not in weaponDict[weapon].keys():
        weaponDict[weapon][district] = {}
        for description in descriptions:
            # if district not in weaponDict[weapon][description].keys():
            weaponDict[weapon][district][description] = {}
            for time in times:
                # if time not in weaponDict[weapon][description][district].keys():
                weaponDict[weapon][district][description][time] = {}
                for month in months:
                    # if month not in weaponDict[weapon][description][district][month].keys():
                    weaponDict[weapon][district][description][time][month] = {}
                    for io in inout:
                        # if inside/outside not in weaponDict[weapon][description][district][month][io].keys():
                        weaponDict[weapon][district][description][time][month][io] = 0
                
counter = 0
for item in dataList:

    wep = item["Weapon"]
    dis = item["District"]
    des = item["Description"]
    io = item["Inside_Outside"]
    time = ""
    month = ""

    if (item["CrimeDateTime"][11] == '0' and item["CrimeDateTime"][12] >= '6') or (item["CrimeDateTime"][11] == '1' and item["CrimeDateTime"][12] < '2') :
        time = "MORNING"
    elif (item["CrimeDateTime"][11] == '1' and item["CrimeDateTime"][12] < '8'):
        time = "AFTERNOON"
    elif (item["CrimeDateTime"][11] == '1' and item["CrimeDateTime"][12] >= '8') or (item["CrimeDateTime"][11] == '2' and item["CrimeDateTime"][12] < '1'):
        time = "EVENING"
    else:
        time = "LATE NIGHT"

    if item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '2' and item["CrimeDateTime"][6] == '4':
        month = "April2022"
    elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '2' and item["CrimeDateTime"][6] == '3':
        month = "March2022"
    elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '2' and item["CrimeDateTime"][6] == '2' and item["CrimeDateTime"][5] == '0':    
        month = "February2022"
    elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '2' and item["CrimeDateTime"][6] == '1' and item["CrimeDateTime"][5] == '0':    
        month = "January2022"
    elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '1' and item["CrimeDateTime"][6] == '2' and item["CrimeDateTime"][5] == '1':    
        month = "December2021"
    elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '1' and item["CrimeDateTime"][6] == '1' and item["CrimeDateTime"][5] == '1':    
        month = "November2021"
    elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '1' and item["CrimeDateTime"][6] == '0' and item["CrimeDateTime"][5] == '1':    
        month = "October2021"
    elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '1' and item["CrimeDateTime"][6] == '9':    
        month = "September2021"
    elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '1' and item["CrimeDateTime"][6] == '8':    
        month = "August2021"
    elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '1' and item["CrimeDateTime"][6] == '7':    
        month = "July2021"
    elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '1' and item["CrimeDateTime"][6] == '6':    
        month = "June2021"
    elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '1' and item["CrimeDateTime"][6] == '5':    
        month = "May2021"
    elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '1' and item["CrimeDateTime"][6] == '4':    
        month = "April2021"
    # elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '1' and item["CrimeDateTime"][6] == '3':    
    #     month = "March2021"
    # elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '1' and item["CrimeDateTime"][6] == '2' and item["CrimeDateTime"][5] == '0':    
    #     month = "February2021"
    # elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '1' and item["CrimeDateTime"][6] == '1' and item["CrimeDateTime"][5] == '0':    
    #     month = "January2021"
    # elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '0' and item["CrimeDateTime"][6] == '2' and item["CrimeDateTime"][5] == '1':    
    #     month = "December2020"
    # elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '0' and item["CrimeDateTime"][6] == '1' and item["CrimeDateTime"][5] == '1':    
    #     month = "November2020"
    # elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '0' and item["CrimeDateTime"][6] == '0' and item["CrimeDateTime"][5] == '1':    
    #     month = "October2020"
    # elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '0' and item["CrimeDateTime"][6] == '9':    
    #     month = "September2020"
    # elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '0' and item["CrimeDateTime"][6] == '8':    
    #     month = "August2020"
    # elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '0' and item["CrimeDateTime"][6] == '7':    
    #     month = "July2020"
    # elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '0' and item["CrimeDateTime"][6] == '6':    
    #     month = "June2020"
    # elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '0' and item["CrimeDateTime"][6] == '5':    
    #     month = "May2020"
    # elif item["CrimeDateTime"][2] == '2' and item["CrimeDateTime"][3] >= '0' and item["CrimeDateTime"][6] == '4':    
    #     month = "April2020"
    else:
        month = "Other"
    
    weaponDict[wep][dis][des][time][month][io] += 1

weaponList.append(weaponDict)
FilteredData.insert_many(weaponList)

##############################




# Put dictionaries of number of occurences in lists and send to respective databases
# timeList.append(timeDict)
# descriptionList.append(descriptionDict)
# weaponList.append(weaponDict)
# districtList.append(districtDict)

# time.insert_many(timeList)
# description.insert_many(descriptionList)
# weapon.insert_many(weaponList)
# district.insert_many(districtList)

# Inserts every entry in the dataList into the database collection
# uncomment when inserting to master collection
#######
###collection.insert_many(dataList)
#######

file.close()
