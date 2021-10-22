from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect, response
from django.contrib.auth import logout
from django.contrib.auth.models import User

from .models import Instructor, Student, Course, Project, Student_Enrollment, Peer_edges, Projects_pref

from .forms import AddFriends, AddProjectPref, AddProjectToListForm, AddEnemies
from django.core.exceptions import ValidationError

def index(request):
    return render(request, 'project_allocation/index.html')

# ###########################################################################################
# ###########################################################################################

def index_login (request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        if Student.objects.filter(student_email = request.user.email).exists():
            p = Student.objects.get(student_email = user.email)
            name = p.student_name
        elif Instructor.objects.filter(instructor_email = request.user.email).exists():
            p = Instructor.objects.get(instructor_email = user.email)
            name = p.instructor_name
        else:
            logout(request)
            response = redirect('/project_allocation/')
            return response
        context={'name':name}
    else:
        context={}
    return render (request,'project_allocation/index_login.html', context)

# ###########################################################################################
# ###########################################################################################

def logout_ (request):
    logout(request)
    response = redirect('/project_allocation/')
    return response

# ###########################################################################################
# ###########################################################################################

def choose (request):
    if request.user.is_authenticated:
        if Student.objects.filter(student_email = request.user.email).exists():
            response= redirect('/project_allocation/student/')
            return response
        elif Instructor.objects.filter(instructor_email = request.user.email).exists():
            response= redirect('/project_allocation/instructor/')
            return response
    response= redirect('/project_allocation/')
    return response

# ###########################################################################################
# ###########################################################################################

def instructor_index(request):
    user = request.user
    if user.is_authenticated:
        if Instructor.objects.filter(instructor_email = request.user.email).exists():
            instructor = Instructor.objects.get(instructor_email = request.user.email)
            courses = Course.objects.filter(instructor_id = instructor)

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
                'user' : instructor,
            }

            return render(request, 'project_allocation/instructor_index.html',context)
    response = redirect('/project_allocation/logout/')
    return response

# ###########################################################################################
# ###########################################################################################

def instructor_course(request, course_id):
    user = request.user
    if user.is_authenticated:
        if Instructor.objects.filter(instructor_email = request.user.email).exists():
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
    response = redirect('/project_allocation/logout/')
    return response

# ###########################################################################################
# ###########################################################################################

def student_index (request):
    user = request.user
    if user.is_authenticated:
        if Student.objects.filter(student_email = request.user.email).exists():
            user = Student.objects.get(student_email = request.user.email)
            dataset = Course.objects.filter(course_id_enrolled__student_roll_num=user.student_roll_num)
            context = {
                'courses' : dataset,
                'user' : user,
            }
            return render(request , 'project_allocation/student_index.html', context)
    response = redirect('/project_allocation/logout/')
    return response

# ###########################################################################################
# ###########################################################################################    

def student_course (request, course_id):
    '''
    When a student clicks any of his enrolled courses, he should see the list of all the projects attached to that course_id
    '''
    user = request.user
    if user.is_authenticated:
        if Student.objects.filter(student_email = request.user.email).exists():
            s = Student.objects.get(student_email = request.user.email)
            course = Course.objects.get(pk=course_id)
            ct=0
            if (request.method=="POST"):
                form = AddProjectPref(course_id,request.POST)
                if form.is_valid():
                    try:
                        Projects_pref.objects.get( student_roll_num = Student.objects.get(student_roll_num=s.student_roll_num), 
                            # course_id=course_id,student_roll_num = form.cleaned_data['student_roll_num'], 
                            project_id = form.cleaned_data['project_id'],)
                    except Projects_pref.DoesNotExist:
                        p = course.course_id_pref.create(student_roll_num = Student.objects.get(student_roll_num=s.student_roll_num), 
                                project_id = form.cleaned_data['project_id'], )
                        p.save()
                        return HttpResponseRedirect('/project_allocation/student/'+str(course_id))
                        # raise ValidationError('Exists Already!')
                    
                    
            else:
                form = AddProjectPref(course_id)
                
            projects = Project.objects.filter(course_id=course_id)
            
            taken_projs = Project.objects.filter(project_id_pref__student_roll_num=s)
            num_projects = taken_projs.count()
            if (num_projects>0):
                ct=1
            context={
                'course' : course,
                'projects' : projects,
                'num' : int(num_projects),
                'ct' : ct,
                'form' : form,
                'taken' : taken_projs,
                'student' : s,
            }
            return render(request, 'project_allocation/student_course.html', context)

# ###########################################################################################
# ###########################################################################################

def student_course_partner (request, course_id):
    user = request.user
    if user.is_authenticated:
        if Student.objects.filter(student_email = request.user.email).exists():
            s = Student.objects.get(student_email = user.email)
            students = Student_Enrollment.objects.filter(course_id=course_id)
            course = Course.objects.get(pk=course_id)
            if (request.method=="POST") and "friend" in request.POST:
                form_f = AddFriends(s.student_roll_num, course_id,request.POST)
                if form_f.is_valid():
                    try:
                        Peer_edges.objects.get(course_id=course_id, student_roll_num = s.student_roll_num, 
                                peer_roll_num = form_f.cleaned_data['peer_roll_num'],)
                    except Peer_edges.DoesNotExist:
                        data_f = course.course_id_peer.create(course_id=course, student_roll_num = s, peer_roll_num = form_f.cleaned_data['peer_roll_num'], status='F')
                        # data_f.status= 'F'
                        data_f.save()
                        return HttpResponseRedirect ('/project_allocation/student/'+str(course_id)+'/partner')

                # =============================================
            if (request.method=="POST") and "enemy" in request.POST:
                form_e = AddEnemies(s.student_roll_num, course_id,request.POST)
                if form_e.is_valid():
                    try:
                        Peer_edges.objects.get(course_id=course_id, student_roll_num = s.student_roll_num, 
                                peer_roll_num = form_e.cleaned_data['peer_roll_num'],)
                    except Peer_edges.DoesNotExist:
                        data_e = course.course_id_peer.create(course_id=course, student_roll_num = s, peer_roll_num = form_e.cleaned_data['peer_roll_num'], status='E')
                        data_e.save()
                        return HttpResponseRedirect ('/project_allocation/student/'+str(course_id)+'/partner')
            
            else:
                form_f = AddFriends(s.student_roll_num, course_id)
                form_e = AddEnemies(s.student_roll_num, course_id)
                friends = Student.objects.filter(peer_id_peer__student_roll_num=s.student_roll_num, peer_id_peer__course_id=course_id, peer_id_peer__status='F')
                enemies = Student.objects.filter(peer_id_peer__student_roll_num=s.student_roll_num, peer_id_peer__course_id=course_id, peer_id_peer__status='E')
            context={
                'user' : user,
                's' : s,
                'course' : course,
                'students' : students,
                'form_f' : form_f,
                'form_e' : form_e,
                'friends' : friends,
                'enemies' : enemies,
            }
            return render(request, 'project_allocation/student_fe.html',context)
    response = redirect('/project_allocation/logout/')
    return response