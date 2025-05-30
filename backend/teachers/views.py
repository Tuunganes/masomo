from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db import models                       # for Q search

from .models import Teacher
from .forms  import TeacherForm


# ───────────  Searchable / Filterable LIST  ────────────
@login_required
def teacher_list(request):
    qs = Teacher.objects.all()

    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(
            models.Q(first_name__icontains=q) |
            models.Q(last_name__icontains=q)  |
            models.Q(employee_id__icontains=q)|
            models.Q(email__icontains=q)
        )

    st = request.GET.get("status")
    if st:
        qs = qs.filter(status=st)

    qs = qs.order_by("last_name", "first_name")

    return render(request, "teacher_list.html", {
        "teachers":      qs,
        "q":             q,
        "status":        st,
        "status_choices": Teacher.STATUS_CHOICES,
    })


# ───────────  ADD  ────────────
@login_required
def teacher_add(request):
    if request.method == "POST":
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("teachers:teacher_list")
    else:
        form = TeacherForm()
    return render(request, "add_teacher.html", {"form": form})


# ───────────  DETAIL  ────────────
@login_required
def teacher_detail(request, slug):
    teacher = get_object_or_404(Teacher, slug=slug)
    return render(request, "teacher_detail.html", {"teacher": teacher})


# ───────────  EDIT  ────────────
@login_required
def teacher_edit(request, slug):
    teacher = get_object_or_404(Teacher, slug=slug)
    if request.method == "POST":
        form = TeacherForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect("teachers:teacher_detail", slug=teacher.slug)
    else:
        form = TeacherForm(instance=teacher)
    return render(request, "teacher_edit.html", {"form": form, "teacher": teacher})


# ───────────  DELETE (confirm)  ────────────
@require_http_methods(["GET", "POST"])
@login_required
def teacher_delete(request, slug):
    teacher = get_object_or_404(Teacher, slug=slug)
    if request.method == "POST":
        teacher.delete()
        return redirect("teachers:teacher_list")
    return render(request, "teacher_delete_confirm.html", {"teacher": teacher})
