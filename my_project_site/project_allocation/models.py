from django.db import models
from django.core.validators import MinValueValidator


class Instructor(models.Model):
    instructor_name = models.CharField(max_length=40)

    def __str__(self):
        return str(self.id)
    


class Student(models.Model):
    student_roll_num = models.IntegerField(primary_key=True, validators=[MinValueValidator(1)])
    student_name = models.CharField(max_length=40)

    def __str__(self):
        return str(self.student_roll_num)



class Course(models.Model):
    course_name = models.CharField(max_length=100)
    course_code = models.SlugField(max_length=30, default="course-code-not-applicable")
    instructor_id =  models.ForeignKey(Instructor, on_delete=models.CASCADE)
    is_pub = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)



class Project(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_id_project')
    project_name = models.CharField(max_length=200)
    project_description = models.TextField()
    team_size = models.IntegerField(validators=[MinValueValidator(1)])
    num_teams = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return (self.id)


class Peer_edges (models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_id')
    student_roll_num = models.ForeignKey (Student, on_delete=models.CASCADE, related_name='student_roll_num')

class Student_Enrollment(models.Model):
    student_roll_num = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_roll_enrolled')
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_id_enrolled')

    def __str__(self):
        return str(self.student_roll_num)+ ": " + str(self.course_id)
