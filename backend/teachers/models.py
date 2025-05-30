from django.db import models
from django.utils.text import slugify

class Teacher(models.Model):
    STATUS_CHOICES = [
        ('active',   'Active'),
        ('inactive', 'Inactive'),
        ('leave',    'On Leave'),
    ]

    first_name        = models.CharField(max_length=100)
    last_name         = models.CharField(max_length=100)
    email             = models.EmailField()
    date_of_birth     = models.DateField()
    slug              = models.SlugField(unique=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    status            = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active',
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(f"{self.first_name}-{self.last_name}-somo")
            unique = base
            counter = 1
            # Ensure uniqueness
            while Teacher.objects.filter(slug=unique).exists():
                unique = f"{base}-{counter}"
                counter += 1
            self.slug = unique
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
