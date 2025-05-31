# backend/academics/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import SchoolClass
from .forms import SchoolClassForm        # we’ll create this in a second

@login_required
@permission_required("academics.view_schoolclass", raise_exception=True)
def class_list(request):
    """List classes and handle the quick-add form."""
    classes = SchoolClass.objects.order_by("name")

    form = SchoolClassForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("academics:class_list")

    return render(request, "class_list.html", {
        "classes": classes,
        "form": form,
    })
