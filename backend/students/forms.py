# forms.py

from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django import forms
from django_flatpickr.widgets import DatePickerInput
from django_flatpickr.schemas import FlatpickrOptions
from .models import Student

date_widget = DatePickerInput(
    options=FlatpickrOptions(
        altFormat='F j, Y',
        allowInput=True,
        maxDate='today',
    )
)

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'student_id', 'first_name', 'last_name', 'gender',
            'date_of_birth', 'nationality', 'address', 'phone',
            'email', 'guardian_name', 'guardian_phone',
            'class_level', 'enrol_date', 'status', 'photo',
        ]
        widgets = {
            'date_of_birth': date_widget,
            'enrol_date':    date_widget,
        }

class CustomAuthForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            "Oups ! Les informations d'identification ne correspondent pas à nos données. Veuillez vérifier et réessayer."
        ),
        'inactive': _("Ce compte est inactif."),
    }