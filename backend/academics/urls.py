from django.urls import path
from . import views

app_name = "academics"              

urlpatterns = [
    path("classes/", views.class_list, name="class_list"),
    path("years/",   views.year_list,  name="year_list"),
]
