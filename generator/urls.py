from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("faculty/", views.faculty_home, name="faculty_home"),
    path("hod/", views.hod_home, name="hod_home"),
    path("hod/status-overview/", views.status_overview, name="status_overview"),
    path(
        "hod/faculty-work-hours/", views.faculty_work_hours, name="faculty_work_hours"
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
    path("admin_hm/generate/", views.set_constraints, name="set_constraints"),
    path("admin_hm/run-generator/", views.run_generator, name="run_generator"),
    path(
        "faculty/select-timetable/",
        views.faculty_timetable_selector,
        name="faculty_timetable_selector",
    ),
    path(
        "faculty/timetable/<int:semester>/<str:division>/",
        views.faculty_timetable_view,
        name="faculty_timetable_view",
    ),
]
