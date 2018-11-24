from django.contrib import admin
from .models import *

admin.site.register(School)
admin.site.register(Course)
admin.site.register(Class)
admin.site.register(Session)
admin.site.register(Student)
admin.site.register(AttendanceRecord)
