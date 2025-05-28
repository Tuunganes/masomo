from django.db import models
from django.utils.text import slugify

class Teacher(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    subject = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)