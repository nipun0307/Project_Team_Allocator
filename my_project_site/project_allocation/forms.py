from django import forms
from django.forms import ModelForm
from django.forms import ModelChoiceField

from .models import Project, Course


class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return str(obj.course_code) + " -> " + obj.course_name

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

# form for professor to add a new project in a specific course
class AddCourseToIndexForm(ModelForm):
    class Meta:
        model = Course
        fields = ()

    dropdown_choice = MyModelChoiceField(label=('Select course'), queryset=Course.objects.filter(is_created=False), empty_label='---')




