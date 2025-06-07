from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.forms import modelformset_factory
from django.utils.timezone import now
from django.db import models as dj_models
from django.urls import reverse 

from .models import Attendance
from .forms import AttendanceForm
from students.models import Student
from teachers.models import Teacher
from academics.models import SchoolClass


# —————— “Select Class & Date” ——————
@login_required
@permission_required("attendance.add_attendance", raise_exception=True)
def attendance_select(request):
    """
    Let the teacher choose one of their assigned classes and pick a date.
    On POST, redirect to the same URL with ?class=ID&date=YYYY-MM-DD
    so that attendance_mark() can pick them up.
    """
    # Step 0: ensure the logged‐in user actually has an associated Teacher record:
    try:
        teacher = request.user.teacher
    except Teacher.DoesNotExist:
        # If they are not a Teacher, forbid access.
        return redirect("students:student_list")  # or HttpResponseForbidden(...) 

    # Determine which classes this teacher can mark (homeroom or subject teacher)
    eligible_classes = SchoolClass.objects.filter(
        dj_models.Q(main_teacher=teacher) | dj_models.Q(teachers=teacher)
    ).distinct().order_by("name")


    if request.method == "POST":
        chosen_class = request.POST.get("school_class")
        chosen_date = request.POST.get("date")
        if chosen_class and chosen_date:
            url = reverse("attendance:attendance_mark")
            return redirect(f"{request.path}?class={chosen_class}&date={chosen_date}")

    return render(request, "attendance_select.html", {
        "classes": eligible_classes,
        "today":   now().date().isoformat(),  # prefill with today's date
    })


# —————— “Mark Attendance” ——————
@login_required
@permission_required("attendance.add_attendance", raise_exception=True)
def attendance_mark(request):
    """
    Display a formset listing all students in that class; prepopulate any existing
    Attendance records for the chosen date. On POST, save each form as needed.
    """
    class_id = request.GET.get("class")
    date_str = request.GET.get("date")

    # If no class or date selected, send back to selection page
    if not (class_id and date_str):
        return redirect("attendance:attendance_select")

    school_class = get_object_or_404(SchoolClass, pk=class_id)
    teacher = request.user.teacher  # can now safely do this

    # Get all students assigned to this class, ordered by last name
    students_in_class = Student.objects.filter(
        school_class=school_class
    ).order_by("last_name", "first_name")

    # Create a formset factory for Attendance
    AttendanceFormSet = modelformset_factory(
        Attendance,
        form=AttendanceForm,
        extra=0,
        can_delete=False,
    )

    # Fetch any existing attendance records for these students on that date
    existing_qs = Attendance.objects.filter(
        student__in=students_in_class,
        date=date_str
    )

    if request.method == "POST":
        formset = AttendanceFormSet(request.POST, queryset=existing_qs)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for inst in instances:
                # If it's a new record (no pk), record which teacher marked it
                if not inst.pk:
                    inst.marked_by = teacher
                inst.save()
            return redirect(f"{request.path}?class={class_id}&date={date_str}")

    else:
        # Build initial data for any students who don't yet have a record
        initial_data = []
        existing_map = {att.student_id: att for att in existing_qs}
        for student in students_in_class:
            if student.id not in existing_map:
                initial_data.append({
                    "student":   student.pk,
                    "date":      date_str,
                    "status":    "present",
                    "marked_by": teacher.pk,
                })

        formset = AttendanceFormSet(queryset=existing_qs, initial=initial_data)

    return render(request, "attendance_mark.html", {
        "school_class": school_class,
        "date_str":     date_str,
        "formset":      formset,
        "form_media":   formset.media,  # ensure Flatpickr JS/CSS get injected
    })


# —————— “Admin Overview” ——————
@login_required
@permission_required("attendance.view_attendance", raise_exception=True)
def attendance_overview(request):
    """
    Show a table of all attendance records, filterable by class and/or date.
    """
    qs = Attendance.objects.select_related(
        "student__school_class",
        "marked_by",
        "student"
    ).order_by("-date", "student__last_name")

    filter_class = request.GET.get("class")
    if filter_class:
        qs = qs.filter(student__school_class_id=filter_class)

    filter_date = request.GET.get("date")
    if filter_date:
        qs = qs.filter(date=filter_date)

    class_choices = SchoolClass.objects.only("id", "name").order_by("name")

    return render(request, "attendance_list.html", {
        "records":       qs,
        "class_choices": class_choices,
        "filter_class":  filter_class or "",
        "filter_date":   filter_date or "",
        "today":         now().date().isoformat(),
    })


# —————— “Edit a single attendance record” ——————
@login_required
@permission_required("attendance.change_attendance", raise_exception=True)
def attendance_edit(request, pk):
    rec = get_object_or_404(Attendance, pk=pk)
    form = AttendanceForm(request.POST or None, instance=rec)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("attendance:attendance_overview")
    return render(request, "attendance_edit.html", {"form": form, "obj": rec})


# —————— “Delete a single attendance record” ——————
@login_required
@permission_required("attendance.delete_attendance", raise_exception=True)
@require_http_methods(["GET", "POST"])
def attendance_delete(request, pk):
    rec = get_object_or_404(Attendance, pk=pk)
    if request.method == "POST":
        rec.delete()
        return redirect("attendance:attendance_overview")
    return render(request, "attendance_delete_confirm.html", {"obj": rec})
