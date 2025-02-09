from django.shortcuts import render
from django.http import HttpResponse
from .models import Student
from .forms import StudentForm

# View to display all students
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})

# View to add a new student
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = StudentForm()
    return render(request, 'students/add_student.html', {'form': form})

# Home view to display a welcome message
#ef index(request):
    #return HttpResponse("Welcome to the Students App!")

def index(request):
    return render(request, 'index.html')
