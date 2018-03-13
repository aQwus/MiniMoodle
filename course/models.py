from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_teach = models.BooleanField(default= True)


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Course(models.Model):
    name = models.CharField(max_length=500, unique=True)
    Inf = models.TextField(default="IITD course")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)


class StudCourse(models.Model):
    stud = models.ForeignKey(Student, null=True ,on_delete=models.CASCADE)
    course = models.ForeignKey(Course , null=True, on_delete=models.CASCADE)
    date = models.DateField(Student, default= datetime.date.today())
    time = models.TimeField(default=datetime.datetime.now().time())


class Message(models.Model):
    subject = models.CharField(max_length=1000)
    date = models.DateField(default=datetime.date.today())
    time = models.TimeField(default=datetime.datetime.now().time())
    msg = models.CharField(max_length=1000, default="Hello!")
    course = models.ForeignKey(Course, null=True, on_delete=models.CASCADE)
