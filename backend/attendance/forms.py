# backend/attendance/forms.py

from django import forms
from django_flatpickr.widgets import DatePickerInput
from django_flatpickr.schemas import FlatpickrOptions
from .models import Attendance

# A reusable date widget for Flatpickr
_date_widget = DatePickerInput(
    options=FlatpickrOptions(
        altFormat='F j, Y',   # e.g. "May 31, 2025"
        allowInput=True,
        maxDate='today',
    )
)

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = [
            "student",
            "date",
            "status",
            "marked_by",
        ]
        widgets = {
            # Render "date" as a Flatpickr date picker
            "date": _date_widget,

            # We’ll hide student and marked_by inputs; they will be set in the view
            "student": forms.HiddenInput(),
            "marked_by": forms.HiddenInput(),
        }
        labels = {
            "date":      "Attendance Date",
            "status":    "Status",
            "student":   "",
            "marked_by": "",
        }
