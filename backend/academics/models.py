from django.db import models
from teachers.models import Teacher 


class AcademicYear(models.Model):
    """e.g. 2025-2026"""
    name       = models.CharField(max_length=15, unique=True)
    start_date = models.DateField()
    end_date   = models.DateField()
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return self.name


class SchoolClass(models.Model):
    """
    One physical / virtual class (P5, 3ᵉ maternelle…)
    """
    name          = models.CharField(max_length=40)
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name="classes"
    )
    main_teacher  = models.ForeignKey(
        Teacher,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="homerooms"
    )
    room          = models.CharField(max_length=30, blank=True)

    class Meta:
        unique_together = ("name", "academic_year")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.academic_year})"


class Subject(models.Model):
    """Math, English, Chimie, … attached to a specific class"""
    code         = models.CharField(max_length=10)
    name         = models.CharField(max_length=80)
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name="subjects"
    )
    teacher      = models.ForeignKey(
        Teacher,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="subjects"
    )

    class Meta:
        unique_together = ("code", "school_class")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} – {self.school_class}"
