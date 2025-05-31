from django import forms
from django_flatpickr.widgets import DatePickerInput
from django_flatpickr.schemas import FlatpickrOptions
from .models import SchoolClass, AcademicYear

# ─── one reusable widget ──────────────────────────────────────────────────────
date_widget = DatePickerInput(
    options=FlatpickrOptions(
        altFormat="F j, Y",   # “May 31 2025”
        allowInput=True,
    )
)

class SchoolClassForm(forms.ModelForm):
    class Meta:
        model  = SchoolClass
        fields = ["name", "academic_year"]
        labels = {"name": "Class name", "academic_year": "Academic year"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["academic_year"].queryset = (
            AcademicYear.objects.order_by("-start_date")
        )

# ─── NEW: AcademicYearForm with widgets ───────────────────────────────────────
class AcademicYearForm(forms.ModelForm):
    class Meta:
        model  = AcademicYear
        fields = ["name", "start_date", "end_date", "is_current"]
        widgets = {
            "start_date": date_widget,
            "end_date":   date_widget,
        }
