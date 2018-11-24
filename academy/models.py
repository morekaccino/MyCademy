from django.db import models
from django.contrib.auth.models import User
from colorfield.fields import ColorField
from random import randint
from accountviews.models import Admin, Teacher


# import recurrence.fields
# Create your models here.

class Student(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    notes = models.TextField(max_length=5000, default="",blank=True)
    RFID_code = models.CharField(max_length=5000, default="", blank=True)

    # student_number = models.CharField(max_length=250)

    def __str__(self):
        return (self.first_name + ' ' + self.last_name)

    def name(self):
        return (self.first_name + ' ' + self.last_name)


class School(models.Model):
    school_name = models.CharField(max_length=250)
    creator = models.ForeignKey(Admin, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    # admins = models.ManyToOneRel()

    def __str__(self):
        return self.school_name


class Course(models.Model):
    course_name = models.CharField(max_length=500)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    creator = models.ForeignKey(Admin, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.course_name


class Class(models.Model):
    random_color1 = 0
    random_color2 = 0
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section = models.CharField(max_length=250)
    tutor = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    # time = recurrence.fields.RecurrenceField()
    date_created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(Student)

    colors = ["#20c997", "#007bff", "#17a2b8", "#ffc107", "#6f42c1", "#dc3545", "#e83e8c", "#28a745", "#f44336",
              "#e91e63", "#9c27b0", "#673ab7", "#3f51b5", "#2196f3", "#03a9f4", "#00bcd4", "#00bcd4", "#4caf50",
              "#8bc34a", "#cddc39", "#ffeb3b", "#ffc107", "#ff9800", "#ff5722"]

    color1 = ColorField(default=randint(0, colors.__len__() - 1))
    color2 = ColorField(default=randint(0, colors.__len__() - 1))


    def __str__(self):
        return (self.course.course_name + ' - Section ' + self.section)


class Session(models.Model):
    session_nember = models.IntegerField(default=1)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    date_datetime = models.DateField()
    start_datetime = models.TimeField()
    end_datetime = models.TimeField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.class_name.__str__() + ' - Session ' + str(self.session_nember))


class AttendanceRecord(models.Model):
    ATTENDANCE_TYPES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('excused', 'Excused'),
        ('late', 'Late'),
    )
    session = models.ForeignKey(Session, on_delete=models.CASCADE, default=None)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=ATTENDANCE_TYPES)

    def __str__(self):
        return (self.student.name() + ' - ' + self.status)
