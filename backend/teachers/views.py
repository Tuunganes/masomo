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


@login_required
def teacher_detail(request, slug):
    teacher = get_object_or_404(Teacher, slug=slug)
    return render(request, 'teacher_detail.html', {'teacher': teacher})

@login_required
def edit_teacher(request, slug):
    teacher = get_object_or_404(Teacher, slug=slug)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teachers:teacher_list')
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'edit_teacher.html', {'form': form})

@login_required
def delete_teacher(request, slug):
    teacher = get_object_or_404(Teacher, slug=slug)
    if request.method == 'POST':
        teacher.delete()
        return redirect('teachers:teacher_list')
    return render(request, 'delete_teacher.html', {'teacher': teacher})