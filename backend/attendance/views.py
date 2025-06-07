# backend/attendance/views.py
from django.shortcuts          import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http   import require_http_methods
from django.forms                   import modelformset_factory
from django.utils.timezone          import now
from django.db                      import models as dj_models
from django.urls                    import reverse

from .models        import Attendance
from .forms         import AttendanceForm
from students.models import Student
from teachers.models import Teacher
from academics.models import SchoolClass


# ────────────────────────────────────────────────────────────────
# 1. “Select Class & Date”
# ────────────────────────────────────────────────────────────────
@login_required
@permission_required("attendance.add_attendance", raise_exception=True)
def attendance_select(request):
    """
    Teacher chooses one of *their* classes + a date and is then
    redirected to attendance_mark?class=<id>&date=<yyyy-mm-dd>.
    """
    # 0️⃣ make sure the user **is** a teacher
    try:
        teacher = request.user.teacher
    except Teacher.DoesNotExist:
        return redirect("students:student_list")   # 👈 fallback (or Http403)

    # 1️⃣ classes the teacher can mark (main-teacher *or* in M2M list)
    eligible_classes = (
        SchoolClass.objects
        .filter(dj_models.Q(main_teacher=teacher) |
                dj_models.Q(teachers=teacher))
        .distinct()
        .order_by("name")
    )

    # 2️⃣ handle the POST (user pressed “Next”)
    if request.method == "POST":
        chosen_class = request.POST.get("school_class")
        chosen_date  = request.POST.get("date")

        if chosen_class and chosen_date:
            # build the absolute URL of attendance_mark
            mark_url = reverse("attendance:attendance_mark")
            return redirect(f"{mark_url}?class={chosen_class}&date={chosen_date}")

    # 3️⃣ initial GET – render simple form
    return render(request, "attendance_select.html", {
        "classes": eligible_classes,
        "today":   now().date().isoformat(),
    })


# ────────────────────────────────────────────────────────────────
# 2. “Mark Attendance”
# ────────────────────────────────────────────────────────────────
@login_required
@permission_required("attendance.add_attendance", raise_exception=True)
def attendance_mark(request):
    """
    Shows a form-set (one row per pupil) and stores / updates the
    Attendance rows for the selected date in one go.
    """
    class_id = request.GET.get("class")
    date_str = request.GET.get("date")

    # ⛔ if somebody jumps here without params → send them back
    if not (class_id and date_str):
        return redirect("attendance:attendance_select")

    school_class = get_object_or_404(SchoolClass, pk=class_id)
    teacher      = request.user.teacher           # safe: already checked above

    # Pupils in that class (ordered nicely)
    # ────────── replace this single line (in attendance_mark) ──────────
    students_in_class = Student.objects.filter(school_class_id=class_id)\
                                   .order_by("last_name", "first_name")


    # The *existing* rows for that date
    existing_qs = Attendance.objects.filter(
        student__in=students_in_class,
        date=date_str
    )

    # ModelFormSet factory – our “table editor”
    AttendanceFormSet = modelformset_factory(
        Attendance,
        form        = AttendanceForm,
        extra       = 0,
        can_delete  = False,
    )

    # ------------------------------------------------------------------ #
    # 1️⃣ POST → validate & save
    # ------------------------------------------------------------------ #
    if request.method == "POST":
        formset = AttendanceFormSet(request.POST, queryset=existing_qs)

        if formset.is_valid():
            # iterate over every sub-form (even those Django thinks “unchanged”)
            for f in formset.forms:
                obj = f.save(commit=False)            # build / update instance
                if obj.pk is None:                    # brand-new ➜ stamp teacher
                    obj.marked_by = teacher
                obj.save()                            # write to DB

            # success flash is handled in template
            return redirect(request.get_full_path())  # PRG-pattern ✔️

    # ------------------------------------------------------------------ #
    # 2️⃣ GET (first visit *or* after redirect)
    # ------------------------------------------------------------------ #
    else:
        # rows we still have to *create* (so they are visible in the UI)
        initial_data = []
        existing_ids = set(existing_qs.values_list("student_id", flat=True))

        for s in students_in_class:
            if s.id not in existing_ids:
                initial_data.append({
                    "student":   s.pk,
                    "date":      date_str,
                    "status":    "present",
                    "marked_by": teacher.pk,
                })

        formset = AttendanceFormSet(queryset=existing_qs, initial=initial_data)

    # ------------------------------------------------------------------ #
    # 3️⃣ render page
    # ------------------------------------------------------------------ #
    return render(request, "attendance_mark.html", {
        "school_class": school_class,
        "date_str":     date_str,
        "formset":      formset,
        "form_media":   formset.media,          # Flatpickr etc.
        "just_saved":   request.method == "POST",
    })


# ────────────────────────────────────────────────────────────────
# 3. “Overview”  (for admins / principals)
# ────────────────────────────────────────────────────────────────
@login_required
@permission_required("attendance.view_attendance", raise_exception=True)
def attendance_overview(request):
    """
    One big table, filterable by class + date.
    """
    qs = (
        Attendance.objects
        .select_related("student__school_class", "marked_by")
        .order_by("-date", "student__last_name")
    )

    filter_class = request.GET.get("class") or ""
    filter_date  = request.GET.get("date")  or ""

    if filter_class:
        qs = qs.filter(student__school_class_id=filter_class)

    if filter_date:
        qs = qs.filter(date=filter_date)

    class_choices = SchoolClass.objects.only("id", "name").order_by("name")

    return render(request, "attendance_list.html", {
        "records":       qs,
        "class_choices": class_choices,
        "filter_class":  filter_class,
        "filter_date":   filter_date,
        "today":         now().date().isoformat(),
    })


# ────────────────────────────────────────────────────────────────
# 4. Edit / Delete (unchanged – just kept for completeness)
# ────────────────────────────────────────────────────────────────
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
