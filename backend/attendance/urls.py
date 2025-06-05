from django.urls import path
from . import views

app_name = "attendance"

urlpatterns = [
    # Step 1: Teacher picks class & date
    path("select/",    views.attendance_select,   name="attendance_select"),

    # Step 2: Mark attendance for that class+date
    path("mark/",      views.attendance_mark,     name="attendance_mark"),

    # Admin overview page
    path("overview/",  views.attendance_overview, name="attendance_overview"),

    # Edit a single attendance record
    path("edit/<int:pk>/",   views.attendance_edit,   name="attendance_edit"),

    # Delete a single attendance record (confirmation)
    path("delete/<int:pk>/", views.attendance_delete, name="attendance_delete"),
]
