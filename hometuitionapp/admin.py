from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register([HomeTuitionSystem,  Course, Subject, Teacher, Student, Rating, Hiring])