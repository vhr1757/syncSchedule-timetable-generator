from django.shortcuts import render

# Create your views here.

def login_view(request):
    return render(request, 'generator/login.html')

def faculty_home(request):
    return render(request, 'generator/faculty/faculty_home.html')

def admin_home(request):
    return render(request, 'generator/admin/admin_home.html')

def hod_home(request):
    return render(request, 'generator/hod_home.html')

def manage_users(request):
    return render(request, "generator/admin/manage_users.html")

def add_student(request):
    return render(request, "generator/admin/add_student.html")

def add_faculty(request):
    return render(request, "generator/admin/add_faculty.html")

def select_view(request):
    return render(request, "generator/select_view.html")

def class_timetable(request):
    return render(request, "generator/class_timetable.html")

def faculty_timetable(request):
    return render(request, "generator/faculty/faculty_timetable.html")
