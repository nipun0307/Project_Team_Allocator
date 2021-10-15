from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Instructor, Student, Course, Project, Student_Enrollment, Peer_edges, Projects_pref

from .forms import AddProjectPref, AddProjectToListForm


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


def instructor_course(request, course_id):

    course = Course.objects.get(pk=course_id)

    added = False
    if request.method == "POST":
        form = AddProjectToListForm(request.POST)
        if form.is_valid():
            p = course.course_id_project.create(project_name = form.cleaned_data['project_name'], 
                        project_description = form.cleaned_data['project_description'],
                        team_size = form.cleaned_data['team_size'],
                        num_teams = form.cleaned_data['num_teams'])
            p.save()
            return HttpResponseRedirect('/project_allocation/instructor/'+str(course_id))
    else:
        form = AddProjectToListForm  
            
    projects = Project.objects.filter(course_id = course_id, ).order_by('id').reverse()

    context = {
        'course': course, 
        'projects': projects,
        'form': form,
        'added': added,
    }

    return render(request, 'project_allocation/instructor_course.html',context)


def student_index (request):
    dataset = Course.objects.all()

    context = {
        'courses' : dataset,
    }
    return render(request , 'project_allocation/student_index.html', context)

def student_course (request, course_id):
    '''
    When a student clicks any of his enrolled courses, he should see the list of all the projects attached to that course_id

    '''
    projects = Project.objects.filter(course_id=course_id)
    course = Course.objects.get(pk=course_id)
    num_projects = projects.count()
    ct=0

    is_pref = False
    if (request.method=="POST"):
        form = AddProjectPref(request.POST)
        if form.is_valid():
            p = course.course_id_pref.create(student_roll_num = form.cleaned_data['student_roll_num'], 
                        project_id = form.cleaned_data['project_id'], )
            p.save()
            return HttpResponseRedirect('/project_allocation/student/'+str(course_id))
    else:
        form = AddProjectPref

    if (num_projects>0):
        ct=1
    context={
        'course' : course,
        'projects' : projects,
        'num' : int(num_projects),
        'ct' : ct,
        'taken' : is_pref,
    }
    return render(request, 'project_allocation/student_course.html', context)
