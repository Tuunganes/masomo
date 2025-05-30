from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from .models import Teacher
from .forms  import TeacherForm


@login_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teacher_list.html', {'teachers': teachers})


@login_required
def teacher_add(request):
    if request.method == 'POST':
        # include request.FILES so the photo upload is processed
        form = TeacherForm(request.POST, request.FILES)
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
def teacher_edit(request, slug):
    teacher = get_object_or_404(Teacher, slug=slug)
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teachers:teacher_detail', slug=teacher.slug)
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'teacher_edit.html', {'form': form, 'teacher': teacher})


@require_http_methods(["GET", "POST"])
@login_required
def teacher_delete(request, slug):
    teacher = get_object_or_404(Teacher, slug=slug)
    if request.method == 'POST':
        teacher.delete()
        return redirect('teachers:teacher_list')
    return render(request, 'teacher_delete_confirm.html', {'teacher': teacher})
