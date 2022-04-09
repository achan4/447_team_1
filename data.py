# CMSC 447 Spring 2022 Team 1
# Crime Data Upload to MongoDB
# Author: Connor Boie

from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from pymongo import MongoClient
from flask_cors import CORS
import certifi
import csv

cluster = MongoClient("mongodb+srv://team1:team1@cluster0.pmmnz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = cluster["team1"]
collection = db["master"]

file = open("Part1_Crime_data.csv")
csvreader = csv.reader(file)
header = next(csvreader)
print(header)
dataList = []
i = 0
for row in csvreader:
    dataDict = {}
    for j in range(18):
        # First element in header list is messed up so manually create it
        if (j == 0): 
            dataDict['X'] = row[j]
        # Rest of elements are fine to index
        else:
            dataDict[header[j]] = row[j]
    dataList.append(dataDict)
    # Displays how many entries have been added to the datalist        
    print(i)
    i = i + 1   

# Inserts every entry in the dataList into the database collection
collection.insert_many(dataList)

file.close()
