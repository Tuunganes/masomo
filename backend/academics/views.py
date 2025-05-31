from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods

from .models import SchoolClass, AcademicYear
from .forms  import SchoolClassForm, AcademicYearForm


# ---------- LIST PAGES (already there) ---------------------------------
@login_required
def class_list(request):
    ...
@login_required
def year_list(request):
    ...

# ======================================================================
#                       CLASS  EDIT  &  DELETE
# ======================================================================
@login_required
@permission_required("academics.change_schoolclass", raise_exception=True)
def class_edit(request, pk):
    school_class = get_object_or_404(SchoolClass, pk=pk)
    form = SchoolClassForm(request.POST or None, instance=school_class)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("academics:class_list")
    return render(request, "class_edit.html", {"form": form, "obj": school_class})


@login_required
@permission_required("academics.delete_schoolclass", raise_exception=True)
@require_http_methods(["GET", "POST"])
def class_delete(request, pk):
    school_class = get_object_or_404(SchoolClass, pk=pk)
    if request.method == "POST":
        school_class.delete()
        return redirect("academics:class_list")
    return render(request, "class_delete_confirm.html", {"obj": school_class})


# ======================================================================
#                      YEAR  EDIT  &  DELETE
# ======================================================================
@login_required
@permission_required("academics.change_academicyear", raise_exception=True)
def year_edit(request, pk):
    year = get_object_or_404(AcademicYear, pk=pk)
    form = AcademicYearForm(request.POST or None, instance=year)
    if request.method == "POST" and form.is_valid():
        if form.cleaned_data.get("is_current"):
            AcademicYear.objects.exclude(pk=year.pk).update(is_current=False)
        form.save()
        return redirect("academics:year_list")
    return render(request, "year_edit.html", {"form": form, "obj": year})


@login_required
@permission_required("academics.delete_academicyear", raise_exception=True)
@require_http_methods(["GET", "POST"])
def year_delete(request, pk):
    year = get_object_or_404(AcademicYear, pk=pk)
    if request.method == "POST":
        year.delete()
        return redirect("academics:year_list")
    return render(request, "year_delete_confirm.html", {"obj": year})
