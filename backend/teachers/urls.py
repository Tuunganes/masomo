from django.urls import path
from . import views

app_name = 'teachers'

urlpatterns = [
    path('',                   views.teacher_list,   name='teacher_list'),
    path('add/',               views.teacher_add,    name='teacher_add'),
    path('<slug:slug>/',       views.teacher_detail, name='teacher_detail'),
    path('<slug:slug>/edit/',  views.teacher_edit,   name='teacher_edit'),
    path('<slug:slug>/delete/',views.teacher_delete, name='teacher_delete'),
]
