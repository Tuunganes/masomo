# backend/attendance/models.py

from django.db import models
from django.utils.timezone import now

class Attendance(models.Model):
    """
    A single attendance record for one student on one date, marked by a teacher.
    """
    STATUS_CHOICES = [
        ("present",            "Present"),
        ("absent",             "Absent"),
        ("sick",               "Sick"), 
        ("late",               "Late"),
        ("temp_exclusion",     "Temporary Exclusion"),
        ("perm_exclusion",     "Permanent Exclusion"),
        ("fees_exclusion",     "Exclusion for Non‐payment"),
        ("internal_exclusion", "Internal/Class Exclusion"),
    ]

    # Link to Student; when a student is deleted, delete their attendance records
    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="attendances"
    )

    # The date this attendance pertains to
    date = models.DateField()

    # status: present, absent, etc.
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="present"
    )

    # Which teacher marked this attendance (nullable, e.g. if imported or system‐marked)
    marked_by = models.ForeignKey(
        "teachers.Teacher",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="attendance_marked"
    )

    class Meta:
        # One record per student+date
        unique_together = ("student", "date")
        ordering = ["-date", "student__last_name", "student__first_name"]

    def __str__(self):
        return f"{self.student.full_name} — {self.date}: {self.get_status_display()}"
