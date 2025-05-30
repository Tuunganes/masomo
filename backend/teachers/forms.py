# teachers/forms.py
from django import forms
from .models import Teacher
from django_flatpickr.widgets import DatePickerInput

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
        widgets = {
            'date_of_birth': DatePickerInput(),  # 💡 this is the key line
        }
