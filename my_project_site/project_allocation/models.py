from django.db import models
from django.core.validators import MinValueValidator


peer_choices = (
    ("E", "Enemy"),
    ("F", "Friend"),
)

# Class - 1
class Instructor(models.Model):
    instructor_name = models.CharField(max_length=40)
    instructor_email = models.EmailField(max_length=40, unique=True)
    def __str__(self):
        return str(self.instructor_name)
    

# Class - 2
class Student(models.Model):
    student_roll_num = models.IntegerField(primary_key=True, validators=[MinValueValidator(1)], unique=True)
    student_email = models.EmailField (max_length=40, unique=True)
    student_name = models.CharField(max_length=40)

    def __str__(self):
        return str(self.student_roll_num) + " -> " + str(self.student_name)


# Class - 3
class Course(models.Model):
    course_name = models.CharField(max_length=100)
    course_code = models.SlugField(max_length=30, default="course-code-not-applicable", unique=True)
    instructor_id =  models.ForeignKey(Instructor, on_delete=models.CASCADE)
    published = models.BooleanField (default=False)
    def __str__(self):
        return str(self.course_code)


# Class - 4
class Project(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_id_project')
    project_name = models.CharField(max_length=200)
    project_description = models.TextField()
    team_size = models.IntegerField(validators=[MinValueValidator(1)])
    num_teams = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return str(self.project_name) + " : " + str(self.course_id)
1   

# Class - 7
class Student_Enrollment(models.Model):
    student_roll_num = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_roll_enrolled')
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_id_enrolled')
    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['student_roll_num','course_id'], name='unique_enrollments')
        ]
    def __str__(self):
        return str(self.student_roll_num) +" : " + str(self.course_id)

# Class - 5
class Peer_edges (models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_id_peer')
    student_roll_num = models.ForeignKey (Student, on_delete=models.CASCADE, related_name='student_id_peer')
    peer_roll_num = models.ForeignKey (Student, on_delete=models.CASCADE, related_name='peer_id_peer')
    status = models.SlugField(max_length=1, default="N")
    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['course_id', 'student_roll_num', 'peer_roll_num'], name='unique_edges')
        ]

    # N - Neutral , F - Friends , E - enemy
    def __str__ (self):
        return str(self.course_id) + "\t:\t(" + str(self.student_roll_num) + " , " + str(self.peer_roll_num) + ")\t:\t" + str(self.status)


# Class - 6
class Projects_pref (models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_id_pref')
    student_roll_num = models.ForeignKey (Student, on_delete=models.CASCADE, related_name='student_id_pref')
    project_id = models.ForeignKey (Project, on_delete=models.CASCADE, related_name= 'project_id_pref', verbose_name='Project Name')
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course_id', 'student_roll_num', 'project_id'], name='unique_pref')
        ]

    def __str__ (self):
        return str(self.course_id) + "\t:\t" + str(self.student_roll_num) + "\t:\t" + str(self.project_id)

# # Class - 8
# class is_pub (models.Model):
#     course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_id_pub')
#     published = models.BooleanField (default=False)
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=['course_id',], name='unique_pub')
#         ]

#     def __str__(self):
#         return str(self.course_id) + " -> " + str(self.published)

# Class - 9
class allocation_data (models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_id_allo')
    student_roll_num = models.ForeignKey (Student, on_delete=models.CASCADE, related_name='student_id_allo')
    project_id = models.ForeignKey (Project, on_delete=models.CASCADE, related_name= 'project_id_allo')
    team_id = models.IntegerField(validators=[MinValueValidator(1)])
    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['student_roll_num','course_id'], name='unique_allocation')
        ]

    def __str__(self):
        return str(self.student_roll_num) + " -> " + str(self.project_id) + " -> " + str(self.team_id)


