from django.shortcuts import render
from django.http import HttpResponse

from .models import Instructor, Student, Course, Project, Student_Enrollment, Peer_edges, Projects_pref

def index(request):
    return render(request, 'project_allocation/index.html')

def instructor_index(request):
    courses = Course.objects.all()

    enrollments = {}
    projects = {}
    pub = {}

    for course in courses:
        row = Student_Enrollment.objects.filter(course_id = course.id)
        enrollments[course.id] = len(row)
        row = Project.objects.filter(course_id = course.id)
        projects[course.id] = len(row)
        pub[course.id] = course.is_pub

    context = {
        'courses': courses, 
        'enrollments': enrollments,
        'projects': projects,
        'pub': pub,
    }

    return render(request, 'project_allocation/instructor_index.html',context)

def student_index (request):
    courses = 