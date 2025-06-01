# backend/academics/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.db.models import ProtectedError
from .models import SchoolClass, AcademicYear
from .forms  import SchoolClassForm, AcademicYearForm
from academics.models import Subject
from academics.forms import SubjectForm
from django.db import models

# ─────────────────────────────────────────────────────────────
# LIST + QUICK-ADD  PAGES
# ─────────────────────────────────────────────────────────────
@login_required
@permission_required("academics.view_schoolclass", raise_exception=True)
def class_list(request):
    """
    • Show all classes (searchable & filterable)
    • Inline “quick-add” form at the bottom
    """

    # ------ search / filter ------------------------------------------------
    qs = SchoolClass.objects.select_related("academic_year")

    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(academic_year__name__icontains=q))

    year_id = request.GET.get("year")
    if year_id:
        qs = qs.filter(academic_year_id=year_id)

    qs = qs.order_by("name")

    # ------ quick-add form -------------------------------------------------
    form = SchoolClassForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("academics:class_list")

    # ALWAYS return an HttpResponse
    return render(
        request,
        "class_list.html",
        {
            "classes":      qs,
            "form":         form,
            "year_choices": AcademicYear.objects.order_by("-start_date"),
        },
    )


@login_required
@permission_required("academics.view_academicyear", raise_exception=True)
def year_list(request):
    """
    • Show all academic years
    • Inline quick-add form
    """

    years = AcademicYear.objects.order_by("-start_date")

    form = AcademicYearForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        #  If the new record is marked “current”, unset others first
        if form.cleaned_data.get("is_current"):
            AcademicYear.objects.update(is_current=False)

        form.save()
        return redirect("academics:year_list")

    return render(
        request,
        "year_list.html",
        {
            "years": years,
            "form":  form,
        },
    )


# ─────────────────────────────────────────────────────────────
# CLASS  EDIT  &  DELETE
# ─────────────────────────────────────────────────────────────
@login_required
@permission_required("academics.change_schoolclass", raise_exception=True)
def class_edit(request, pk):
    obj  = get_object_or_404(SchoolClass, pk=pk)
    form = SchoolClassForm(request.POST or None, instance=obj)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("academics:class_list")

    return render(request, "class_edit.html", {"form": form, "obj": obj})


@login_required
@permission_required("academics.delete_schoolclass", raise_exception=True)
@require_http_methods(["GET", "POST"])
def class_delete(request, pk):
    obj = get_object_or_404(SchoolClass, pk=pk)

    if request.method == "POST":
        obj.delete()
        return redirect("academics:class_list")

    return render(request, "class_delete_confirm.html", {"obj": obj})


# ─────────────────────────────────────────────────────────────
# YEAR  EDIT  &  DELETE
# ─────────────────────────────────────────────────────────────
@login_required
@permission_required("academics.change_academicyear", raise_exception=True)
def year_edit(request, pk):
    obj  = get_object_or_404(AcademicYear, pk=pk)
    form = AcademicYearForm(request.POST or None, instance=obj)

    if request.method == "POST" and form.is_valid():
        if form.cleaned_data.get("is_current"):
            AcademicYear.objects.exclude(pk=obj.pk).update(is_current=False)
        form.save()
        return redirect("academics:year_list")

    return render(request, "year_edit.html", {"form": form, "obj": obj})


@login_required
@permission_required("academics.delete_academicyear", raise_exception=True)
@require_http_methods(["GET", "POST"])
def year_delete(request, pk):
    year = get_object_or_404(AcademicYear, pk=pk)

    # ─── user clicked the red “Delete” button ───────────────────────────
    if request.method == "POST":
        try:
            year.delete()
            return redirect("academics:year_list")

        # ---- the year is still used by at least one SchoolClass --------
        except ProtectedError as exc:
            # exc.protected_objects returns the queryset that blocks delete
            blocking = exc.protected_objects
            return render(
                request,
                "year_delete_blocked.html",
                {"obj": year, "blocking": blocking},
                status=409,              # “conflict”
            )

    # ─── initial GET: regular confirmation page ────────────────────────
    return render(request, "year_delete_confirm.html", {"obj": year})


# ----------------------------------------------------------------------
#                        SUBJECT   LIST  / ADD
# ----------------------------------------------------------------------
@login_required
@permission_required("academics.view_subject", raise_exception=True)
def subject_list(request):
    qs = Subject.objects.select_related("school_class", "teacher")
    q  = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(
            models.Q(code__icontains=q) |
            models.Q(name__icontains=q) |
            models.Q(school_class__name__icontains=q) |
            models.Q(teacher__last_name__icontains=q)
        )

    form = SubjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("academics:subject_list")

    return render(request, "subject_list.html", {
        "subjects": qs.order_by("code"),
        "form":     form,
        "q":        q,
    })


# ----------------------------------------------------------------------
#                  SUBJECT  EDIT   /   DELETE
# ----------------------------------------------------------------------
@login_required
@permission_required("academics.change_subject", raise_exception=True)
def subject_edit(request, pk):
    subj = get_object_or_404(Subject, pk=pk)
    form = SubjectForm(request.POST or None, instance=subj)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("academics:subject_list")
    return render(request, "subject_edit.html", {"form": form, "obj": subj})


@login_required
@permission_required("academics.delete_subject", raise_exception=True)
@require_http_methods(["GET", "POST"])
def subject_delete(request, pk):
    subj = get_object_or_404(Subject, pk=pk)
    if request.method == "POST":
        subj.delete()
        return redirect("academics:subject_list")
    return render(request, "subject_delete_confirm.html", {"obj": subj})
