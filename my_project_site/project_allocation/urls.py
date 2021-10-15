from django.urls import path

from . import views

app_name = 'project_allocation'

urlpatterns = [
    path('', views.index, name='index'),


    path('instructor/', views.instructor_index, name='instructor_index'),
    path('instructor/<int:course_id>', views.instructor_course, name='instructor_course'),


    path('student/', views.student_index, name='student_index'),
    path('student/<int:course_id>', views.student_course, name='student_course'),
    path('student/<int:course_id>/partner', views.student_course_partner, name='student_course_partner'),
]