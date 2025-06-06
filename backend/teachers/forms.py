# backend/teachers/forms.py

from django import forms
from django.contrib.auth import get_user_model # to get the User model
from django_flatpickr.widgets import DatePickerInput
from django_flatpickr.schemas import FlatpickrOptions
from django.utils.translation import gettext_lazy as _
from .models import Teacher


User = get_user_model()  

# Reusable Flatpickr date widget
date_widget = DatePickerInput(
    options=FlatpickrOptions(
        altFormat='j F, Y',   # e.g. “31 May, 2025”
        allowInput=True,
        maxDate='today',
    )
)

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        # We must include "user" here so that the form renders a <select> of existing User accounts.
        fields = [
            'user',               # ForeignKey to User model
            'employee_id',
            'first_name',
            'last_name',
            'gender',
            'date_of_birth',
            'nationality',
            'address',
            'phone',
            'email',
            'emergency_contact',
            'subject',
            'qualifications',
            'hire_date',
            'status',
            'photo',
        ]
        widgets = {
            'date_of_birth': date_widget,
            'hire_date':     date_widget,
        }
        labels = {
            'user':   _("User account"),
            'photo':  _("Profile photo (jpg/png ≤ 2 MB)"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optionally, you could order the User dropdown by username/email, for instance:
        self.fields['user'].queryset = Teacher._meta.get_field('user').remote_field.model.objects.order_by('username')
        self.fields['user'].label_from_instance = lambda u: f"{u.username} ({u.email})"
