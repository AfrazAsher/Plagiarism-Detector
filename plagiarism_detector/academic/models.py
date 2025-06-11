# from django.db import models
# from django.contrib.auth.models import User

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     is_student = models.BooleanField(default=False)
#     is_teacher = models.BooleanField(default=False)

#     def __str__(self):
#         role = 'Teacher' if self.is_teacher else 'Student'
#         return f"{self.user.username} ({role})"

# class Course(models.Model):
#     name = models.CharField(max_length=100)
#     teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_taught')

#     def __str__(self):
#         return self.name

# class Assignment(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#     deadline = models.DateTimeField()
#     content = models.FileField(upload_to='assignments/')

#     def __str__(self):
#         return self.title


### New code for PyMongo

# models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    full_name = models.CharField(max_length=255, default="Default Name")
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({'Student' if self.is_student else 'Teacher'})"

class Course(models.Model):
    name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=20, unique=True, default="UNKNOWN")
    description = models.TextField(default="No description provided")
    start_date = models.DateField()
    end_date = models.DateField()
    instructors = models.CharField(max_length=255)
    department = models.CharField(max_length=100, blank=True)
    credits = models.IntegerField(null=True, blank=True)
    prerequisites = models.TextField(blank=True)
    teacher = models.ForeignKey(User, related_name='courses', on_delete=models.CASCADE)
    students = models.ManyToManyField(User, related_name='enrolled_courses', blank=True)  # New ManyToManyField for students

    def __str__(self):
        return self.name

class Assignment(models.Model):
    course = models.ForeignKey(Course, related_name='assignments', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(default="No description provided")
    due_date = models.DateTimeField()
    submission_format = models.CharField(max_length=50, default="PDF")
    max_marks = models.IntegerField(default=100)
    file_upload_instructions = models.TextField(blank=True, default="No specific instructions")
    attachments = models.FileField(upload_to='attachments/', blank=True)
    grading_criteria = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Submission(models.Model):
    course = models.ForeignKey(Course, related_name='submissions', on_delete=models.CASCADE, null=True)
    assignment = models.ForeignKey(Assignment, related_name='submissions', on_delete=models.CASCADE)
    student = models.ForeignKey(User, related_name='submissions', on_delete=models.CASCADE)
    submitted_file = models.FileField(upload_to='student_submissions/')
    submission_date = models.DateTimeField(auto_now_add=True)
    plagiarism_percentage = models.FloatField(default=0.0, blank=True, null=True)
    marks_awarded = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"