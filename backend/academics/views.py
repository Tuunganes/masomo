from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import SchoolClass, AcademicYear
from .forms  import SchoolClassForm, AcademicYearForm


@login_required
@permission_required("academics.view_schoolclass", raise_exception=True)
def class_list(request):
    """List classes & quick-add form."""
    classes = SchoolClass.objects.select_related("academic_year").order_by("name")
    form    = SchoolClassForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("academics:class_list")

    return render(request, "class_list.html", {
        "classes": classes,
        "form":    form,
    })


@login_required
@permission_required("academics.view_academicyear", raise_exception=True)
def year_list(request):
    """List academic years & quick-add form."""
    years = AcademicYear.objects.order_by("-start_date")
    form  = AcademicYearForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        # If you tick “is_current”, unset others
        if form.cleaned_data.get("is_current"):
            AcademicYear.objects.update(is_current=False)
        form.save()
        return redirect("academics:year_list")

    return render(request, "year_list.html", {
        "years": years,
        "form":  form,
    })
