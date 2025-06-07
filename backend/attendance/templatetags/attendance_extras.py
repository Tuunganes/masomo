# backend/attendance/templatetags/attendance_extras.py
from django import template
from students.models import Student

register = template.Library()

@register.filter
def get_student_name(student_id):
    """Return the full name for a given student primary-key."""
    try:
        return Student.objects.get(pk=student_id).full_name
    except Student.DoesNotExist:
        return "?"
