
import pandas as pd

# df = pd.read_csv("data_csv/student.csv")
# s = Student(student_roll_num = 19110127, student_name = "Nipun Mahajan", student_email = "mahajan.n@iitgn.ac.in")
# print(df.head)

from project_allocation.models import Student, Instructor, Course, Student_Enrollment

df = pd.read_csv("project_allocation/data_csv/student.csv")

# for i in range (len(df)):
#     c = Course (course_code = df.iloc[i]['course_code'], course_name = df.iloc[i]['course_name'], instructor_id = Instructor.objects.get(instructor_email=df.iloc[i]['instructor_email']))
#     c.save()

# for i in range (len(df)):
#     ins = Instructor (instructor_name = df.iloc[i]['instructor_name'], instructor_email = df.iloc[i]['instructor_email'])
#     ins.save()

for i in range (len(df)):
    s = Student (student_roll_num = df.iloc[i]['student_roll'], student_name = df.iloc[i]['student_name'], student_email = df.iloc[i]['student_email'])
    s.save()
# ans=0
# for i in  range (len(df)):
#     student = Student.objects.get(student_roll_num=df.iloc[i]['student_roll'])
#     lst = str(df.iloc[i]['course_list']).split(',')

#     for course in lst:
#         data = Student_Enrollment (student_roll_num = student , course_id = Course.objects.get(course_code = course))
#         data.save()
# print(ans)