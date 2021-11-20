from django import forms
from django.db.models.query import QuerySet
from django.forms import ModelForm

from .models import Peer_edges, Project, Projects_pref, Student, Student_Enrollment, Instructor

peer_choice_enemy = (
    ('E','Enemy'),
)
peer_choice_friend = (
    ('F','Friend'),
)

# form for professor to add a new project in a specific course
class AddProjectToListForm(ModelForm):
    class Meta():
        model = Project
        fields = ('project_name', 'project_description', 'team_size', 'num_teams')

        '''
        labels = {
            'project_name': '', 
            'project_description': '', 
            'team_size': '', 
            'num_teams': '',
        }

        # add styling here later
        widgets = {
            'project_name': forms.TextInput(attrs={'class':'', 'placeholder':''}), 
            'project_description': forms.TextInput(), 
            'team_size': forms.IntegerField(), 
            'num_teams': forms.IntegerField(),
        }

        '''

'''
Creating a form for the student where he can select the project he wants to take
'''
class AddProjectPref (ModelForm):
    def __init__ (self, roll_num, course_id, *args, **kwargs):
        super(AddProjectPref, self).__init__(*args, **kwargs)
        students=Student.objects.filter(student_roll_enrolled__course_id=course_id).distinct()
        projects=Project.objects.filter(course_id=course_id).distinct().exclude(project_id_pref__student_roll_num = roll_num)
        # self.fields['student_roll_num']=forms.ModelChoiceField(queryset=students)
        self.fields['project_id']=forms.ModelChoiceField(queryset=projects)
        self.fields['project_id'].label="Project Name\t\t"
    class Meta():
        model = Projects_pref
        fields=('project_id',)

        labels = {
            "project_id" : "Project Name",
        }

class AddFriends (ModelForm):
    def __init__ (self, roll_num, course_id, *args, **kwargs):
        super(AddFriends, self).__init__(*args, **kwargs)
        curr_student = Student.objects.get(student_roll_num = roll_num)
        students=Student.objects.filter(student_roll_enrolled__course_id=course_id )
        # students= students.student_roll_enrolled.all()
        
        # self.fields['student_roll_num']=forms.ModelChoiceField(queryset=students)
        self.fields['peer_roll_num']=forms.ModelChoiceField(queryset=students)
        self.fields['peer_roll_num'].label="Preferred Teammate ID\t\t"
        # self.fields['status']= forms.ChoiceField(choices=peer_choice_friend)
    
    class Meta():
        model = Peer_edges
        fields = ('peer_roll_num',)
        # student_roll_num_choices = forms.MultipleChoiceField(queryset=Student_Enrollment.objects.filter(course_id=1))
        

class AddEnemies (ModelForm):
    def __init__ (self, roll_num, course_id, *args, **kwargs):
        super(AddEnemies, self).__init__(*args, **kwargs)
        students=Student.objects.filter(student_roll_enrolled__course_id=course_id).exclude(student_roll_num = roll_num)
        # students= students.student_roll_enrolled.all()
        
        # self.fields['student_roll_num']=forms.ModelChoiceField(queryset=students)
        self.fields['peer_roll_num']=forms.ModelChoiceField(queryset=students)
        self.fields['peer_roll_num'].label="Non-Preferred Teammate ID\t\t"
        # self.fields['status']= forms.ChoiceField(choices=peer_choice_enemy)

    class Meta():
        model = Peer_edges
        fields = ('peer_roll_num', )
     
