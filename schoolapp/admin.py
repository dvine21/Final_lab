from django.contrib import admin
from .models import UserProfile, Student, Subject, Grade

admin.site.register(UserProfile)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Grade)
