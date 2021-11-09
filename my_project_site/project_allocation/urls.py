from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.auth.views import LogoutView

from . import views

app_name = 'project_allocation'

urlpatterns = [
    # path('', views.index, name='index'),
    # path ('', TemplateView.as_view (template_name="index_login.html")),
    path ('', views.index_login, name='index_login'),
    path ('logout/', views.logout_, name='my_logout'),
    path ('choose/', views.choose , name='choose'),

    path('instructor/', views.instructor_index, name='instructor_index'),
    path('instructor/<int:course_id>', views.instructor_course, name='instructor_course'),
    path('instructor/<int:course_id>/calc', views.start_allocation, name='instructor_compute'),
    path('instructor/<int:course_id>/publish', views.publish_project, name='instructor_publish'),


    path('student/', views.student_index, name='student_index'),
    path('student/<int:course_id>', views.student_course, name='student_course'),
    path('student/<int:course_id>/delete/<int:project_id>', views.student_course_delete, name='student_course_delete'),
    path('student/<int:course_id>/partner', views.student_course_partner, name='student_course_partner'),
    path('student/<int:course_id>/partner/delete/<int:peer_id>', views.student_course_partner_delete , name="student_course_partner_delete")
]