from django import template
from students.models import Student

register = template.Library()

@register.filter
def get_student_name(student_id):
    """
    Return "John Doe" for a given student PK (used in the mark-attendance table
    for rows that haven’t been saved yet).
    """
    try:
        return Student.objects.get(pk=student_id).full_name
    except Student.DoesNotExist:
        return "?"
