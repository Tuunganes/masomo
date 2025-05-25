# forms.py
from django import forms
from django_flatpickr.widgets import DatePickerInput
from django_flatpickr.schemas import FlatpickrOptions
from .models import Student

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
