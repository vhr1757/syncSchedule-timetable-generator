from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Room)
admin.site.register(FacultyProfile)
admin.site.register(HODProfile)
admin.site.register(Timetable)
admin.site.register(TimetableEntry)
admin.site.register(Constraint)
