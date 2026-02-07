from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path("admin_hm/", views.admin_home, name="admin_home"),
    path("faculty/", views.faculty_home, name="faculty_home"),
    path("hod/", views.hod_home, name="hod_home"),
    path("admin_hm/manage-users/", views.manage_users, name="manage_users"),
    path("admin_hm/add-student/", views.add_student, name="add_student"),
    path("admin_hm/add-faculty/", views.add_faculty, name="add_faculty"),
    path("select-view/", views.select_view, name="select_view"),
    path("class-timetable/", views.class_timetable, name="class_timetable"),
    path("faculty-timetable/", views.faculty_timetable, name="faculty_timetable"),
]