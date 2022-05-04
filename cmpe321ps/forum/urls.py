from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home',views.homePage,name="homePage"),
    path('admin', views.managerHomePage, name="managerHomePage"),
    path('student', views.studentHomePage, name="studentHomePage"),
    path('instructor', views.instructorHomePage, name="instructorHomePage"),

    #admin insert
    path('createInstructor', views.createInstuctopr, name="createInstructor"),
    path('createStudent', views.createStudent, name="createStudent"),
    path('deleteStudent', views.deleteStudent, name="deleteStudent"),
    path('changeInstructorTitle', views.changeTitle, name="changeInstructorTitle"),

    #admin select
    path('studentList', views.getStudents, name="getStudents"),
    path('instructorList', views.getInstructors, name="getInstructors"),
    path('studentCourseList', views.getStudentCourseList, name="getStudentCourses"),
    path('instructorCourseList', views.getInstructorCourseList, name="getInstructorCourses"),
    path('getCourseGrades', views.getCourseGrades, name="getCourseGrades"),

    #instructor insert
    path('addCourseInstructor', views.addCourseInstructor, name="addCourseInstructor"),
    path('addPrerequiste', views.addPrerequiste, name="addPrerequiste"),
    path('updateCourseName', views.updateCourseName, name="updateCourseName"),
    path('giveGrade', views.giveGrade, name="giveGrade"),

    #instructor select
    path('timeSlotAvailableList', views.getTimeSlotAvailable, name="timeSlotAvailableList"),
    path('coursesGivenList', views.coursesGivenList, name="coursesGivenList"),
    path('studentsTakingCourse', views.studentsTakingCourse, name="studentsTakingCourse"),

    #student insert
    path('addCourseStudent', views.addCourseStudent, name="addCourseStudent"),

    #student select
    path('listAllCourses', views.listAllCourses, name="listAllCourses"),
    path('coursesTaken', views.coursesTaken, name="coursesTaken"),
    path('searchCourse', views.searchCourse, name="searchCourse"),
    path('filterCourse', views.filterCourse, name="filterCourse"),

    path('login',views.login,name="login"),
]