# forms.py
from django import forms
from django_flatpickr.widgets import DatePickerInput
from django_flatpickr.schemas import FlatpickrOptions
from .models import Student
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'date_of_birth']
        widgets = {
            'date_of_birth': DatePickerInput(
                options=FlatpickrOptions(
                    altFormat='F j, Y',    # human-readable display; e.g. “April 15, 1998”
                    allowInput=True,       # still allow typing
                    maxDate='today',       # prevent future dates
                )
            ),
        }
class CustomAuthForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            "Oups ! Les informations d'identification ne correspondent pas à nos données. Veuillez vérifier et réessayer."
        ),
        'inactive': _("Ce compte est inactif."),
    }