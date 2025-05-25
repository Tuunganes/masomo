from django.urls import path
from . import views

app_name = 'students'  # Namespace for the students app

urlpatterns = [
    path('', views.index, name='index'),  # Root URL for the students app
    path('student_list/', views.student_list, name='student_list'),  # URL for displaying all students
    path('add_student/', views.add_student, name='add_student'),  # URL for adding a new student
    path('gestion/', views.gestion_view, name='gestion'),
    # path('student/<int:pk>/',   views.student_detail, name='student_detail'),
    # path('student/<int:pk>/edit/', views.student_edit,   name='student_edit'),
    path('student/<slug:slug>/',       views.student_detail, name='student_detail'),
    path('student/<slug:slug>/edit/',  views.student_edit,   name='student_edit'),
    path('student/<slug:slug>/delete/', views.student_delete, name='student_delete'),

]
