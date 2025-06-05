# backend/attendance/urls.py

from django.urls import path
from . import views

app_name = "attendance"

urlpatterns = [
    # Step 1: teacher picks class & date
    path("select/", views.attendance_select, name="attendance_select"),

    # Step 2: mark attendance for that class+date
    path("mark/", views.attendance_mark, name="attendance_mark"),

    # Admin overview page
    path("overview/", views.attendance_overview, name="attendance_overview"),

    # (to be added  edit/delete paths here later,
    # path("<int:pk>/edit/",   views.attendance_edit,   name="attendance_edit"),
    # path("<int:pk>/delete/", views.attendance_delete, name="attendance_delete"),
    # path("<int:pk>/blocked/", views.attendance_delete_blocked, name="attendance_delete_blocked"),
    # )
]
