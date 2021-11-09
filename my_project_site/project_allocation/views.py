from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect, response
from django.contrib.auth import logout
from django.contrib.auth.models import User

from .models import Instructor, Student, Course, Project, Student_Enrollment, Peer_edges, Projects_pref

from .forms import AddFriends, AddProjectPref, AddProjectToListForm, AddEnemies
from django.core.exceptions import ValidationError

import gurobipy as grb
import random

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
        if Instructor.objects.filter(instructor_email = request.user.email).exists():
            response= redirect('/project_allocation/instructor/')
            return response
        elif Student.objects.filter(student_email = request.user.email).exists():
            response= redirect('/project_allocation/student/')
            return response
    response= redirect('/project_allocation/')
    return response

# ###########################################################################################
# ###########################################################################################

def instructor_index(request):
    if request.user.is_authenticated == False:
        return redirect('/project_allocation/logout/')
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
                pub[course.id] = course.published

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

def publish_project (request, course_id):
    if request.user.is_authenticated == False:
        return redirect('/project_allocation/logout/')
    user = request.user
    if user.is_authenticated:
        if Instructor.objects.filter(instructor_email = request.user.email).exists() == False:
            return redirect('/project_allocation/logout/')
    course = Course.objects.get (pk=course_id)
    course.published = True
    course.save()
    return HttpResponseRedirect('/project_allocation/instructor/')

# ###########################################################################################
# ###########################################################################################

def instructor_course(request, course_id):
    if request.user.is_authenticated == False:
        return redirect('/project_allocation/logout/')
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
    if request.user.is_authenticated == False:
        return redirect('/project_allocation/logout/')
    user = request.user
    if user.is_authenticated:
        if Student.objects.filter(student_email = request.user.email).exists():
            student = Student.objects.get(student_email = request.user.email)
            dataset = Course.objects.filter(course_id_enrolled__student_roll_num=student.student_roll_num)
            context = {
                'courses' : dataset,
                'user' : user,
                'student' : student,
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
    if request.user.is_authenticated == False:
        return redirect('/project_allocation/logout/')
    user = request.user
    if user.is_authenticated:
        if Student.objects.filter(student_email = request.user.email).exists():
            s = Student.objects.get(student_email = request.user.email)
            roll_num = s.student_roll_num
            course = Course.objects.get(pk=course_id)
            ct=0
            if (request.method=="POST"):
                form = AddProjectPref(roll_num, course_id,request.POST)
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
                form = AddProjectPref(roll_num, course_id)
                
            projects = Project.objects.filter(course_id=course_id)
            
            taken_projs = Project.objects.filter(project_id_pref__student_roll_num=s)
            num_projects = taken_projs.count()
            if (num_projects>0):
                ct=1
            published = course.published
            context={
                'course' : course,
                'projects' : projects,
                'num' : int(num_projects),
                'ct' : ct,
                'form' : form,
                'taken' : taken_projs,
                'student' : s,
                'published' : published,
            }
            return render(request, 'project_allocation/student_course.html', context)

# ###########################################################################################
# ###########################################################################################

def student_course_delete(request, course_id, project_id):
    if request.user.is_authenticated == False:
        return redirect('/project_allocation/logout/')
    user = request.user
    if user.is_authenticated:
        if Student.objects.filter(student_email = request.user.email).exists():
            course=Course.objects.get(pk=course_id)
            student = Student.objects.get(student_email = request.user.email)
            project = Project.objects.get(pk=project_id)
            if Projects_pref.objects.filter(course_id=course , student_roll_num = student, project_id=project).exists():
                Projects_pref.objects.filter(course_id=course , student_roll_num = student, project_id=project).delete()
            return HttpResponseRedirect ('/project_allocation/student/'+str(course_id))
    response = redirect('/project_allocation/logout/')
    return response

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

# ###########################################################################################
# ###########################################################################################

def student_course_partner_delete(request, course_id, peer_id):
    if request.user.is_authenticated == False:
        return redirect('/project_allocation/logout/')
    user = request.user
    if user.is_authenticated:
        if Student.objects.filter(student_email = request.user.email).exists():
            student = Student.objects.get(student_email = request.user.email)
            peer = Student.objects.get(student_roll_num = peer_id)
            course = Course.objects.get(pk=course_id)
            if Peer_edges.objects.filter(course_id=course , student_roll_num = student, peer_roll_num =peer).exists():
                Peer_edges.objects.get(course_id=course , student_roll_num = student, peer_roll_num =peer).delete()
            return HttpResponseRedirect('/project_allocation/student/'+str(course_id)+'/partner')

    response = redirect('/project_allocation/logout/')
    return response

# ###########################################################################################
# ###########################################################################################

def start_allocation (request, course_id):
    if request.user.is_authenticated == False:
        return redirect('/project_allocation/logout/')
    user = request.user
    if user.is_authenticated:
        if Instructor.objects.filter(instructor_email = request.user.email).exists() == False:
            return redirect('/project_allocation/logout/')
    
    # the instructor clicks on start button for particular objects.
    # It sets the start published for that project to be false
    is_calc = True

    course = Course.objects.get(pk = course_id)
    course.published = False
    course.save()
    # get all the students for the course
    students = Student.objects.filter(student_roll_enrolled__course_id=course_id)
    # get the projects for the course
    projects = Project.objects.filter(course_id = course)
    # get the project pref
    project_prefs = Projects_pref.objects.filter(course_id=course)
    # get the peer edges : social matrix
    peer_edges = Peer_edges.objects.filter(course_id=course)
    # Now creating a mapping for student and projects
    student_ind = []
    project_ind = []
    i=-1
    for student in students:
        i+=1
        student_ind.append(student)
    i=-1
    for project in projects:
        i+=1
        project_ind.append(project)
    # creating a project pref network
    H =[]
    for i in range(len(student_ind)):
        lst = [0]*projects.count()
        curr_student = student_ind[i]
        curr_pref = project_prefs.filter(student_roll_num = curr_student)
        j=-1
        for project in projects:
            j+=1
            if curr_pref.filter(project_id=project).exists():
                lst[j]=1
        H.append(lst)
    # creating the social network
    G = []
    for i in range(len(student_ind)):
        lst = [0]*students.count()
        curr_student = student_ind[i]
        curr_edges = peer_edges.filter(student_roll_num = curr_student)
        j=-1
        for friend in students:
            j+=1
            if curr_edges.filter(peer_roll_num = friend, status = 'F').exists():
                lst[j] = 1
        j=-1
        for enemy in students:
            j+=1
            if curr_edges.filter(peer_roll_num = enemy, status = 'E').exists():
                lst[j] = -1
        G.append(lst)
    # Generating the project maximum in-take tuple list
    P=[]
    for project in projects:
        P.append((project.num_teams , project.team_size))
    
    # Starting the computation
    m = projects.count()
    n = students.count()
    curr_model, curr_y = computation (n,m,P,G,H)
    is_calc = False
    # Interpreting the Results
    # For a particular Student, print the project he got and team number
    # results is a mapping such that:
        # result[project_name] -> result[project_name][team] -> list of students
    results = []
    for a in range(n):
        for i in range(m):
            for t in range(P[i][0]):
                if (curr_y[(i,t,a)].X != 0):
                    results.append((student_ind[a] , project_ind[i] , t))
    
    dict_res = {}
    i=-1
    for project in projects:
        i+=1
        dict_res[project] = {}
        for t in range(project.num_teams):
            dict_res[project][t]=[]
            for a in range(n):
                if (curr_y[(i,t,a)].X != 0):
                    dict_res[project][t].append(student_ind[a])

    for project in projects:
        for net in dict_res[project]:
            print(dict_res[project][net])
    ans=0
    lst=[]
    for result in results:
        lst.append(result[0])
    lst = set(lst)
    print(len(lst))

    dict = {1 : ['d','s','a'], 2: ['w','r']}

    context = {
        'results' : results,
        'user' : user,
        'is_calc' : is_calc,
        'res' : dict_res,
        'projects' : projects,
        'dict' : dict,
        'course' : course
    }
    return render(request, 'project_allocation/instructor_compute.html', context)

# ###########################################################################################

def computation (n, m, P, G, H):
    GRB = grb.GRB
    model =grb.Model("Cluster")
    y_indices = []
    for i in range(m):
        for t in range(P[i][0]):
            for a in range(n):
                y_indices.append((i,t,a))
    y = model.addVars(y_indices,vtype=GRB.BINARY,name="y")

    l_indices = []
    for i in range(m):
        for t in range(P[i][0]):
            for a1 in range(n):
                for a2 in range(n):
                    l_indices.append((i,t,a1,a2))
    l = model.addVars(l_indices,vtype=GRB.BINARY,name="l")

    for a in range(n):
        model.addConstr( 1 == sum(y[(i,t,a)] for i in range (m) for t in range (P[i][0])) )    

    for i in range(m):
        for t in range (P[i][0]):
            for a1 in range(n):
                for a2 in range(n):
                    model.addConstr(l[(i,t,a1,a2)] == y[(i,t,a1)]*y[(i,t,a2)])

    for i in range(m):
        for t in range (P[i][0]):
            model.addConstr( P[i][1] >= sum(y[(i,t,a)] for a in range(n)))
    
    model.setObjective(sum((y[(i,t,a)]*H[a][i]) for i in range(m) for t in range (P[i][0]) for a in range (n)) + 
    sum((l[(i,t,a1, a2)]*G[a1][a2]) for i in range(m) for t in range (P[i][0]) for a1 in range (n) for a2 in range(n) if (a1!=a2))
    ,GRB.MAXIMIZE)

    model.optimize()
    print('Obj:', model.objVal)

    return model , y



