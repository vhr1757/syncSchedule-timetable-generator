from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.cache import never_cache
from .models import *


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
            return render(request, "generator/login.html", {"error": "Invalid username or password"})

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

    return render(request, "generator/admin/admin_home.html", {
        "faculty_count": faculty_count
    })


@login_required
@never_cache
def hod_home(request):
    if request.user.role != "HOD":
        return redirect("login")
    return render(request, "generator/hod/hod_home.html")


@login_required
@never_cache
def faculty_home(request):
    if request.user.role != "FACULTY":
        return redirect("login")
    return render(request, "generator/faculty/faculty_home.html")



@login_required
def manage_users(request):
    if request.user.role != "ADMIN":
        return redirect("login")
    return render(request, "generator/admin/manage_users.html")

@login_required
def manage_subjects(request):
    subjects = Subject.objects.all()
    return render(request, "generator/admin/manage_subjects.html", {"subjects": subjects})


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

    return render(request, "generator/admin/manage_faculties.html", {
        "faculties": faculties
    })

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
            return render(request, "generator/admin/add_faculty.html", {
                "error": "Username exists",
                "subjects": subjects
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role="FACULTY"
        )

        profile = FacultyProfile.objects.create(
            user=user,
            department=department,
            workload_hours=workload
        )

        profile.subjects.set(selected_subjects)  # save relation

        return render(request, "generator/admin/add_faculty.html", {
            "success": "Faculty added successfully",
            "subjects": subjects
        })

    return render(request, "generator/admin/add_faculty.html", {
        "subjects": subjects
    })

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

    return render(request, "generator/admin/update_faculty.html", {
        "faculty": faculty,
        "subjects": subjects
    })

from django.shortcuts import get_object_or_404, redirect
from generator.models import FacultyProfile

@login_required
def delete_faculty(request, faculty_id):
    if request.user.role != "ADMIN":
        return redirect("login")

    faculty = get_object_or_404(FacultyProfile, id=faculty_id)

    faculty.user.delete()

    return redirect("manage_faculties")

@login_required
def select_view(request):
    return render(request, "generator/select_view.html")


@login_required
def class_timetable(request):
    return render(request, "generator/class_timetable.html")


@login_required
def faculty_timetable(request):
    return render(request, "generator/faculty/faculty_timetable.html")
