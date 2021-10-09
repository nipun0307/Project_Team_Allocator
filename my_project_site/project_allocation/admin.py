from django.contrib import admin

# Register your models here.

from .models import Instructor, Student, Course, Project, Student_Enrollment

admin.site.register(Instructor)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Project)
admin.site.register(Student_Enrollment)