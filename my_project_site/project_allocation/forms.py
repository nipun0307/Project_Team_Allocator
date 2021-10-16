from django import forms
from django.db.models.query import QuerySet
from django.forms import ModelForm

from .models import Peer_edges, Project, Projects_pref, Student_Enrollment

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
    class Meta():
        model = Projects_pref
        fields=('student_roll_num','project_id')

class AddFriends (ModelForm):
    def __init__ (self, course_id, *args, **kwargs):
        super(AddFriends, self).__init__(*args, **kwargs)
        students=Student_Enrollment.objects.filter(course_id=course_id)
        lst=[]
        for student in students:
            lst.append(student.student_roll_num)
        self.fields['student_roll_num']=forms.ChoiceField(choices=tuple([(roll,roll) for roll in lst]))
        self.fields['peer_roll_num']=forms.ChoiceField(choices=tuple([(roll,roll) for roll in lst]))
        # self.fields['status']= 'E'
    
    class Meta():
        model = Peer_edges
        fields = ('student_roll_num', 'peer_roll_num','status')
        # student_roll_num_choices = forms.MultipleChoiceField(queryset=Student_Enrollment.objects.filter(course_id=1))
        

class AddEnemies (ModelForm):
    def __init__ (self, course_id, *args, **kwargs):
        super(AddEnemies, self).__init__(*args, **kwargs)
        students=Student_Enrollment.objects.filter(course_id=course_id)
        lst=[]
        for student in students:
            lst.append(student.student_roll_num)
        self.fields['student_roll_num']=forms.ChoiceField(choices=tuple([(int(roll), int(roll)) for roll in lst]))
        self.fields['peer_roll_num']=forms.ChoiceField(choices=tuple([(int(roll), int(roll)) for roll in lst]))
        # self.fields['status']= 'E'

    class Meta():
        model = Peer_edges
        fields = ('student_roll_num', 'peer_roll_num', 'status')
     
