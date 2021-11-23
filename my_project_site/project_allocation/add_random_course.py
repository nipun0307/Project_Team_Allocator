import pandas as pd
import random

df = pd.read_csv('project_allocation/data_csv/student.csv')

course_list =['ES242', 'ES301', 'CS402', 'CS302', 'ES101', 'CS301']

n=len(df)

enrollments =[]
print(n)
for i in range (n):
    num_taken = random.randint(1,len(course_list))
    index_list = random.sample(range(0,len(course_list)) , num_taken)
    string=""
    for c in index_list:
        string+= str(course_list[c])+","
    string=string[:-1]
    enrollments.append(string)
# print(enrollments)

df = pd.read_csv('project_allocation/data_csv/student_enrollment.csv')

for i in range(len(df)):
    df.loc[i , 'course_list']=enrollments[i]

df.to_csv('project_allocation/data_csv/enrollments.csv', index=False)