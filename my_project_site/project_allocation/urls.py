from django.urls import path

from . import views

app_name = 'project_allocation'

urlpatterns = [
    path('', views.index, name='index'),
    path('instructor/', views.instructor_index, name='instructor_index'),
    # path('instructor/<string:course_id>', views.insructor_course, name='instructor_course'),
    # path('student/', views.student_index, name='student_index'),
    # path('student/<string:course_id>', views.student_course, name='student_course'),
]