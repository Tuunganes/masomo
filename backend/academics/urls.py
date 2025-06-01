from django.urls import path
from . import views

app_name = "academics"

urlpatterns = [

    # list pages

    path("classes/", views.class_list,           name="class_list"),
    path("years/",   views.year_list,            name="year_list"),

    # ---- Class CRUD --------------------------------------------------

    path("class/<int:pk>/edit/",   views.class_edit,   name="class_edit"),
    path("class/<int:pk>/delete/", views.class_delete, name="class_delete"),

    # ---- Year CRUD ---------------------------------------------------
    path("year/<int:pk>/edit/",   views.year_edit,   name="year_edit"),
    path("year/<int:pk>/delete/", views.year_delete, name="year_delete"),

    # ---- Subject CRUD ------------------------------------------------

    path("subjects/", views.subject_list,   name="subject_list"),
    path("subject/<int:pk>/edit/",   views.subject_edit,   name="subject_edit"),
    path("subject/<int:pk>/delete/", views.subject_delete, name="subject_delete"),

    # ---- Term CRUD ---------------------------------------------------

    path("terms/",                views.term_list,   name="term_list"),
    path("term/<int:pk>/edit/",   views.term_edit,   name="term_edit"),
    path("term/<int:pk>/delete/", views.term_delete, name="term_delete"),
]
