from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import *
from .db_utils import run_statement


def index(req):
    #Logout the user if logged 
    if req.session:
        req.session.flush()
    
    isFailed=req.GET.get("fail",False) #Check the value of the GET parameter "fail"
    
    loginForm=UserLoginForm() #Use Django Form object to create a blank form for the HTML page

    return render(req,'loginIndex.html',{"login_form":loginForm,"action_fail":isFailed})


def login(req):
    username=req.POST["username"]
    password=req.POST["password"]

    resultManager=run_statement(f"SELECT * FROM DatabaseManagers WHERE username='{username}' and password='{password}';") #Run the query in DB
    resultUser=run_statement(f"SELECT * FROM UserPasswords WHERE username='{username}' and password='{password}';") #Run the query in DB
    resultInstructor=run_statement(f"SELECT * FROM Instructors WHERE username='{username}';") #Run the query in DB
    resultStudent=run_statement(f"SELECT * FROM Students WHERE username='{username}';") #Run the query in DB

    if resultManager: #If a result is retrieved
        req.session["username"]=username #Record username into the current session
        return HttpResponseRedirect('../forum/admin') #Redirect user to home page

    elif resultUser and resultInstructor:
        req.session["username"]=username #Record username into the current session
        return HttpResponseRedirect('../forum/instructor') #Redirect user to home page
    elif resultUser and resultUser:
        req.session["username"]=username #Record username into the current session
        return HttpResponseRedirect('../forum/student') #Redirect user to home page
    else:
        return HttpResponseRedirect('../forum?fail=true')


def homePage(req):
    result=run_statement(f"SELECT * FROM Post;") #Run the query in DB

    username=req.session["username"] #Retrieve the username of the logged-in user
    isFailed=req.GET.get("fail",False) #Try to retrieve GET parameter "fail", if it's not given set it to False

    return render(req,'userHome.html',{"results":result,"action_fail":isFailed,"username":username})

def createPost(req):
    #Retrieve data from the request body
    title=req.POST["title"]
    body=req.POST["body"]
    logged_user=req.session["username"]
    try:
        run_statement(f"CALL CreatePost('{title}','{body}','{logged_user}')")
        return HttpResponseRedirect("../forum/home")
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../forum/home?fail=true')


def managerHomePage(req):
    username=req.session["username"] #Retrieve the username of the logged-in user
    isFailed=req.GET.get("fail",False) #Try to retrieve GET parameter "fail", if it's not given set it to False
    isSuccess=req.GET.get("success",False)

    return render(req,'managerHome.html',{"action_fail":isFailed,"action_success":isSuccess,"username":username})

def studentHomePage(req):
    username = req.session["username"]  # Retrieve the username of the logged-in user
    isFailed = req.GET.get("fail", False)  # Try to retrieve GET parameter "fail", if it's not given set it to False
    isSuccess = req.GET.get("success", False)

    return render(req, 'studentHome.html', {"action_fail": isFailed, "action_success": isSuccess, "username": username})


def instructorHomePage(req):
    username = req.session["username"]  # Retrieve the username of the logged-in user
    isFailed = req.GET.get("fail", False)  # Try to retrieve GET parameter "fail", if it's not given set it to False
    isSuccess = req.GET.get("success", False)

    return render(req, 'instructorHome.html', {"action_fail": isFailed, "action_success": isSuccess, "username": username})


def createInstuctopr(req):
    username=req.POST["username"]
    password=req.POST["password"]
    department_id =req.POST["department_id"]
    email=req.POST["email"]
    title=req.POST["title"]
    name=req.POST["name"]
    surname=req.POST["surname"]

    try:
        result = run_statement(f"INSERT INTO Users VALUES('{username}', '{name}', '{surname}');")
        result = run_statement(f"INSERT INTO UserPasswords VALUES('{username}', '{password}');")
        result = run_statement(f"INSERT INTO UserDepartments VALUES('{username}', '{department_id}');")
        result = run_statement(f"INSERT INTO UserMails VALUES('{username}', '{email}');")
        result = run_statement(f"INSERT INTO Instructors VALUES('{username}', '{title}');")
        req.session["username"] = username  # Record username into the current session
        return HttpResponseRedirect('../forum/admin?success=true')  # Redirect user to home page
    except:
        return HttpResponseRedirect('../forum/admin?fail=true')


def createStudent(req):
    username=req.POST["username"]
    password=req.POST["password"]
    department_id =req.POST["department_id"]
    email=req.POST["email"]
    student_id=req.POST["student_id"]
    name=req.POST["name"]
    surname=req.POST["surname"]

    try:
        result = run_statement(f"INSERT INTO Users VALUES('{username}', '{name}', '{surname}');")
        result = run_statement(f"INSERT INTO UserPasswords VALUES('{username}', '{password}');")
        result = run_statement(f"INSERT INTO UserDepartments VALUES('{username}', '{department_id}');")
        result = run_statement(f"INSERT INTO UserMails VALUES('{username}', '{email}');")
        result = run_statement(f"INSERT INTO Students VALUES('{username}', '{student_id}');")
        req.session["username"] = username  # Record username into the current session
        return HttpResponseRedirect('../forum/admin?success=true')  # Redirect user to home page
    except:
        return HttpResponseRedirect('../forum/admin?fail=true')


def deleteStudent(req):
    #to be filled
    return None


def changeTitle(req):
    username=req.POST["username"]
    title=req.POST["title"]
    try:
        result = run_statement(f"UPDATE Instructors SET title='{title}' WHERE username='{username}';")
        req.session["username"] = username  # Record username into the current session
        return HttpResponseRedirect('../forum/admin?success=true')  # Redirect user to home page
    except:
        return HttpResponseRedirect('../forum?fail=true')


def getStudents(req):
    # gpa, completed credits tba and ordering
    result = run_statement(f"SELECT Students.username, name, surname, email, department_id AS department FROM Students JOIN UserMails ON Students.username = UserMails.username JOIN Users ON Students.username = Users.username JOIN UserDepartments ON Students.username = UserDepartments.username;")
    return render(req,'studentList.html', {"results":result})

def getInstructors(req):
    result = run_statement(f"SELECT Instructors.username, name, surname, email, department_id AS department, Instructors.title FROM Instructors JOIN UserMails ON Instructors.username = UserMails.username JOIN Users ON Instructors.username = Users.username JOIN UserDepartments ON Instructors.username = UserDepartments.username;")
    return render(req,'instructorList.html', {"results":result})


def getStudentCourseList(req):
    student_id=req.POST["student_id"]
    result = run_statement(f"SELECT Takes.course_id, CourseNames.course_name, Takes.grade FROM Takes JOIN CourseNames ON Takes.course_id = CourseNames.course_id JOIN Students ON Students.username = Takes.username WHERE Students.student_id = '{student_id}';")
    return render(req, 'studentGradeList.html', {"results": result, "username": student_id})


def getInstructorCourseList(req):
    username = req.POST["username"]
    result = run_statement(f"SELECT CourseNames.course_id, course_name, TimePlaces.classroom_id, campus, slot_id FROM CourseNames JOIN Instructs ON CourseNames.course_id = Instructs.course_id JOIN CourseTimePlaces ON Instructs.course_id = CourseTimePlaces.course_id JOIN TimePlaces ON TimePlaces.time_place_id = CourseTimePlaces.time_place_id JOIN Classrooms ON Classrooms.classroom_id = TimePlaces.classroom_id WHERE username='{username}';")
    return render(req, 'studentGradeList.html', {"results": result, "username": username})


def getCourseGrades(req):
    course_id = req.POST["course_id"]
    result = run_statement(f" SELECT Takes.course_id, course_name, avg(grade) as average FROM Takes JOIN CourseNames ON CourseNames.course_id = Takes.course_id WHERE Takes.course_id = '{course_id}' GROUP BY CourseNames.course_id;")
    return render(req, 'courseGrades.html', {"results": result, "course_id": course_id})


def addCourseStudent(req):
    course_id = req.POST["course_id"]
    username = req.session["username"]

    try:
        result = run_statement(f"INSERT INTO Takes VALUES('{username}', '{course_id}', NULL);")
        return HttpResponseRedirect('../forum/student?success=true')  # Redirect user to home page
    except:
        return HttpResponseRedirect('../forum/student?fail=true')


def addPrerequiste(req):
    course_id = req.POST["course_id"]
    prerequisite_id = req.POST["prerequisite_id"]
    try:
        result = run_statement(f"INSERT INTO Prerequisites (course1_id, course2_id) VALUES('{course_id}', '{prerequisite_id}');")
        return HttpResponseRedirect('../forum/instructor?success=true')  # Redirect user to home page
    except:
        return HttpResponseRedirect('../forum/instructor?fail=true')


def updateCourseName(req):
    #only instructors courses check
    course_id = req.POST["course_id"]
    course_name = req.POST["course_name"]
    try:
        result = run_statement(f"UPDATE CourseNames SET course_name='{course_name}' WHERE course_id='{course_id}';")
        return HttpResponseRedirect('../forum/instructor?success=true')  # Redirect user to home page
    except:
        return HttpResponseRedirect('../forum/instructor?fail=true')


def giveGrade(req):
    #unfinished, also search with student id
    course_id = req.POST["course_id"]
    student_id = req.POST["student_id"]
    grade = req.POST["grade"]

    try:
        result = run_statement(f"UPDATE CourseNames SET grade='{grade}' WHERE course_id='{course_id}';")
        return HttpResponseRedirect('../forum/instructor?success=true')  # Redirect user to home page
    except:
        return HttpResponseRedirect('../forum/instructor?fail=true')


def getTimeSlotAvailable():
    return None


def coursesGivenList():
    return None


def studentsTakingCourse():
    return None


def listAllCourses():
    return None


def searchCourse():
    return None


def filterCourse():
    return None


def coursesTaken():
    return None


def addCourseInstructor(req):
    #problem with course time places auto incrementation wip
    course_id = req.POST["username"]
    course_name = req.POST["course_name"]
    credits = req.POST["credits"]
    classroom_id = req.POST["classroom_id"]
    time_slot = req.POST["time_slot"]
    quota = req.POST["quota"]

    try:
        result = run_statement(f"INSERT INTO Courses VALUES('{course_id}', '{credits}', '{quota}');")
        result = run_statement(f"INSERT INTO CourseNames VALUES('{course_id}', '{course_name}');")
        return HttpResponseRedirect('../forum/instructor?success=true')  # Redirect user to home page
    except:
        return HttpResponseRedirect('../forum/instructor?fail=true')