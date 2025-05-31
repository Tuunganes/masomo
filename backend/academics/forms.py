# backend/academics/forms.py
from django import forms
from .models import SchoolClass


class SchoolClassForm(forms.ModelForm):
    """
    Minimal form used on /academics/classes/ to add a class quickly.
    """
    class Meta:
        model  = SchoolClass
        fields = ["name", "academic_year"]
        widgets = {
            "name":          forms.TextInput(attrs={"class": "input"}),
            "academic_year": forms.TextInput(attrs={"class": "input"}),
        }
        labels = {
            "name": "Class name",
            "academic_year": "Academic year",
        }
