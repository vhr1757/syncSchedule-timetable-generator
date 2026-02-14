from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('FACULTY', 'Faculty'),
        ('HOD', 'Head of Department'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"


class Subject(models.Model):
    subject_code = models.CharField(max_length=20, unique=True)
    subject_name = models.CharField(max_length=100)
    semester = models.IntegerField()
    lecture_hours = models.IntegerField()
    lab_hours = models.IntegerField(default=0)

    def __str__(self):
        return self.subject_name


class Room(models.Model):
    ROOM_TYPE = (
        ('CLASS', 'Classroom'),
        ('LAB', 'Lab'),
    )
    room_number = models.CharField(max_length=20)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE)
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.room_number


class FacultyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    workload_hours = models.IntegerField(default=0)
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.user.username


class HODProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Timetable(models.Model):
    semester = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Semester {self.semester} Timetable"


class TimetableEntry(models.Model):
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, related_name="entries")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    faculty = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    day = models.CharField(max_length=10)
    time_slot = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.subject} - {self.day} {self.time_slot}"


class Constraint(models.Model):
    working_days = models.IntegerField(default=5)
    time_slots_per_day = models.IntegerField(default=6)
    max_lectures_per_day = models.IntegerField(default=4)
    max_hours_per_week = models.IntegerField(default=20)
    max_daily_work_hours = models.IntegerField(default=6)

    def __str__(self):
        return "Timetable Constraints"
