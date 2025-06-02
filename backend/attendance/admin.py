# backend/attendance/admin.py

from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "date", "status", "marked_by")
    list_filter  = ("date", "status")
    search_fields = (
        "student__first_name",
        "student__last_name",
        "marked_by__first_name",
        "marked_by__last_name",
    )
