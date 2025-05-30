from django import forms
from django_flatpickr.widgets import DatePickerInput
from django_flatpickr.schemas import FlatpickrOptions
from .models import Teacher

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'  # ✅ includes all fields from the Teacher model

        widgets = {
            'date_of_birth': DatePickerInput(
                options=FlatpickrOptions(
                    altFormat='F j, Y',  # e.g. “April 15, 1990”
                    allowInput=True,
                    maxDate='today',     # no future dates
                )
            ),
        }
