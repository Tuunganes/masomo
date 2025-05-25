from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Student
from .forms  import StudentForm

# View to display all students
def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})

# View to add a new student
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')      # redirect after successful save
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})

# ————————————————————————————————————————
# View to show details for a single student
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'student_detail.html', {'student': student})

# View to edit an existing student
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_edit.html', {'form': form, 'student': student})
# c'est dans ce code que vous devez mettre creer une fonction de votre fichier htmnl ensuite creer un url lien de la fonction dans urls.py

# index and gestion pages
def index(request):
    return render(request, 'index.html')

def gestion_view(request):
    return render(request, 'Gestionduneecole.html')
