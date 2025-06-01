from django.contrib import admin
from .models import AcademicYear, SchoolClass, Subject, Term

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display  = ("name", "start_date", "end_date", "is_current")
    list_editable = ("is_current",)

@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display  = ("name", "academic_year", "main_teacher", "room")
    list_filter   = ("academic_year",)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display  = ("name", "code", "school_class", "teacher")
    list_filter   = ("school_class__academic_year",)

@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display  = ("name", "academic_year", "start_date", "end_date", "is_current")
    list_editable = ("is_current",)
    list_filter   = ("academic_year",)