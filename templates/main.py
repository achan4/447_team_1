from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from pymongo import MongoClient
from flask_cors import CORS
import certifi
import csv

# Instantiation
app = Flask(__name__)

#cluster = MongoClient("mongodb+srv://team1:team1@cluster0.pmmnz.mongodb.net/smallData?retryWrites=true&w=majority", tlsCAFile=certifi.where())
cluster = MongoClient("mongodb+srv://team1:team1@cluster0.pmmnz.mongodb.net/smallData?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = cluster["smallData"]
crimeData = db["smallCrime"]

# Settings
CORS(app)

# Routes

@app.route('/')
def index():
    crimes = []
    crimeDataCol = crimeData.find({}).limit(2)
    for thing in crimeDataCol:
        crimes.append(thing)
    return render_template("index.html",crimes=crimes)

@app.route('/main')
def main():
    return render_template("index.html")
@app.route('/map')
def map():
    return render_template("map.html")
@app.route('/data')
def data():
    return render_template("data.html")

if __name__ == "__main__":
    # file = open("Part1_Crime_data.csv")
    # csvreader = csv.reader(file)
    # header = next(csvreader)
    # print(header)
    # dataList = []
    # i = 0
    # for row in csvreader:
    #     dataDict = {}
    #     for j in range(18):
    #         # First element in header list is messed up so manually create it
    #         if (j == 0): 
    #             dataDict['X'] = row[j]
    #     # Rest of elements are fine to index
    #         else:
    #             dataDict[header[j]] = row[j]
    #     dataList.append(dataDict)
    # # Displays how many entries have been added to the datalist        
    #     print(i)
    


    # file.close()
    app.run(debug=True)