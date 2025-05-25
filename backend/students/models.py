# backend/students/models.py

from django.db import models
from django.utils.text import slugify

class Student(models.Model):
    first_name    = models.CharField(max_length=100)
    last_name     = models.CharField(max_length=100)
    email         = models.EmailField()
    date_of_birth = models.DateField()
    slug          = models.SlugField(unique=True, blank=True)

    # NEW: timestamp when the student was created
    registration_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Base slug: first-last-somo (somo is a placeholder meaning "classroom" in Swahili)
            base_slug = slugify(f"{self.first_name}-{self.last_name}-somo")
            unique_slug = base_slug

            # adding a counter
            counter = 1
            while Student.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = unique_slug

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
