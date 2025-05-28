from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from .models import Teacher
from .forms import TeacherForm
from django.contrib.auth.decorators import login_required