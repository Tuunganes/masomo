from django.shortcuts          import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http   import require_http_methods
from django.forms                   import modelformset_factory
from django.utils.timezone          import now
from django.db                      import models as dj_models
from django.urls                    import reverse

from .models     import Attendance
from .forms      import AttendanceForm
from students.models  import Student
from teachers.models  import Teacher
from academics.models import SchoolClass


# ————————————————————————————————————————————————————————————————
#  “Select Class & Date”
# ————————————————————————————————————————————————————————————————
@login_required
@permission_required("attendance.add_attendance", raise_exception=True)
def attendance_select(request):
    """
    Let the teacher choose one of their assigned classes and pick a date.
    On POST, redirect to /attendance/mark/?class=ID&date=YYYY-MM-DD
    so that attendance_mark() can pick them up.
    """
    # Step 0  ——————————————————————————————————————————————
    # Make sure the logged-in User actually HAS a Teacher record.
    try:
        teacher = request.user.teacher
    except Teacher.DoesNotExist:
        # If they are not a Teacher we simply bounce them away.
        return redirect("students:student_list")   # (or HttpResponseForbidden)

    # Step 1  ——————————————————————————————————————————————
    # Which classes may this teacher mark?  (homeroom OR subject teacher)
    eligible_classes = SchoolClass.objects.filter(
        dj_models.Q(main_teacher=teacher) | dj_models.Q(teachers=teacher)
    ).distinct().order_by("name")

    # Step 2  ——————————————————————————————————————————————
    if request.method == "POST":
        chosen_class = request.POST.get("school_class")
        chosen_date  = request.POST.get("date")
        if chosen_class and chosen_date:
            mark_url = reverse("attendance:attendance_mark")        # /attendance/mark/
            # Jump directly to the mark-view with query-string.
            return redirect(f"{mark_url}?class={chosen_class}&date={chosen_date}")

    # Step 3  ——————————————————————————————————————————————
    return render(
        request,
        "attendance_select.html",
        {
            "classes": eligible_classes,
            "today":   now().date().isoformat(),   # pre-fill date picker with “today”
        },
    )


# ————————————————————————————————————————————————————————————————
#  “Mark Attendance”
# ————————————————————————————————————————————————————————————————
@login_required
@permission_required("attendance.add_attendance", raise_exception=True)
def attendance_mark(request):
    """
    Show a table of all students in that class; pre-populate any existing rows.
    On POST, save or update each attendance record.
    """
    class_id = request.GET.get("class")
    date_str = request.GET.get("date")

    # Guard-rail: if user typed URL directly w/out params → send back.
    if not (class_id and date_str):
        return redirect("attendance:attendance_select")

    school_class = get_object_or_404(SchoolClass, pk=class_id)
    teacher      = request.user.teacher         # safe because view is @login_required

    # ------------------------------------------------------------------ #
    # 1.  All students that BELONG to this class
    # ------------------------------------------------------------------ #
    students_qs = Student.objects.filter(
        school_class=school_class
    ).order_by("last_name", "first_name")

    # ------------------------------------------------------------------ #
    # 2.  Existing attendance rows for that date
    # ------------------------------------------------------------------ #
    existing_qs = Attendance.objects.filter(
        student__in=students_qs,
        date=date_str
    )

    # ------------------------------------------------------------------ #
    # 3.  Build the list of INITIAL rows that are still missing ★★ added
    # ------------------------------------------------------------------ #
    missing_ids = students_qs.exclude(
        id__in=existing_qs.values_list("student_id", flat=True)
    ).values_list("id", flat=True)

    initial_rows = [
        {
            "student":   sid,
            "date":      date_str,
            "status":    "present",     # default value
            "marked_by": teacher.pk,
        }
        for sid in missing_ids
    ]

    # ------------------------------------------------------------------ #
    # 4.  ONE form-set factory (extra == number of missing rows) ★★ updated
    # ------------------------------------------------------------------ #
    AttendanceFormSet = modelformset_factory(
        Attendance,
        form       = AttendanceForm,
        extra      = len(initial_rows),      # ← could be 0
        can_delete = False,
    )

    # ------------------------------------------------------------------ #
    # 5.  POST: validate & save   (always pass the SAME initial_rows) ★★ updated
    # ------------------------------------------------------------------ #
    if request.method == "POST":
        formset = AttendanceFormSet(
            request.POST,
            queryset=existing_qs,
            initial = initial_rows,          # keep hidden fields alive
        )
        if formset.is_valid():
            for f in formset.forms:          # walk every sub-form
                if not f.cleaned_data:       # empty → skip (nothing submitted)
                    continue
                obj = f.save(commit=False)
                if obj.pk is None:           # brand-new row → stamp teacher
                    obj.marked_by = teacher
                obj.save()
            # no m2m, so no save_m2m()
            return redirect(request.get_full_path())
        
        just_saved_flag = False

    else:   # GET ─ build the form-set
        formset = AttendanceFormSet(queryset=existing_qs, initial=initial_rows)

        just_saved_flag   = False

    # ------------------------------------------------------------------ #
    # 6.  Render template
    # ------------------------------------------------------------------ #
    return render(
        request,
        "attendance_mark.html",
        {
            "school_class": school_class,
            "date_str":     date_str,
            "formset":      formset,
            "form_media":   formset.media,   # Flatpickr JS/CSS etc.
            "just_saved":   request.method == "POST",
            "just_saved":   just_saved_flag,
        },
    )


# ————————————————————————————————————————————————————————————————
#  “Admin Overview”
# ————————————————————————————————————————————————————————————————
@login_required
@permission_required("attendance.view_attendance", raise_exception=True)
def attendance_overview(request):
    """
    Show a table of all attendance records, filterable by class and/or date.
    """
    qs = Attendance.objects.select_related(
        "student__school_class",
        "marked_by",
        "student",
    ).order_by("-date", "student__last_name")

    filter_class = request.GET.get("class")
    if filter_class:
        qs = qs.filter(student__school_class_id=filter_class)

    filter_date = request.GET.get("date")
    if filter_date:
        qs = qs.filter(date=filter_date)

    class_choices = SchoolClass.objects.only("id", "name").order_by("name")

    return render(
        request,
        "attendance_list.html",
        {
            "records":       qs,
            "class_choices": class_choices,
            "filter_class":  filter_class or "",
            "filter_date":   filter_date or "",
            "today":         now().date().isoformat(),
        },
    )


# ————————————————————————————————————————————————————————————————
#  “Edit / Delete” single attendance (unchanged)
# ————————————————————————————————————————————————————————————————
@login_required
@permission_required("attendance.change_attendance", raise_exception=True)
def attendance_edit(request, pk):
    rec  = get_object_or_404(Attendance, pk=pk)
    form = AttendanceForm(request.POST or None, instance=rec)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("attendance:attendance_overview")
    return render(request, "attendance_edit.html", {"form": form, "obj": rec})


@login_required
@permission_required("attendance.delete_attendance", raise_exception=True)
@require_http_methods(["GET", "POST"])
def attendance_delete(request, pk):
    rec = get_object_or_404(Attendance, pk=pk)
    if request.method == "POST":
        rec.delete()
        return redirect("attendance:attendance_overview")
    return render(request, "attendance_delete_confirm.html", {"obj": rec})
