from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Root URL for the students app
    path('student_list/', views.student_list, name='student_list'),  # URL for displaying all students
    path('add_student/', views.add_student, name='add_student'),  # URL for adding a new student
]
