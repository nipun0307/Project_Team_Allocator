
from project_allocation.models import Student
import pandas as pd
df = pd.read_csv("data_csv/student.csv")
s = Student(student_roll_num = 19110127, student_name = "Nipun Mahajan", student_email = "mahajan.n@iitgn.ac.in")
# print(df.head)

'''
from project_allocation.models import Instructor , Course

for i in range (len(df)):
    c = Course (course_code = df.iloc[i]['course_code'], course_name = df.iloc[i]['course_name'], instructor_id = Instructor.objects.get(intructor_email=df.iloc[i]['instructor_email']))
    c.save()

'''