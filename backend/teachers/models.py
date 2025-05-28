from django.db import models
from django.utils.text import slugify

class Teacher(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('On Leave', 'On Leave'),
        ('Retired', 'Retired'),
    ]

    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    subject = models.CharField(max_length=255)
    qualifications = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    emergency_contact = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    profile_picture = models.ImageField(upload_to='teacher_profiles/', null=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.full_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name