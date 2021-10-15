from django import forms
from django.forms import ModelForm

from .models import Peer_edges, Project, Projects_pref

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
    class Meta():
        model = Peer_edges
        fields = ('student_roll_num', 'peer_roll_num', 'status')

class AddEnemies (ModelForm):
    class Meta():
        model = Peer_edges
        fields = ('student_roll_num', 'peer_roll_num', 'status')


