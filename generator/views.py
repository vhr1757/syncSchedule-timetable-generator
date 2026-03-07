from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.views.decorators.cache import never_cache
from .models import *
from django.db.models import Count
from django.contrib import messages
from .models import TimetableEntry, Constraint
from generator.services.timetable_engine import generate_all_timetables
from django.db.models import F


User = get_user_model()


@never_cache
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect based on role
            if user.role == "ADMIN":
                return redirect("admin_home")
            elif user.role == "HOD":
                return redirect("hod_home")
            elif user.role == "FACULTY":
                return redirect("faculty_home")
            elif user.role == "STUDENT":
                return redirect("student_home")
        else:
            return render(
                request,
                "generator/login.html",
                {"error": "Invalid username or password"},
            )

    return render(request, "generator/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
@never_cache
def admin_home(request):
    if request.user.role != "ADMIN":
        return redirect("login")

    faculty_count = User.objects.filter(role="FACULTY").count()
    room_count = RoomLab.objects.count()

    return render(
        request,
        "generator/admin/admin_home.html",
        {
            "faculty_count": faculty_count,
            "room_count": room_count,
        },
    )


@login_required
def manage_users(request):
    if request.user.role != "ADMIN":
        return redirect("login")
    return render(request, "generator/admin/manage_users.html")


@login_required
def manage_subjects(request):
    subjects = Subject.objects.all()
    return render(
        request, "generator/admin/manage_subjects.html", {"subjects": subjects}
    )


@login_required
def add_subject(request):
    if request.method == "POST":
        Subject.objects.create(
            subject_code=request.POST["subject_code"],
            subject_name=request.POST["subject_name"],
            semester=request.POST["semester"],
            lecture_hours=request.POST["lecture_hours"],
            lab_hours=request.POST.get("lab_hours") or 0,
        )
        return redirect("manage_subjects")

    return render(request, "generator/admin/add_subject.html")


@login_required
def update_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)

    if request.method == "POST":
        subject.subject_code = request.POST["subject_code"]
        subject.subject_name = request.POST["subject_name"]
        subject.semester = request.POST["semester"]
        subject.lecture_hours = request.POST["lecture_hours"]
        subject.lab_hours = request.POST.get("lab_hours") or 0
        subject.save()
        return redirect("manage_subjects")

    return render(request, "generator/admin/update_subject.html", {"subject": subject})


@login_required
def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    subject.delete()
    return redirect("manage_subjects")


@login_required
def manage_faculties(request):
    if request.user.role != "ADMIN":
        return redirect("login")

    faculties = FacultyProfile.objects.select_related("user").all()

    return render(
        request, "generator/admin/manage_faculties.html", {"faculties": faculties}
    )


@login_required
def add_faculty(request):
    if request.user.role != "ADMIN":
        return redirect("login")

    subjects = Subject.objects.all()

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        department = request.POST.get("department")
        workload = request.POST.get("workload_hours")

        selected_subjects = request.POST.getlist("subjects")

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "generator/admin/add_faculty.html",
                {"error": "Username exists", "subjects": subjects},
            )

        user = User.objects.create_user(
            username=username, email=email, password=password, role="FACULTY"
        )

        profile = FacultyProfile.objects.create(
            user=user, department=department, workload_hours=workload
        )

        profile.subjects.set(selected_subjects)  # save relation

        return render(
            request,
            "generator/admin/add_faculty.html",
            {"success": "Faculty added successfully", "subjects": subjects},
        )

    return render(request, "generator/admin/add_faculty.html", {"subjects": subjects})


@login_required
def update_faculty(request, faculty_id):
    if request.user.role != "ADMIN":
        return redirect("login")

    faculty = get_object_or_404(FacultyProfile, id=faculty_id)
    subjects = Subject.objects.all()

    if request.method == "POST":
        faculty.user.username = request.POST.get("username")
        faculty.user.email = request.POST.get("email")
        faculty.user.save()

        faculty.department = request.POST.get("department")
        faculty.workload_hours = request.POST.get("workload_hours")

        selected_subjects = request.POST.getlist("subjects")
        faculty.subjects.set(selected_subjects)

        faculty.save()
        return redirect("manage_faculties")

    return render(
        request,
        "generator/admin/update_faculty.html",
        {"faculty": faculty, "subjects": subjects},
    )


@login_required
def delete_faculty(request, faculty_id):
    if request.user.role != "ADMIN":
        return redirect("login")

    faculty = get_object_or_404(FacultyProfile, id=faculty_id)

    faculty.user.delete()

    return redirect("manage_faculties")

@login_required
def add_room_lab(request):
    if request.method == "POST":
        roomNo = request.POST.get("roomNo")
        room_type = request.POST.get("room_type")
        capacity = request.POST.get("capacity")

        if roomNo and room_type and capacity:
            RoomLab.objects.create(
                roomNo=roomNo, room_type=room_type, capacity=capacity
            )
            return redirect("add_room_lab")

    return render(request, "generator/admin/add_room_lab.html")

@login_required
def set_constraints(request):

    constraint = Constraint.objects.first()

    if request.method == "POST":
        working_days = request.POST.get("working_days")
        time_slots_per_day = request.POST.get("time_slots_per_day")
        max_lectures_per_day = request.POST.get("max_lectures_per_day")
        max_hours_per_week = request.POST.get("max_hours_per_week")
        max_daily_work_hours = request.POST.get("max_daily_work_hours")

        if constraint:
            constraint.working_days = working_days
            constraint.time_slots_per_day = time_slots_per_day
            constraint.max_lectures_per_day = max_lectures_per_day
            constraint.max_hours_per_week = max_hours_per_week
            constraint.max_daily_work_hours = max_daily_work_hours
            constraint.save()
        else:
            Constraint.objects.create(
                working_days=working_days,
                time_slots_per_day=time_slots_per_day,
                max_lectures_per_day=max_lectures_per_day,
                max_hours_per_week=max_hours_per_week,
                max_daily_work_hours=max_daily_work_hours
            )

        return render(request, "generator/admin/set_constraints.html", {
            "success": "Constraints saved successfully!",
            "constraint": Constraint.objects.first()
        })

    return render(request, "generator/admin/set_constraints.html", {
        "constraint": constraint
    })

@login_required
def generate_timetable_view(request):

    if request.method == "POST":
        try:
            generate_all_timetables()

            # clear old messages
            storage = get_messages(request)
            for _ in storage:
                pass

            messages.success(
                request,
                "Timetable generated successfully for all semesters and divisions."
            )

            return redirect("admin_home")

        except Exception as e:
            messages.error(request, str(e))

    return render(request, "generator/admin/generate_timetable.html")

def select_view(request):

    semesters = [1,2,3,4,5,6,7]
    divisions = ["A1","A2","A3","A4","B1","B2","B3","B4"]

    if request.method == "POST":

        semester = request.POST.get("semester")
        division = request.POST.get("division")

        return redirect(f"/admin_hm/view-timetable/?semester={semester}&division={division}")

    return render(
        request,
        "generator/admin/select_view.html",
        {
            "semesters": semesters,
            "divisions": divisions
        }
    )

@login_required
def view_timetable(request):

    semester = request.GET.get("semester")
    division = request.GET.get("division")

    if not semester or not division:
        return redirect("select_view")

    semester = int(semester)

    if not TimetableEntry.objects.filter(semester=semester, division=division).exists():
        messages.error(request,"Timetable not generated yet.")
        return redirect("generate_timetable")

    days = ["MON", "TUE", "WED", "THU", "FRI"]

    slots = (
        TimeSlot.objects
        .values("start_time", "end_time", "is_break")
        .distinct()
        .order_by("start_time")
    )

    entries = TimetableEntry.objects.filter(
        semester=semester,
        division=division
    ).select_related("subject", "faculty", "room", "timeslot")

    rows = []

    for slot in slots:

        row = {
            "slot": slot,
            "cells": []
        }

        for day in days:

            entry = entries.filter(
                timeslot__day=day,
                timeslot__start_time=slot["start_time"],
                timeslot__end_time=slot["end_time"]
            ).first()

            row["cells"].append(entry)

        rows.append(row)

    context = {
        "rows": rows,
        "days": days,
        "semester": semester,
        "division": division
    }

    return render(request, "generator/admin/view_timetable.html", context)


@login_required
@never_cache
def hod_home(request):

    overloaded_count = get_overloaded_faculties_count()
    room_conflicts = get_room_conflicts_count()
    total_hours = TimetableEntry.objects.count()

    semesters = [1,2,3,4,5,6,7]
    divisions = ["A1","A2","A3","A4","B1","B2","B3","B4"]

    context = {
        "overloaded_count": overloaded_count,
        "room_conflicts": room_conflicts,
        "total_hours": total_hours,
        "semesters": semesters,
        "divisions": divisions
    }

    return render(request, "generator/hod/hod_home.html", context)


@login_required
@never_cache
def faculty_home(request):
    if request.user.role != "FACULTY":
        return redirect("login")

    faculty_profile = FacultyProfile.objects.get(user=request.user)

    faculty_name = faculty_profile.user.username
    work_hours = faculty_profile.workload_hours

    days = ["MON", "TUE", "WED", "THU", "FRI"]

    slots = (
        TimeSlot.objects
        .values("start_time", "end_time", "is_break")
        .distinct()
        .order_by("start_time")
    )

    entries = TimetableEntry.objects.filter(
        faculty=faculty_profile
    ).select_related("subject", "room", "timeslot")

    rows = []

    for slot in slots:

        row = {
            "slot": slot,
            "cells": []
        }

        for day in days:

            entry = entries.filter(
                timeslot__day=day,
                timeslot__start_time=slot["start_time"],
                timeslot__end_time=slot["end_time"]
            ).first()

            row["cells"].append(entry)

        rows.append(row)

    context = {
        "faculty_name": faculty_name,
        "work_hours": work_hours,
        "rows": rows,
        "days": days,
    }

    return render(
        request,
        "generator/faculty/faculty_home.html",
        context,
    )


@login_required
def faculty_select_view(request):

    semesters = [1,2,3,4,5,6,7]
    divisions = ["A1","A2","A3","A4","B1","B2","B3","B4"]

    if request.method == "POST":

        semester = request.POST.get("semester")
        division = request.POST.get("division")

        return redirect(f"/faculty/view-timetable/?semester={semester}&division={division}")

    return render(
        request,
        "generator/faculty/select_view.html",
        {
            "semesters": semesters,
            "divisions": divisions
        }
    )

@login_required
def faculty_view_timetable(request):

    semester = request.GET.get("semester")
    division = request.GET.get("division")

    if not semester or not division:
        return redirect("faculty_select_view")

    semester = int(semester)

    if not TimetableEntry.objects.filter(semester=semester, division=division).exists():
        messages.error(request,"Timetable not generated yet.")
        return redirect("faculty_select_view")

    days = ["MON","TUE","WED","THU","FRI"]

    slots = (
        TimeSlot.objects
        .values("start_time","end_time","is_break")
        .distinct()
        .order_by("start_time")
    )

    entries = TimetableEntry.objects.filter(
        semester=semester,
        division=division
    ).select_related("subject","faculty","room","timeslot")

    rows = []

    for slot in slots:

        row = {"slot":slot,"cells":[]}

        for day in days:

            entry = entries.filter(
                timeslot__day=day,
                timeslot__start_time=slot["start_time"],
                timeslot__end_time=slot["end_time"]
            ).first()

            row["cells"].append(entry)

        rows.append(row)

    context = {
        "rows":rows,
        "days":days,
        "semester":semester,
        "division":division
    }

    return render(request,"generator/faculty/view_timetable.html",context)


from django.db.models import Count

def get_overloaded_faculties_count():

    overloaded = (
        FacultyProfile.objects
        .annotate(total_hours=Count("timetableentry"))
        .filter(total_hours__gt=F("workload_hours"))
    )

    return overloaded.count()


@login_required
def status_overview(request):
    if request.user.role != "HOD":
        return redirect("login")

    rooms = RoomLab.objects.all()

    context = {
        "rooms": rooms,
    }

    return render(request, "generator/hod/status_overview.html", context)

from django.db.models import Count

def get_room_conflicts_count():

    conflicts = (
        TimetableEntry.objects
        .values("room", "timeslot")
        .annotate(total=Count("id"))
        .filter(total__gt=1)
    )

    return conflicts.count()

@login_required
def hod_faculty_workload(request):

    if request.user.role != "HOD":
        return redirect("login")

    faculty_profiles = FacultyProfile.objects.select_related("user")

    faculty_data = []

    for profile in faculty_profiles:

        workload = TimetableEntry.objects.filter(
            faculty=profile
        ).count()

        faculty_data.append({
            "name": profile.user.username,
            "email": profile.user.email,
            "assigned_hours": workload,
            "allowed_hours": profile.workload_hours
        })

    context = {
        "faculty_data": faculty_data
    }

    return render(
        request,
        "generator/hod/faculty_workload.html",
        context
    )

import csv
from django.http import HttpResponse


@login_required
def download_timetable_csv(request):

    semester = request.GET.get("semester")
    division = request.GET.get("division")

    entries = TimetableEntry.objects.filter(
        semester=semester,
        division=division
    ).select_related("subject", "faculty", "room", "timeslot")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="timetable_sem{semester}_{division}.csv"'

    writer = csv.writer(response)

    writer.writerow(["Day", "Start Time", "End Time", "Subject", "Faculty", "Room"])

    for e in entries:
        writer.writerow([
            e.timeslot.day,
            e.timeslot.start_time,
            e.timeslot.end_time,
            e.subject.subject_name,
            e.faculty.user.username,
            e.room.roomNo
        ])

    return response