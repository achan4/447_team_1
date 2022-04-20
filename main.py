from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from pymongo import MongoClient
from flask_cors import CORS
import certifi
import csv

# Instantiation
app = Flask(__name__)

cluster = MongoClient("mongodb+srv://team1:team1@cluster0.pmmnz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = cluster["smallData"]
crimeData = db["smallCrime"]

# cluster = MongoClient("mongodb+srv://cboie1:test123@cluster0.fzs5d.mongodb.net/test?retryWrites=true&w=majority", tlsCAFile=certifi.where())

# db = cluster["Connor_A1"]
# studentsCollection = db["Students"]
# instructorsCollection = db["Instructors"]
# coursesCollection = db["Courses"]
# gradesCollection = db["Grades"]

# Settings
CORS(app)

# Routes

@app.route('/')
def index():
    crimes = []
    crimeDataCol = crimeData.find({})
    for i in range(5):
        crimes.append(crimeDataCol[i])
    return render_template("index.html")

# @app.route('/')
# def index():
#     students = []
#     instructors = []
#     courses = []
#     grades = []
#     studentsCol = studentsCollection.find({})
#     instructorsCol = instructorsCollection.find({})
#     coursesCol = coursesCollection.find({})
#     gradesCol = gradesCollection.find({})
#     for result in studentsCol:
#         students.append(result)
#     for result in instructorsCol:
#         instructors.append(result)
#     for result in coursesCol:
#         courses.append(result)
#     for result in gradesCol:
#         grades.append(result)

#     return render_template("index.html", students=students, instructors=instructors, courses=courses, grades=grades)

# @app.route('/create_student')
# def create_student():
#     return render_template("create_student.html", rejected = 0)

# @app.route('/add_student', methods = ['GET', 'POST'])
# def add_student():
#     if request.method == 'POST':
#         add = True
#         students = studentsCollection.find({"StudentID": request.form["StudentID"]})
#         for result in students:
#             add = False
#         if add:
#             post = {"StudentID" : request.form["StudentID"], "StudentName" : request.form["StudentName"], "CreditsEarned" : request.form["CreditsEarned"]}
#             studentsCollection.insert_one(post)
#             return redirect(url_for('index'))
#         else:
#             return render_template("create_student.html", rejected = 1)

# @app.route('/update_student/<id>')
# def update_student(id):
#     student = studentsCollection.find({"StudentID" : id})
#     for result in student:
#         StudentName = result["StudentName"]
#         CreditsEarned = result["CreditsEarned"]
#     return render_template("update_student.html", id = id, StudentName = StudentName, CreditsEarned = CreditsEarned)

# @app.route('/confirm_update_student/<id>', methods = ['GET', 'POST'])
# def change_student(id):
#     if request.method == 'POST':
#         query = {"StudentID" : id}
#         newValues = {"$set": {"StudentID" : id, "StudentName" : request.form["StudentName"], "CreditsEarned" : request.form["CreditsEarned"]}}
#         studentsCollection.update_one(query, newValues)
#     return redirect(url_for('index'))


# @app.route('/remove_student/<id>/', methods = ['GET', 'POST'])
# def remove_student(id):
#     studentsCollection.delete_one({"StudentID": id})
#     gradesCollection.delete_many({"StudentID": id})
#     return redirect(url_for('index'))

# @app.route('/create_instructor')
# def create_instructor():
#     return render_template("create_instructor.html", rejected = 0)

# @app.route('/add_instructor', methods = ['GET', 'POST'])
# def add_instructor():
#     if request.method == 'POST':
#         add = True
#         instructors = instructorsCollection.find({"InstructorID": request.form["InstructorID"]})
#         for result in instructors:
#             add = False
#         if add:
#             post = {"InstructorID" : request.form["InstructorID"], "InstructorName" : request.form["InstructorName"], "Department" : request.form["Department"]}
#             instructorsCollection.insert_one(post)
#             return redirect(url_for('index'))
#         else:
#             return render_template("create_instructor.html", rejected = 1)

# @app.route('/update_instructor/<id>')
# def update_instructor(id):
#     instructor = instructorsCollection.find({"InstructorID" : id})
#     for result in instructor:
#         InstructorName = result["InstructorName"]
#         Department = result["Department"]
#     return render_template("update_instructor.html", id = id, InstructorName = InstructorName, Department = Department)

# @app.route('/confirm_update_instructor/<id>', methods = ['GET', 'POST'])
# def change_instructor(id):
#     if request.method == 'POST':
#         query = {"InstructorID" : id}
#         newValues = {"$set": {"InstructorID" : id, "InstructorName" : request.form["InstructorName"], "Department" : request.form["Department"]}}
#         instructorsCollection.update_one(query, newValues)
#     return redirect(url_for('index'))


# @app.route('/remove_instructor/<id>/', methods = ['GET', 'POST'])
# def remove_instructor(id):
#     instructorsCollection.delete_one({"InstructorID": id})
#     coursesCollection.delete_many({"InstructorID": id})
#     return redirect(url_for('index'))

# @app.route('/create_course')
# def create_course():
#     return render_template("create_course.html", rejected = 0)

# @app.route('/add_course', methods = ['GET', 'POST'])
# def add_course():
#     if request.method == 'POST':
#         iid = False
#         add = True
#         instructor = instructorsCollection.find({"InstructorID" : request.form["InstructorID"]})
#         courses = coursesCollection.find({"CourseID": request.form["CourseID"]})
#         for result in courses:
#             add = False
#         for result in instructor:
#             iid = True
#         if iid and add:
#             post = {"CourseID" : request.form["CourseID"], "CourseTitle" : request.form["CourseTitle"], "InstructorID" : request.form["InstructorID"]}
#             coursesCollection.insert_one(post)
#             return redirect(url_for('index'))
#         else: 
#             return render_template("create_course.html", rejected = 1)


# @app.route('/update_course/<id>')
# def update_course(id):
#     course = coursesCollection.find({"CourseID" : id})
#     for result in course:
#         CourseTitle = result["CourseTitle"]
#         InstructorID = result["InstructorID"]
#     return render_template("update_course.html", id = id, CourseTitle = CourseTitle, InstructorID = InstructorID, rejected = 0)

# @app.route('/confirm_update_course/<id>', methods = ['GET', 'POST'])
# def change_course(id):
#     if request.method == 'POST':
#         iid = False
#         instructor = instructorsCollection.find({"InstructorID" : request.form["InstructorID"]})
#         for result in instructor:
#             iid = True
#         if iid == True:
#             query = {"CourseID" : id}
#             newValues = {"$set": {"CourseID" : id, "CourseTitle" : request.form["CourseTitle"], "InstructorID" : request.form["InstructorID"]}}
#             coursesCollection.update_one(query, newValues)
#             return redirect(url_for('index'))
#         else:
#             courses = coursesCollection.find({"CourseID" : id})
#             for result in courses:
#                 course = result
#             return render_template("update_course.html", id = id, CourseTitle = course["CourseTitle"], InstructorID = course["InstructorID"], rejected = 1)

# @app.route('/remove_course/<id>/', methods = ['GET', 'POST'])
# def remove_course(id):
#     coursesCollection.delete_one({"CourseID": id})
#     gradesCollection.delete_many({"CourseID": id})
#     return redirect(url_for('index'))

# @app.route('/create_grade')
# def create_grade():
#     return render_template("create_grade.html", rejected = 0)

# @app.route('/add_grade', methods = ['GET', 'POST'])
# def add_grade():
#     if request.method == 'POST':
#         sid_exists = False
#         cid_exists = False
#         student = studentsCollection.find({"StudentID" : request.form["StudentID"]})
#         course = coursesCollection.find({"CourseID" : request.form["CourseID"]})
#         for result in student: 
#             sid_exists = True
#         for result in course:
#             cid_exists = True
#         if sid_exists and cid_exists:
#             post = {"StudentID" : request.form["StudentID"], "CourseID" : request.form["CourseID"], "Grade" : request.form["Grade"]}
#             gradesCollection.insert_one(post)
#             return redirect(url_for('index'))
#         else:
#             return render_template("create_grade.html", rejected = 1)
        
# @app.route('/update_grade/<sid>/<cid>')
# def update_grade(sid, cid):
#     grade = gradesCollection.find({"StudentID" : sid, "CourseID" : cid})
#     Grade = ""
#     for result in grade:
#         Grade = result["Grade"]
#     return render_template("update_grade.html", sid = sid, cid = cid, Grade = Grade, rejected = 0)

# @app.route('/confirm_update_grade/<sid>/<cid>', methods = ['GET', 'POST'])
# def change_grade(sid, cid):
#     if request.method == 'POST':
#         sid_exists = False
#         cid_exists = False
#         student = studentsCollection.find({"StudentID" : request.form["StudentID"]})
#         course = coursesCollection.find({"CourseID" : request.form["CourseID"]})
#         for result in student: 
#             sid_exists = True
#         for result in course:
#             cid_exists = True
#         if sid_exists and cid_exists:
#             query = {"StudentID" : sid, "CourseID" : cid}
#             newValues = {"$set": {"StudentID" : request.form["StudentID"], "CourseID" : request.form["CourseID"], "Grade" : request.form["Grade"]}}
#             gradesCollection.update_one(query, newValues)
#             return redirect(url_for('index'))
#         else:
#             grades = gradesCollection.find({"StudentID" : sid, "CoursesID" : cid})
#             Grade = ""
#             for result in grades:
#                 Grade = result["Grade"]
#             return render_template("update_grade.html", sid = sid, cid = cid, Grade = Grade, rejected = 1)

# @app.route('/remove_grade/<sid>/<cid>', methods = ['GET', 'POST'])
# def remove_grade(sid, cid):
#     gradesCollection.delete_one({"StudentID": sid, "CourseID" : cid})
#     return redirect(url_for('index'))

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