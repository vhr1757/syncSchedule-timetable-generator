from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path("faculty/", views.faculty_home, name="faculty_home"),
    path("hod/", views.hod_home, name="hod_home"),
    path("admin_hm", views.admin_home, name="admin_home"),
    path("admin_hm/manage-users/", views.manage_users, name="manage_users"),
    path("admin_hm/manage-users/faculties/", views.manage_faculties, name="manage_faculties"),
    path("admin_hm/manage-users/add-faculty/", views.add_faculty, name="add_faculty"),
    path("admin_hm/manage-users/update-faculty/<int:faculty_id>/", views.update_faculty, name="update_faculty"),
    path("admin_hm/manage-users/delete-faculty/<int:faculty_id>/", views.delete_faculty, name="delete_faculty"),
    path("admin_hm/manage-users/subjects/", views.manage_subjects, name="manage_subjects"),
    path("admin_hm/manage-users/add-subject/", views.add_subject, name="add_subject"),
    path("admin_hm/manage-users/update-subject/<int:subject_id>/", views.update_subject, name="update_subject"),
    path("admin_hm/manage-users/delete-subject/<int:subject_id>/", views.delete_subject, name="delete_subject"),
    path('admin_hm/add-room-lab/', views.add_room_lab, name='add_room_lab'),
    path("select-view/", views.select_view, name="select_view"),
    path("class-timetable/", views.class_timetable, name="class_timetable"),
    path("faculty-timetable/", views.faculty_timetable, name="faculty_timetable"),
    path("faculty/select-timetable/", views.faculty_timetable_selector, name="faculty_timetable_selector"),
    path("faculty/timetable/<int:semester>/<str:division>/", views.faculty_timetable_view, name="faculty_timetable_view"),
]