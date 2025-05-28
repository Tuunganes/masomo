from django import forms
from .models import Teacher
from django_flatpickr.widgets import DatePickerInput

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = [
            'full_name', 'gender', 'date_of_birth', 'nationality', 'address',
            'subject', 'qualifications', 'phone', 'email', 'emergency_contact',
            'status', 'profile_picture'
        ]
        widgets = {
            'date_of_birth': DatePickerInput(),
        }