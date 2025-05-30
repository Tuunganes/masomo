# backend/teachers/forms.py
from django import forms
from django_flatpickr.widgets import DatePickerInput
from django_flatpickr.schemas import FlatpickrOptions
from django.utils.translation import gettext_lazy as _
from .models import Teacher

date_widget = DatePickerInput(
    options=FlatpickrOptions(
        altFormat='F j, Y',
        allowInput=True,
        maxDate='today',
    )
)

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = [
            'employee_id', 'first_name', 'last_name', 'gender',
            'date_of_birth', 'nationality', 'address', 'phone',
            'email', 'emergency_contact', 'subject', 'qualifications',
            'hire_date', 'status', 'photo',
        ]
        widgets = {
            'date_of_birth': date_widget,
            'hire_date':     date_widget,
        }
        labels = {
            'photo': _("Profile photo (jpg/png ≤ 2 MB)"),
        }
