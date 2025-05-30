from django import forms
from django_flatpickr.widgets import DatePickerInput
from django_flatpickr.schemas import FlatpickrOptions
from django.utils.translation import gettext_lazy as _
from .models import Teacher

class TeacherForm(forms.ModelForm):
    # Custom error messages for required fields
    default_error_messages = {
        'required': _("Le champ %(field_name)s est obligatoire."),
        'invalid':  _("Le champ %(field_name)s contient une valeur invalide."),
    }

    class Meta:
        model = Teacher
        fields = [
            'first_name',
            'last_name',
            'email',
            'date_of_birth',
            'status',
        ]
        widgets = {
            'date_of_birth': DatePickerInput(
                options=FlatpickrOptions(
                    altFormat='F j, Y',
                    allowInput=True,
                    maxDate='today',
                )
            ),
        }
        error_messages = {
            'email': {
                'invalid': _("Veuillez entrer une adresse e-mail valide."),
                'required': _("L'adresse e-mail est requise."),
            },
            'first_name': {
                'required': _("Le prénom est requis."),
            },
            'last_name': {
                'required': _("Le nom de famille est requis."),
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply default error message format to each field
        for field_name, field in self.fields.items():
            field.error_messages.setdefault('required',
                self.default_error_messages['required'] % {'field_name': field.label})
            field.error_messages.setdefault('invalid',
                self.default_error_messages['invalid'] % {'field_name': field.label})
