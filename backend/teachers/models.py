# backend/teachers/models.py

from django.db import models
from django.utils.text import slugify

class Teacher(models.Model):
    STATUS_CHOICES = [
        ('active',   'Active'),
        ('inactive', 'Inactive'),
        ('leave',    'On Leave'),
    ]
    GENDER_CHOICES = [
        ('male',   'Male'),
        ('female', 'Female'),
        
    ]

    employee_id       = models.CharField(max_length=30, unique=True)
    first_name        = models.CharField(max_length=100)
    last_name         = models.CharField(max_length=100)
    gender            = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True)
    date_of_birth     = models.DateField()
    nationality       = models.CharField(max_length=100, blank=True)
    address           = models.CharField(max_length=255, blank=True)
    phone             = models.CharField(max_length=30, blank=True)
    email             = models.EmailField()
    emergency_contact = models.CharField(max_length=255, blank=True)
    subject           = models.CharField(max_length=120, blank=True)
    qualifications    = models.TextField(blank=True)
    hire_date         = models.DateField()
    status            = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    photo             = models.ImageField(upload_to='teacher_photos/', blank=True)

    slug              = models.SlugField(unique=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(f"{self.first_name}-{self.last_name}-somo")
            unique = base
            cnt = 1
            while Teacher.objects.filter(slug=unique).exists():
                unique = f"{base}-{cnt}"
                cnt += 1
            self.slug = unique
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name
