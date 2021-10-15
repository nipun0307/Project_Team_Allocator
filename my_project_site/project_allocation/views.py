from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Instructor, Student, Course, Project, Student_Enrollment, Peer_edges, Projects_pref

from .forms import AddProjectToListForm, AddCourseToIndexForm


def index(request):
    return render(request, 'project_allocation/index.html')


def instructor_index(request):

    if request.method == "POST":
        form = AddCourseToIndexForm(request.POST)
        if form.is_valid():
            c = form.cleaned_data['dropdown_choice']
            c.is_created = True
            c.save()
            print(form.cleaned_data['dropdown_choice'])
            return HttpResponseRedirect('/project_allocation/instructor/')
    else:
        form = AddCourseToIndexForm  

    courses = Course.objects.all().order_by('-last_updated')

    enrollments = {}
    projects = {}
    pub = {}
    not_created_courses = []

    for course in courses:
        if(course.is_created == True):
            row = Student_Enrollment.objects.filter(course_id = course.id)
            enrollments[course.id] = len(row)
            row = Project.objects.filter(course_id = course.id)
            projects[course.id] = len(row)
            pub[course.id] = course.is_pub
        else:
            not_created_courses.append(course)

    context = {
        'courses': courses, 
        'enrollments': enrollments,
        'projects': projects,
        'pub': pub,
        'not_created_courses': not_created_courses,
        'form': form,
    }

    return render(request, 'project_allocation/instructor_index.html',context)


def instructor_course(request, course_id):

    course = Course.objects.get(pk=course_id)

    if(course.is_created):

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
        }

        return render(request, 'project_allocation/instructor_course.html',context)

    else:
        return HttpResponseRedirect('/project_allocation/instructor/')


def student_index (request):
    dataset = Student_Enrollment.objects.filter(student_id = Student.id)

    context = {
        'courses' : dataset,
    }
    return render(request , 'project_allocation/student_index.html', context)
