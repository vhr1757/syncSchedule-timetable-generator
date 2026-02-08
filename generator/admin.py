
from django.contrib import admin
from .models import User, Department, Subject, ClassRoom, TimeTable

admin.site.register(User)
admin.site.register(Department)
admin.site.register(Subject)
admin.site.register(ClassRoom)
admin.site.register(TimeTable)
