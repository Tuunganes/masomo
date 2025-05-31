from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db import models                      # for Q search
from academics.models import SchoolClass

from .models import Student
from .forms  import StudentForm, CustomAuthForm

# ───────────  Custom login / logout  ────────────
from django.contrib.auth.views import LoginView, LogoutView

class CustomLoginView(LoginView):
    template_name       = "login.html"
    authentication_form = CustomAuthForm

class CustomLogoutView(LogoutView):
    pass


# ───────────  Searchable / Filterable LIST  ────────────

@login_required
def student_list(request):
    qs = Student.objects.select_related("school_class")

    # — search —
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(
            models.Q(first_name__icontains=q) |
            models.Q(last_name__icontains=q)  |
            models.Q(student_id__icontains=q) |
            models.Q(email__icontains=q)
        )

    # — filter by class id —
    class_id = request.GET.get("class_id")
    if class_id:
        qs = qs.filter(school_class_id=class_id)

    qs = qs.order_by("last_name", "first_name")

    # list of classes (current year or all)
    classes = SchoolClass.objects.all().order_by("name")

    return render(request, "student_list.html", {
        "students":  qs,
        "q":         q,
        "class_id":  class_id,
        "classes":   classes,   # ⬅ pass to template
    })

# ───────────  ADD  ────────────
@login_required
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("students:student_list")
    else:
        form = StudentForm()
    return render(request, "add_student.html", {"form": form})


# ───────────  DETAIL  ────────────
@login_required
def student_detail(request, slug):
    student = get_object_or_404(Student, slug=slug)
    return render(request, "student_detail.html", {"student": student})


# ───────────  EDIT  ────────────
@login_required
def student_edit(request, slug):
    student = get_object_or_404(Student, slug=slug)
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect("students:student_detail", slug=student.slug)
    else:
        form = StudentForm(instance=student)
    return render(request, "student_edit.html", {"form": form, "student": student})


# ───────────  DELETE (confirm)  ────────────
@require_http_methods(["GET", "POST"])
@login_required
def student_delete(request, slug):
    student = get_object_or_404(Student, slug=slug)
    if request.method == "POST":
        student.delete()
        return redirect("students:student_list")
    return render(request, "student_delete_confirm.html", {"student": student})


# ───────────  Static / landing pages  ────────────
@login_required
def gestion_view(request):
    return render(request, "Gestionduneecole.html")

def index(request):
    return render(request, "index.html")
