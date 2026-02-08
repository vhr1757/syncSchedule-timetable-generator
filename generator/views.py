from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.cache import never_cache


User = get_user_model()

# --------------------
# LOGIN
# --------------------
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


# --------------------
# LOGOUT
# --------------------
def logout_view(request):
    logout(request)
    return redirect("login")


# --------------------
# DASHBOARDS
# --------------------
@login_required
@never_cache
def admin_home(request):
    if request.user.role != "ADMIN":
        return redirect("login")
    return render(request, "generator/admin/admin_home.html")


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



# --------------------
# ADMIN: MANAGE USERS
# --------------------
@login_required
def manage_users(request):
    if request.user.role != "ADMIN":
        return redirect("login")
    return render(request, "generator/admin/manage_users.html")


@login_required
def add_student(request):
    if request.user.role != "ADMIN":
        return redirect("login")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        User.objects.create_user(
            username=username,
            password=password,
            email=email,
            role="STUDENT"
        )
        return redirect("manage_users")

    return render(request, "generator/admin/add_student.html")


@login_required
def add_faculty(request):
    if request.user.role != "ADMIN":
        return redirect("login")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        User.objects.create_user(
            username=username,
            password=password,
            email=email,
            role="FACULTY"
        )
        return redirect("manage_users")

    return render(request, "generator/admin/add_faculty.html")


# --------------------
# OTHER PAGES
# --------------------
@login_required
def select_view(request):
    return render(request, "generator/select_view.html")


@login_required
def class_timetable(request):
    return render(request, "generator/class_timetable.html")


@login_required
def faculty_timetable(request):
    return render(request, "generator/faculty/faculty_timetable.html")
