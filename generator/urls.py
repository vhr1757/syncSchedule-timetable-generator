from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("faculty/", views.faculty_home, name="faculty_home"),
    path("hod/", views.hod_home, name="hod_home"),
    path("hod/status-overview/", views.status_overview, name="status_overview"),
    path(
        "hod/faculty-workload/",
        views.hod_faculty_workload,
        name="hod_faculty_workload"
    ),
    path(
        "hod/download-timetable-csv/",
        views.download_timetable_csv,
        name="download_timetable_csv",
    ),
    path("admin_hm", views.admin_home, name="admin_home"),
    path("admin_hm/manage-users/", views.manage_users, name="manage_users"),
    path(
        "admin_hm/manage-users/faculties/",
        views.manage_faculties,
        name="manage_faculties",
    ),
    path("admin_hm/manage-users/add-faculty/", views.add_faculty, name="add_faculty"),
    path(
        "admin_hm/manage-users/update-faculty/<int:faculty_id>/",
        views.update_faculty,
        name="update_faculty",
    ),
    path(
        "admin_hm/manage-users/delete-faculty/<int:faculty_id>/",
        views.delete_faculty,
        name="delete_faculty",
    ),
    path(
        "admin_hm/manage-users/subjects/", views.manage_subjects, name="manage_subjects"
    ),
    path("admin_hm/manage-users/add-subject/", views.add_subject, name="add_subject"),
    path(
        "admin_hm/manage-users/update-subject/<int:subject_id>/",
        views.update_subject,
        name="update_subject",
    ),
    path(
        "admin_hm/manage-users/delete-subject/<int:subject_id>/",
        views.delete_subject,
        name="delete_subject",
    ),
    path("admin_hm/add-room-lab/", views.add_room_lab, name="add_room_lab"),
    path(
        "admin_hm/set-constraints/",
        views.set_constraints,
        name="set_constraints"
    ),
    path(
        "admin_hm/generate-timetable/",
        views.generate_timetable_view,
        name="generate_timetable"
    ),
    path(
        "admin_hm/select-view/", 
        views.select_view, 
        name="select_view"
    ),
    path(
        "admin_hm/view-timetable/", 
        views.view_timetable, 
        name="view_timetable"
    ),
    path(
        "faculty/select-view/",
        views.faculty_select_view,
        name="faculty_select_view"
    ),

    path(
        "faculty/view-timetable/",
        views.faculty_view_timetable,
        name="faculty_view_timetable"
    ),
]
