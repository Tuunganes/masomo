from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from .models import Teacher
from .forms import TeacherForm
from django.contrib.auth.decorators import login_required

@login_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teacher_list.html', {'teachers': teachers})

@login_required
def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teachers:teacher_list')
    else:
        form = TeacherForm()
    return render(request, 'add_teacher.html', {'form': form})