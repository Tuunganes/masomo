from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.shortcuts import render
from .models import Student
from .forms  import StudentForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from .forms import CustomAuthForm


class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = CustomAuthForm

class CustomLogoutView(LogoutView):
    pass

# locak the views to authenticated users
@login_required
# View to display all students
def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})

@login_required
# View to add a new student
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('students:student_list')      # redirect after successful save
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})

@login_required
# ————————————————————————————————————————
# View to show details for a single student
def student_detail(request, slug):
    student = get_object_or_404(Student, slug=slug)
    return render(request, 'student_detail.html', {'student': student})

@login_required
# View to edit an existing student
def student_edit(request, slug):
    student = get_object_or_404(Student, slug=slug)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('students:student_detail', slug=student.slug)
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_edit.html', {'form': form, 'student': student})
# c'est dans ce code que vous devez mettre creer une fonction de votre fichier htmnl ensuite creer un url lien de la fonction dans urls.py

@login_required
def gestion_view(request):
    return render(request, 'Gestionduneecole.html')
# index and gestion pages
def index(request):
    return render(request, 'index.html')