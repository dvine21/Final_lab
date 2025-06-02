from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = [('admin', 'Admin'), ('student', 'Student')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    def __str__(self):
        return f"{self.user.username} ({self.role})"
    
class Student(models.Model):
    name = models.CharField(max_length=100) 
    email = models.EmailField(unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name
    
class Subject(models.Model):
    name = models.CharField(max_length=100)
    student = models.ForeignKey(Student, related_name='subjects', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.student.name}"

    
class Grade(models.Model):
    GRADE_TYPE_CHOICES = [
        ('Activity', 'Activity'),
        ('Quiz', 'Quiz'),
        ('Exam', 'Exam')
    ]
    subject = models.ForeignKey(Subject, related_name='grades', on_delete=models.CASCADE)
    grade_type = models.CharField(max_length=20, choices=GRADE_TYPE_CHOICES)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.subject.name} - {self.grade_type} - {self.score}"
