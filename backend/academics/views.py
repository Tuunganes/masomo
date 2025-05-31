from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import SchoolClass, AcademicYear
from .forms  import SchoolClassForm, AcademicYearForm



@login_required
@permission_required("academics.view_schoolclass", raise_exception=True)
def class_list(request):
    """List classes & quick-add form."""
    qs = SchoolClass.objects.select_related("academic_year")

    # --- simple search ------------------------------------------------------
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(name__icontains=q)

    # --- year filter --------------------------------------------------------
    year_id = request.GET.get("year")
    if year_id:
        qs = qs.filter(academic_year_id=year_id)

    # nice ordering
    classes = qs.order_by("academic_year__start_date", "name")

    # quick-add form ---------------------------------------------------------
    form = SchoolClassForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("academics:class_list")

    return render(
        request,
        "class_list.html",   # template path (matches previous answer)
        {
            "classes": classes,
            "form":    form,
            "q":       q,
            "year":    year_id,
            "year_choices": AcademicYear.objects.order_by("-start_date"),
        },
    )


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
