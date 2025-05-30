from django.db import models
from django.utils.text import slugify

class Teacher(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('on_leave', 'On Leave'),
        ('retired', 'Retired'),
        ('terminated', 'Terminated'),
    ]

    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=100)
    address = models.TextField()
    subject = models.CharField(max_length=100)
    qualifications = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    emergency_contact = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    photo = models.ImageField(upload_to='teacher_photos/', null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.full_name)
            slug = base_slug
            count = 1
            while Teacher.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
