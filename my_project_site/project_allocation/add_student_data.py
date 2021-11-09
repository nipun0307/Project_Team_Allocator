
import pandas as pd
import random


# df = pd.read_csv("data_csv/student.csv")
# s = Student(student_roll_num = 19110127, student_name = "Nipun Mahajan", student_email = "mahajan.n@iitgn.ac.in")
# print(df.head)

from project_allocation.models import Student, Instructor, Course, Student_Enrollment, Peer_edges, Project, Projects_pref

df = pd.read_csv("project_allocation/data_csv/student_enrollment.csv")

# for i in range (len(df)):
#     c = Course (course_code = df.iloc[i]['course_code'], course_name = df.iloc[i]['course_name'], instructor_id = Instructor.objects.get(instructor_email=df.iloc[i]['instructor_email']))
#     c.save()

# for i in range (len(df)):
#     ins = Instructor (instructor_name = df.iloc[i]['instructor_name'], instructor_email = df.iloc[i]['instructor_email'])
#     ins.save()

# for i in range (len(df)):
#     s = Student (student_roll_num = df.iloc[i]['student_roll'], student_name = df.iloc[i]['student_name'], student_email = df.iloc[i]['student_email'])
#     s.save()
# ans=0
# for i in  range (len(df)):
#     student = Student.objects.get(student_roll_num=df.iloc[i]['student_roll'])
#     lst = str(df.iloc[i]['course_list']).split(',')

#     for course in lst:
#         data = Student_Enrollment (student_roll_num = student , course_id = Course.objects.get(course_code = course))
#         data.save()

# students = Student.objects.all()
# for student in students:
#     data = Student_Enrollment (student_roll_num = student , course_id = Course.objects.get(course_code = "ES-333"))
#     data.save()

# # Creating Random Peer edges for the social network
course = Course.objects.get(course_code = "ES-333")
students = Student.objects.filter(student_roll_enrolled__course_id=course)
projects = Project.objects.filter(course_id = course)
for student in students:
    for project in projects:
        rand = random.randint(0,1)
        if rand==1:
            data = Projects_pref(course_id=course, student_roll_num = student, project_id = project)
            data.save()
# stat = ['E', 'F', 'N']
# for i in range(len(students)):
#     for j in range (len(students)):
#         if i==j:
#             data = Peer_edges(course_id = course, student_roll_num = students[i], peer_roll_num = students[j], status='N')
#             data.save()
#         else:
#             stat_ = stat[random.randint(0,2)]
#             data = Peer_edges(course_id = course, student_roll_num = students[i], peer_roll_num = students[j], status=stat_)
#             data.save()

