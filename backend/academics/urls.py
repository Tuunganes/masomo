from django.urls import path
from . import views

app_name = "academics"                #  ← makes the “academics:” namespace

urlpatterns = [
    path("classes/", views.class_list, name="class_list"),
]
